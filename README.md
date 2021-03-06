# kakao_blind_2022_2nd_codetest

2022 카카오 신입공채 2차 코딩테스트 풀이 코드입니다.
문제공개가 되지않아, 기억나는 것대로만 작성합니다.
점수 가중치를 고려하지 않은 스코어보드 결과로 200등 안쪽의 점수를 받았습니다.

코드는 api호출 관련된 부분과 로직을 수행하는 부분으로 크게 나뉩니다.
json 파서는 파이썬의 json 라이브러리를 이용하였으며, api 호출시에는 requests 라이브러리를 이용하였습니다.
로직의 경우에는 파이썬의 기본 라이브러리를 사용하여 처리하였습니다.

## 로직
게임 리그오브레전드의 elo 시스템을 생각하면서 구현하였습니다.
유저 id별 점수 정보와 총 전적 수를 각각 user_dict,battle_dict에 저장하였습니다.

1. 최초 각 사용자별로 기본점수를 설정해주었습니다. 점수가 최소 0에서 최대 8000 사이 정도였던걸로 기억합니다. 정규분포를 따르는 구조를 갖고있기에 중위값인 4000을 기본점수로 책정하였습니다.

2. 매 분별로 들어오는 매칭을 원하는 유저 정보와, 대전 결과를 조회하면서 반복문을 수행합니다. 이때 0분일 때는, 최초에 책정했던 기본점수를 api를 통해 갱신합니다.

3. 들어오는 매칭대기 정보와, 대전결과 정보를 다음과 같이 처리합니다.
    - 전적이 3전 이하인 경우에는 대기없이 매칭(전적횟수 튜닝)
    - 매칭 대기시간이 2분지나면 매칭 필요한 그룹에 넣음(대기시간 튜닝)
    - 대기 그룹중 grade차이가 300이하인 사람이 오면 바로 매칭시킴 (점수차이 튜닝), match_needed_group에서 해당 id들은 삭제.
    - match_needed_group에 있는 것들 끼리 매칭시킴.(grade로 정렬해서 두쌍씩)

4. 대전결과 정보에 대한 점수변동 처리는 게임길이를 바탕으로 문제에서 주어졌던 게임길이 산정방식을 역연산해서 유저간 점수차이를 도출하여 변동을 시켰습니다.