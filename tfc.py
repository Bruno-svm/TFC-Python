# -*- coding: utf-8 -*-
"""tfc

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1wI_uxio3QaD7KvnKp3ehQVmDOChYs2Q6
"""

import pandas as pd
import math

# importando os dados da tabela do excel
# A configuração de importação foi feita em cima da tabela gerada pelo site da WEG, sem nenhuma edição anterior.


df = pd.read_excel("/content/30CV_premi.xlsx", header=1, skiprows=3)

# Tabela antes do tratamento dos dados
df.head(8)

# Excluindo algumas colunas que não serão usadas :
colunas_para_excluir = ['Unnamed: 6','Altitude','Unnamed: 21','Nível de ruído',
             'Temperatura Ambiente','Fator de serviço','Proteção',
             'Unnamed: 17','Unnamed: 18','Unnamed: 20','Regime']
df = df.drop(colunas_para_excluir, axis=1)

# Retirando as linhas nulas da tabela
linhas_para_excluir = [0]
df = df.drop(linhas_para_excluir)

!pip install openpyxl

# Tabela apos a retirada das linhas nulas e colunas que não serão usadas
df.head()

import re


# Definindo uma função para extrair apenas os números de uma string
def extrair_numeros(valor):
    numeros = re.findall(r'\d+\.\d+|\d+', str(valor))
    return ''.join(numeros)

# Aplicando a função à coluna 'Momento de inércia' para extrair apenas os números
df['Momento de inércia'] = df['Momento de inércia'].apply(extrair_numeros)

import re


# Definindo uma função para extrair apenas os números de uma string
def extrair_numeros(valor):
    numeros = re.findall(r'\d+\.\d+|\d+', str(valor))
    return ''.join(numeros)

# Aplicando a função à coluna 'Rotação nominal' para extrair apenas os números
df['Rotação nominal'] = df['Rotação nominal'].apply(extrair_numeros)

# Mudando o tipo de dado para float
df['Rotação nominal'] = df['Rotação nominal'].astype(float)

# Mudando o tipo de dado para float
df['Potência'] = df['Potência'].astype(float)

# Retirando possiveis dados nulos
df = df.dropna(subset=['Momento de inércia'])

# mudando o tipo de dado para float
df['Momento de inércia'] = df['Momento de inércia'].astype(float)

# formato dos dados da tabela
df.dtypes

# Tabela pronta para a leitura do programa
df.head()

import pandas as pd
import math

def calcular_tempo_de_partida(potencia_Motor, inercia_Carga, torque_Inicial, torque_maximo,
                              inercia_motor, conjugado_carga, velocidade_motor):

    torque_nominal = (potencia_Motor*745.7)/(velocidade_motor*0.10471)
    conjugado_inicial_carga = (conjugado_carga / 5)
    conjugado_resistente = ((2 * conjugado_inicial_carga + conjugado_carga) / 3)
    conjugado_medio_motor = (0.45 * ((torque_Inicial/3) + (torque_maximo/3)) * torque_nominal )
    tempo_aceleracao = (2 * math.pi * (velocidade_motor/60) * (inercia_Carga + inercia_motor)) / (conjugado_medio_motor - conjugado_resistente)
    return tempo_aceleracao, torque_nominal

#Calculo realizado considerando 1/3 do torque

# Número total de linhas na tabela
total_linhas = len(df)

# Listas para armazenar os resultados
resultados_tempo_partida = []
resultados_torque_nominal = []

# Iterando sobre cada linha do DataFrame
for i in range(total_linhas):
    # Extrair os dados das colunas para a linha atual
    torque_Inicial = df.iloc[i, 7]
    torque_maximo = df.iloc[i, 8]
    inercia_motor = df.iloc[i, 9]
    conjugado_carga = 122.07  # Definido pela carga escolhida
    inercia_Carga = 0.292  # Definido pela carga escolhida
    potencia_Motor = df.iloc[i, 4]
    velocidade_motor = df.iloc[i, 12]

    # Calcular tempo de partida e torque nominal para a linha atual
    tempo_partida, torque_nominal = calcular_tempo_de_partida(potencia_Motor, inercia_Carga, torque_Inicial, torque_maximo,
                                                              inercia_motor, conjugado_carga, velocidade_motor)

    # Armazenar os resultados para a linha atual
    resultados_tempo_partida.append(tempo_partida)
    resultados_torque_nominal.append(torque_nominal)

# Exibindo os resultados
for i in range(total_linhas):
    print("Para o Motor", i+1, "- Tempo de partida é:", resultados_tempo_partida[i], "segundos - Torque nominal do Motor:", resultados_torque_nominal[i])

