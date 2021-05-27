from pybkb.common.bayesianKnowledgeBase import bayesianKnowledgeBase as BKB     
from pybkb.common.bayesianKnowledgeBase import BKB_S_node                       
                                                                                
import dash                                                                     
import dash_cytoscape as cyto                                                   
import dash_html_components as html                                             
import dash_core_components as dcc                                              
import networkx as nx 
from dash.dependencies import Input, Output, State
import json                                                                     

styles = {
    'json-output': {
        'overflow-y': 'scroll',
        'height': 'calc(50% - 25px)',
        'border': 'thin lightgrey solid'
    },
    'tab': {'height': 'calc(98vh - 115px)'}
}
                                                                                
app = dash.Dash(__name__, suppress_callback_exceptions=True)                                                       
                                                                                 
app.layout = html.Div([                                                         

    html.Div(className='banner', children=[
        html.H1(children="Eamon Hanley BKB Visualization")
    ]),

    html.Div(className='buttons', children=[
        dcc.Upload(
            id='upload-bkb',
            children = html.Button('Upload BKB')),

        html.Hr(),

        html.Button("Remove Selected Node", id='remove-button', n_clicks_timestamp=0),

        html.H4("Last Visited Node: ", id='cytoscape-mouseoverNodeData-output'),

#        html.H4('Node Data JSON:', id='selected-node-data-json-output', style=styles['json-output']),
        html.Pre("Node Data JSON: ",
            id='selected-node-data-json-output',
            style=styles['json-output']
        ),

        html.Hr(),
    ]),

    html.Div(className='add-nodes', children=[
        dcc.Dropdown(
            id='node-type-data',
            options=[
                {'label': 'I Node', 'value': 'i'},
                {'label': 'S Node', 'value': 's'}
            ],
            clearable=False
        ),
        dcc.Input(
            id='node-label-data',
            placeholder='Enter the node label...',
            type='text',
        ),
        html.Button(
            "Make Node",
            id='add-button',
            n_clicks_timestamp=0
        )
    ]),


    html.Div(className='display', children=[
        html.Div(id='output-bkb-upload'),
    ])

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
#                element['data']['selectable'] = True

        dc_elements = cg['elements']['nodes'] + cg['elements']['edges']                 

        children = [cyto.Cytoscape(                                                             
            id='bkb-cyto',                                                          
            layout={'name': 'breadthfirst'},                                        
            style={'width': '1500px', 'height': '1500px'},                          
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
#                        'background-color': 'blue',
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
#                        'background-color': 'red',
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

    

# @app.callback(Output('bkb-cyto', 'elements'),                                  
#               [Input('remove-button', 'n_clicks')],                             
#               [State('bkb-cyto', 'elements'),                                  
#               State('bkb-cyto', 'selectedNodeData')])                         
# def remove_selected_nodes(_, elements, data):                                   
#     if elements and data:                                                       
#         ids_to_remove = {ele_data['id'] for ele_data in data}                   
#         new_elements = [ele for ele in elements if ele['data']['id'] not in ids_to_remove]
#         return new_elements                                                     
#                                                                                 
#     return elements
# 
# 
# 
# @app.callback(
#         Output('bkb-cyto', 'elements'),
#         [Input('make-node', 'n_clicks'),
#         Input('node-label-data', 'node-label'),
#         Input('node-type-data', 'node-type')],
#         [State('bkb-cyto', 'elements'),
#         State('bkb-cyto', 'selectedNodeData')]
#         )
# 
# 
# def add_node_to_output(_, node_label, node_type, elements, data):
#     if elements and data:
#         node=", {'data': {'node_type': '" + node_type + "', 'label': '" + node_label + "', 'id': '" + len(elements)
#         + "', 'value': '" + len(elements) + "', 'name': '" + len(elements) + "'}}"
# 
#         edge=", {'data': {'source': " + data['id'] + ", 'target': " + len(elements) + "}}"
#         
#         new_elements=elements
#         new_elements+=node
#         new_elements+=edge
#         return new_elements
#     
#     return elements

@app.callback(Output('bkb-cyto', 'elements'),
#          Output('remove-button', 'n_clicks_timestamp'=0),
#          Output('add-button', 'n_clicks_timestamp'=0)],
        [Input('remove-button', 'n_clicks_timestamp'),
         Input('add-button', 'n_clicks_timestamp')],    
        [State('node-label-data', 'value'),
         State('node-type-data', 'value'),
         State('bkb-cyto', 'elements'),
         State('bkb-cyto', 'selectedNodeData')]
        )

def edit_nodes(remove, add, node_label, node_type, elements, data):
    if elements and data:

        if int(remove) > int(add):
            ids_to_remove = {ele_data['id'] for ele_data in data}                   
            new_elements = [ele for ele in elements if ele['data']['id'] not in ids_to_remove]
            return new_elements 

        elif int(remove) < int(add):
#             node=", {'data': {'node_type': '" + str(node_type) + "', 'label': '" + str(node_label) + "', 'id': '" + str(len(elements))+ "', 'value': '" + str(len(elements)) + "', 'name': '" + str(len(elements)) + "'}}"
#             edge=", {'data': {'source': " + str(data[0]['id']) + ", 'target': " + str(len(elements)) + "}}"                                                                             
            
            new_elements=elements

            node = {'data': {}}
            node['data']['node_type']=node_type
            node['data']['label']=node_label
            node['data']['id']=len(elements)
            node['data']['value']=len(elements)
            node['data']['name']=len(elements)

            edge = {'data': {}}
            edge['data']['source']=data[0]['id']
            edge['data']['target']=len(elements)

            new_elements.append(node)
            new_elements.append(edge)

            return new_elements

        else:
            return elements

    return elements


@app.callback(Output('selected-node-data-json-output', 'children'),
              [Input('bkb-cyto', 'selectedNodeData')])
def displaySelectedNodeData(data):
    return json.dumps(data, indent=2)

                                                                              
if __name__ == '__main__':                                                      
    app.run_server(debug=True) 






