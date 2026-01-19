import requests
import math
import pandas as pd

# 1. 초기 설정
numOfRows = 1000  # 한 페이지당 1,000개씩 호출
pageNo = 1
all_data = []
url = 'http://apis.data.go.kr/B552584/EvCharger/getChargerInfo'

# 2. 첫 호출로 전체 개수 파악
params = {'serviceKey': "insert_key_number", 'pageNo': 1, 'numOfRows': 1, 'dataType': 'JSON'}
response = requests.get(url, params=params).json()
total_count = int(response['totalCount'])  # 전체 건수 
total_pages = math.ceil(total_count / numOfRows) # 전체 페이지 수 계산

# 3. 반복문을 이용해 pageNo 증가시키며 호출
for i in range(1, total_pages + 1):
    params['pageNo'] = i
    params['numOfRows'] = numOfRows
    
    res = requests.get(url, params=params).json()
    items = res['items']['item'] # 해당 페이지의 데이터 리스트
    all_data.extend(items)
    
    print(f"{i}/{total_pages} 페이지 수집 중...")

df = pd.DataFrame(all_data)
df.to_csv("ev_chargers_data.csv", index=False, encoding='utf-8-sig')