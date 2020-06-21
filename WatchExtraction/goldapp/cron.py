from goldapp.models import *

import requests
from datetime import datetime,date, timedelta
import time
import pytz

class GoldCron():

    def insert_gold_data(self):
        rate,ddate = self.get_date_rate()
        metals = self.get_date_ounce()

        if metals and rate and ddate:
            goldH = GoldHistory()
            goldH.date = datetime.now()
            goldH.price = metals["Gold"]
            goldH.save()

            gpWeight = GoldPriceWeight.objects.filter(pk=1).first()
            gpWeight.gold_price = rate
            gpWeight.gold_weight = metals["Gold"]
            gpWeight.platinum_weight = metals["Platinum"]
            gpWeight.silver_weight = metals["Silver"]
            gpWeight.last_updated = datetime.now()
            gpWeight.save()
            print("Data Updated Succesfully ",str(datetime.now()))

    def get_date_rate(self):
        i = 0
        while True:
            today = (date.today() - timedelta(days=i)).strftime("%d/%m/%Y")
            rate_resp = self.pull_rate_resp(today)
            rate_data = rate_resp['cotizacionesoutlist']['Cotizaciones']
            i = i+1
            if len(rate_data)>0:
                return rate_data[0]['TCV'], today
            else:
                print("No data for date: ",today)
        return None

    def get_date_ounce(self):
        ounce_resp = self.pull_ounce_resp()
        precious_metals = ounce_resp["PreciousMetals"]["PM"]
        metals = {}
        for metal in precious_metals:
            if metal["Symbol"] == "AG":
                metals["Silver"] = metal["Bid"]
            if metal["Symbol"] == "AU":
                metals["Gold"] = metal["Bid"]
            if metal["Symbol"] == "PT":
                metals["Platinum"] = metal["Bid"]
        return metals

    def pull_ounce_resp(self):
        response = requests.get('https://proxy.kitco.com/getPM?symbol=AG,AU,PD,PT&type=json',
            headers={'Accept-Encoding': 'gzip, deflate, br',
                    'Accept-Language': 'en-US,en;q=0.9',
                    'User-Agent':'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.169 Safari/537.36',
                    'Accept':'text/plain, /; q=0.01',
                    'Origin':'https://www.kitco.com',
                    'Referer':'https://www.kitco.com/jewelry/',
                    'Connection':'keep-alive'}
        )
        return response.json()


    def pull_rate_resp(self,today):

        data = '{"KeyValuePairs":{"Monedas":[{"Val":"2225","Text":"DLS. USA BILLETE"}],"FechaDesde":"'+today+'","FechaHasta":"'+today+'","Grupo":"2"}}'
        response = requests.get('https://www.bcu.gub.uy/_layouts/BCU.Cotizaciones/handler/CotizacionesHandler.ashx?op=getcotizaciones',
            data = data,
            headers={'Connection':'keep-alive',
                    'Pragma':'no-cache',
                    'Cache-Control':'no-cache',
                    'Accept':'application/json, text/javascript, /; q=0.01',
                    'X-Requested-With':'XMLHttpRequest',
                    'User-Agent':'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.129 Safari/537.36',
                    'Content-Type':'application/json; charset=UTF-8',
                    'Origin':'https://www.bcu.gub.uy',
                    'Sec-Fetch-Site':'same-origin',
                    'Sec-Fetch-Mode':'cors',
                    'Sec-Fetch-Dest':'empty',
                    'Referer':'https://www.bcu.gub.uy/Estadisticas-e-Indicadores/Paginas/Cotizaciones.aspx',
                    'Accept-Language':'en-US,en;q=0.9',
                    'Cookie':'ASP.NET_SessionId=qlfmbtphqw5kj214fdugmxgj; WSS_FullScreenMode=false'}
            )
        return response.json()

def gold_data_cron():
    goldCron = GoldCron()
    goldCron.insert_gold_data()