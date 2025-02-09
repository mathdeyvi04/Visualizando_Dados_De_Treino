# Código responsável por providenciar ferramentas de carregamento
from pandas import DataFrame, Series
import json as js
import xmltojson as xjs
from pprint import pprint
import streamlit as st
from os import listdir
import tempfile
import plotly.express as px


def lendo_arquivo(
        nome_arquivo: str
) -> None | tuple[dict, str]:
    """
    Descrição:
        Lerá um determinado arquivo dado, desde que seja .tcx

    Retorno:
        Tupla contendo nome da atividade e dicionário de informações cruciais.
    """

    with open(
            nome_arquivo,
            "r"
    ) as dados_brutos_de_treino:
        dados_tcx: dict = js.loads(
            xjs.parse(
                dados_brutos_de_treino.read()
            )
        )

    dados_tcx = dados_tcx[
        "TrainingCenterDatabase"
    ][
        "Activities"
    ][
        "Activity"
    ]

    return (
        dados_tcx.get("Notes"),
        dados_tcx.get("Lap")
    )


def organizando_dados(
        dados_tcx: dict
) -> tuple[str, DataFrame]:
    """
    Descrição:
        Lerá informações retiradas do gpx e criará um dataframe contendo os
        dados de forma mais apropriada.
    """

    info_fixas = {
        # Coisas que não tínhamos no gpx.
        "Data": dados_tcx.get("@StartTime").split("T")[0],
        "Calorias Gastas": dados_tcx.get("Calories"),
        "Distância (m)": dados_tcx.get("DistanceMeters"),
        "Batimento Cardíaco Médio": dados_tcx.get("AverageHeartRateBpm"),
        "Batimento Cardíaco Máximo": dados_tcx.get("MaximumHeartRateBpm"),
        "Tempo Total (min,seg)": (
            dados_tcx.get("TotalTimeSeconds") // 60, dados_tcx.get("TotalTimeSeconds") % 60
        )
    }

    dados_tcx = dados_tcx[
        "Track"
    ][
        "Trackpoint"
    ]

    pass


def carregando_arquivo_no_servidor(
        # streamlit.runtime.uploaded_file_manager.UploadedFile
        arquivo_dado_pelo_usuario
) -> str:
    """
    Descrição:
        Há uma explicação no local onde essa função é utilizada.
        Salvamos o arquivo dado pelo usuário no servidor para podermos
        utilizar como se estivesse em condições.

    Retorno:
        Caminho do arquivo.

    """

    path_arquivo_temporario = tempfile.mktemp()

    with open(
            path_arquivo_temporario,
            "wb"
    ) as arquivo_temporario_a_ser_preenchido:
        arquivo_temporario_a_ser_preenchido.write(
            arquivo_dado_pelo_usuario.read()
        )

    return path_arquivo_temporario


def tratando_data_do_treino(
        data: str
) -> str:
    """
    Descrição:
        Recebe data na forma 20250207 e conserta para 07-02-2025
    """

    ano = data[:4]
    mes = data[4:6]
    dia = data[6:]

    return f"{dia}-{mes}-{ano}"
