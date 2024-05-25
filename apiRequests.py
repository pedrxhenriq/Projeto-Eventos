from datetime import datetime
import requests
import json
from collections import defaultdict

def api_viacep(cep):
    url = f"https://viacep.com.br/ws/{cep}/json/"
    
    try:
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()
        return data
    except requests.exceptions.RequestException as e:
        print("Error:", e)
        return None

def api_condicoes_climaticas(cidade, chave_api="1808e00f4931966416e1af70b1e28e89"):
    url = f"http://api.openweathermap.org/data/2.5/forecast?q={cidade}&appid={chave_api}&units=metric"
    
    resposta = requests.get(url)
    dados_climaticos = resposta.json()
    
    if 'list' not in dados_climaticos:
        return {"erro": "Dados de previsão não encontrados."}

    retorno = []

    for tempo in dados_climaticos["list"]:
        dt_str = datetime.utcfromtimestamp(tempo["dt"]).strftime('%d/%m/%Y %H:%M:%S')
        retorno.append({"dt": dt_str, "main": {
            "temperatura" : tempo["main"]["temp"],
            "sensacao_termica" : tempo["main"]["feels_like"],
            "temperatura_min" : tempo["main"]["temp_min"],
            "temperatura_max" : tempo["main"]["temp_max"]
        }})

    average_temperatures = calcular_media_temperaturas(retorno)
    
    return average_temperatures

def calcular_media_temperaturas(dados):
    temperaturas_por_data = defaultdict(list)

    for item in dados:
        data = item['dt'].split()[0]
        temperaturas_por_data[data].append(item)

    media_temperaturas = {}

    for data, temperaturas in temperaturas_por_data.items():
        media = {}
        for atributo in temperaturas[0]['main']:
            valores = [item['main'][atributo] for item in temperaturas]
            media[atributo] = float("{:.2f}".format(sum(valores) / len(valores)))

        media_temperaturas[data] = media

    resultado = [{"{}-{}-{}".format(data[6:], data[3:5], data[:2]): media} for data, media in media_temperaturas.items()]

    return resultado