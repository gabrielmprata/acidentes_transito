# :warning::ambulance: Acidentes de Trânsito nas Rodovias Federais Brasileiras :red_car::police_car:
Dados Abertos da Polícia Rodoviária Federal (PRF)

# :radio_button: Definição do problema
A malha rodoviária é a principal forma de locomoção do país no que tange o deslocamento de pessoas, produtos, matérias primas, alimentos e combustível a curtas e longas distâncias.

Este trabalho visa mostrar através dos dados abertos disponibilizados pela Polícia Rodoviária Federal, dentre os 70.000 Km de rodovias onde atua, o impacto dos acidentes de trânsito e sua letalidade nas rodovias federais, tendo como período analisado o ano de 2024.

O Brasil é o terceiro país com mais mortes no trânsito, ficando atrás apenas da Índia e da China segundo o relatório Global Status Report on Road Safety da Organização Mundial de Saúde (OMS).

Cerca de 84% dos acidentes de trânsito nas rodovias federais brasileiras, são com vítimas, tendo em vista esse grande percentual de vítimas, nesse estudo, queremos entender os fatores que contribuem para os acidentes acontecerem.

# :floppy_disk: Coleta de Dados
>
Os dados foram coletados do sítio da Polícia Rodoviária Federal.
<img align="left" width="80" height="94" src="https://github.com/gabrielmprata/MVP_Sprint01_Puc_Rio/assets/119508139/f9646e84-d274-406b-9a7a-12add19acb07">
>
https://www.gov.br/prf/pt-br/acesso-a-informacao/dados-abertos/dados-abertos-acidentes
>
Dataset: 2024, Agrupado por ocorrência e por pessoas envolvidas.
>
Infrações
<br><br>
# 🔨 Ferramentas utilizadas
<img loading="lazy" src="https://cdn.jsdelivr.net/gh/devicons/devicon@latest/icons/python/python-original.svg" width="40" height="40"/> <img src="https://cdn.jsdelivr.net/gh/devicons/devicon@latest/icons/pandas/pandas-original-wordmark.svg" width="40" height="40"/>   <img loading="lazy" src="https://cdn.jsdelivr.net/gh/devicons/devicon@latest/icons/plotly/plotly-original-wordmark.svg" width="40" height="40"/>  <img loading="lazy" src="https://cdn.jsdelivr.net/gh/devicons/devicon@latest/icons/streamlit/streamlit-original-wordmark.svg" width="40" height="40"/>


<br></br>
>
# **<font color=#85d338> 3. Pré-processamento**
>
[![Colab Notebook](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/gabrielmprata/anatel/blob/main/Anatel_PreProcessamento.ipynb)
>
Esta é a etapa mais demorada e trabalhosa do projeto de ciência de dados, e estima-se que consuma pelo menos 70% do tempo total do projeto.
>
Após coletar e analisar os dados na etapa anterior, é necessário limpar, transformar e apresentar melhor os seus dados, a fim de obter, na próxima etapa, os melhores resultados possíveis nos algoritmos de machine learning ou simplesmente apresentar dados mais confiáveis para os clientes em soluções de
business intelligence.
>
Como o nosso objetivo é criar um Dashboard com **Python** e **Streamlit**, iremos minimizar ao máximo o tamanho e a granularidade dos Datasets disponibilizados, a fim de termos um ambiente mais "leve" para a leitura dos dados.
>
Principais técnicas utilizadas:
>
**Limpeza:** Consiste na verificação da consistência das informações, correção de possíveis erros de preenchimento ou eliminação de valores desconhecidos, redundantes ou não pertencentes ao domínio.
>
**Agregação:** Também pode ser considerada uma técnica de redução de dimensionalidade, pois reduz o número de linhas e colunas de um dataset.
>
**Tratamendo de dados faltantes (missing):** Identificamos e, em seguida, tratamos com um valor adequado. Não foi necessario a exclusão desses registros.
>
# **<font color=#85d338> 4. Apresentação dos resultados**
>
