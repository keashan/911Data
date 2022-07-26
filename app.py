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

