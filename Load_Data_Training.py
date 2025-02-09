from pandas import DataFrame
import json as js
import xmltojson as xjs
from pprint import pprint
import streamlit as st


def lendo_arquivo(
        nome_arquivo: str
) -> None | dict:
    """
    Descrição:
        Lerá um determinado arquivo dado, desde que seja .gpx

    Retorno:
        Dicionário contendo informações cruciais.
        Exemplo:
            {'name': '20250207 Corrida ao ar livre',
             'trkseg': {'trkpt': [{'@lat': '-22.94348032',
                                   '@lon': '-43.15602432',
                                   'ele': '0.0',
                                   'extensions': {'ns3:TrackPointExtension': {'ns3:cad': '0.0',
                                                                              'ns3:hr': '122',
                                                                              'ns3:speed': '0.5138889'}},
                                    ...
                                ]
    """

    if not nome_arquivo.endswith(
            ".gpx"
    ):
        return None

    with open(
            nome_arquivo,
            "r"
    ) as dados_brutos_de_treino:
        dados_gpx = js.loads(
            xjs.parse(
                dados_brutos_de_treino.read()
            )
        )

    return dados_gpx[
        "gpx"
    ][
        "trk"
    ]


def organizando_dados(
        dados_gpx: dict
) -> tuple[str, DataFrame]:
    """
    Descrição:
        Lerá informações retiradas do gpx e criará um dataframe contendo os
        dados de forma mais apropriada.
    """

    data_e_tipo_de_atividade = dados_gpx[
        "name"
    ]

    # Limpando e Selecionando Melhor
    dados_gpx.pop(
        "name"
    )
    dados_gpx = dados_gpx[
        "trkseg"
    ][
        "trkpt"
    ]

    nomes_apropriados_correspondentes = {
        "@lat": "Latitude",
        "@lon": "Longitude",
        "ele": "Elevação",
        "time": "Instante",
        "ns3:cad": "Cadência",
        "ns3:hr": "Batimento Cardíaco",
        "ns3:speed": "Velocidade"
    }

    info = {
        nome_de_coluna_apropriado: [] for nome_de_coluna_apropriado in nomes_apropriados_correspondentes.values()
    }

    for ponto_de_medida in dados_gpx:
        for chave_do_ponto_de_medida in ponto_de_medida:
            if chave_do_ponto_de_medida in nomes_apropriados_correspondentes:
                if not chave_do_ponto_de_medida.startswith(
                    "t"
                ):
                    info[
                        nomes_apropriados_correspondentes[
                            chave_do_ponto_de_medida
                        ]
                    ].append(
                        ponto_de_medida[
                            chave_do_ponto_de_medida
                        ]
                    )
                else:
                    # Então estamos mexendo no tempo
                    info[
                        nomes_apropriados_correspondentes[
                            chave_do_ponto_de_medida
                        ]
                    ].append(
                        # Assim ficamos com o tempo em H:M:S
                        ponto_de_medida[
                            chave_do_ponto_de_medida
                        ].split(
                            "T"
                        )[
                            -1
                        ][
                            :-1
                        ]
                    )

            else:
                # Sabemos que estamos nas extensões
                for extensao_disponivel in ponto_de_medida[
                    chave_do_ponto_de_medida
                ][
                    "ns3:TrackPointExtension"
                ]:
                    try:
                        info[
                            nomes_apropriados_correspondentes[
                                extensao_disponivel
                            ]
                        ].append(
                            ponto_de_medida[
                                chave_do_ponto_de_medida
                            ][
                                "ns3:TrackPointExtension"
                            ][
                                extensao_disponivel
                            ]
                        )
                    except KeyError:
                        # Caso tenha uma extensão que não consideramos
                        print(
                            f"{extensao_disponivel} não foi cadastrada em nomes_apropriados. Arq: Load_Data_Training / Lin 123."
                        )

                        # Se está rodando uma aplicação streamlit
                        if st.runtime.exists():
                            st.sidebar.warning(
                                f"{extensao_disponivel} não foi cadastrada em nomes_apropriados. Arq: Load_Data_Training / Lin 123."
                            )

    return data_e_tipo_de_atividade, DataFrame(
        info
    )

print(
    organizando_dados(
        lendo_arquivo(
            "z_1.gpx"
        )
    )[1]
)
