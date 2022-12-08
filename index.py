import configparser
import warnings

from dash import html, Output, Input, dcc
from flask_login import LoginManager, UserMixin
from flask_sqlalchemy import SQLAlchemy

from app import app, server

import dash_bootstrap_components as dbc

from pages import home_page

warnings.filterwarnings("ignore")

db = SQLAlchemy(app.server)
config = configparser.ConfigParser()
con = db.engine

db.init_app(server)

# setup login manager
login_manager = LoginManager()
login_manager.init_app(server)
login_manager.login_view = "/login"



app.layout = dbc.Container([
    dbc.Row([
        dbc.Col(html.Div("911 Data Analysis", className="header_text"), width=12),
        dcc.Location(id="url")
    ]),
    dbc.Row([
        dbc.Col([
            html.Div(id="page-content", children=[]),
        ])
    ])
], fluid=True)


@app.callback(
    Output("page-content", "children"),
    Input("url", "pathname")
)
def render_page_content(pathname):
    if pathname == "/":
        return home_page.home_page()
    elif pathname == "/apps/home":
        return home_page.home_page()


# run the app
if __name__ == '__main__':
    app.run_server(port=8050, debug=True)
