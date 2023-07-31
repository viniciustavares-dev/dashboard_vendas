#iniciando novo projeto de dashboard com mais colunas e gráficos
from dash import html, dcc, Input, Output, State
import dash_bootstrap_components as dbc
import dash_core_components as dcc
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px

#importando temas
from dash_bootstrap_templates import ThemeSwitchAIO
import dash

FONT_AWESOME = ["https://use.fonteawesome.com/releases/v5.10.2/css/all.css"]
app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])
app.scripts.config.serve_locally = True
server = app.server

#tratando nossa base de dados
df = pd.read_excel('Vendas.xlsx')

#selecionar apenas a coluna das lojas
opcoes = list(df['ID Loja'].unique())
opcoes.append("Todas as lojas")

#vamos agrupar todas as colunas por loja e ver o valor total vendido por loja
dfSelecionado = df.filter(items=['ID Loja', 'Valor Final'])
dfValorTotal = dfSelecionado.groupby(['ID Loja'], as_index=False)['Valor Final'].sum()

#primeiro gráfico 
gValorTotal = px.bar(dfValorTotal, y="Valor Final", x="ID Loja")

#segundo grafico
fig = px.bar(df, x="Produto", y="Quantidade", color="ID Loja", barmode="group")

#terceiro grafico
dfSelecionado2 = df.filter(items=['Data', 'ID Loja', 'Produto', 'Quantidade', 'Valor Final'])
dfQuantidade = dfSelecionado2.groupby(['Data','ID Loja', 'Produto', 'Quantidade'], as_index=False).mean().sort_values(by='Data')

fig2 = px.line(dfQuantidade, y="Valor Final", x="Data", color="ID Loja")

fig.update_layout(
    legend=dict(orientation='h', yanchor='top', y=1.1, xanchor='center', x=0.5),
    font=dict(size=10)
)

fig2.update_layout(
    legend=dict(orientation='h', yanchor='top', y=1.1, xanchor='center', x=0.5),
    font=dict(size=10)
)


gValorTotal.update_layout(
    legend=dict(orientation='h', yanchor='top', y=1.1, xanchor='center', x=0.5),
    font=dict(size=10)
)


#layout
# ... Código anterior ...

# Layout do aplicativo
# ... Código anterior ...

import dash_bootstrap_components as dbc

import dash_bootstrap_components as dbc

# Layout do aplicativo
app.layout = dbc.Container(fluid=True, className='vh-100', children=[
    dbc.Row([
        # Sidebar
        dbc.Col(
            [  
                ThemeSwitchAIO(),
                html.Div(
                    [
                        html.Img(src='usuario.jpg', className='rounded-circle', style={'width': '200px'}),
                        html.H5('Nome do Usuário', className='mt-2')
                    ],
                    style={'text-align': 'center'},
                    className='mt2'
                ),
                dcc.Dropdown(
                    options=[{'label': loja, 'value': loja} for loja in opcoes],
                    value="Todas as lojas",
                    id='lista-de-lojas',
                    style={'font-size': '11px'}
                )
            ],
            className='col-lg-2 bg-light p-4'  # Defina o tamanho da sidebar aqui e aplique um estilo de fundo
        ),
        # Gráficos
        dbc.Col([
            dbc.Row([
                dbc.Col(
                    dbc.Card(
                        dbc.CardBody(
                            dcc.Graph(
                                id='grafico-quantidade-vendas',
                                figure=gValorTotal,
                                className='h-100'  # Defina a altura do gráfico para ocupar 100% do CardBody
                            )
                        ),
                        className='h-100 border border-0 shadow'  # Defina a altura do Card para ocupar 100% da Row
                    ),
                    className='col-lg-6'  # Defina o tamanho dos gráficos aqui
                ),
                dbc.Col(
                    dbc.Card(
                        dbc.CardBody(
                            dcc.Graph(
                                id='grafico-geral',
                                figure=fig,
                                className='h-100'  # Defina a altura do gráfico para ocupar 100% do CardBody
                            )
                        ),
                        className='h-100 border border-0 shadow'  # Defina a altura do Card para ocupar 100% da Row
                    ),
                    className='col-lg-6 h-100'  # Coloque um offset para alinhar com a sidebar
                ),
            ], className='my-2 h-50'),
            dbc.Row([
                dbc.Col(
                    dbc.Card(
                        dbc.CardBody(
                            dcc.Graph(
                                id='grafico-geral2',
                                figure=fig2,
                                className='h-100'  # Defina a altura do gráfico para ocupar 100% do CardBody
                            )
                        ),
                        className='h-100 border border-0 shadow'  # Defina a altura do Card para ocupar 100% da Row
                    ),
                    className='col-lg-12 h-100'  # Defina o tamanho do gráfico aqui
                )
            ], className='h-50')  # Defina a altura da row para ocupar metade da viewport height
        ], className='col-lg-10', style={'max-height': '100vh'})  # Defina a altura da coluna para ocupar a viewport height
    ], className='vh-100 mx-auto p-0')
])

# Adicione o callback para atualizar o tema
@app.callback(
    Output('theme-switch', 'data-theme'),
    Input('toggle-theme', 'n_clicks'),
    State('theme-switch', 'data-theme')
)
def toggle_theme(n_clicks, current_theme):
    if n_clicks is None:
        return current_theme

    # Alternar entre o tema escuro e claro
    return 'dark' if current_theme == 'light' else 'light'



# ... Código dos callbacks ...
@app.callback(
    Output('grafico-quantidade-vendas', 'figure'),
    Output('grafico-geral', 'figure'),
    Output('grafico-geral2', 'figure'),
    Input('lista-de-lojas', 'value')
)
def update_graphs(selected_loja):
    # Filtrar os dados com base na loja selecionada
    if selected_loja == "Todas as lojas":
        df_filtrado = df
    else:
        df_filtrado = df[df['ID Loja'] == selected_loja]

    # Atualizar o primeiro gráfico (gValorTotal) com base nos dados filtrados
    dfSelecionado = df_filtrado.filter(items=['ID Loja', 'Valor Final'])
    dfValorTotal = dfSelecionado.groupby(['ID Loja'], as_index=False)['Valor Final'].sum()
    gValorTotal = px.bar(dfValorTotal, y="Valor Final", x="ID Loja")
    gValorTotal.update_layout(
        legend=dict(orientation='h', yanchor='top', y=1.1, xanchor='center', x=0.5),
        font=dict(size=10)
    )

    # Atualizar o segundo gráfico (fig) com base nos dados filtrados
    fig = px.bar(df_filtrado, x="Produto", y="Quantidade", color="ID Loja", barmode="group")
    fig.update_layout(
        legend=dict(orientation='h', yanchor='top', y=1.1, xanchor='center', x=0.5),
        font=dict(size=10)
    )

    # Atualizar o terceiro gráfico (fig2) com base nos dados filtrados
    fig2 = px.line(df_filtrado, y="Valor Final", x="Data", color="ID Loja")
    fig2.update_layout(
        legend=dict(orientation='h', yanchor='top', y=1.1, xanchor='center', x=0.5),
        font=dict(size=10)
    )

    # Retornar os gráficos atualizados
    return gValorTotal, fig, fig2



# ... Código dos callbacks ...



if __name__ == '__main__':
    app.run(debug=False)