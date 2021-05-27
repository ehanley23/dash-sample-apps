import matplotlib.pyplot as plt
import numpy as np
from io import BytesIO
import base64
import dash
import dash_html_components as html
import dash_core_components as dcc
from dash.dependencies import Input, Output

from IPython import display
import os
def show_app(app, port = 9999,
             width = 700,
             height = 350,
             offline = False,
            in_binder = None):
    in_binder ='JUPYTERHUB_SERVICE_PREFIX' in os.environ if in_binder is None else in_binder
    if in_binder:
        base_prefix = '{}proxy/{}/'.format(os.environ['JUPYTERHUB_SERVICE_PREFIX'], port)
        url = 'https://hub.mybinder.org{}'.format(base_prefix)
        app.config.requests_pathname_prefix = base_prefix
    else:
        url = 'http://localhost:%d' % port

    iframe = '<a href="{url}" target="_new">Open in new window</a><hr><iframe src="{url}" width={width} height={height}></iframe>'.format(url = url,
                                                                                  width = width,
                                                                                  height = height)

    display.display_html(iframe, raw = True)
    if offline:
        app.css.config.serve_locally = True
        app.scripts.config.serve_locally = True
    return app.run_server(debug=False, # needs to be false in Jupyter
                          host = '0.0.0.0',
                          port=port)

def fig_to_uri(in_fig, close_all=True, **save_args):
    # type: (plt.Figure) -> str
    """
    Save a figure as a URI
    :param in_fig:
    :return:
    """
    out_img = BytesIO()
    in_fig.savefig(out_img, format='png', **save_args)
    if close_all:
        in_fig.clf()
        plt.close('all')
    out_img.seek(0)  # rewind file
    encoded = base64.b64encode(out_img.read()).decode("ascii").replace("\n", "")
    return "data:image/png;base64,{}".format(encoded)
app_iplot = dash.Dash()

app_iplot.layout = html.Div([
    dcc.Input(id='plot_title', value='Type title...', type="text"),
    dcc.Slider(
        id='box_size',
        min=1,
        max=10,
        value=4,
        step=1,
        marks=list(range(0, 10))
    ),
    html.Div([html.Img(id = 'cur_plot', src = '')],
             id='plot_div')
])

@app_iplot.callback(
    Output(component_id='cur_plot', component_property='src'),
    [Input(component_id='plot_title', component_property='value'), Input(component_id = 'box_size', component_property='value')]
)
def update_graph(input_value, n_val):
    fig, ax1 = plt.subplots(1,1)
    np.random.seed(len(input_value))
    ax1.matshow(np.random.uniform(-1,1, size = (n_val,n_val)))
    ax1.set_title(input_value)
    out_url = fig_to_uri(fig)
    return out_url

show_app(app_iplot)
