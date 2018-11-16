from django.shortcuts import render, redirect
from django.conf import settings
from django.urls import reverse
import requests
import json

# Create your views here.
def bonus(request):
    bono = {}    
    tmc = {}
    val_TMC = []
    val_Tipo = []
    val_Tasa = []
    if request.method == "POST":
        ano = request.POST.get('ano', '')
        bono['ano'] = ano
        try:
            int(ano)
            urlTMC = settings.URL_SBIF_TMC + ano + '?apikey=' + settings.API_KEY + '&formato=' + settings.FORMAT_SBIF
            #Llamada a API SBIF Dolar
            responseTMC = requests.get(urlTMC)
            jsonTMC = responseTMC.json()
            dumpTMC = json.dumps(jsonTMC)
            dataTMC = json.loads(dumpTMC)
            try:
                for valor in dataTMC['TMCs']:
                    val_Tasa.append(valor['Valor'])
                    val_Tipo.append(valor['Tipo'])
                    val_TMC.append(valor)
                
                tmc['TMCs'] = val_TMC
            except:
                return redirect(reverse('bonus')+"?nok")
        except:
            return redirect(reverse('bonus')+"?fail")

    return render(request, "bonus/bonus.html", {
        'bonus': bono,
        'TMC' : val_TMC,
        'val_Tasa' : json.dumps(val_Tasa),
        'val_Tipo' : json.dumps(val_Tipo)
    })