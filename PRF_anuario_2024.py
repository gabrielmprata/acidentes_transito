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
import plotly.graph_objects as go
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

df_pessoas['feridos'] = df_pessoas['feridos_leves'] + \
    df_pessoas['feridos_graves']

# ----------------------------------------------------------------------------#
# ****************************************************************************#
# Construção dos Datasets
# 3.1.1 Quadro comparativo
# agrupa por ano
df_ind_anual = df_hs_acidentes.groupby('ano')[['sinistro', 'pessoas', 'mortos', 'feridos_leves',
                                               'feridos_graves', 'ilesos', 'ignorados', 'veiculos']].apply(lambda x: x.sum()).reset_index()

sinistro_atual = (df_ind_anual.sinistro.values[1]/1000).round(1)
sinistro_ant = (df_ind_anual.sinistro.values[0]/1000).round(1)
sinistro_delta = (sinistro_atual - sinistro_ant).round(1)

veiculos_atual = (df_ind_anual.veiculos.values[1]/1000).round(1)
veiculos_ant = (df_ind_anual.veiculos.values[0]/1000).round(1)
veiculos_delta = (veiculos_atual - veiculos_ant).round(1)

pessoas_atual = (df_ind_anual.pessoas.values[1]/1000).round(1)
pessoas_ant = (df_ind_anual.pessoas.values[0]/1000).round(1)
pessoas_delta = (pessoas_atual - pessoas_ant).round(1)

feridos_leves_atual = (df_ind_anual.feridos_leves.values[1]/1000).round(1)
feridos_leves_ant = (df_ind_anual.feridos_leves.values[0]/1000).round(1)
feridos_leves_delta = (feridos_leves_atual - feridos_leves_ant).round(1)

feridos_graves_atual = (df_ind_anual.feridos_graves.values[1]/1000).round(1)
feridos_graves_ant = (df_ind_anual.feridos_graves.values[0]/1000).round(1)
feridos_graves_delta = (feridos_graves_atual - feridos_graves_ant).round(1)

mortos_atual = (df_ind_anual.mortos.values[1]/1000).round(1)
mortos_ant = (df_ind_anual.mortos.values[0]/1000).round(1)
mortos_delta = (mortos_atual - mortos_ant).round(1)

ilesos_atual = (df_ind_anual.ilesos.values[1]/1000).round(1)
ilesos_ant = (df_ind_anual.ilesos.values[0]/1000).round(1)
ilesos_delta = (ilesos_atual - ilesos_ant).round(1)

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

# ****************************************************************************#
# 3.2 Anuário, 2024
# 3.2.1 Sinistros por mês
# Dataframe agrupando por mês e acidentes
df_sin_mes = df_acidentes.groupby(['mes', 'mes_char'])[
    'sinistro'].sum().reset_index()

# 3.2.2 Óbitos por mês
df_mor_mes = df_acidentes.groupby(['mes', 'mes_char'])[
    'mortos'].sum().reset_index()

# 3.2.3 Sinistros por dia da semana, horário e fase do dia
# Dataframe agrupando por dia da semana
df_semana = df_acidentes.groupby(['semana', 'dia_semana'])[
    'sinistro'].sum().reset_index()

# Dataframe agrupando por dia da semana e hora
df_hora_semana = df_acidentes.groupby(['semana', 'dia_semana', 'hora'])[
    'sinistro'].sum().reset_index()

# Dataframe agrupando por dia da semana e hora
df_fase_dia = df_acidentes.groupby(
    ['fase_dia'])['sinistro'].sum().reset_index()

# classificar fase do dia
# recebe o dia da semana em numeral, para depois poder ordenar de maneira correta
df_fase_dia["ordem"] = df_fase_dia["fase_dia"]
dicwk = {"Amanhecer": 0, "Pleno dia": 1, "Anoitecer": 2, "Plena Noite": 3}
df_fase_dia = df_fase_dia.replace({'ordem': dicwk})

# Ordenar
df_fase_dia = df_fase_dia.sort_values(by='ordem', ascending=True)

# 3.2.4 Sinistros por unidade federativa e região
# Dataframe agrupando por uf e região  para usar com o mapa do Streamlit
df_uf_regiao_hist = df_acidentes.groupby(["ano", "uf", "regiao"])[
    'sinistro'].sum().reset_index()

# Carga do Json com as limitações dos estados brasileiros
with urlopen('https://raw.githubusercontent.com/codeforamerica/click_that_hood/master/public/data/brazil-states.geojson') as response:
    Brasil = json.load(response)

# definindo a informação do gráfico
state_id_map = {}
for feature in Brasil["features"]:
    feature["id"] = feature["properties"]["sigla"]
    state_id_map[feature["properties"]["sigla"]] = feature["id"]

# 3.2.5 Óbitos por unidade federativa e região
df_uf_regiao_mortos = df_acidentes.groupby(["ano", "uf", "regiao"])[
    'mortos'].sum().reset_index()

# 3.2.6 Rodovias com mais sinistros
# Agrupando por BR e UF, para saber em qual trecho da BR teve mais sinistros
df_br = df_acidentes.groupby(["br", "uf"])['sinistro'].sum().reset_index()

# ordenando e selecionando o TOP 10
df_br = df_br.sort_values(by='sinistro', ascending=False).head(10)

# Concatenando os campos BR e UF
df_br['BR/UF'] = 'BR ' + df_br['br'].map(str) + '/' + df_br['uf']

# 3.2.6 Rodovias com mais registros de mortos
df_br_mortos = df_acidentes.groupby(["br", "uf"])['mortos'].sum().reset_index()

# ordenando e selecionando o TOP 10
df_br_mortos = df_br_mortos.sort_values(by='mortos', ascending=False).head(10)

# Concatenando os campos BR e UF
df_br_mortos['BR/UF'] = 'BR ' + \
    df_br_mortos['br'].map(str) + '/' + df_br_mortos['uf']

# 3.2.7 Sinistros por condição climática
# Dataframe agrupando por condicao climatica
df_clima = df_acidentes.groupby(["condicao_metereologica"])[
    'sinistro'].sum().reset_index()

# Proporção
df_prop_clima = df_acidentes.groupby('condicao_metereologica')[
    ['sinistro', 'mortos', 'feridos_leves', 'feridos_graves']].apply(lambda x: x.sum()).reset_index()

df_prop_clima = df_prop_clima.melt(id_vars=["condicao_metereologica"],
                                   var_name="metrica",
                                   value_name="quantidade")

df_prop_clima['%'] = 100 * df_prop_clima['quantidade'] / \
    df_prop_clima.groupby('metrica')['quantidade'].transform('sum')

# 3.2.8 Sinistros por tipo e causa de acidente
# Dataframe agrupando por tipo de acidente
df_tipo_acidente = (df_acidentes.groupby(["tipo_acidente"])['sinistro'].sum().reset_index()
                    ).sort_values(by='sinistro', ascending=False)

# Dataframe agrupando por causa de acidente
df_causa_acidente = (df_acidentes.groupby(["causa_acidente"])['sinistro'].sum().reset_index()
                     ).sort_values(by='sinistro', ascending=False)

# 3.2.9 Óbitos por tipo e causa de acidente
# Dataframe agrupando por tipo de acidente
df_tipo_acid_mortos = (df_acidentes.groupby(["tipo_acidente"])['mortos'].sum().reset_index()
                       ).sort_values(by='mortos', ascending=False)

# Dataframe agrupando por causa de acidente
df_causa_acid_mortos = (df_acidentes.groupby(["causa_acidente"])['mortos'].sum().reset_index()
                        ).sort_values(by='mortos', ascending=False)

# 3.3 Pessoas Envolvidas
# 3.3.1 Pessoas Envolvidas por mês
df_pessoas_mes = df_pessoas.groupby(['mes', 'mes_char'])[
    'pessoas'].sum().reset_index()

# 3.3.2 Pessoas Envolvidas por dia da semana, horário e fase do dia
# Dataframe agrupando por dia da semana
df_pes_semana = df_pessoas.groupby(['semana', 'dia_semana'])[
    'pessoas'].sum().reset_index()

# Dataframe agrupando por dia da semana e hora
df_pes_hora = df_pessoas.groupby(['semana', 'dia_semana', 'hora'])[
    'pessoas'].sum().reset_index()

# Dataframe agrupando por dia da semana e hora
df_pes_fase_dia = df_pessoas.groupby(
    ['fase_dia'])['pessoas'].sum().reset_index()

# 3.3.3 Tipo de Pessoas Envolvidas
df_tipo_pessoa = df_pessoas.groupby('tipo_envolvido')[
    ['pessoas', 'mortos', 'feridos_leves', 'feridos_graves', 'ilesos']].apply(lambda x: x.sum()).reset_index()

# prop
df_prop_tipo_pes = df_tipo_pessoa.melt(id_vars=["tipo_envolvido"],
                                       var_name="metrica",
                                       value_name="quantidade")

df_prop_tipo_pes['%'] = 100 * df_prop_tipo_pes['quantidade'] / \
    df_prop_tipo_pes.groupby('metrica')['quantidade'].transform('sum')


# 3.3.4 Envolvidos por gênero
# Criando dataframe
# Total
gr_pes_genero = df_pessoas.groupby(['sexo_tratado'])[
    'pessoas'].sum().reset_index()

# Como condutor
gr_pes_genero_cond = df_pessoas[(df_pessoas['tipo_envolvido'] == 'Condutor')].groupby([
    'sexo_tratado'])['pessoas'].sum().reset_index()

# 3.3.5 Pirâmide etária dos envolvidos em acidentes de trânsito
# Visão Total de pessoas
# SUM(CASE WHEN)
gr_ac_faixa_idade = df_pessoas.groupby(['faixa_idade'], as_index=False).apply(lambda x: pd.Series({'Masculino': x.loc[x.sexo_tratado == 'Masculino']['pessoas'].sum(),
                                                                                                   'Feminino': x.loc[x.sexo_tratado == 'Feminino']['pessoas'].sum()}))

# SUM(CASE WHEN)
gr_ac_faixa_idade_condutor = df_pessoas[(df_pessoas['tipo_envolvido'] == 'Condutor')].groupby(['faixa_idade'], as_index=False).apply(lambda x: pd.Series({'Masculino': x.loc[x.sexo_tratado == 'Masculino']['pessoas'].sum(),
                                                                                                                                                          'Feminino': x.loc[x.sexo_tratado == 'Feminino']['pessoas'].sum()}))
# Setando os eixos
# Total
y_idade = gr_ac_faixa_idade['faixa_idade']
x_M = gr_ac_faixa_idade['Masculino']
# multiplicar por -1 para inverter o eixoX
x_F = gr_ac_faixa_idade['Feminino'] * -1

# Condutor
y_idade_c = gr_ac_faixa_idade_condutor['faixa_idade']
x_M_c = gr_ac_faixa_idade_condutor['Masculino']
# multiplicar por -1 para inverter o eixoX
x_F_c = gr_ac_faixa_idade_condutor['Feminino'] * -1

# 3.3.7 Pessoas envolvidas por tipo de veículo
# agrupa
# df_tipo_veiculo = df_pessoas.groupby('classe_veiculos')[
#   ['pessoas', 'mortos', 'feridos', 'feridos_leves', 'feridos_graves', 'ilesos']].apply(lambda x: x.sum()).reset_index()


df_tipo_veiculo = df_pessoas.groupby('classe_veiculos')[
    ['pessoas', 'mortos', 'feridos_leves', 'feridos_graves', 'ilesos']].apply(lambda x: x.sum()).reset_index()

df_tipo_veiculo['feridos'] = df_tipo_veiculo['feridos_leves'] + \
    df_tipo_veiculo['feridos_graves']

# 3.3.8 Condutores envolvidos por tipo de veículo
# condutor pessoas
gr_pes_veic_cond = df_pessoas[(df_pessoas['tipo_envolvido'] == 'Condutor')].groupby([
    'classe_veiculos'])['pessoas'].sum().reset_index()

# condutor mortos
gr_mort_veic_cond = df_pessoas[(df_pessoas['tipo_envolvido'] == 'Condutor')].groupby([
    'classe_veiculos'])['mortos'].sum().reset_index()


# 3.3.9 Proporção de envolvidos por tipo de veículo
# agrupa
df_gp_veicular = df_pessoas.groupby('classe_veiculos')[
    ['mortos', 'feridos_leves', 'feridos_graves', 'ilesos']].apply(lambda x: x.sum()).reset_index()

df_prop_veicular = df_gp_veicular.melt(id_vars=["classe_veiculos"],
                                       var_name="metrica",
                                       value_name="quantidade")

df_prop_veicular['%'] = 100 * df_prop_veicular['quantidade'] / \
    df_prop_veicular.groupby('metrica')['quantidade'].transform('sum')

# 3.4.1 Pessoas envolvidos por região e tipo de veículo
df_pes_reg_veic = df_pessoas.groupby(['regiao', 'classe_veiculos'])[
    'pessoas'].sum().reset_index()

# 3.4.2 Número de feridos por região e tipo de veículo
df_fer_reg_veic = df_pessoas.groupby(['regiao', 'classe_veiculos'])[
    'feridos'].sum().reset_index()

# 3.4.3 Número de mortos por região e tipo de veículo
df_mor_reg_veic = df_pessoas.groupby(['regiao', 'classe_veiculos'])[
    'mortos'].sum().reset_index()

# 3.4.4 Condutores envolvidos por faixa etária e tipo de veículo
# condutor pessoas
gr_pes_faixa_cond = df_pessoas[(df_pessoas['tipo_envolvido'] == 'Condutor')].groupby(
    ['faixa_idade', 'classe_veiculos'])['pessoas'].sum().reset_index()

# 3.4.5 Condutores mortos por faixa etária e tipo de veículo

gr_mor_faixa_cond = df_pessoas[(df_pessoas['tipo_envolvido'] == 'Condutor')].groupby(
    ['faixa_idade', 'classe_veiculos'])['mortos'].sum().reset_index()

# 3.4.6 Pedestres envolvidos por faixa etária e estado
gr_pedestre_faixa = df_pessoas[(df_pessoas['tipo_envolvido'] == 'Pedestre')].groupby([
    'faixa_idade', 'uf'])['pessoas'].sum().reset_index()

# 3.4.7 Pedestres mortos por faixa etária e estado
gr_pedestre_faixa_mor = df_pessoas[(df_pessoas['tipo_envolvido'] == 'Pedestre')].groupby([
    'faixa_idade', 'uf'])['mortos'].sum().reset_index()

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

# Estado das vítimas por ano

gr_hs_vitimas = px.line(df_hs_anual, x='ano', y=['feridos_leves', 'mortos', 'feridos_graves'],
                        markers=True, text='value',
                        # height=600, width=800, #altura x largura
                        line_shape="spline",
                        template="plotly_dark",
                        render_mode="svg",
                        title="Estado das vítimas por Ano",
                        labels=dict(ano="Ano", value="Envolvidos(k)",
                                    variable="Envolvidos")
                        )
# se o type for date, vai respeitar o intervalo
gr_hs_vitimas.update_xaxes(type="category", title=None)
gr_hs_vitimas.update_traces(line_width=2, textposition='top center')

# ****************************************************************************#
# 3.2 Anuário, 2024
# 3.2.1 Sinistros por mês
gr_an_mes = px.line(df_sin_mes, x='mes_char', y=['sinistro'],
                    markers=True, text='value', line_shape="spline",
                    template="plotly_dark", render_mode="svg",
                    labels=dict(mes_char="Mês", value="Sinistros",
                                variable="Sinistros")
                    )
gr_an_mes.update_xaxes(type="category", title=None)
gr_an_mes.update_layout(showlegend=False)
gr_an_mes.update_traces(line_width=2, textposition='top center')

# 3.2.2 Óbitos por mês
gr_an_obito_mes = px.line(df_mor_mes, x='mes_char', y=['mortos'],
                          markers=True, text='value', line_shape="spline", template="plotly_dark",
                          render_mode="svg",
                          labels=dict(mes_char="Mês",
                                      value="Óbitos", variable="Óbitos")
                          )
# se o type for date, vai respeitar o intervalo
gr_an_obito_mes.update_xaxes(type="category", title=None)
gr_an_obito_mes.update_layout(showlegend=False)
gr_an_obito_mes.update_traces(
    line_width=2, textposition='top center', line_color='red')

# 3.2.3 Sinistros por dia da semana, horário e fase do dia
gr_an_semana = px.bar(df_semana, x="dia_semana", y="sinistro",
                      labels=dict(dia_semana="Dia da semana",
                                  sinistro="Sinistros"),
                      height=350, width=600,  # altura x largura
                      color_discrete_sequence=px.colors.sequential.Blues_r,  text_auto='.2s',
                      template="plotly_dark"
                      )

gr_an_fase_dia = px.bar(df_fase_dia, x="fase_dia", y="sinistro",
                        labels=dict(fase_dia="Fase do dia",
                                    sinistro="Sinistros"),
                        height=350, width=600,  # altura x largura
                        color_discrete_sequence=px.colors.sequential.Blues_r,  text_auto='.2s',
                        template="plotly_dark"
                        )

gr_an_hora_semana = px.density_heatmap(df_hora_semana, x="dia_semana", y="hora", z="sinistro",
                                       histfunc="sum", text_auto=True, height=500,
                                       labels=dict(
                                           dia_semana="Dia da semana",  hora="Hora"),
                                       color_continuous_scale="RdYlBu_r", template="plotly_dark"
                                       )
gr_an_hora_semana.layout['coloraxis']['colorbar']['title'] = 'Sinistros'
gr_an_hora_semana.update_yaxes(type="category")
gr_an_hora_semana.update_xaxes(type="category")


# 3.2.4 Sinistros por unidade federativa e região
# Plotando o mapa
gr_an_mapa = px.choropleth_mapbox(
    df_uf_regiao_hist,  # database
    locations='uf',  # define os limites no mapa
    geojson=Brasil,  # Coordenadas geograficas dos estados
    color="sinistro",  # define a metrica para a cor da escala
    hover_name='uf',  # informação no box do mapa
    hover_data=["uf"],
    labels=dict(uf="UF", sinistro="Sinistros"),
    mapbox_style="white-bg",  # define o style do mapa
    center={"lat": -14, "lon": -55},  # define os limites para plotar
    zoom=2.5,  # zoom inicial no mapa
    color_continuous_scale="blues",  # cor dos estados
    opacity=0.5  # opacidade da cor do mapa, para aparecer o fundo
)
gr_an_mapa.update_layout(plot_bgcolor='rgba(0, 0, 0, 0)',
                         coloraxis_showscale=True,  # Tira a legenda
                         margin=dict(l=0, r=0, t=0, b=0), height=350
                         )

gr_an_regiao = px.pie(df_uf_regiao_hist, values='sinistro', names='regiao', labels=dict(regiao="Região", sinistro="Sinistros"),
                      height=350, width=350, color_discrete_sequence=px.colors.sequential.Blues_r, template="plotly_dark"
                      )
gr_an_regiao.update_layout(showlegend=False)
gr_an_regiao.update_traces(textposition='outside', textinfo='percent+label')

# 3.2.5 Óbitos por unidade federativa e região
# Plotando o mapa
gr_an_mapa_ob = px.choropleth_mapbox(
    df_uf_regiao_mortos,  # database
    locations='uf',  # define os limites no mapa
    geojson=Brasil,  # Coordenadas geograficas dos estados
    color="mortos",  # define a metrica para a cor da escala
    hover_name='uf',  # informação no box do mapa
    hover_data=["uf"],
    labels=dict(uf="UF", mortos="Mortos"),
    mapbox_style="white-bg",  # define o style do mapa
    center={"lat": -14, "lon": -55},  # define os limites para plotar
    zoom=2.5,  # zoom inicial no mapa
    color_continuous_scale="RdYlBu_r",  # cor dos estados

    opacity=0.5  # opacidade da cor do mapa, para aparecer o fundo

)
gr_an_mapa_ob.update_layout(
    plot_bgcolor='rgba(0, 0, 0, 0)',
    coloraxis_showscale=True,  # Tira a legenda
    margin=dict(l=0, r=0, t=0, b=0),
    height=350
)

gr_an_regiao_ob = px.pie(df_uf_regiao_mortos, values='mortos', names='regiao', labels=dict(regiao="Região", sinistro="Mortos"),
                         height=350, width=350, color_discrete_sequence=px.colors.sequential.Blues_r, template="plotly_dark"
                         )
gr_an_regiao_ob.update_layout(showlegend=False)
gr_an_regiao_ob.update_traces(textposition='outside', textinfo='percent+label')

# 3.2.6 Rodovias com mais sinistros
gr_an_br_uf = px.bar(df_br, x="BR/UF", y="sinistro",
                     labels=dict(sinistro="Sinistros"),
                     # hover_data=['semagestac', 'gestacao'],
                     color_discrete_sequence=px.colors.sequential.Blues_r,  text_auto='.2s',
                     template="plotly_dark"
                     )

# 3.2.6 Rodovias com mais registros de mortos
gr_an_br_uf_ob = px.bar(df_br_mortos, x="BR/UF", y="mortos",
                        labels=dict(mortos="Mortos"),
                        color_discrete_sequence=px.colors.sequential.Blues_r,  text_auto='.2s',
                        template="plotly_dark"
                        )

# 3.2.7 Sinistros por condição climática
gr_an_clima = px.bar(df_clima.sort_values(by='sinistro', ascending=False), x="condicao_metereologica", y="sinistro",
                     labels=dict(
                         condicao_metereologica="Condição climática", sinistro="Sinistros"),
                     height=350, width=600,  # altura x largura
                     color_discrete_sequence=px.colors.sequential.Blues_r,  text_auto='.2s',
                     template="plotly_dark"
                     )


# proporção
gr_an_clima_prop = px.bar(df_prop_clima.sort_values(['metrica', '%'], ascending=[True, False]), x='metrica', y='%', color='condicao_metereologica',
                          labels=dict(
                              condicao_metereologica="Condição climática", metrica="Métrica"),
                          # height=350, width=600, #altura x largura
                          color_discrete_sequence=px.colors.sequential.Blues_r,
                          template="plotly_dark", text="condicao_metereologica"
                          )
gr_an_clima_prop.update_layout(showlegend=False)
gr_an_clima_prop.update_yaxes(
    ticksuffix="%", showgrid=True)  # the y-axis is in percent

# 3.2.8 Sinistros por tipo e causa de acidente
gr_an_tipo_acidente = px.bar(df_tipo_acidente, x='sinistro', y='tipo_acidente', color='tipo_acidente', orientation='h',
                             labels=dict(sinistro="Sinistros",
                                         tipo_acidente="Tipo de acidente"),
                             color_discrete_sequence=["blue"],
                             template="plotly_dark",  text_auto='.2s'

                             )
gr_an_tipo_acidente.update_layout(showlegend=False)


# tipo acidente
gr_an_causa_acidente = px.bar(df_causa_acidente.head(16), x='sinistro', y='causa_acidente', color='causa_acidente', orientation='h',
                              labels=dict(sinistro="Sinistros",
                                          causa_acidente="Causa do acidente"),
                              color_discrete_sequence=["blue"],
                              template="plotly_dark",  text_auto='.2s'

                              )
gr_an_causa_acidente.update_layout(showlegend=False)

# 3.2.9 Óbitos por tipo e causa de acidente
gr_an_tipo_obito = px.bar(df_tipo_acid_mortos, x='mortos', y='tipo_acidente', color='tipo_acidente', orientation='h',
                          labels=dict(mortos="Mortos",
                                      tipo_acidente="Tipo de acidente"),
                          color_discrete_sequence=["red"],
                          template="plotly_dark",  text_auto='.2s'

                          )
gr_an_tipo_obito.update_layout(showlegend=False)

gr_an_causa_obito = px.bar(df_causa_acid_mortos.head(16), x='mortos', y='causa_acidente', color='causa_acidente', orientation='h',
                           labels=dict(mortos="Mortos",
                                       causa_acidente="Causa do acidente"),
                           color_discrete_sequence=["red"],
                           template="plotly_dark",  text_auto='.2s'

                           )
gr_an_causa_obito.update_layout(showlegend=False)

# 3.3 Pessoas Envolvidas
# 3.3.1 Pessoas Envolvidas por mês

gr_an_pessoas = px.line(df_pessoas_mes, x='mes_char', y=['pessoas'],
                        markers=True, text='value',
                        # height=600, width=800, #altura x largura
                        line_shape="spline",
                        template="plotly_dark",
                        render_mode="svg",

                        labels=dict(mes_char="Mês", value="Pessoas",
                                    variable="Pessoas")
                        )
# se o type for date, vai respeitar o intervalo
gr_an_pessoas.update_xaxes(type="category", title=None)
gr_an_pessoas.update_layout(showlegend=False)
gr_an_pessoas.update_traces(line_width=2, textposition='top center')

# 3.3.2 Pessoas Envolvidas por dia da semana, horário e fase do dia
gr_an_pes_semana = px.bar(df_pes_semana, x="dia_semana", y="pessoas",
                          labels=dict(dia_semana="Dia da semana",
                                      pessoas="Pessoas"),
                          height=350, width=600,  # altura x largura
                          color_discrete_sequence=px.colors.sequential.Blues_r,  text_auto='.2s',
                          template="plotly_dark"
                          )

gr_an_pes_heat = px.density_heatmap(df_pes_hora,
                                    x="dia_semana",
                                    y="hora",
                                    z="pessoas",
                                    histfunc="sum", text_auto=True,
                                    # labels=dict(mes="Mês"),
                                    labels=dict(
                                        dia_semana="Dia da semana",  hora="Hora"),
                                    color_continuous_scale="RdYlBu_r", template="plotly_dark"
                                    )

gr_an_pes_heat.layout['coloraxis']['colorbar']['title'] = 'Pessoas'
# se o type for date, vai respeitar o intervalo
gr_an_pes_heat.update_yaxes(type="category")
# se o type for date, vai respeitar o intervalo
gr_an_pes_heat.update_xaxes(type="category")

gr_an_pes_fase = px.bar(df_pes_fase_dia, x="fase_dia", y="pessoas",
                        labels=dict(fase_dia="Fase do dia", pessoas="Pessoas"),
                        height=350, width=600,  # altura x largura
                        color_discrete_sequence=px.colors.sequential.Blues_r,  text_auto='.2s',
                        template="plotly_dark",
                        category_orders={"fase_dia": [
                            "Amanhecer", "Pleno dia", "Anoitecer", "Plena Noite"]}
                        )

# 3.3.3 Tipo de Pessoas Envolvidas
gr_an_tipo_pess = px.pie(df_tipo_pessoa, values='pessoas', names='tipo_envolvido',
                         labels=dict(
                             tipo_envolvido="Tipo de pessoa envolvida", pessoas="Pessoas"),
                         height=350, width=350, color_discrete_sequence=px.colors.sequential.Blues_r, template="plotly_dark"
                         )
gr_an_tipo_pess.update_layout(showlegend=False)
gr_an_tipo_pess.update_traces(textposition='outside', textinfo='percent+label')

gr_an_tipo_pess_prop = px.bar(df_prop_tipo_pes.sort_values(['metrica', '%'], ascending=[True, True]), x='metrica', y='%', color='tipo_envolvido',
                              labels=dict(
                                  tipo_envolvido="Tipo pessoa envolvida", metrica="Métrica"),
                              # height=350, width=600, #altura x largura
                              color_discrete_sequence=px.colors.sequential.Blues_r,
                              template="plotly_dark", text="tipo_envolvido"
                              )
gr_an_tipo_pess_prop.update_yaxes(
    ticksuffix="%", showgrid=True)  # the y-axis is in percent

# 3.3.4 Envolvidos por gênero

gr_an_genero = px.pie(gr_pes_genero, names='sexo_tratado', values='pessoas', height=300, width=600, hole=0.7,
                      color_discrete_sequence=px.colors.sequential.Blues_r, title="Visão Geral")
gr_an_genero.update_traces(
    hovertemplate=None, textposition='outside', textinfo='percent+label', rotation=50)
gr_an_genero.update_layout(margin=dict(t=50, b=35, l=0, r=0), showlegend=False,
                           plot_bgcolor='#fafafa', paper_bgcolor='#fafafa',
                           font=dict(size=17, color='#8a8d93'),
                           hoverlabel=dict(bgcolor="#444", font_size=13, font_family="Lato, sans-serif"))
gr_an_genero.add_annotation(dict(x=0.5, y=0.4,  align='center',
                                 xref="paper", yref="paper",
                                 showarrow=False, font_size=22,
                                 text="Gênero"))
gr_an_genero.add_layout_image(
    dict(
        source="https://i.imgur.com/3Cab96Z.jpg",
        xref="paper", yref="paper",
        x=0.48, y=0.48,
        sizex=0.3, sizey=0.25,
        xanchor="right", yanchor="bottom", sizing="contain",
    )
)
gr_an_genero.add_layout_image(
    dict(
        source="https://i.imgur.com/c6QKoDy.jpg",
        xref="paper", yref="paper",
        x=0.55, y=0.48,
        sizex=0.3, sizey=0.25,
        xanchor="right", yanchor="bottom", sizing="contain",
    )
)


# Visão Condutor
gr_an_genero_con = px.pie(gr_pes_genero_cond, names='sexo_tratado', values='pessoas', height=300, width=600, hole=0.7,
                          color_discrete_sequence=px.colors.sequential.Blues_r, title="Visão Condutor")
gr_an_genero_con.update_traces(
    hovertemplate=None, textposition='outside', textinfo='percent+label', rotation=50)
gr_an_genero_con.update_layout(margin=dict(t=50, b=35, l=0, r=0), showlegend=False,
                               plot_bgcolor='#fafafa', paper_bgcolor='#fafafa',
                               font=dict(size=17, color='#8a8d93'),
                               hoverlabel=dict(bgcolor="#444", font_size=13, font_family="Lato, sans-serif"))
gr_an_genero_con.add_annotation(dict(x=0.5, y=0.4,  align='center',
                                     xref="paper", yref="paper",
                                     showarrow=False, font_size=22,
                                     text="Gênero"))
gr_an_genero_con.add_layout_image(
    dict(
        source="https://i.imgur.com/3Cab96Z.jpg",
        xref="paper", yref="paper",
        x=0.48, y=0.48,
        sizex=0.3, sizey=0.25,
        xanchor="right", yanchor="bottom", sizing="contain",
    )
)
gr_an_genero_con.add_layout_image(
    dict(
        source="https://i.imgur.com/c6QKoDy.jpg",
        xref="paper", yref="paper",
        x=0.55, y=0.48,
        sizex=0.3, sizey=0.25,
        xanchor="right", yanchor="bottom", sizing="contain",
    )
)

# 3.3.5 Pirâmide etária dos envolvidos em acidentes de trânsito
gr_an_piramide = go.Figure()

# Adicionando as informações de Masculino
gr_an_piramide.add_trace(go.Bar(y=y_idade, x=x_M,
                                name='Masculino',
                                marker_color='cornflowerblue',
                                orientation='h'))

# Adicionando as informações de Masculino
gr_an_piramide.add_trace(go.Bar(y=y_idade, x=x_F, marker_color='lightblue',
                                name='Feminino', orientation='h'))

# Updating the layout for our graph
gr_an_piramide.update_layout(title='Visão Geral',
                             title_font_size=13, barmode='relative',
                             plot_bgcolor='#918d8d', paper_bgcolor='#918d8d',
                             bargap=0.0, bargroupgap=0,
                             xaxis=dict(tickvals=[-30000, -20000, -6000,
                                                  0, 6000, 20000, 30000],  # valores dos intervalos do eixoX

                                          ticktext=['30k', '20k', '6k', '0',
                                                    '6k', '20k', '30k'],  # rotulo do eixoX

                                          title='Pessoas (k)',
                                          title_font_size=14)
                             )


# Visao Condutor
gr_an_piramide_c = go.Figure()

# Adicionando as informações de Masculino
gr_an_piramide_c.add_trace(go.Bar(y=y_idade_c, x=x_M_c,
                                  name='Masculino',
                                  marker_color='cornflowerblue',
                                  orientation='h'))

# Adicionando as informações de Masculino
gr_an_piramide_c.add_trace(go.Bar(y=y_idade_c, x=x_F_c, marker_color='lightblue',
                                  name='Feminino', orientation='h'))

# Updating the layout for our graph
gr_an_piramide_c.update_layout(title='Visão Condutor',
                               title_font_size=13, barmode='relative',
                               plot_bgcolor='#918d8d', paper_bgcolor='#918d8d',
                               bargap=0.0, bargroupgap=0,
                               xaxis=dict(tickvals=[-30000, -20000, -6000,
                                                    0, 6000, 20000, 30000],  # valores dos intervalos do eixoX

                                            ticktext=['30k', '20k', '6k', '0',
                                                      '6k', '20k', '30k'],  # rotulo do eixoX

                                          title='Pessoas (k)',
                                          title_font_size=14)
                               )

# 3.3.7 Pessoas envolvidas por tipo de veículo
# pessoas
gr_an_pes_tipo_vec = px.pie(df_tipo_veiculo, values='pessoas', names='classe_veiculos',
                            labels=dict(
                                classe_veiculos="Tipo de Veículo", pessoas="Pessoas"),
                            title='Pessoas',
                            height=350, width=350, color_discrete_sequence=px.colors.sequential.Blues_r, template="plotly_dark"
                            )
gr_an_pes_tipo_vec.update_layout(showlegend=False)
gr_an_pes_tipo_vec.update_traces(
    textposition='outside', textinfo='percent+label')

# mortos
gr_an_mort_tipo_vec = px.pie(df_tipo_veiculo, values='mortos', names='classe_veiculos',
                             labels=dict(
                                 classe_veiculos="Tipo de Veículo", mortos="Mortos"),
                             title='Mortos',
                             height=350, width=350, color_discrete_sequence=px.colors.sequential.Blues_r, template="plotly_dark"
                             )
gr_an_mort_tipo_vec.update_layout(showlegend=False)
gr_an_mort_tipo_vec.update_traces(
    textposition='outside', textinfo='percent+label')


# feridos
gr_an_fer_tipo_vec = px.pie(df_tipo_veiculo, values='feridos', names='classe_veiculos',
                            labels=dict(
                                classe_veiculos="Tipo de Veículo", feridos="Feridos"),
                            title='Feridos',
                            height=350, width=350, color_discrete_sequence=px.colors.sequential.Blues_r, template="plotly_dark"
                            )
gr_an_fer_tipo_vec.update_layout(showlegend=False)
gr_an_fer_tipo_vec.update_traces(
    textposition='outside', textinfo='percent+label')

# 3.3.8 Condutores envolvidos por tipo de veículo
# pessoas condutor
gr_an_pes_veic_cond = px.pie(gr_pes_veic_cond, values='pessoas', names='classe_veiculos',
                             labels=dict(
                                 classe_veiculos="Tipo de Veículo", pessoas="Pessoas"),
                             title='Pessoas',
                             height=350, width=350, color_discrete_sequence=px.colors.sequential.Blues_r, template="plotly_dark"
                             )
gr_an_pes_veic_cond.update_layout(showlegend=False)
gr_an_pes_veic_cond.update_traces(
    textposition='outside', textinfo='percent+label')

# mortos
gr_an_mort_veic_cond = px.pie(gr_mort_veic_cond, values='mortos', names='classe_veiculos',
                              labels=dict(
                                  classe_veiculos="Tipo de Veículo", mortos="Mortos"),
                              title='Mortos',
                              height=350, width=350, color_discrete_sequence=px.colors.sequential.Blues_r, template="plotly_dark"
                              )
gr_an_mort_veic_cond.update_layout(showlegend=False)
gr_an_mort_veic_cond.update_traces(
    textposition='outside', textinfo='percent+label')


gr_an_prop_vec = px.bar(df_prop_veicular.sort_values(['metrica', '%'], ascending=[True, True]), x='metrica', y='%', color='classe_veiculos',
                        labels=dict(classe_veiculos="Grupo Veicular",
                                    metrica="Métrica"),
                        # height=350, width=600, #altura x largura
                        color_discrete_sequence=px.colors.sequential.Blues_r,
                        template="plotly_dark", text="classe_veiculos"
                        )
gr_an_prop_vec.update_yaxes(ticksuffix="%", showgrid=True)

# 3.4.1 Pessoas envolvidos por região e tipo de veículo
gr_an_pes_reg_vec = px.density_heatmap(df_pes_reg_veic,
                                       x="regiao",
                                       y="classe_veiculos",
                                       z="pessoas",
                                       histfunc="sum", text_auto=True,
                                       # labels=dict(mes="Mês"),
                                       labels=dict(
                                           classe_veiculos="Classe veículo",  regiao="Região"),
                                       color_continuous_scale="RdYlBu_r", template="plotly_dark"
                                       )

gr_an_pes_reg_vec.layout['coloraxis']['colorbar']['title'] = 'Pessoas'
# fig.update_traces(dict(colorscale='RdYlBu_r',showscale=True,coloraxis=None),)
gr_an_pes_reg_vec.update_yaxes(type="category")
gr_an_pes_reg_vec.update_xaxes(type="category")

# 3.4.2 Número de feridos por região e tipo de veículo
gr_an_fer_reg_vec = px.density_heatmap(df_fer_reg_veic,
                                       x="regiao",
                                       y="classe_veiculos",
                                       z="feridos",
                                       histfunc="sum", text_auto=True,
                                       # labels=dict(mes="Mês"),
                                       labels=dict(
                                           classe_veiculos="Classe veículo",  regiao="Região"),
                                       color_continuous_scale="RdYlBu_r", template="plotly_dark"
                                       )

gr_an_fer_reg_vec.layout['coloraxis']['colorbar']['title'] = 'Feridos'
gr_an_fer_reg_vec.update_yaxes(type="category")
gr_an_fer_reg_vec.update_xaxes(type="category")

# 3.4.3 Número de mortos por região e tipo de veículo
gr_an_mor_reg_vec = px.density_heatmap(df_mor_reg_veic,
                                       x="regiao",
                                       y="classe_veiculos",
                                       z="mortos",
                                       histfunc="sum", text_auto=True,
                                       # labels=dict(mes="Mês"),
                                       labels=dict(
                                           classe_veiculos="Classe veículo",  regiao="Região"),
                                       color_continuous_scale="RdYlBu_r", template="plotly_dark"
                                       )

gr_an_mor_reg_vec.layout['coloraxis']['colorbar']['title'] = 'Mortos'
gr_an_mor_reg_vec.update_yaxes(type="category")
gr_an_mor_reg_vec.update_xaxes(type="category")

# 3.4.4 Condutores envolvidos por faixa etária e tipo de veículo
gr_an_pes_faixa_cond = px.density_heatmap(gr_pes_faixa_cond,
                                          x="faixa_idade",
                                          y="classe_veiculos",
                                          z="pessoas",
                                          histfunc="sum", text_auto=True,
                                          # labels=dict(mes="Mês"),
                                          labels=dict(
                                              classe_veiculos="Classe veículo",  faixa_idade="Faixa Etária"),
                                          color_continuous_scale="RdYlBu_r", template="plotly_dark"
                                          )

gr_an_pes_faixa_cond.layout['coloraxis']['colorbar']['title'] = 'Pessoas'
gr_an_pes_faixa_cond.update_yaxes(type="category")
gr_an_pes_faixa_cond.update_xaxes(type="category")

# 3.4.5 Condutores mortos por faixa etária e tipo de veículo
gr_an_mor_faixa_cond = px.density_heatmap(gr_mor_faixa_cond,
                                          x="faixa_idade",
                                          y="classe_veiculos",
                                          z="mortos",
                                          histfunc="sum", text_auto=True,
                                          # labels=dict(mes="Mês"),
                                          labels=dict(
                                              classe_veiculos="Classe veículo",  faixa_idade="Faixa Etária"),
                                          color_continuous_scale="RdYlBu_r", template="plotly_dark"
                                          )

gr_an_mor_faixa_cond.layout['coloraxis']['colorbar']['title'] = 'Mortos'
gr_an_mor_faixa_cond.update_yaxes(type="category")
gr_an_mor_faixa_cond.update_xaxes(type="category")

# 3.4.6 Pedestres envolvidos por faixa etária e estado
gr_an_pes_uf_faixa = px.density_heatmap(gr_pedestre_faixa,
                                        x="uf",
                                        y="faixa_idade",
                                        z="pessoas",
                                        histfunc="sum", text_auto=True,
                                        # labels=dict(mes="Mês"),
                                        labels=dict(
                                            uf="UF",  faixa_idade="Faixa Etária"),
                                        color_continuous_scale="RdYlBu_r", template="plotly_dark"
                                        )

gr_an_pes_uf_faixa.layout['coloraxis']['colorbar']['title'] = 'Pessoas'
gr_an_pes_uf_faixa.update_yaxes(type="category")
gr_an_pes_uf_faixa.update_xaxes(type="category")

# 3.4.7 Pedestres mortos por faixa etária e estado
gr_an_pes_uf_mort = px.density_heatmap(gr_pedestre_faixa_mor,
                                       x="uf",
                                       y="faixa_idade",
                                       z="mortos",
                                       histfunc="sum", text_auto=True,
                                       # labels=dict(mes="Mês"),
                                       labels=dict(
                                           uf="UF",  faixa_idade="Faixa Etária"),
                                       color_continuous_scale="RdYlBu_r", template="plotly_dark"
                                       )

gr_an_pes_uf_mort.layout['coloraxis']['colorbar']['title'] = 'Mortos'
gr_an_pes_uf_mort.update_yaxes(type="category")
gr_an_pes_uf_mort.update_xaxes(type="category")

###################################################################################################
###################################################################################################
###################################################################################################
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
        st.metric(delta_color="inverse", label="", value=str(
            sinistro_atual)+" k", delta=str(sinistro_delta)+" k")

    with col[1]:
        st.markdown('### Veículos')
        st.metric(delta_color="inverse", label="", value=str(
            veiculos_atual)+" k", delta=str(veiculos_delta)+" k")

    with col[2]:
        st.markdown('### Pessoas')
        st.metric(delta_color="inverse", label="", value=str(
            pessoas_atual)+" k", delta=str(pessoas_delta)+" k")

    with col[3]:
        st.markdown('### Ilesos')
        st.metric(label="", value=str(
            ilesos_atual)+" k", delta=str(ilesos_delta)+" k")

    with col[0]:
        st.markdown('### Feridos Leves')
        st.metric(delta_color="inverse", label="", value=str(
            feridos_leves_atual)+" k", delta=str(feridos_leves_delta)+" k")

    with col[1]:
        st.markdown('### Feridos Graves')
        st.metric(delta_color="inverse", label="", value=str(
            feridos_graves_atual)+" k", delta=str(feridos_graves_delta)+" k")

    with col[2]:
        st.markdown('### Óbitos')
        st.metric(delta_color="inverse", label="", value=str(
            mortos_atual)+" k", delta=str(mortos_delta)+" k")


text = """:orange[**Série histórica, 2007-2024**]"""

with st.expander(text, expanded=True):
    st.plotly_chart(gr_hs_anual, use_container_width=True)
    st.plotly_chart(gr_hs_anual_dif, use_container_width=True)
    st.plotly_chart(gr_hs_vitimas, use_container_width=True)


st.markdown("<h1 style='text-align: center; color: blue;'>Anuário 2024</h1>",
            unsafe_allow_html=True)

text = """:orange[**Sinistros por mês**]"""

with st.expander(text, expanded=True):
    st.plotly_chart(gr_an_mes, use_container_width=True)

text = """:orange[**Óbitos por mês**]"""

with st.expander(text, expanded=True):
    st.plotly_chart(gr_an_obito_mes, use_container_width=True)

text = """:orange[**Sinistros por dia da semana, horário e fase do dia**]"""

with st.expander(text, expanded=True):
    col = st.columns((5.1, 2.1), gap='medium')

    with col[0]:
        st.plotly_chart(gr_an_semana, use_container_width=True)

    with col[1]:
        st.plotly_chart(gr_an_fase_dia, use_container_width=True)

    st.plotly_chart(gr_an_hora_semana, use_container_width=True)

text = """:orange[**Sinistros por unidade federativa e região**]"""

with st.expander(text, expanded=True):
    col = st.columns((4.1, 3.1), gap='medium')

    with col[0]:
        st.plotly_chart(gr_an_mapa, use_container_width=True)

    with col[1]:
        st.plotly_chart(gr_an_regiao, use_container_width=True)

text = """:orange[**Óbitos por unidade federativa e região**]"""

with st.expander(text, expanded=True):
    col = st.columns((4.1, 3.1), gap='medium')

    with col[0]:
        st.plotly_chart(gr_an_mapa_ob, use_container_width=True)

    with col[1]:
        st.plotly_chart(gr_an_regiao_ob, use_container_width=True)

text = """:orange[**Rodovias com mais sinistros**]"""

with st.expander(text, expanded=True):
    st.plotly_chart(gr_an_br_uf, use_container_width=True)


text = """:orange[**Rodovias com mais registros de mortos**]"""

with st.expander(text, expanded=True):
    st.plotly_chart(gr_an_br_uf_ob, use_container_width=True)


text = """:orange[**Sinistros por condição climática**]"""

with st.expander(text, expanded=True):
    col = st.columns((3.1, 5.1), gap='medium')

    with col[0]:
        st.plotly_chart(gr_an_clima, use_container_width=True)

    with col[1]:
        st.plotly_chart(gr_an_clima_prop, use_container_width=True)


text = """:orange[**Sinistros por tipo e causa de acidente**]"""

with st.expander(text, expanded=True):
    col = st.columns((4.1, 5.1), gap='medium')

    with col[0]:
        st.plotly_chart(gr_an_tipo_acidente, use_container_width=True)

    with col[1]:
        st.plotly_chart(gr_an_causa_acidente, use_container_width=True)

text = """:orange[**Óbitos por tipo e causa de acidente**]"""

with st.expander(text, expanded=True):
    col = st.columns((4.1, 5.1), gap='medium')

    with col[0]:
        st.plotly_chart(gr_an_tipo_obito, use_container_width=True)

    with col[1]:
        st.plotly_chart(gr_an_causa_obito, use_container_width=True)


st.markdown(
    "### :blue[Pessoas envolvidas]")


text = """:orange[**Pessoas Envolvidas por mês**]"""

with st.expander(text, expanded=True):
    st.plotly_chart(gr_an_pessoas, use_container_width=True)


text = """:orange[**Pessoas envolvidas por dia da semana, horário e fase do dia**]"""

with st.expander(text, expanded=True):
    col = st.columns((4.1, 3.1), gap='medium')

    with col[0]:
        st.plotly_chart(gr_an_pes_semana, use_container_width=True)

    with col[1]:
        st.plotly_chart(gr_an_pes_fase, use_container_width=True)

    st.plotly_chart(gr_an_pes_heat, use_container_width=True)

text = """:orange[**Tipo de Pessoas Envolvidas**]"""

with st.expander(text, expanded=True):
    col = st.columns((3.1, 5.1), gap='medium')

    with col[0]:
        st.plotly_chart(gr_an_tipo_pess, use_container_width=True)

    with col[1]:
        st.plotly_chart(gr_an_tipo_pess_prop, use_container_width=True)

text = """:orange[**Envolvidas por gênero**]"""

with st.expander(text, expanded=True):
    col = st.columns((4.1, 4.1), gap='medium')

    with col[0]:
        st.markdown('### Visão Geral')
        st.plotly_chart(gr_an_genero, use_container_width=True)

    with col[1]:
        st.markdown('### Visão do Condutor')
        st.plotly_chart(gr_an_genero_con, use_container_width=True)


text = """:orange[**Pirâmide etária dos envolvidos em acidentes de trânsito**]"""

with st.expander(text, expanded=True):
    col = st.columns((4.1, 4.1), gap='medium')

    with col[0]:
        st.plotly_chart(gr_an_piramide, use_container_width=True)

    with col[1]:
        st.plotly_chart(gr_an_piramide_c, use_container_width=True)

text = """:orange[**Pessoas envolvidas por tipo de veículo**]"""

with st.expander(text, expanded=True):
    col = st.columns((3.1, 3.1, 3.1), gap='medium')

    with col[0]:
        st.plotly_chart(gr_an_pes_tipo_vec, use_container_width=True)

    with col[1]:
        st.plotly_chart(gr_an_mort_tipo_vec, use_container_width=True)

    with col[2]:
        st.plotly_chart(gr_an_fer_tipo_vec, use_container_width=True)

text = """:orange[**Condutores envolvidos por tipo de veículo**]"""

with st.expander(text, expanded=True):
    col = st.columns((4.1, 4.1), gap='medium')

    with col[0]:
        st.plotly_chart(gr_an_pes_veic_cond, use_container_width=True)

    with col[1]:
        st.plotly_chart(gr_an_mort_veic_cond, use_container_width=True)


text = """:orange[**Proporção de envolvidos por tipo de veículo**]"""

with st.expander(text, expanded=True):
    st.plotly_chart(gr_an_prop_vec, use_container_width=True)

text = """:orange[**Pessoas envolvidos por região e tipo de veículo**]"""

with st.expander(text, expanded=True):
    st.plotly_chart(gr_an_pes_reg_vec, use_container_width=True)

text = """:orange[**Número de feridos por região e tipo de veículo**]"""

with st.expander(text, expanded=True):
    st.plotly_chart(gr_an_fer_reg_vec, use_container_width=True)

text = """:orange[**Número de mortos por região e tipo de veículo**]"""

with st.expander(text, expanded=True):
    st.plotly_chart(gr_an_mor_reg_vec, use_container_width=True)

text = """:orange[**Condutores envolvidos por faixa etária e tipo de veículo**]"""

with st.expander(text, expanded=True):
    st.plotly_chart(gr_an_pes_faixa_cond, use_container_width=True)


text = """:orange[**Condutores mortos por faixa etária e tipo de veículo**]"""

with st.expander(text, expanded=True):
    st.plotly_chart(gr_an_mor_faixa_cond, use_container_width=True)

text = """:orange[**Pedestres envolvidos por faixa etária e estado**]"""

with st.expander(text, expanded=True):
    st.plotly_chart(gr_an_pes_uf_faixa, use_container_width=True)

text = """:orange[**Pedestres mortos por faixa etária e estado**]"""

with st.expander(text, expanded=True):
    st.plotly_chart(gr_an_pes_uf_mort, use_container_width=True)
