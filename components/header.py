import dash_html_components as html


navbar = html.Div([
        html.Img(src="https://c1exchange.com/images/stories/joomla/logo-c1x.png", width="75px", style={'float': 'left',
                                                                                                       'margin-left': '2px',
                                                                                                       'margin-top': '2px'}),
        html.H3('SOKA INSIGHTS', style={'margin': '0', 'left': '7%', 'position': 'absolute'})
    ], style={'display': 'inline-flex',
              'color': '#111111', 'font-weight': '200', 'font-family':"Impact"}
)


