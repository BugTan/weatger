import urllib.request
import urllib.error
import pickle as p
import time



def visitWeb(url):
    try:
        return urllib.request.urlopen(url).read()

        # if content1=={} or content1==None:
        #     time.sleep(3)
        #     return visitWeb(url)  #必须加上这样的一句，不然返回的老是NoneType
        # else:
        #     return content1
    except urllib.error.URLError:
        print('URLError被调用了')
        time.sleep(3)
        # 必须加上这样的一句，不然返回的老是NoneType
        return visitWeb(url)  # 访问出错，延时3秒再访问





#获取省份编号
url0 = 'http://m.weather.com.cn/data5/city'
cityStr = ''
postfix = '.xml'
url = url0 + cityStr + postfix
content1 = visitWeb(url)
#content1 = urllib.request.urlopen(url).read()

#得到的是一个省份的list，后面需要进行bytes到str的转换
provincesList = content1.split(b',')

#建立省份索引的字典
citys = {}   #创建字典，声明作用，存储的是每一个身份对应的编号
for province in provincesList:
    province = bytes.decode(province)  #转换为字符串str
    dashIndex = province.find('|')  #'|'的索引
    if dashIndex != -1:
        provinceIndex = province[0:dashIndex]  #省份转换为int格式索引,注意python的引号表示偏移量
        #就是说province[0:dashIndex表示从-0开始偏移dashIndex个量并不是从0到2
        provinceName = province[dashIndex+1:len(province)]

        #获取地级城市编号
       # cityStr = provinceIndex
        url = url0 + provinceIndex + postfix
        content1 = visitWeb(url)
        cityList = content1.split(b',')
      #  locals()[name] = {}  #吧字符串转换为变量名
        for city in cityList:
            city = bytes.decode(city)
            dashIndex = city.find('|')
            if dashIndex != -1:
                cityIndex = city[0:dashIndex]  # 省份转换为int格式索引,注意python的引号表示偏移量
                # 就是说province[0:dashIndex表示从-0开始偏移dashIndex个量并不是从0到2
                cityName = city[dashIndex + 1:len(city)]

                url = url0 + cityIndex + postfix
                content1 = visitWeb(url)
                countyList = content1.split(b',')
                for county in countyList:
                    county = bytes.decode(county)
                    dashIndex = county.find('|')
                    if dashIndex != -1:
                        countyIndex = county[0:dashIndex]
                        countyName = county[dashIndex + 1:len(county)]
                        url = url0 + countyIndex + postfix    #再查询一次就可以得到最终编码
                        content1 = visitWeb(url)

                        serialNum = bytes.decode(content1)
                        dashIndex = serialNum.find('|')
                        if dashIndex != -1:
                            cityNum = serialNum[dashIndex + 1:len(serialNum)]
                            citys[countyName] = cityNum  # 向字典添加项,101表示中国的号码
                            print(countyName + '|' +cityNum)
                          #  time.sleep(4)

#将抓取到的数据存储在文件里
cityFile = 'cityFile.data'
f = open(cityFile, 'wb')
p.dump(citys, f) # dump the object to a file
f.close()
