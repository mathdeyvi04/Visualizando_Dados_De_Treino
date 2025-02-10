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
) -> tuple[dict, DataFrame]:
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
        "Batimento Cardíaco Médio": dados_tcx.get("AverageHeartRateBpm").get("Value"),
        "Batimento Cardíaco Máximo": dados_tcx.get("MaximumHeartRateBpm"),
        "Tempo Total (min,seg)": f"{int(dados_tcx.get('TotalTimeSeconds')) // 60}:{int(dados_tcx.get('TotalTimeSeconds')) % 60}"
    }

    dados_tcx = dados_tcx[
        "Track"
    ][
        "Trackpoint"
    ]

    nomes_correspondentes = {
        "Cadence": "Cadência",
        "HeartRateBpm": "Batimento Cardíaco",
        "Time": "Instante",
        "LatitudeDegrees": "Latitude",
        "LongitudeDegrees": "Longitude",
        "ns3:Speed": "Pace"
    }

    info = {
        nome_de_coluna_apropriado: [] for nome_de_coluna_apropriado in nomes_correspondentes.values()
    }

    for ponto_de_medida in dados_tcx:
        for chave_do_ponto_de_medida in ponto_de_medida:
            if chave_do_ponto_de_medida in nomes_correspondentes:

                if chave_do_ponto_de_medida.startswith(
                        "H"
                ):
                    info[
                        nomes_correspondentes[
                            chave_do_ponto_de_medida
                        ]
                    ].append(
                        int(
                            ponto_de_medida[
                                chave_do_ponto_de_medida
                            ][
                                "Value"
                            ]
                        )
                    )

                    continue

                if chave_do_ponto_de_medida.startswith(
                        "T"
                ):
                    info[
                        nomes_correspondentes[
                            chave_do_ponto_de_medida
                        ]
                    ].append(
                        ponto_de_medida[
                            chave_do_ponto_de_medida
                        ][
                            11:19
                        ]
                    )

                    continue

                info[
                    nomes_correspondentes[
                        chave_do_ponto_de_medida
                    ]
                ].append(
                    float(
                        ponto_de_medida[
                            chave_do_ponto_de_medida
                        ]
                    )
                )

            else:
                if chave_do_ponto_de_medida.startswith(
                        "E"
                ):
                    # Então estamos nas extensões
                    for extensao_disponivel in ponto_de_medida[
                        chave_do_ponto_de_medida
                    ][
                        "ns3:TPX"
                    ]:
                        if extensao_disponivel in nomes_correspondentes:
                            info[
                                nomes_correspondentes[
                                    extensao_disponivel
                                ]
                            ].append(
                                50 / (
                                    3 * float(
                                        ponto_de_medida[
                                            chave_do_ponto_de_medida
                                        ][
                                            "ns3:TPX"
                                        ][
                                            extensao_disponivel
                                        ]
                                    )
                                )
                            )
                        else:
                            print(
                                f"A extensão {extensao_disponivel} não está cadastradas em nomes_correspondentes"
                            )

                            if st.runtime.exists():
                                st.warning(
                                    f"A extensão {extensao_disponivel} não está cadastradas em nomes_correspondentes"
                                )

                elif chave_do_ponto_de_medida.startswith(
                    "P"
                ):
                    # Estamos em Position
                    for coord in ponto_de_medida[
                        chave_do_ponto_de_medida
                    ]:
                        info[
                            nomes_correspondentes[
                                coord
                            ]
                        ].append(
                            float(
                                ponto_de_medida[
                                    chave_do_ponto_de_medida
                                ][
                                    coord
                                ]
                            )
                        )

    return info_fixas, DataFrame(
        info
    )


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
