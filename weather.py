import json
import urllib.request
import urllib.error
import pickle as p

try:
    f = open('cityFile.data','rb')
    citys = p.load(f)
except:
    import getCItyNum
else:
    url0 = 'http://www.weather.com.cn/data/cityinfo/'
    postfix = '.html'
    city = input('你想查看哪个城市的天气？')
    if city in citys.keys():
        try:
            url = url0 + citys[city] + postfix
            urldata = urllib.request.urlopen(url).read()
            weather_data = json.loads(urldata.decode())
            cityWeather = [weather_data['weatherinfo']['weather'] + weather_data['weatherinfo']['city'] ]
            print(weather_data['weatherinfo']['weather'])
            print(weather_data['weatherinfo']['temp1']+'~'+weather_data['weatherinfo']['temp2'])
        except urllib.error.URLError:   #异常处理
            print('查询失败！')
    else:
        print('没有找到该城市！')