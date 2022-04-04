import sys
import datetime
import requests
import json


class WeatherForecast:
    def __init__(self):
        ...

    def __getitem__(self, date):
        return self.spr_danych_o_deszczu()[date]

    def __iter__(self):
        ...

    def items(self):
        ...

    def odp_o_deszczu(self):
        print(f"Opady w dniu {date_to_check}: {saved_history[date_to_check]}")
        if saved_history[date_to_check] > 0:
            return "Będzie padać"
        else:
            return "Nie będzie padać"

    def spr_danych_o_deszczu(self):
        if date_to_check in saved_history:
            self.odp_o_deszczu()
        else:
            from datetime import datetime  # TODO: ? -> dlaczego nie zaciąga fromtimestamp z import datetime tylko trzeba wpisać dodatkowy import?
            url = "https://community-open-weather-map.p.rapidapi.com/forecast/daily"
            params = {"q": "san francisco,us", "lat": "35", "lon": "139", "cnt": "10", "units": "metric or imperial"}
            headers = {"X-RapidAPI-Host": "community-open-weather-map.p.rapidapi.com", "X-RapidAPI-Key": sys.argv[1]}
            response = requests.get(url, headers=headers, params=params)
            user_object = response.json()
            for element in user_object["list"]:
                rain = element.get("pop", 0)
                date_info = element["dt"]
                day = datetime.fromtimestamp(date_info).date()
                saved_history[str(day)] = rain
            if date_to_check in saved_history:
                self.odp_o_deszczu()
                with open("history_of_weather.json", "w") as f2:  #TODO: nadpisuje wszystko, zmienić na możliwość dopisywania?
                    json.dump(saved_history, f2)
            else:
                print("Nie wiem - zapytanie o datę spoza bazy")


with open("history_of_weather.json", "r") as f:
    saved_history = json.load(f)

wf = WeatherForecast()
date_to_check = sys.argv[2]
wf[date_to_check]

#
# if len(sys.argv) == 3:  # podano datę na wejściu
#     API_key = sys.argv[1]
#     date_to_check = sys.argv[2]    # TODO: sprawdzać popoprawność podania daty?
#     wf[date_to_check]    # spr_danych_o_deszczu()
# elif len(sys.argv) == 2:  # nie podano daty na wejściu
#     API_key = sys.argv[1]
#     date_to_check = str(datetime.datetime.now().date() + datetime.timedelta(days=1))
#     spr_danych_o_deszczu()
# else:
#     print("Błąd - wprowadzono niepoprawne dane wejściowe z std")
#
# wf = WeatherForecast()
# print(wf["2022-04-01"])

