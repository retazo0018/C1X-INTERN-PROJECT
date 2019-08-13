
import dash_core_components as dcc

import dash_html_components as html

from dash.dependencies import Input, Output

from app import app

import callbacks

import dash

from layouts import home, noPage


app.config.suppress_callback_exceptions = True



app.index_string = ''' 

<!DOCTYPE html>

<html>

    <head>

        {%metas%}

        <title>SOKA Analysis Report</title>

        <link rel="icon"  
            href="https://c1exchange.com/images/stories/joomla/logo-c1x.png" type="image/x-icon"/>
        {%css%}

    </head>

    <body>

        {%app_entry%}
    
        <footer>

            {%config%}

            {%scripts%}
            
            {%renderer%}

        </footer>

        <div></div>
        
        

    </body>

</html>

'''



app.layout = html.Div([

    dcc.Location(id='url', refresh=False),

    html.Div(id='page-content')

])

# Update page


@app.callback(Output('page-content', 'children'),

              [Input('url', 'pathname')])
def display_page(pathname):
    if pathname == '/SOKA-analysis/':
        return home

    else:
        return noPage


external_css = []

for css in external_css:

    app.css.append_css({"external_url": css})


external_js = []


for js in external_js:

    app.scripts.append_script({"": js})

if __name__ == '__main__':
    app.run_server(debug=True)
