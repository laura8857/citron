import requests
from config import api_key as key


def get_current_data(city):

    url = "https://api.weatherbit.io/v2.0/current?key="+key+"&lang=en&units=M&city="+city

    data_list ={}
    response = requests.get(url)

    if response.status_code == 200:
        data = response.json()
        print(data)
        data_list["weather_des"] = data["data"][0]["weather"]["description"]
        data_list["temp"] = data["data"][0]["temp"]
        data_list["app_temp"] = data["data"][0]["app_temp"]
        data_list["wind_spd"] = data["data"][0]["wind_spd"]
        data_list["precip"] = data["data"][0]["precip"]
        data_list["uv"] = data["data"][0]["uv"]

        
        print(data_list)

        return True, data_list
    # 如果不是狀態回應不是200，則印出狀態碼
    else:
        print("壞了，根本就不能用啊，ERROR CODE:",response.status_code)
        return False,""
    #req:1 it means today;2 it meand tomorrow
def get_forcast_data(city,hour=24,req=1):
    url = f"https://api.weatherbit.io/v2.0/forecast/hourly?city={city}&key={key}&hours={hour}"
    data_list ={}
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        # print(data)
        time = data["data"][0]["timestamp_local"][-8:-6]
        diff = 24-int(time)
        if req == 1 :
            for i in range(0,diff):
                data_list[i] = data["data"][i]
        elif req == 2 :
            k=0
            for i in range(diff,len(data["data"])):
                data_list[k] = data["data"][i]
                k+=1
        return True,data_list
        # print(data_list)

    else:
        print("壞了，根本就不能用啊，ERROR CODE:",response.status_code)
        return False,""

def data_process(data,req):
    data_procees_list ={}
    time = data["data"][0]["timestamp_local"][-8:-6]
    diff = 24-int(time)
    if req == 1 :
        for i in range(0,diff):
            data_procees_list[i] = data["data"][i]
    elif req == 2 :
        k=0
        for i in range(diff,len(data["data"])):
            data_procees_list[k] = data["data"][i]
            k+=1
    return data_procees_list

def temps_list_procees(data_list):
    temp_list = []
    for i in range(0,len(data_list)):
        temp_list.append(data_list[i]["temp"])
    return temp_list

def rain_process(data_list):
    rain_list ={}
    k=0
    # print(data_list)
    for i in range(0,len(data_list)):
        if data_list[i]["pop"] >=40:
            rain_list[k] = data_list[i]
            k+=1
    # print(rain_list)
    return rain_list

def wind_process(data_list):
    wind_list={}
    k=0
    # print(data_list)
    for i in range(0,len(data_list)):
        if data_list[i]["pop"] >=4:
            wind_list[k] = data_list[i]
            k+=1
    # print(rain_list)
    return wind_list

