import sys
import datetime
import requests
import json

URL = "https://community-open-weather-map.p.rapidapi.com/forecast/daily"
PARAMS = {"q": "san francisco,us", "lat": "35", "lon": "139", "cnt": "10", "units": "metric or imperial"}


class WeatherForecast:
    def __init__(self, apikey):
        self.apikey = apikey
        self.wczytaj_dane_o_pogodzie()

    def __getitem__(self, date):
        return self.spr_danych_o_deszczu(date)

    def __iter__(self):
        ...

    def items(self):
        return self.saved_history.items()

    def odp_o_deszczu(self, date_to_check2):
        print(f"Opady w dniu {date_to_check2}: {self.saved_history[date_to_check2]}")
        if self.saved_history[date_to_check2] > 0:
            return "Będzie padać"
        else:
            return "Nie będzie padać"

    def spr_danych_o_deszczu(self, date_to_check):
        if date_to_check in self.saved_history:
            return self.odp_o_deszczu(date_to_check)
        else:
            from datetime import datetime
            headers = {"X-RapidAPI-Host": "community-open-weather-map.p.rapidapi.com", "X-RapidAPI-Key": self.apikey}
            response = requests.get(URL, headers=headers, params=PARAMS)
            user_object = response.json()
            for element in user_object["list"]:
                rain = element.get("pop", 0)
                date_info = element["dt"]
                day = datetime.fromtimestamp(date_info).date()
                self.saved_history[str(day)] = rain
            if date_to_check in self.saved_history:
                with open("history_of_weather.json", "w") as f2:
                    json.dump(self.saved_history, f2)
                return self.odp_o_deszczu(date_to_check)
            else:
                print("Nie wiem - zapytanie o datę spoza bazy")

    def wczytaj_dane_o_pogodzie(self):
        with open("history_of_weather.json", "r") as f:
            self.saved_history = json.load(f)


wf = WeatherForecast(sys.argv[1])
# wf.spr_danych_o_deszczu(sys.argv[2])
print(wf[sys.argv[2]])


# date_to_check = sys.argv[2]
# wf[date_to_check]


if len(sys.argv) == 2 or len(sys.argv) == 3:
    wf = WeatherForecast(sys.argv[1])
    if len(sys.argv) == 2:
        date_to_check = str(datetime.datetime.now().date() + datetime.timedelta(days=1))
    elif len(sys.argv) == 3:
        date_to_check = sys.argv[2]
    print(wf[date_to_check])
else:
    print("Błąd - wprowadzono niepoprawne dane wejściowe z std")

# if len(sys.argv) == 3:  # podano datę na wejściu
#     API_key = sys.argv[1]
#     date_to_check = sys.argv[2]
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

