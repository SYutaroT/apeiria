import requests


class WeatherResponder:

    def is_weather(self, place):
        API_KEY = "52da9073a0440c73adee4aa68f62daf1"
        URL = "http://api.openweathermap.org/data/2.5/"
        data = requests.get(URL+"forecast?lang=ja&q=" +
                            place+"&appid="+API_KEY).json()
        i = 0
        forecast = "天気予報です\n"
        if "list" in data:
            for d in data["list"]:
                if (i+1) % 4 == 0:
                    forecast += "["+d["dt_txt"]+"]" + \
                        d["weather"][0]["description"]+"\n"
                i = i+1
        else:
            forecast = "ごめんなさい、そこはわからないです"
        return forecast
