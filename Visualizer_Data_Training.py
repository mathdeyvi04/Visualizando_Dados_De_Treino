# Código responsável por providenciar os gráficos.

from Load_Data_Training import *


def apresentar_numeros_principais(
        df: dict
) -> None:
    """
    Descrição:
        Disporá os valores principais do treino,
        tempo total e distância total percorrida.
    """

    col1, col2 = st.columns(
        2
    )

    with col1:
        # Colocando Distância Percorrida
        st.markdown(
            """
            <style>
            .big-title {
                font-size: 60px;
                text-align: center;
                font-family: 'Roboto', sans-serif;
                margin-top: 0%;
            }
            
            .title {
                font-size: 60px;
                text-align: center;
                color: #c4804f;
                font-family: 'Roboto', sans-serif;
                margin-top: 0%;
            }
            </style>
            """ + f"""
            <div class="big-title">
                Distância
            </div>
            
            <div class="title">
                {df['Distância (m)']}m
            </div>
            """,
            unsafe_allow_html=True
        )

        st.divider()

        st.markdown(
            """
            <style>
            .big-title {
                font-size: 40px;
                text-align: center;
                font-family: 'Roboto', sans-serif;
                margin-top: 0%;
            }

            .title {
                font-size: 60px;
                text-align: center;
                color: #c4804f;
                font-family: 'Roboto', sans-serif;
                margin-top: 0%;
            }
            </style>
            """ + f"""
            <div class="big-title">
                Batimento Cardíaco Médio
            </div>

            <div class="title">
                {df['Batimento Cardíaco Médio']}
            </div>
            """,
            unsafe_allow_html=True
        )

    with col2:
        # Colocando Tempo Total
        st.markdown(
            """
            <style>
            .big-title {
                font-size: 60px;
                text-align: center;
                font-family: 'Roboto', sans-serif;
                margin-top: 0%;
            }

            .title {
                font-size: 60px;
                text-align: center;
                color: #c4804f;
                font-family: 'Roboto', sans-serif;
                margin-top: 0%;
            }
            </style>
            """ + f"""
            <div class="big-title">
                Tempo Total
            </div>

            <div class="title">
                {df['Tempo Total (min,seg)']}
            </div>
            """,
            unsafe_allow_html=True
        )

        st.divider()

        # Calorias Gastas
        st.markdown(
            """
            <style>
            .big-title {
                font-size: 60px;
                text-align: center;
                font-family: 'Roboto', sans-serif;
                margin-top: 0%;
            }

            .title {
                font-size: 60px;
                text-align: center;
                color: #c4804f;
                font-family: 'Roboto', sans-serif;
                margin-top: 0%;
            }
            </style>
            """ + f"""
            <div class="big-title">
                Calorias Gastas
            </div>

            <div class="title">
                {df['Calorias Gastas']}
            </div>
            """,
            unsafe_allow_html=True
        )