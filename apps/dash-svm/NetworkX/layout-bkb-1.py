from pybkb.common.bayesianKnowledgeBase import bayesianKnowledgeBase as BKB     
from pybkb.common.bayesianKnowledgeBase import BKB_S_node                       
from pybkb.python_base.reasoning.reasoning import checkMutex
                                                                                
import dash                                                                     
import dash_cytoscape as cyto                                                   
import dash_html_components as html                                             
import dash_core_components as dcc                                              
#import utils.dash_reusable_components as drc
import networkx as nx 
from dash.dependencies import Input, Output, State
import json                                                                     

edges = None
nodes = None

styles = {
    'json-output': {
        'overflow-y': 'scroll',
        'height': 'calc(50% - 25px)',
        'border': 'thin lightgrey solid'
    },
    'tab': {'height': 'calc(98vh - 115px)'}
}

# Display utility functions
def _merge(a, b):
    return dict(a, **b)


def _omit(omitted_keys, d):
    return {k: v for k, v in d.items() if k not in omitted_keys}


# Custom Display Components
def Card(children, **kwargs):
    return html.Section(
        children,
        style=_merge({
            'padding': 20,
            'margin': 5,
            'borderRadius': 5,
            'border': 'thin lightgrey solid',

            # Remove possibility to select the text for better UX
            'user-select': 'none',
            '-moz-user-select': 'none',
            '-webkit-user-select': 'none',
            '-ms-user-select': 'none'
        }, kwargs.get('style', {})),
        **_omit(['style'], kwargs)
    )

                                                                                
app = dash.Dash(__name__, suppress_callback_exceptions=True)                                                       
                                                                                 
app.layout = html.Div(                                                         
    children=[

        html.Div(
            className='banner', 
            children=[
                html.Div(
                    className='container scalable',
                    children=[
                        html.H1(
                            id='banner-title',
                            children=[
                                html.A(
                                    "Eamon Hanley BKB Visualization",
                                    style={
                                        'text-decoration': 'none',
                                        'color': 'inherit',
                                    },
                                )
                            ],
                        ),
                    ],
                )
            ]
        ),
                                
        html.Div(
            id='body',
            className='container scalable',
            children=[
                html.Div(
                    id='app-container',
                    children=[
                        html.Div(
                            id='left-column',
                            children=[
                                Card(
                                    id='first-card',
                                    children=[
                                        dcc.Upload(
                                            id='upload-bkb',
                                            children = [
                                                html.Button('Upload BKB')
                                            ]
                                        ),
                                    ],
                                ),
                                Card(
                                    id='information-card',
                                    children=[
                                        html.H4(
                                            "Last Visited Node: ", 
                                            id='cytoscape-mouseoverNodeData-output'
                                        ),
                                        html.Pre(
                                            "Node Data JSON: ",
                                            id='selected-node-data-json-output',
                                            style=styles['json-output'],
                                        ),
                                    ],
                                ),
                                Card(
                                    id='add-remove-card',
                                    children=[
                                        html.Button(
                                            "Remove Selected Node", 
                                            id='remove-button', 
                                            n_clicks_timestamp=0
                                        ),
                                        html.Hr(),
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
                                    ],
                                ),     
                                Card(
                                    id='mutex',
                                    children=[
                                        html.Button(
                                            "Mutex Check",
                                            id='mutex-button',
                                        ),
                                        html.Div(
                                            id='mutex-check',
                                        ),
                                    ]
                                ),
#                                 Card(
#                                     id='multi-dropdown',
#                                     children=[
#                                         dcc.Dropdown(
#                                             options=[
#                                             ],
#                                             multi=True
#                                         )
#                                     ),
                            ],
                        ),
                        html.Div(
                            id='bkbs',
                            children=[
                                html.Div(
                                    id='output-bkb-upload'
                                )
                            ],
                        ),        
                    ],
                ),
            ],
        ),
    ],        
)
                                                                         
@app.callback(
        Output('output-bkb-upload', 'children'),
        [Input('upload-bkb', 'contents'),
        Input('upload-bkb', 'filename')]
        )

def update_output(contents, filename):
    global edges, nodes

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

        for element in cg['elements']['nodes']:
            if element['data']['node_type'] == "s":
                temp1 = element['data']['label'].split("{")
                temp2 = temp1[1].split("} = ")
                temp3 = temp2[1].split("$")

                element['data']['label'] = "s" + temp2[0] + " = " + temp3[0]

        dc_elements = cg['elements']['nodes'] + cg['elements']['edges']                 
        print(dc_elements)
        edges = cg['elements']['edges']
        nodes = cg['elements']['nodes']

        children = [cyto.Cytoscape(                                                             
            id='bkb-cyto',                                                          
            layout={'name': 'breadthfirst'},                                        
            style={'width': '1500px', 'height': '1000px'},                          
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


@app.callback(Output('bkb-cyto', 'elements'),
        [Input('remove-button', 'n_clicks_timestamp'),
         Input('add-button', 'n_clicks_timestamp')],    
        [State('node-label-data', 'value'),
         State('node-type-data', 'value'),
         State('bkb-cyto', 'elements'),
         State('bkb-cyto', 'selectedNodeData')]
        )

def edit_nodes(remove, add, node_label, node_type, elements, data):
    global nodes, edges

    if elements and data:

        if int(remove) > int(add):
            ids_to_remove = {ele_data['id'] for ele_data in data}                   
            new_elements = [ele for ele in elements if ele['data']['id'] not in ids_to_remove]
            
            new_nodes = [ele for ele in nodes if ele['data']['id'] not in ids_to_remove]
            new_edges = [ele for ele in edges if ele['data']['target'] or ele['data']['source'] not in ids_to_remove]

            nodes = new_nodes
            edges = new_edges

            return nodes + edges

#            return new_elements 

        elif int(remove) < int(add):
            
            new_elements=elements

            node = {'data': {}}
            node['data']['node_type']=node_type
            node['data']['label']=node_label
#             node['data']['id']=len(elements)
#             node['data']['value']=len(elements)
#             node['data']['name']=len(elements)
            node['data']['id'] = len(nodes)
            node['data']['value'] = len(nodes)
            node['data']['label'] = len(nodes)

            edge = {'data': {}}
            edge['data']['source']=data[0]['id']
#            edge['data']['target']=len(elements)
            edge['data']['target']=len(nodes)

            new_elements.append(node)
            new_elements.append(edge)

            nodes.append(node)
            edges.append(edge)

            return nodes + edges

#            return new_elements

        else:
            return elements

    return elements


@app.callback(Output('selected-node-data-json-output', 'children'),
              Input('bkb-cyto', 'selectedNodeData')
             )
def displaySelectedNodeData(data):
    return json.dumps(data, indent=2)

@app.callback(Output('mutex-check', 'children'),
              Input('mutex-button', 'n_clicks'),
              State('bkb-cyto', 'elements'),
             )

#TODO: Make a function that reads in a cyto bkb and returns a PyBKB bkb.
def make_bkb_from_cyto(cyto_data):
    # Do Something
    return bkb

def simple_mutex_check(bkb):
    # Scan all snodes for appropriate config.
    ## No multi-heads
    ## No Free floaters

    # Scan all inodes for appropriate config.
    ## All have at least one incoming S-node.
    return True or False


def mutex_check(_, elements):
    bkb = make_bkb_from_cyto(elements)
    if not simple_mutex_check(bkb):
        return False
    
    bkb = BKB()
    component_set = set()
    parentless_s_set = set()
#     for ne in elements:
#         if elements['data']['node_type'] == 'i':
#             comp = elements['data']['label'].split('\n')[0]
#             state = elements['data']['label'].split('\n')[1]
#             
#             if comp not in component_set:
#                 bkb.addComponent(comp)
#                 component_set.add(comp)
# 
#             bkb.addComponentState(comp, state)
# 
#        elif elements['data']['node_type'] == 's':

    def search_tail(node_id):
        n_list = []
        for edge in edges:
            if edge['data']['target'] == node_id:
                n_list.append(edge['data']['target'])
        return n_list

    def search_head(node_id):
        n_list = []
        for edge in edges:
            if edge['data']['source'] == node_id:
                n_list.append(edge['data']['source'])
        return n_list

    def return_node(node_id):
        for node in nodes:
            if node['data']['id'] == node_id:
                return node
        return None

    for edge in edges:
        print(edge)
        n_id = edge['data']['target']
        parentless_s_set.add(n_id)

    for node in nodes:
        if node['data']['node_type'] == 'i':
            comp = node['data']['label'].split('\n')[0]
            state = node['data']['label'].split('\n')[1]

            if comp not in component_set:
                comp_idx = bkb.addComponent(comp)
                component_set.add(comp)
            state_idx = bkb.addComponentState(comp_idx, state)
        else:
            s_id = node['data']['id']
            if s_id not in parentless_s_set:
                target_id = search_tail(s_id)[0]
                target_node = return_node(target_id)

                comp = target_node['data']['label'].split('\n')[0]
                state = target_node['data']['label'].split('\n')[1]
                prob = float(node['data']['label'].split(' = ')[1])

                # Find a component index
                comp_idx = bkb.getComponentIndex(comp)
                # Find a state index
                state_idx = bkb.getComponentINodeIndex(comp_idx, state)

                bkb.addSNode(comp_idx, state_idx, prob)
            else:
                source_ids = search_head(s_id)
                source_node = return_node(source_id)
                target_ids = search_tail(s_id)
                target_node = return_node(target_id)

                s_comp = source_node['data']['label'].split('\n')[0]
                s_state = source_node['data']['label'].split('\n')[1]
                t_comp = target_node['data']['label'].split('\n')[0]
                t_state = target_node['data']['label'].split('\n')[1]
                prob = node['data']['label'].split(' = ')[1]

                bkb.addSNode(t_comp_idx, t_state_idx, prob, [(s_comp_idx, s_state_idx)])

                if len(source_ids) == 1:
                    source_node = return_node(source_ids[0])
                    s_comp = source_node['data']['label'].split('\n')[0]
                    s_state = source_node['data']['label'].split('\n')[1]

                    for t_id in target_ids:
                        t_node = return_node(t_id)
                        t_comp = target_node['data']['label'].split('\n')[0]
                        t_state = target_node['data']['label'].split('\n')[1] 
                        bkb.addSNode(t_comp, t_state, prob, [(s_comp, s_state)])




    return checkMutex(bkb)

                                                                              
if __name__ == '__main__':                                                      
    app.run_server(debug=True) 






