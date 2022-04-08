import sys
import datetime
import requests
import json
import os

URL = "https://community-open-weather-map.p.rapidapi.com/forecast/daily"
PARAMS = {"q": "san francisco,us", "lat": "35", "lon": "139", "cnt": "10", "units": "metric or imperial"}


class WeatherForecast:
    def __init__(self, apikey):
        self.apikey = apikey
        self.wczytaj_dane_o_pogodzie()

    def __getitem__(self, date):
        return self.spr_danych_o_deszczu(date)

    def __iter__(self):
        return iter(self.saved_history.keys())

    def wczytaj_dane_o_pogodzie(self):
        with open("history_of_weather.json", "r") as f:
            self.saved_history = json.load(f)

    def items(self):
        return self.saved_history.items()

    def odp_o_deszczu(self, date_to_check2):
        # print(f"Opady w dniu {date_to_check2}: {self.saved_history[date_to_check2]}")
        if self.saved_history[date_to_check2] > 0:
            return f"{date_to_check2} -> Będzie padać"
        else:
            return f"{date_to_check2} -> Nie będzie padać"

    def spr_danych_o_deszczu(self, date_to_check1):
        if date_to_check1 in self.saved_history:
            return self.odp_o_deszczu(date_to_check1)
        else:
            headers = {"X-RapidAPI-Host": "community-open-weather-map.p.rapidapi.com", "X-RapidAPI-Key": self.apikey}
            response = requests.get(URL, headers=headers, params=PARAMS)
            user_object = response.json()
            for element in user_object["list"]:
                rain = element.get("pop", 0)
                date_info = element["dt"]
                day = datetime.datetime.fromtimestamp(date_info).date()
                self.saved_history[str(day)] = rain
            if date_to_check1 in self.saved_history:
                with open("history_of_weather.json", "w") as f2:
                    json.dump(self.saved_history, f2)
                return self.odp_o_deszczu(date_to_check1)
            else:
                return f"{date_to_check1} -> Nie wiem - zapytanie o datę spoza bazy"


def separator():
    w, h = os.get_terminal_size()
    print(w * "-")


wf = WeatherForecast(sys.argv[1])

if len(sys.argv) == 2 or len(sys.argv) == 3:
    if len(sys.argv) == 2:
        date_to_check = str(datetime.datetime.now().date() + datetime.timedelta(days=1))
    else:
        date_to_check = sys.argv[2]

separator()

print("Informacja o opadach dla następującego terminu:   ", wf[date_to_check])

separator()

print("Pogoda znana jest dla następujących terminów:")
lista_dat_z_pogoda = []
for elem in wf:
    lista_dat_z_pogoda.append(elem)
print(lista_dat_z_pogoda)

separator()

if wf:
    print("Znane informacje o deszczu to:")
    lista_deszczu = []
    for idx in wf.items():
        lista_deszczu.append(idx)
    print(lista_deszczu)
