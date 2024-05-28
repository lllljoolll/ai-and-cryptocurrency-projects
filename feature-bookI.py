import pandas as pd

def read_csv_in_chunks(filename, chunk_size=10):
    
    column_names = ['P', 'Q', 'T', 'S']
    
    
    df = pd.DataFrame(columns=column_names)
    rdf = pd.DataFrame(columns=['timestamp', 'mid_price', 'book-imbalance-0.2-5-1'])
    
    for chunk in pd.read_csv(filename, chunksize=chunk_size, header=None):
        
        chunk.columns = column_names
        chunk.index = range(chunk_size)

        midprice = (chunk.iloc[0].P + chunk.iloc[5].P)*0.5

        Quantchunk = chunk.Q
        Pricechunk = chunk.P

        quant_v_bid = Quantchunk[0:5] ** 0.2
        price_v_bid = Pricechunk[0:5] * quant_v_bid
        
        quant_v_ask = Quantchunk[5:] ** 0.2
        price_v_ask = Pricechunk[5:] *quant_v_ask

        askQty = quant_v_ask.values.sum()
        bidPx = price_v_bid.values.sum()
        bidQty = quant_v_bid.values.sum()
        askPx = price_v_ask.values.sum()
        
        book_price = 0 #because of warning, divisible by 0
        if bidQty > 0 and askQty > 0:
            book_price = (((askQty*bidPx)/bidQty) + ((bidQty*askPx)/askQty)) / (bidQty+askQty)
        
        booki = book_price - midprice
      

        timestamp = chunk.iloc[0].S

        data = {'timestamp':[timestamp]
                ,'mid_price': [midprice]
                ,'book-imbalance-0.2-5-1' :[booki]
                }
        featurechunck = pd.DataFrame(data)

        rdf =pd.concat([rdf,featurechunck], ignore_index=True)
        
        
        df = pd.concat([df, chunk], ignore_index=True)
        print(featurechunck)
        # Process each chunk (optional)
        #print("Processing new chunk:")
        #print(chunk)
        #print(midprice)
        #print(booki)
        #print(timestamp)
        
    rdf.to_csv("2024-04-29-bithumb-btc-feature.csv", index=False, header=False, mode = 'a')
    return rdf
filename = '2024-04-29-bithumb-btc.csv'
dataframe = read_csv_in_chunks(filename)
print(dataframe)


#2024-04-29-bithumb-btc.csv
#2024-04-29-bithumb-btc-feature.csv