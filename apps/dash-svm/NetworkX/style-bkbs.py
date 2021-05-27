from pybkb.common.bayesianKnowledgeBase import bayesianKnowledgeBase as BKB     
from pybkb.common.bayesianKnowledgeBase import BKB_S_node                       
                                                                                
import dash                                                                     
import dash_cytoscape as cyto                                                   
import dash_html_components as html                                             
import dash_core_components as dcc                                              
import networkx as nx 
from dash.dependencies import Input, Output
import json                                                                     
                                                                                
app = dash.Dash(__name__, suppress_callback_exceptions=True)                                                       
                                                                                 
app.layout = html.Div([                                                         

    html.H1(children="Eamon Hanley BKB Visualization"),

    dcc.Upload(
        id='upload-bkb',
        children = html.Button('Upload BKB')),

    html.Hr(),

    html.Div(id='output-bkb-upload'),

    html.P(id='cytoscape-mouseoverNodeData-output'),

    ])

                                                                         
@app.callback(
        Output('output-bkb-upload', 'children'),
        [Input('upload-bkb', 'contents'),
        Input('upload-bkb', 'filename')]
        )

def update_output(contents, filename):
    
    bkb = BKB()                                                                     

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
#        print(json.dumps(cg, indent=2))

        for element in cg['elements']['nodes']:
            if element['data']['node_type'] == "s":
                temp1 = element['data']['label'].split("{")
                temp2 = temp1[1].split("} = ")
                temp3 = temp2[1].split("$")

                element['data']['label'] = "s" + temp2[0] + " = " + temp3[0]

        dc_elements = cg['elements']['nodes'] + cg['elements']['edges']                 

        children = [cyto.Cytoscape(                                                             
            id='bkb-cyto',                                                          
            layout={'name': 'breadthfirst'},                                        
            style={'width': '1900px', 'height': '1500px'},                          
            elements=dc_elements,
            stylesheet=[
                {
                    'selector': 'node',
                    'style': {
                        'label': 'data(label)',
                        'text-wrap': 'wrap',
#                        "text-background-color": "white",
                    }
                },
                {
                    'selector': '[node_type *= "i"]',
                    'style': {
                        'background-color': 'blue',
                        'text-halign':'center',
                        'text-valign':'center',
                        'width':'label',
                        'height':'label',
                        'shape': 'rectangle',

                    }
                },
                {
                    'selector': '[node_type *= "s"]',
                    'style': {
                        'background-color': 'red',
                        'shape': 'circle',
                    }
                },
                {
                    'selector': 'edge',
                    'style': {
                        'curve-style': 'bezier',
                        'mid-target-arrow-shape': 'triangle',
                    }
                }]

           )]
        return children
    
@app.callback(Output('cytoscape-mouseoverNodeData-output', 'children'),
              Input('bkb-cyto', 'mouseoverNodeData'))
def displayTapNodeData(data):
    if data:
        return "Node Data: " + data['label']
                                                                              
if __name__ == '__main__':                                                      
    app.run_server(debug=True) 






