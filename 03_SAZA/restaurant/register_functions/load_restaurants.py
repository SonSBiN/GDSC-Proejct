from restaurant.models import Restaurant

import requests
import re

import pandas as pd

def isNaN(num):
    return num != num

def load_restaurants_api(): 
    
    i = 1

    while True: 

        restaurant = Restaurant()

        url = 'http://openapi.seoul.go.kr:8088/6663747a4672746135396c696b614a/xml/LOCALDATA_072404/{0}/{0}/'.format(i)

        response = requests.get(url).content
        html = response.decode('UTF-8') 

        code = re.findall('<CODE>(.*?)</CODE>', html)

        # 해당하는 데이터가 없습니다.
        if ( code == "INFO-200"):
            break

        if ( i % 1000 == 0):
            print('{0} 번째 데이터 저장이 완료되었습니다.'.format(i))

        name = re.findall('<BPLCNM>(.*?)</BPLCNM>', html)[0]
        address = re.findall('<SITEWHLADDR>(.*?)</SITEWHLADDR>', html)[0]

        restaurant.name = name 
        restaurant.address = address
        restaurant.save()

        i += 1

    print("모든 데이터 저장이 완료되었습니다.")


def get_cheonan_gu_df(filepath): 

    df = pd.read_excel(filepath)

    df = df.reset_index(drop=True)

    header = df.iloc[0]

    df = df[1:]

    df.rename(columns=header, inplace=True)
    
    return df 

def get_cheonan_df(df1, df2): 
    df = pd.concat([df1,df2], ignore_index=True)
    return df

def load_restaurants_csv():

    northwestgu = get_cheonan_gu_df('restaurant/register_functions/2022.5월 서북구 일반음식점 운영 현황.xls')
    dongnamgu = get_cheonan_gu_df('restaurant/register_functions/일반음식점.xlsx')

    cheonan = get_cheonan_df(northwestgu, dongnamgu)
    
    for i in range(len(cheonan)):
        try:
            name = cheonan['업소명'][i]

            address = cheonan['소재지(지번)'][i]
            dong = address.split(' ')[3]

            if (isNaN(cheonan['소재지(도로명)'][i])):
                continue

            address = cheonan['소재지(도로명)'][i]

            Restaurant.objects.create(name=name, address=address, dong=dong)
        
        except:
            continue
    
    print('모든 데이터 저장이 완료 되었습니다.')

