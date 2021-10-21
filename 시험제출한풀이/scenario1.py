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

def waitingline_api(auth_key):
    headers={"Authorization":auth_key,"Content-Type":"application/json"}

    waitingline_response=requests.get(base_url+"/waiting_line",headers=headers)
    waitingline_data=waitingline_response.json()
    waitingline_json=json.loads(json.dumps(waitingline_data)).get("waiting_line")

    return waitingline_json

def gameresult_api(auth_key):
    headers={"Authorization":auth_key,"Content-Type":"application/json"}

    gameresult_response=requests.get(base_url+"/game_result",headers=headers)
    gameresult_data=gameresult_response.json()
    gameresult_json=json.loads(json.dumps(gameresult_data))

    return gameresult_json

def userinfo_api(auth_key):
    headers={"Authorization":auth_key,"Content-Type":"application/json"}

    userinfo_response=requests.get(base_url+"/user_info",headers=headers)
    userinfo_data=userinfo_response.json()
    userinfo_json=json.loads(json.dumps(userinfo_data))

    return userinfo_json

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

def score_api(auth_key):
    headers={"Authorization":auth_key,"Content-Type":"application/json"}

    score_response=requests.get(base_url+"/score",headers=headers)
    score_data=score_response.json()
    score_json=json.loads(json.dumps(score_data))

    return score_json

def calculate_diff_by_time(time):
    return 445*(43-time)//35

def make_to_json_object(user_data):
    commands=[]
    for k,v in user_data.items():
        new_d={};
        new_d["id"]=k;new_d["grade"]=v
        commands.append(new_d)
    return json.dumps(commands)

problem1_auth_key=get_start_key("1")

user_dict={}
battle_dict={}

# user들의 랭크 초기화
for i in range(1,31):
    user_dict[i]=4000
    battle_dict[i]=0;

for i in range(0,596):
    if(i==0):
        changegrade_api(problem1_auth_key,make_to_json_object(user_dict))
    
    current_match=[]
    match_needed_group={};
    waiting_dict={};

    waitingline_info=waitingline_api(problem1_auth_key)
    for w in waitingline_info:
        waiting_dict[w.get('id')]=w.get('from')

    '''
    게임결과를 받아서 점수를 계산한다.
    '''
    gameresult_info=gameresult_api(problem1_auth_key).get("game_result")

    for result in gameresult_info:
        diff=calculate_diff_by_time(int(result.get("taken")))
        winner=result.get("win")
        loser=result.get("lose")
        user_dict[winner]=abs(user_dict[winner]+diff);
        user_dict[loser]=abs(user_dict[loser]-diff);

    for id,start_time in waiting_dict.items():
        '''
        1. 전적이 3전 이하인 경우에는 대기없이 매칭
        2. 매칭 대기시간이 2분지나면 매칭 필요한 그룹에 넣음.
        '''
        if(battle_dict[id]<=3 or i-start_time>2):
            match_needed_group[id]=user_dict[id];

        '''
        3. 대기 그룹중 grade차이가 300이하인 사람이 오면 바로 매칭시킴 (점수차이 튜닝)
            match_needed_group에서 해당 id들은 삭제.
        '''
        for nid in waiting_dict.keys():
            if(nid==id): continue
            if(abs(user_dict[nid]-user_dict[id])<=300):
                pair=[];pair.append(id);pair.append(nid);
                current_match.append(pair)
                battle_dict[id]+=1;battle_dict[nid]+=1
                if(match_needed_group.get(id)!=None):
                    del match_needed_group[id]
                if(match_needed_group.get(nid)!=None):
                    del match_needed_group[nid]
                
    '''
    match_needed_group에 있는 것들 끼리 매칭시킴.(grade로 정렬해서 두쌍씩)
    그리고 match api를 통해 매칭한 것들을 보낸다.
    '''
    my_list=sorted(match_needed_group.items(), key=lambda x: x[1])

    for i in range(0,len(my_list)-1,2):
        pair=[];pair.append(my_list[i][0]);pair.append(my_list[i+1][0]);
        current_match.append(pair)
        battle_dict[my_list[i][0]]+=1
        battle_dict[my_list[i+1][0]]+=1
    
    res=match_api(problem1_auth_key,current_match)

    print(res)
    changegrade_api(problem1_auth_key,make_to_json_object(user_dict))

userinfo=userinfo_api(problem1_auth_key)
score=score_api(problem1_auth_key)

print(score)
# problem2_auth_key=get_start_key("2")