#######################
# Importando libraries
import streamlit as st
import altair as alt
import json
from urllib.request import urlopen
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import plotly.express as px
from streamlit_extras.metric_cards import style_metric_cards


#######################
# Configuração da página
st.set_page_config(
    page_title="PRF Anuário 2024",
    page_icon=":police_car:",
    layout="wide",
    initial_sidebar_state="collapsed"
)

alt.themes.enable("dark")

#######################
# Projeto utilizando streamlit_extras.metric_cards
# pip install streamlit-extras
# streamlit-extras==0.3.5
# https://arnaudmiribel.github.io/streamlit-extras/extras/metric_cards/


#######################
# Carregando dataset
# URL de importação
url = "https://raw.githubusercontent.com/gabrielmprata/acidentes_transito/main/datasets/df_acidentes_2024.csv.bz2"
url2 = "https://raw.githubusercontent.com/gabrielmprata/acidentes_transito/main/datasets/df_hs_acidentes.csv.bz2"
url3 = "https://raw.githubusercontent.com/gabrielmprata/acidentes_transito/main/datasets/hs_acidentes.csv"
url4 = "https://raw.githubusercontent.com/gabrielmprata/acidentes_transito/main/datasets/df_pessoas.csv.bz2"


df_acidentes = pd.read_csv(url, compression='bz2',
                           encoding="utf8", delimiter=',')

# Ano atual com 2023 somente para comparativo
df_hs_acidentes = pd.read_csv(
    url2, compression='bz2', encoding="utf8", delimiter=',')

df_hs_anual = pd.read_csv(url3, delimiter=';')

# Pessoas envolvidas
df_pessoas = pd.read_csv(url4, compression='bz2',
                         encoding="utf8", delimiter=',')

# ----------------------------------------------------------------------------#
# ****************************************************************************#
# Construção dos Datasets
# 3.1.1 Quadro comparativo
# agrupa por ano
df_ind_anual = df_hs_acidentes.groupby('ano')[['sinistro', 'pessoas', 'mortos', 'feridos_leves',
                                               'feridos_graves', 'ilesos', 'ignorados', 'veiculos']].apply(lambda x: x.sum()).reset_index()

sinistro_atual = df_ind_anual.sinistro.values[1]
sinistro_ant = df_ind_anual.sinistro.values[0]
sinistro_delta = sinistro_atual - sinistro_ant

veiculos_atual = df_ind_anual.veiculos.values[1]
veiculos_ant = df_ind_anual.veiculos.values[0]
veiculos_delta = veiculos_atual - veiculos_ant

pessoas_atual = df_ind_anual.pessoas.values[1]
pessoas_ant = df_ind_anual.pessoas.values[0]
pessoas_delta = pessoas_atual - pessoas_ant

feridos_leves_atual = df_ind_anual.feridos_leves.values[1]
feridos_leves_ant = df_ind_anual.feridos_leves.values[0]
feridos_leves_delta = feridos_leves_atual - feridos_leves_ant

feridos_graves_atual = df_ind_anual.feridos_graves.values[1]
feridos_graves_ant = df_ind_anual.feridos_graves.values[0]
feridos_graves_delta = feridos_graves_atual - feridos_graves_ant

mortos_atual = df_ind_anual.mortos.values[1]
mortos_ant = df_ind_anual.mortos.values[0]
mortos_delta = mortos_atual - mortos_ant

ilesos_atual = df_ind_anual.ilesos.values[1]
ilesos_ant = df_ind_anual.ilesos.values[0]
ilesos_delta = ilesos_atual - ilesos_ant

# 3.1.2 Série histórica, 2007-2024
# Criar métrica com o valor do ano anterior
df_hs_anual['sinistro_ant'] = df_hs_anual.sinistros.shift(1)
df_hs_anual['feridos_ant'] = df_hs_anual.feridos.shift(1)
df_hs_anual['mortos_ant'] = df_hs_anual.mortos.shift(1)
# Variação em percentual
df_hs_anual['var_sinistro'] = (
    ((df_hs_anual['sinistros']/df_hs_anual['sinistro_ant'])*100)-100).round(1)
df_hs_anual['var_feridos'] = (
    (df_hs_anual['feridos']/df_hs_anual['feridos_ant'])*100)-100
df_hs_anual['var_mortos'] = (
    (df_hs_anual['mortos']/df_hs_anual['mortos_ant'])*100)-100
# Modificar a cor da barra quando negativo ou positiva
df_hs_anual['color'] = np.where(
    df_hs_anual['var_sinistro'] < 0, '#4c60d6', '#e8816e')

# Arredondamento em K para gráfico
df_hs_anual['sinistros'] = (df_hs_anual['sinistros']/1000).round(1)
df_hs_anual['feridos_leves'] = (df_hs_anual['feridos_leves']/1000).round(1)
df_hs_anual['feridos_graves'] = (df_hs_anual['feridos_graves']/1000).round(1)
df_hs_anual['mortos'] = (df_hs_anual['mortos']/1000).round(1)

# ----------------------------------------------------------------------------#
# ****************************************************************************#
# Construção dos Gráficos

# 1. Quadro comparativo
# todos os cards foram feitos com st.metric direto no Main Panel

# ----------------------------------------------------------------------------#
# 3.1.2 Série histórica, 2007-2024
gr_hs_anual = px.line(df_hs_anual, x='ano', y='sinistros',
                      markers=True, text='sinistros',
                      # height=600, width=800, #altura x largura
                      line_shape="spline",
                      template="plotly_dark",
                      render_mode="svg",
                      title="Sinistros por Ano",
                      labels=dict(ano="Ano", sinistros="Sinistros(k)")
                      )
# se o type for date, vai respeitar o intervalo
gr_hs_anual.update_xaxes(type="category", title=None)
gr_hs_anual.update_traces(line_width=2, textposition='top center')


gr_hs_anual_dif = px.bar(df_hs_anual, x="ano", y="var_sinistro", title="Diferença YxY(%)", template="plotly_dark", text_auto=True,
                         # height=300, width=1160,  #largura
                         # , hover_data=['ano', 'dif','var']
                         labels=dict(ano="Ano", var_sinistro='Variação')
                         )
gr_hs_anual_dif.update_traces(textangle=0, textfont_size=12, textposition='outside',
                              cliponaxis=False, marker_color=df_hs_anual["color"])
gr_hs_anual_dif.update_yaxes(
    showticklabels=False, showgrid=False, visible=False, fixedrange=True)
gr_hs_anual_dif.update_xaxes(showgrid=False, visible=False, fixedrange=True)
# se o type for date, vai respeitar o intervalo
gr_hs_anual_dif.update_xaxes(type="category", title=None)


#######################
# Dashboard Main Panel


st.markdown(
    " # :warning::ambulance: Acidentes de Trânsito nas Rodovias Federais Brasileiras :red_car::police_car:")


st.markdown(
    "### :blue[Sinistros de Trânsito no Brasil, comparativo e série histórica]")


style_metric_cards(background_color="#071021",
                   border_left_color="#1f66bd", border_radius_px=5)

text = """:orange[**Quadro Comparativo, 2023-2024**]"""

with st.expander(text, expanded=True):
    col = st.columns((1.1, 1.1, 1.1, 1.1), gap='medium')

    with col[0]:
        #######################
        # Quadro com o total e a variação
        st.markdown('### Sinistros')
        st.metric(label="", value=str(
            (sinistro_atual).round(2)), delta=str(sinistro_delta))

    with col[1]:
        st.markdown('### Veículos')
        st.metric(label="", value=str(
            veiculos_atual), delta=str(veiculos_delta))

    with col[2]:
        st.markdown('### Pessoas')
        st.metric(delta_color="inverse", label="", value=str(
            pessoas_atual), delta=str(pessoas_delta))

    with col[3]:
        st.markdown('### Ilesos')
        st.metric(delta_color="inverse", label="", value=str(
            ilesos_atual), delta=str(ilesos_delta))


text = """:orange[**Série histórica, 2007-2024**]"""

with st.expander(text, expanded=True):
    st.plotly_chart(gr_hs_anual, use_container_width=True)
    st.plotly_chart(gr_hs_anual_dif, use_container_width=True)


st.markdown("<h1 style='text-align: center; color: blue;'>Anuário 2024</h1>",
            unsafe_allow_html=True)

st.markdown("##")
