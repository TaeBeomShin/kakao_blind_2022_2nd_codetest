import json
import requests

base_url=""
my_token=""

def get_start_key(problem_num):
    headers={"X-Auth-Token":my_token,"Content-Type":"application/json"}
    # data 값은 전체 문자열로 전달하기
    post_parameter='{"problem":'+problem_num+'}'

    key_response=requests.post(base_url+"/start",headers=headers,data=post_parameter)
    auth_data=key_response.json()
    auth_json=json.loads(json.dumps(auth_data))
    auth_key=auth_json.get("auth_key")
    return auth_key

def get_api(auth_key,url):
    headers={"Authorization":auth_key,"Content-Type":"application/json"}

    response=requests.get(base_url+url,headers=headers)
    data=response.json()
    response_json=json.loads(json.dumps(data))

    return response_json


def match_api(auth_key,match_data):
    headers={"Authorization":auth_key,"Content-Type":"application/json"}

    new_d={};new_d["pairs"]=match_data
    put_parameter=json.dumps(new_d)
    match_response=requests.put(base_url+"/match",headers=headers,data=put_parameter)
    match_data=match_response.json()
    match_json=json.loads(json.dumps(match_data))

    return match_json

def changegrade_api(auth_key,grade_data):
    headers={"Authorization":auth_key,"Content-Type":"application/json"}

    put_parameter='{"commands":'+grade_data+'}'
    changegrade_response=requests.put(base_url+"/change_grade",headers=headers,data=put_parameter)
    changegrade_data=changegrade_response.json()
    changegrade_json=json.loads(json.dumps(changegrade_data))

    return changegrade_json

def calculate_diff_by_time(time):
    return 445*(43-time)//35

def make_to_json_object(user_data):
    commands=[]
    for k,v in user_data.items():
        new_d={}
        new_d["id"]=k;new_d["grade"]=v
        commands.append(new_d)
    return json.dumps(commands)

problem1_auth_key=get_start_key("1")

user_dict={}
battle_dict={}

for i in range(1,31):
    user_dict[i]=4000
    battle_dict[i]=0

for i in range(0,596):
    if(i==0):
        changegrade_api(problem1_auth_key,make_to_json_object(user_dict))
    
    current_match=[]
    match_needed_group={}
    waiting_dict={}

    waitingline_info=get_api(problem1_auth_key,"/waiting_line").get("waiting_line")
    for w in waitingline_info:
        waiting_dict[w.get('id')]=w.get('from')
    
    gameresult_info=get_api(problem1_auth_key,"/game_result").get("game_result")

    for result in gameresult_info:
        diff=calculate_diff_by_time(int(result.get("taken")))
        winner,loser=result.get("win"),result.get("lose")
        user_dict[winner]=abs(user_dict[winner]+diff)
        user_dict[loser]=abs(user_dict[loser]-diff)

    for id,start_time in waiting_dict.items():
        if(battle_dict[id]<=3 or i-start_time>2):
            match_needed_group[id]=user_dict[id]

        for nid in waiting_dict.keys():
            if(nid==id): continue
            if(abs(user_dict[nid]-user_dict[id])<=300):
                current_match.append([id,nid])
                battle_dict[id]+=1;battle_dict[nid]+=1
                if(match_needed_group.get(id)!=None):
                    del match_needed_group[id]
                if(match_needed_group.get(nid)!=None):
                    del match_needed_group[nid]
                
    my_list=sorted(match_needed_group.items(), key=lambda x: x[1])

    for i in range(0,len(my_list)-1,2):
        current_match.append([my_list[i][0],my_list[i+1][0]])
        battle_dict[my_list[i][0]]+=1
        battle_dict[my_list[i+1][0]]+=1
    
    res=match_api(problem1_auth_key,current_match)

    changegrade_api(problem1_auth_key,make_to_json_object(user_dict))

userinfo=get_api(problem1_auth_key,"/user_info")
score=get_api(problem1_auth_key,"/score")