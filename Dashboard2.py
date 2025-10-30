from dash import Dash, dcc, html, Input, Output, callback
import plotly.express as px
import plotly.graph_objects as go
from plotly.data import gapminder
import plotly.io as pio

# 设置默认主题，避免 "Invalid value" 错误
pio.templates.default = "plotly_white"

# 加载数据
gapminder_df = gapminder()

# 获取唯一的年份与洲
continents = gapminder_df["continent"].unique()
years = sorted(gapminder_df["year"].unique())

# 创建 Dash 应用
app = Dash(__name__)
app.title = "Gapminder Dashboard"


##################### 图表函数 #########################
def create_table():
    fig = go.Figure(data=[go.Table(
        header=dict(values=list(gapminder_df.columns), align='left'),
        cells=dict(values=[gapminder_df[col] for col in gapminder_df.columns], align='left'))
    ])
    fig.update_layout(paper_bgcolor="#e5ecf6", margin={"t": 0, "l": 0, "r": 0, "b": 0}, height=700)
    return fig


def create_population_chart(continent="Asia", year=1952):
    filtered_df = gapminder_df[(gapminder_df["continent"] == continent) & (gapminder_df["year"] == year)]
    if filtered_df.empty:
        return px.scatter(title=f"No data available for {continent} ({year})")

    filtered_df = filtered_df.sort_values(by="pop", ascending=False).head(15)
    fig = px.bar(filtered_df, x="country", y="pop", color="country",
                 title=f"Top 15 Populations in {continent} ({year})", text_auto=True)
    fig.update_layout(paper_bgcolor="#e5ecf6", height=600)
    return fig


def create_gdp_chart(continent="Asia", year=1952):
    filtered_df = gapminder_df[(gapminder_df["continent"] == continent) & (gapminder_df["year"] == year)]
    if filtered_df.empty:
        return px.scatter(title=f"No data available for {continent} ({year})")

    filtered_df = filtered_df.sort_values(by="gdpPercap", ascending=False).head(15)
    fig = px.bar(filtered_df, x="country", y="gdpPercap", color="country",
                 title=f"Top 15 GDP per Capita in {continent} ({year})", text_auto=True)
    fig.update_layout(paper_bgcolor="#e5ecf6", height=600)
    return fig


def create_life_exp_chart(continent="Asia", year=1952):
    filtered_df = gapminder_df[(gapminder_df["continent"] == continent) & (gapminder_df["year"] == year)]
    if filtered_df.empty:
        return px.scatter(title=f"No data available for {continent} ({year})")

    filtered_df = filtered_df.sort_values(by="lifeExp", ascending=False).head(15)
    fig = px.bar(filtered_df, x="country", y="lifeExp", color="country",
                 title=f"Top 15 Life Expectancy in {continent} ({year})", text_auto=True)
    fig.update_layout(paper_bgcolor="#e5ecf6", height=600)
    return fig


def create_choropleth_map(variable="lifeExp", year=1952):
    filtered_df = gapminder_df[gapminder_df["year"] == year]
    fig = px.choropleth(filtered_df, color=variable,
                        locations="iso_alpha", locationmode="ISO-3",
                        color_continuous_scale="RdYlBu",
                        hover_data=["country", variable],
                        title=f"{variable} Map ({year})")
    fig.update_layout(paper_bgcolor="#e5ecf6", height=600, margin={"l": 0, "r": 0})
    return fig


##################### 页面布局 #########################
app.layout = html.Div([
    # 标题区域
    html.Div([
        html.H1("🌍 Gapminder Data Explorer",
                style={
                    "textAlign": "center",
                    "color": "white",
                    "marginBottom": "10px",
                    "fontSize": "2.5rem",
                    "fontWeight": "bold",
                    "textShadow": "2px 2px 4px rgba(0,0,0,0.3)"
                }),
        html.P("Explore global development indicators across time and continents",
               style={
                   "textAlign": "center",
                   "color": "white",
                   "marginBottom": "30px",
                   "fontSize": "1.1rem",
                   "opacity": "0.9"
               })
    ], style={
        "background": "linear-gradient(135deg, #667eea 0%, #764ba2 100%)",
        "padding": "30px",
        "borderRadius": "15px",
        "marginBottom": "30px",
        "boxShadow": "0 4px 15px rgba(0,0,0,0.2)"
    }),

    # 主要内容区域
    html.Div([
        # 左侧标签页
        html.Div([
            dcc.Tabs([
                dcc.Tab(label="📊 Dataset", value="tab-1",
                        style={'padding': '15px', 'fontSize': '16px', 'fontWeight': 'bold'},
                        selected_style={'backgroundColor': '#f8f9fa', 'border': '2px solid #667eea'}),
                dcc.Tab(label="👥 Population", value="tab-2",
                        style={'padding': '15px', 'fontSize': '16px', 'fontWeight': 'bold'},
                        selected_style={'backgroundColor': '#f8f9fa', 'border': '2px solid #667eea'}),
                dcc.Tab(label="💰 GDP per Capita", value="tab-3",
                        style={'padding': '15px', 'fontSize': '16px', 'fontWeight': 'bold'},
                        selected_style={'backgroundColor': '#f8f9fa', 'border': '2px solid #667eea'}),
                dcc.Tab(label="❤️ Life Expectancy", value="tab-4",
                        style={'padding': '15px', 'fontSize': '16px', 'fontWeight': 'bold'},
                        selected_style={'backgroundColor': '#f8f9fa', 'border': '2px solid #667eea'}),
                dcc.Tab(label="🌎 Choropleth Map", value="tab-5",
                        style={'padding': '15px', 'fontSize': '16px', 'fontWeight': 'bold'},
                        selected_style={'backgroundColor': '#f8f9fa', 'border': '2px solid #667eea'}),
            ],
                vertical=True,
                id="vertical-tabs",
                style={
                    "height": "500px",
                    "borderRight": "2px solid #e9ecef",
                    "backgroundColor": "white",
                    "borderRadius": "10px",
                    "padding": "10px",
                    "boxShadow": "0 2px 10px rgba(0,0,0,0.1)"
                },
                content_style={"display": "none"})
        ], style={"width": "250px", "float": "left", "paddingRight": "25px"}),

        # 右侧内容区域
        html.Div([
            html.Div(id="tab-content", style={"backgroundColor": "white", "padding": "25px", "borderRadius": "10px",
                                              "boxShadow": "0 2px 10px rgba(0,0,0,0.1)"})
        ], style={"marginLeft": "275px", "minHeight": "600px"})
    ])
], style={
    "background": "linear-gradient(120deg, #f6f9fc 0%, #e9ecef 100%)",
    "padding": "25px",
    "minHeight": "100vh",
    "fontFamily": "'Segoe UI', Tahoma, Geneva, Verdana, sans-serif"
})


##################### 交互逻辑 #########################
@app.callback(Output("tab-content", "children"),
              Input("vertical-tabs", "value"))
def render_content(tab):
    if tab == "tab-1":
        return dcc.Graph(id="dataset", figure=create_table())
    elif tab == "tab-2":
        return html.Div([
            html.H3("Population Analysis", style={"color": "#2c3e50", "marginBottom": "20px"}),
            html.Div([
                html.Label("Select Continent:", style={"fontWeight": "bold", "marginBottom": "5px"}),
                dcc.Dropdown(id="cont_pop", options=[{"label": c, "value": c} for c in continents],
                             value="Asia", clearable=False)
            ], style={"marginBottom": "15px"}),
            html.Div([
                html.Label("Select Year:", style={"fontWeight": "bold", "marginBottom": "5px"}),
                dcc.Dropdown(id="year_pop", options=[{"label": y, "value": y} for y in years],
                             value=1952, clearable=False)
            ], style={"marginBottom": "25px"}),
            dcc.Graph(id="population")
        ])
    elif tab == "tab-3":
        return html.Div([
            html.H3("GDP per Capita Analysis", style={"color": "#2c3e50", "marginBottom": "20px"}),
            html.Div([
                html.Label("Select Continent:", style={"fontWeight": "bold", "marginBottom": "5px"}),
                dcc.Dropdown(id="cont_gdp", options=[{"label": c, "value": c} for c in continents],
                             value="Asia", clearable=False)
            ], style={"marginBottom": "15px"}),
            html.Div([
                html.Label("Select Year:", style={"fontWeight": "bold", "marginBottom": "5px"}),
                dcc.Dropdown(id="year_gdp", options=[{"label": y, "value": y} for y in years],
                             value=1952, clearable=False)
            ], style={"marginBottom": "25px"}),
            dcc.Graph(id="gdp")
        ])
    elif tab == "tab-4":
        return html.Div([
            html.H3("Life Expectancy Analysis", style={"color": "#2c3e50", "marginBottom": "20px"}),
            html.Div([
                html.Label("Select Continent:", style={"fontWeight": "bold", "marginBottom": "5px"}),
                dcc.Dropdown(id="cont_life_exp", options=[{"label": c, "value": c} for c in continents],
                             value="Asia", clearable=False)
            ], style={"marginBottom": "15px"}),
            html.Div([
                html.Label("Select Year:", style={"fontWeight": "bold", "marginBottom": "5px"}),
                dcc.Dropdown(id="year_life_exp", options=[{"label": y, "value": y} for y in years],
                             value=1952, clearable=False)
            ], style={"marginBottom": "25px"}),
            dcc.Graph(id="life_expectancy")
        ])
    elif tab == "tab-5":
        return html.Div([
            html.H3("Global Choropleth Map", style={"color": "#2c3e50", "marginBottom": "20px"}),
            html.Div([
                html.Label("Select Variable:", style={"fontWeight": "bold", "marginBottom": "5px"}),
                dcc.Dropdown(id="var_map",
                             options=[
                                 {"label": "Population", "value": "pop"},
                                 {"label": "GDP per Capita", "value": "gdpPercap"},
                                 {"label": "Life Expectancy", "value": "lifeExp"}],
                             value="lifeExp", clearable=False)
            ], style={"marginBottom": "15px"}),
            html.Div([
                html.Label("Select Year:", style={"fontWeight": "bold", "marginBottom": "5px"}),
                dcc.Dropdown(id="year_map", options=[{"label": y, "value": y} for y in years],
                             value=1952, clearable=False)
            ], style={"marginBottom": "25px"}),
            dcc.Graph(id="choropleth_map")
        ])
    else:
        return html.Div("Please select a tab")


# 更新回调函数，添加 suppress_callback_exceptions
app.config.suppress_callback_exceptions = True


# 回调函数保持不变
@callback(Output("population", "figure"),
          [Input("cont_pop", "value"), Input("year_pop", "value")])
def update_population_chart(continent, year):
    return create_population_chart(continent, year)


@callback(Output("gdp", "figure"),
          [Input("cont_gdp", "value"), Input("year_gdp", "value")])
def update_gdp_chart(continent, year):
    return create_gdp_chart(continent, year)


@callback(Output("life_expectancy", "figure"),
          [Input("cont_life_exp", "value"), Input("year_life_exp", "value")])
def update_life_exp_chart(continent, year):
    return create_life_exp_chart(continent, year)


@callback(Output("choropleth_map", "figure"),
          [Input("var_map", "value"), Input("year_map", "value")])
def update_choropleth_map(variable, year):
    return create_choropleth_map(variable, year)


##################### 运行应用 #########################
if __name__ == "__main__":
    app.run(debug=True, port=8080)
