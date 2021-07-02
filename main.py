# coding: utf-8
import time
import openpyxl
import tweepy
from tweepy.error import TweepError
import pandas as pd
from pprint import pprint

API_KEY = "Sua chave"
API_SECRET_KEY = "Sua chave secreta"
ACCESS_TOKEN = "Seu token de acesso"
ACCESS_TOKEN_SECRET = "Seu token de acesso secreto"


def converte_mes(mes):
    dict_mes = {
        "Jan": "01",
        "Feb": "02",
        "Mar": "03",
        "Apr": "04",
        "May": "05",
        "jun": "06",
        "Jul": "07",
        "Aug": "08",
        "Sep": "09",
        "Oct": "10",
        "Nov": "11",
        "Dec": "12"
    }
    return dict_mes[mes]


# Autenticando no twitter
auth = tweepy.OAuthHandler(API_KEY, API_SECRET_KEY)
auth.set_access_token(ACCESS_TOKEN, ACCESS_TOKEN_SECRET)
# Criando a API
api = tweepy.API(auth)
from_date = "202105230354" # formato da data de inicio da busca
to_date = "202106220154"    # final da data de busca
dicionario_hashtag = []

while to_date != from_date:
    dados = api.search_30_day(environment_name="nome do ambiente no twetter developers",
                              query="o que quer pesquisar",
                              fromDate=from_date,
                              toDate=to_date,
                              maxResults=100
                              )

    for dado in dados:
        name = dado._json['user']['name']
        dia_semana, mes, dia, hora, _, ano = dado._json['created_at'].split()
        data = f"{dia}-{mes}-{ano}"

        try:
            cidade = dado._json['user']['location'].split(',')[0]
        except AttributeError:
            cidade = ""
            pass

        try:
            mensagem = dado._json['extended_tweet']['full_text']
        except KeyError:
            mensagem = dado._json['text']

        if "RT" in mensagem.split():
            tipo_mensagem = "Retweet"
            try:
                mensagem = dado._json['retweeted_status']['text']
            except KeyError:
                pass
        else:
            tipo_mensagem = "Tweet"

        dicionario = {"data": data,
                      "nome": name,
                      "cidade": cidade,
                      "tipo_mensagem": tipo_mensagem,
                      "mensagem": mensagem.replace("\n", "")
                      }
        dicionario_hashtag.append(dicionario)

        mes = converte_mes(mes)
        hora, minuto, segundo = hora.split(":")
        to_date = f"{ano}{mes}{dia}{hora}{minuto}"
    print(to_date)
    time.sleep(5)

df = pd.DataFrame(dicionario_hashtag)
df.to_excel("usemascara.xlsx", index=False)
