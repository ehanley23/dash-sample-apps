from pybkb.common.bayesianKnowledgeBase import bayesianKnowledgeBase as BKB     
from pybkb.common.bayesianKnowledgeBase import BKB_S_node                       
                                                                                
import dash                                                                     
import dash_cytoscape as cyto                                                   
import dash_html_components as html                                             
import dash_core_components as dcc                                              
import networkx as nx 
from dash.dependencies import Input, Output
import json                                                                     
import os
                                                                                
app = dash.Dash(__name__)                                                       
                                                                                 
app.layout = html.Div([                                                         
    dcc.Upload(
        id='upload-bkb',
        children = html.Button('Upload BKB')),

    html.Hr(),

    html.Div(id='output-bkb-upload'),
    ])
                                                                         
@app.callback(
        Output('output-bkb-upload', 'children'),
        [Input('upload-bkb', 'contents'),
        Input('upload-bkb', 'filename')]
        )

def update_output(contents, filename):
    
    bkb = BKB()                                                                     
#    bkb.load('../examples/' + chosen.os.path.basename(__file__))
#    bkb.save('../examples/' + chosen.os.path.basename(__file__), use_pickle=True)
    if contents is not None:
        
        binary = filename.split('.')
        if 'binary' not in filename: 
            bkb.load('/Users/Eamon/source/PyBKB/examples/' + filename)
            bkb.save('/Users/Eamon/source/PyBKB/examples/' + binary[0] + '_binary.bkb', use_pickle=True)
        else:
            bkb = bkb.load('/Users/Eamon/source/PyBKB/examples/' + filename, use_pickle=True)

        graph, fig  = bkb.makeGraph(show=False)                                         
        G = graph._build_bkb_graph()                                                    
        cg = nx.readwrite.json_graph.cytoscape_data(G)                                  
        dc_elements = cg['elements']['nodes'] + cg['elements']['edges']                 

        print(json.dumps(cg, indent=2))
        print(dc_elements)

        children = [cyto.Cytoscape(                                                             
            id='bkb-cyto',                                                          
            layout={'name': 'breadthfirst'},                                        
            style={'width': '2000px', 'height': '1500px'},                          
            elements=dc_elements
            )]
        return children
        
                                                                              
if __name__ == '__main__':                                                      
    app.run_server(debug=True) 






