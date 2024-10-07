import requests


def get_forecast_data():
    key = "02a8900661ee4c25a881e9cd2bdf6f83"
    url = "https://api.weatherbit.io/v2.0/forecast/hourly?city=Montrouge&key="+key+"&hours=48"


    response = requests.get(url)

    if response.status_code == 200:
        data = response.json()
        # print(data)
        weather_des = data["data"][0]["weather"]["description"]
        temps = data["data"][0]["temp"]
        timestamp_local =data["data"][0]["timestamp_local"]

        print(weather_des,temps,timestamp_local)
    # 如果不是狀態回應不是200，則印出狀態碼
    else:
        print("壞了，根本就不能用啊，ERROR CODE:",response.status_code)

    # 印出來​
    # print(data)

if __name__ == '__main__':
    get_forecast_data()