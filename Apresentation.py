import tempfile

from Visualizer_Data_Training import *

st.set_page_config(
    layout="wide"
)

st.sidebar.title(
    "TCX Examinator :runner: :checkered_flag:"
)

combbox = st.sidebar.selectbox(
    label="Selecione o Arquivo TCX",
    options=[
        "Carregar Arquivo Agora"
    ] + listdir(
        r"C:\Users\deyvi\Documents\ImperioPy\CienciaDados\Visualizando_Dados_De_Treino\Dados"
    ),
    help="Selecione entre um arquivo já baixado ou carregue o arquivo arrastando-o até a área."
)

st.sidebar.divider()

if not combbox.endswith(
    ".tcx"
):
    # Então vamos carregá-lo agora.

    arquivo_dado = st.sidebar.file_uploader(
        "Coloque o Arquivo Aqui",
        type=["tcx"]
    )

    if arquivo_dado is not None:
        # Aparentemente, isso não é um arquivo ou uma string, é um upload_file.
        # Precisamos baixar esse arquivo dentro do "servidor" para podermos usá-lo da maneira tradicional.

        combbox = carregando_arquivo_no_servidor(
             arquivo_dado
        )
else:
    combbox = fr"C:\Users\deyvi\Documents\ImperioPy\CienciaDados\Visualizando_Dados_De_Treino\Dados\{combbox}"

if not combbox.startswith(
    "Ca"
):
    atividade, dados_brutos = lendo_arquivo(
        combbox
    )

    info_fixas, df = organizando_dados(
        dados_brutos
    )

    st.markdown(
        """
        <style>
        .big-title {
            font-size: 60px;
            text-align: center;
            font-family: 'Roboto', sans-serif;
            margin-top: 0%;
        }
        
        </style>
        """ + f"""
        <div class="big-title">
            {info_fixas['Data']} | {atividade}
        </div>
        """,
        unsafe_allow_html=True
    )

    st.divider()

    st.subheader(
        "Localização"
    )

    st.map(
        df,
        latitude="Latitude",
        longitude="Longitude",
        size=1,
        height=800
    )

    st.divider()

    apresentar_numeros_principais(
        info_fixas
    )




