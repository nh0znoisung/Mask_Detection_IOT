
# import urllib3
# http = urllib3.PoolManager()
# resp = http.request("GET", 'https://io.adafruit.com/api/v2/GodOfThunderK19/feeds?x-aio-key=aio_hVNA81gluI7deGkFZK34L7zTRCdX')

# print(resp.json())

# data = r.data.decode(encoding='UTF-8',errors='strict')
# result = filter(lambda x: x.name =='btn_Start' , data)
# print(list(result))


import requests

url = 'https://io.adafruit.com/api/v2/GodOfThunderK19/feeds?x-aio-key=aio_hVNA81gluI7deGkFZK34L7zTRCdX'
response = requests.get(url)


def getData(name):
    data = response.json()
    try:
        result = filter(lambda x: x['key'] == name , data)
        return list(result)[0]['last_value']
    except:
        print("An exception occurred or Not Found")



print(getData("btn-start") )    