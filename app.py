import dash

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(__name__, external_stylesheets=external_stylesheets, url_base_pathname='/SOKA-analysis/')

server = app.server

app.config.suppress_callback_exceptions = True

import dash_auth

# Keep this out of source code repository - save in a file or a database

VALID_USERNAME_PASSWORD_PAIRS = [

    ['admin', 'admin']

]

auth = dash_auth.BasicAuth(

    app,

    VALID_USERNAME_PASSWORD_PAIRS

)