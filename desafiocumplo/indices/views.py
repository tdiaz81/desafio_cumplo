from django.shortcuts import render, redirect
from django.conf import settings
from django.urls import reverse
from datetime import datetime, timedelta
import requests
import json

# Create your views here.
def promedio(lista):
    sum=0
    for i in range(0,len(lista)):
        lista[i] = lista[i].replace(".", "")        
        lista[i] = lista[i].replace(",", ".")
        sum=sum+float(lista[i])
    return sum/len(lista)

def indices(request):
    indice = {}
    val_Dolar = []
    val_Uf = []
    rango_Dolar = []
    rango_Uf = []
    rango_fechas = []
    if request.method == "POST":
        inputfechad = request.POST.get('desde', '')
        inputfechah = request.POST.get('hasta', '')
        fechad = datetime.strptime(inputfechad, '%Y-%m-%d')
        fechah = datetime.strptime(inputfechah, '%Y-%m-%d')
        indice['fechaDesde'] = str(datetime.strptime(inputfechad, '%Y-%m-%d').strftime('%d-%m-%Y'))
        indice['fechaHasta'] = str(datetime.strptime(inputfechah, '%Y-%m-%d').strftime('%d-%m-%Y'))
        if(fechad < fechah):
            lista_fechas = [fechad + timedelta(days=d) for d in range((fechah - fechad).days + 1)] 
            for fecha in lista_fechas:
                rango_fechas.append(str(datetime.strftime(fecha,'%d-%m-%Y')))
                ano = datetime.strftime(fecha,'%Y')
                mes = datetime.strftime(fecha,'%m')
                dia = datetime.strftime(fecha,'%d')
                urlDolar = settings.URL_SBIF_DOLAR + ano + '/' + mes + '/dias/' + dia + '?apikey=' + settings.API_KEY + '&formato=' + settings.FORMAT_SBIF
                urlUF = settings.URL_SBIF_UF + ano + '/' + mes + '/dias/' + dia + '?apikey=' + settings.API_KEY + '&formato=' + settings.FORMAT_SBIF
                #Llamada a API SBIF Dolar
                responseDolar = requests.get(urlDolar)
                jsonDolar = responseDolar.json()
                dumpDolar = json.dumps(jsonDolar)
                dataDolar = json.loads(dumpDolar)
                #Llamada a API SBIF UF
                responseUF = requests.get(urlUF)
                jsonUF = responseUF.json()
                dumpUF = json.dumps(jsonUF)
                dataUF = json.loads(dumpUF)
                try:
                    val_Dolar.append(str(dataDolar["Dolares"][0]["Valor"]))
                    rango_Dolar.append(str(datetime.strftime(fecha,'%d-%m-%Y')))
                    rango_Dolar.append(str(dataDolar["Dolares"][0]["Valor"]))
                except:
                    val_Dolar.append(str("0"))
                    rango_Dolar.append(str(datetime.strftime(fecha,'%d-%m-%Y')))
                    rango_Dolar.append(str("0"))
                try:
                    val_Uf.append(str(dataUF["UFs"][0]["Valor"]))
                    rango_Uf.append(str(datetime.strftime(fecha,'%d-%m-%Y')))
                    rango_Uf.append(str(dataUF["UFs"][0]["Valor"]))
                except:
                    val_Uf.append(str("0"))
                    rango_Uf.append(str(datetime.strftime(fecha,'%d-%m-%Y')))
                    rango_Uf.append(str("0"))

            indice['promDolar'] = "{0:.2f}".format(promedio(val_Dolar))
            indice['maxDolar'] = max(val_Dolar)
            indice['minDolar'] = min(val_Dolar)
            indice['rango_Dolar'] = rango_Dolar
            indice['promUf'] = "{0:.2f}".format(promedio(val_Uf))
            indice['maxUf'] = max(val_Uf)
            indice['minUf'] = min(val_Uf)
            indice['rango_Uf'] = rango_Uf
        else:
            return redirect(reverse('indices')+"?fail")

    return render(request, "indices/indices.html", {
        'indices': indice, 
        'rango_fechas': json.dumps(rango_fechas), 
        'val_Dolar': json.dumps(val_Dolar), 
        'val_Uf': json.dumps(val_Uf)
    })
