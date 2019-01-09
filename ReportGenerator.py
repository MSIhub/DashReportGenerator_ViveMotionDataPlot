# -*- coding: utf-8 -*-
"""
Created on Tue Jan 08 23:00:33 2019

@author: sadiq@MSIHub
"""


import dash
import dash_core_components as dcc
import dash_html_components as html
import pandas as pd
import time
import plotly.graph_objs as go


######################################### RAW DATA INPUT ###########################################################################################
InFilePath1 = "D:/Sadiq/PythonFiles/TrackerDataSink/TR1_334_1546973950.txt";
InFilePath2 = "D:/Sadiq/PythonFiles/TrackerDataSink/TR2_334_1546973950.txt";
InFilePath3 = "D:/Sadiq/PythonFiles/TrackerDataSink/VRCameraRoot_334_1546973950.txt";

headers = ["Timestamp","Position data in X axis","Position data in Y axis","Position data in Z axis",\
           "Linear Velocity data in X axis","Linear Velocity data in Y axis","Linear Velocity data in Z axis",\
           "Linear Acceleration data in X axis","Linear Acceleration data in Y axis","Linear Acceleration data in Z axis",\
           "Orientation data in X axis","Orientation data in Y axis","Orientation data in Z axis",\
           "Angular Velocity data in X axis","Angular Velocity data in Y axis","Angular Velocity data in Z axis",\
           "Angular Acceleration data in X axis","Angular Acceleration data in Y axis","Angular Acceleration data in Z axis"];

start = time.time()
TR1 = pd.read_csv(InFilePath1, names = headers, delimiter=" ", low_memory=True); # TR1 -> Data of Tracker 1 (Head) with respect to the base frame
TR2 = pd.read_csv(InFilePath2, names = headers, delimiter=" ", low_memory=True); # TR2 -> Data of Tracker 2 (Sternum) with respect to the base frame
VRCameraRoot = pd.read_csv(InFilePath3, names = headers, delimiter=" ", low_memory=True); # VRCameraRoot -> Data of TR1 with respect to the TR2 frame
end = time.time()
TimeTakenToLoadData = end-start;
print('pandas',pd.__version__,'read',len(TR1),'lines in',TimeTakenToLoadData)
#####################################################################################################################################################

###################### Creating a dictionary for drop down menu  between data and headers ###########################################################
data_dict = {"Timestamp":VRCameraRoot[headers[0]].values,
"Position data in X axis": VRCameraRoot[headers[1]].values,
"Position data in Y axis": VRCameraRoot[headers[2]].values,
"Position data in Z axis": VRCameraRoot[headers[3]].values,
"Linear Velocity data in X axis": VRCameraRoot[headers[4]].values,
"Linear Velocity data in Y axis": VRCameraRoot[headers[5]].values,
"Linear Velocity data in Z axis": VRCameraRoot[headers[6]].values,
"Linear Acceleration data in X axis": VRCameraRoot[headers[7]].values,
"Linear Acceleration data in Y axis": VRCameraRoot[headers[8]].values,
"Linear Acceleration data in Z axis": VRCameraRoot[headers[9]].values,
"Orientation data in X axis": VRCameraRoot[headers[10]].values,
"Orientation data in Y axis": VRCameraRoot[headers[11]].values,
"Orientation data in Z axis": VRCameraRoot[headers[12]].values,
"Angular Velocity data in X axis": VRCameraRoot[headers[13]].values,
"Angular Velocity data in Y axis": VRCameraRoot[headers[14]].values,
"Angular Velocity data in Z axis": VRCameraRoot[headers[15]].values,
"Angular Acceleration data in X axis": VRCameraRoot[headers[16]].values,
"Angular Acceleration data in Y axis": VRCameraRoot[headers[17]].values,
"Angular Acceleration data in Z axis": VRCameraRoot[headers[18]].values,
}

######################################################################################################################################################

################################################### Dash Section #####################################################################################
app = dash.Dash('Report: Motion Simulation Perception Analysis') # Declaring dash component

# Layout of how the page should look and do (Asthetics and functionalities on the page)
app.layout = html.Div([
# Title
    html.Div([
        html.H2('Report: Motion Simulation Perception Analysis',
                style={'float': 'left',
                       }),
        ]),
# Drop down menu
    dcc.Dropdown(id='plot-data-name',
                 options=[{'label': s, 'value': s}
                          for s in data_dict.keys()],
                 value=headers[1:19],
                 multi=True
                 ),
# Graphs plot
    html.Div(children=html.Div(id='graphs'), className='row'),
# Refresh rate for live graph    
    dcc.Interval(
        id='graph-update',
        interval=1000),
    ], className="container",style={'width':'98%','margin-left':10,'margin-right':10,'max-width':50000})


@app.callback(
    dash.dependencies.Output('graphs','children'),
    [dash.dependencies.Input('plot-data-name', 'value')],
  #  events=[dash.dependencies.Event('graph-update', 'interval')]
    )
def update_graph(data_names):
    graphs = []

    if len(data_names)>2:
        class_choice = 'col s12 m6 l4'
    elif len(data_names) == 2:
        class_choice = 'col s12 m6 l6'
    else:
        class_choice = 'col s12'


    for data_name in data_names:

        data = go.Scatter(
            x=list(data_dict["Timestamp"]),
            y=list(data_dict[data_name]),
            name='Scatter',
            fill="tozerox",
            fillcolor="#6897bb"
            )

        graphs.append(html.Div(dcc.Graph(
            id=data_name,
            animate=True,
            figure={'data': [data],'layout' : go.Layout(xaxis=dict(range=[min(data_dict["Timestamp"]),max(data_dict["Timestamp"])]),
                                                        yaxis=dict(range=[min(data_dict[data_name]),max(data_dict[data_name])]),
                                                        margin={'l':50,'r':1,'t':45,'b':1},
                                                        title='{}'.format(data_name))}
            ), className=class_choice))

    return graphs



external_css = ["https://cdnjs.cloudflare.com/ajax/libs/materialize/0.100.2/css/materialize.min.css"]
for css in external_css:
    app.css.append_css({"external_url": css})

external_js = ['https://cdnjs.cloudflare.com/ajax/libs/materialize/0.100.2/js/materialize.min.js']
for js in external_css:
    app.scripts.append_script({'external_url': js})


if __name__ == '__main__':
    app.run_server(debug=True)