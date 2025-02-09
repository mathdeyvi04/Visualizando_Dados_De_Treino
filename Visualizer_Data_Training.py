# Código responsável por providenciar os gráficos.

from Load_Data_Training import *


def apresentar_numeros_principais(
        df: DataFrame
) -> None:
    """
    Descrição:
        Disporá os valores principais do treino,
        tempo total e distância total percorrida.
    """

    pprint(
        df
    )


apresentar_numeros_principais(
    organizando_dados(lendo_arquivo(
        "Dados/z_1.gpx"
    ))[1]
)
