import pymongo
import pandas as pd
import csv

client = pymongo.MongoClient(host='47.103.7.87', port=27017,connect=False)
db = client['cdershouche']
collection = db['car_info']

queryset = collection.find()
dataframe = pd.DataFrame(queryset, columns=['c_type', 'c_series', 'year', 'distance', 'price']).sort_index().drop_duplicates()
dataframe.to_csv('../results/carinfo.csv', index=False, header=['品牌', '车系', '上牌时间', '里程', '价格'])

