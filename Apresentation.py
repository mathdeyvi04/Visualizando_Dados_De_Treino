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
    data_e_tipo, df = organizando_dados(lendo_arquivo(
        combbox
    ))

    data, atividade = tratando_data_do_treino(
        data_e_tipo[:8]
    ), data_e_tipo[8:]

    st.title(
        f"{data} :arrow_forward: {atividade}"
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
        height=500
    )

    st.divider()

    apresentar_numeros_principais(
        df
    )




