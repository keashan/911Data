import os

import dash
import dash_bootstrap_components as dbc
from flask import Flask
from flask_caching import Cache

# Initialize the app
app = dash.Dash(__name__, suppress_callback_exceptions=True,
                meta_tags=[{'name': 'viewport', 'content': "width=device-width, initial-scale=1.0"}],
                external_stylesheets=[dbc.themes.LUX], title="911 Data Analysis")
cache = Cache(app.server, config={
    # try 'FileSystemCache' if you don't want to setup redis
    'CACHE_TYPE': 'SimpleCache',
    'CACHE_DEFAULT_TIMEOUT': 600
})
# Initialize the server
server = app.server

app.config.suppress_callback_exceptions = True

# config
server.config.update(
    SECRET_KEY=os.urandom(12),
    SQLALCHEMY_DATABASE_URI='postgresql://soknmkqscvzrmw:1dbfd508eb100989cba47535362bd54d93a5607f05f558b8952ae2f20515521d@ec2-52-209-171-51.eu-west-1.compute.amazonaws.com:5432/d7vpl3clbr272v',
    SQLALCHEMY_TRACK_MODIFICATIONS=False
)

