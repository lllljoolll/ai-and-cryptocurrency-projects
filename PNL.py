import csv
from decimal import Decimal, InvalidOperation
def read_csv_to_list(file_path):
    rows = []
    with open(file_path, mode='r', newline='') as file:
        csv_reader = csv.reader(file)
        next(csv_reader)  # 첫 줄(헤더)을 건너뜁니다.
        for row in csv_reader:
            rows.append(row)
    return rows

# 파일 경로를 지정하세요
file_path = 'ai-crypto-project-3-live-btc-krw.csv'

# CSV 파일을 읽어 리스트로 변환 (첫 줄 제외)
csv_data = read_csv_to_list(file_path)

pnl1 = 0 # amount
pnl2 = 0 # price*quantity - fee
quantity = 0 # 남은 수량
ne_quan_err_count = 0 # 남은 수량이 음수가 되는지 체크
b = 0
a = [] # 수량이 움수가 된 줄



# 결과 출력

for line in csv_data:
    pnl1 += Decimal(line[4])
    
    if line[5] == '1': # sell
        pnl2 += Decimal(line[2])*Decimal(line[1])-Decimal(line[3])
        quantity -= Decimal(line[1])
        b += 1
        if quantity <0:
            ne_quan_err_count += 1
            a.append(b)
            #print(line)
            
    else:   # buy
        pnl2 += (-1) * Decimal(line[2])*Decimal(line[1])-Decimal(line[3])
        quantity += Decimal(line[1])
        b += 1
    #print(quantity) 
    

print('PNL(amount) : '+ str(pnl1))
print('PNL(price*quantity - fee) : ' + str(pnl2))
print('남아있는 수량 : ' + str(quantity))
print(ne_quan_err_count) 
#print(a)
#print(b) #header 제외 27201줄 