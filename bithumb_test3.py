import time
import requests
import pandas as pd
import datetime
import os
import sys




def wait_until_midnight():
    # 현재 시간 가져오기
    current_time = time.localtime()
    current_hour = current_time.tm_hour
    current_minute = current_time.tm_min
    current_second = current_time.tm_sec

    # 자정까지 남은 시간 계산
    remaining_hours = 24 - current_hour - 1
    remaining_minutes = 59 - current_minute
    remaining_seconds = 60 - current_second
    
    print( remaining_hours, remaining_minutes, remaining_seconds)

    # 대기
    time.sleep(remaining_hours * 3600 + remaining_minutes * 60 + remaining_seconds)

    # 자정에 프로그램 시작
    print("프로그램 시작!")

# 자정까지 대기
wait_until_midnight()

while(1):
    
    try:

        book = {}
        book2 = {}
        response = requests.get ('https://api.bithumb.com/public/orderbook/BTC_KRW/?count=5')
        response2 = requests.get ('https://api.bithumb.com/public/orderbook/ETH_KRW/?count=5')
        book = response.json()
        book2 = response2.json()


    
        data = book['data']
        data2 = book2['data']
    
    
        bids = (pd.DataFrame(data['bids'])).apply(pd.to_numeric,errors='ignore')
        bids.sort_values('price', ascending=False, inplace=True)
        bids = bids.reset_index(); del bids['index']
        bids['type'] = 0

        bids2 = (pd.DataFrame(data2['bids'])).apply(pd.to_numeric,errors='ignore')
        bids2.sort_values('price', ascending=False, inplace=True)
        bids2 = bids2.reset_index(); del bids2['index']
        bids2['type'] = 0
    
        asks = (pd.DataFrame(data['asks'])).apply(pd.to_numeric,errors='ignore')
        asks.sort_values('price', ascending=True, inplace=True)
        asks['type'] = 1 

        asks2 = (pd.DataFrame(data2['asks'])).apply(pd.to_numeric,errors='ignore')
        asks2.sort_values('price', ascending=True, inplace=True)
        asks2['type'] = 1 

        #print (bids)  #
        #print ("\n")  
        #print (asks)  

        df = pd.concat([bids, asks])    # df = bids.append(asks) >>>>  df = pd.concat([bids, asks])
        df2 = pd.concat([bids2, asks2])
    
        timestamp = datetime.datetime.now()
        req_timestamp = timestamp.strftime('%Y-%m-%d %H:%M:%S')

        df['quantity'] = df['quantity'].round(decimals=4)
        df['timestamp'] = req_timestamp

        df2['quantity'] = df2['quantity'].round(decimals=4)
        df2['timestamp'] = req_timestamp
    
        #print (df)
        #print ("\n")
    
        df.to_csv("./book-2024-04-29-bithumb-btc.csv", index=False, header=False, mode = 'a') # 파일명 날짜 변경 필요
        df2.to_csv(".book-2024-04-29-bithumb-eth.csv", index=False, header=False, mode = 'a')
        '''
        should_write_header = os.path.exists(fn)
        if should_write_header == False:
        df.to_csv(fn, index=False, header=True, mode = 'a')
        else:
            df.to_csv(fn, index=False, header=False, mode = 'a')

        '''
    
        time.sleep(4.1)
    except Exception as e:
        print(e)
        time.sleep(4.1)