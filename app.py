import pandas as pd
import numpy as np

import dash
import dash_core_components as dcc
import dash_html_components as html
import plotly.graph_objs as go

import matplotlib.pyplot as plt

import seaborn as sns
from plotly.offline import init_notebook_mode, iplot

from datetime import datetime
import warnings
import plotly.offline as py
py.init_notebook_mode(connected=True)
import plotly.tools as tls
import plotly.figure_factory as ff
from dash.dependencies import Input, Output

warnings.filterwarnings('ignore')

data = pd.read_csv('WA_Fn-UseC_-HR-Employee-Attrition.csv')
# Reassign target
data.Attrition.replace(to_replace = dict(Yes = 1, No = 0), inplace = True)
# Drop useless feat
data = data.drop(columns=['StandardHours', 
                          'EmployeeCount', 
                          'Over18',
                        ])

attrition = data[(data['Attrition'] != 0)]
no_attrition = data[(data['Attrition'] == 0)]

def getAttritionFigure():
    data = pd.read_csv('../WA_Fn-UseC_-HR-Employee-Attrition.csv')
    attrition = data[(data['Attrition'] != 'No')]
    no_attrition = data[(data['Attrition'] == 'No')]

    trace = go.Bar(x = (len(attrition), len(no_attrition)), y = ['Yes_attrition', 'No_attrition'], orientation = 'h', opacity = 0.8, marker=dict(
            color=['orangered', 'lightskyblue'],
            line=dict(color='#000000',width=1.5)))
    layout = dict(title =  'Count of attrition variable')
    fig1 = dict(data = [trace], layout=layout)
    trace = go.Pie(labels = ['No_attrition', 'Yes_attrition'], values = data['Attrition'].value_counts(), 
                   textfont=dict(size=15), opacity = 0.8,
                   marker=dict(colors=['lightskyblue','red'], 
                               line=dict(color='#000000', width=1.5)))

    layout = dict(title =  'Distribution of attrition variable')
    fig2 = dict(data = [trace], layout=layout)
    return fig1, fig2


def plot_distribution(var_select, bin_size) : 
# Calculate the correlation coefficient between the new variable and the target
    corr = data['Attrition'].corr(data[var_select])
    corr = np.round(corr,3)
    tmp1 = attrition[var_select]
    tmp2 = no_attrition[var_select]
    hist_data = [tmp1, tmp2]
    group_labels = ['Yes_attrition', 'No_attrition']
    colors = ['#FFD700', '#7EC0EE']
    fig = ff.create_distplot(hist_data, group_labels, colors = colors, show_hist = True, curve_type='kde', bin_size = bin_size)
    
    fig['layout'].update(title = var_select+' '+'(corr target ='+ str(corr)+')')
    return fig


def barplot(var_select, x_no_numeric) :
    tmp1 = data[(data['Attrition'] != 0)]
    tmp2 = data[(data['Attrition'] == 0)]
    tmp3 = pd.DataFrame(pd.crosstab(data[var_select],data['Attrition']), )
    tmp3['Attr%'] = tmp3[1] / (tmp3[1] + tmp3[0]) * 100
    if x_no_numeric == True  : 
        tmp3 = tmp3.sort_values(1, ascending = False)

    color=['lightskyblue','gold' ]
    trace1 = go.Bar(
        x=tmp1[var_select].value_counts().keys().tolist(),
        y=tmp1[var_select].value_counts().values.tolist(),
        name='Yes_Attrition',opacity = 0.8, marker=dict(
        color='gold',
        line=dict(color='#000000',width=1)))

    
    trace2 = go.Bar(
        x=tmp2[var_select].value_counts().keys().tolist(),
        y=tmp2[var_select].value_counts().values.tolist(),
        name='No_Attrition', opacity = 0.8, marker=dict(
        color='lightskyblue',
        line=dict(color='#000000',width=1)))
    
    trace3 =  go.Scatter(   
        x=tmp3.index,
        y=tmp3['Attr%'],
        yaxis = 'y2',
        name='% Attrition', opacity = 0.6, marker=dict(
        color='black',
        line=dict(color='#000000',width=0.5
        )))

    layout = dict(title =  str(var_select),
              xaxis=dict(), 
              yaxis=dict(title= 'Count'), 
              yaxis2=dict(range= [-0, 75], 
                          overlaying= 'y', 
                          anchor= 'x', 
                          side= 'right',
                          zeroline=False,
                          showgrid= False, 
                          title= '% Attrition'
                         ))

    fig = go.Figure(data=[trace1, trace2, trace3], layout=layout)
    fig2 = dict(data = [fig], layout=layout)
    return fig
    
    
# Initialise the app
app = dash.Dash(__name__)

def get_options(list_stocks):
    dict_list = []
    for i in list_stocks:
        dict_list.append({'label': i, 'value': i})

    return dict_list


app.layout = html.Div(
    children=[
        html.Div(className='row',
                 children=[
                    html.Div([
                                html.Div(
                                    [
                                        html.H6("""Select data feature""",
                                                style={'margin-right': '2em'})
                                    ],
                                ),

                                dcc.Dropdown(
                                    id='business_area_dropdown',
                                    options=[
                                        {'label': 'Attrition', 'value': 'Attrition'},
                                        {'label': 'Age', 'value': 'Age'},
                                        {'label': 'Distance from Home', 'value': 'DistanceFromHome'},
                                        {'label': 'Monthly Income', 'value': 'Monthly Income'},
                                        {'label': 'Number of Companies Worked', 'value': 'NumCompaniesWorked'},
                                        {'label': 'Percent Salary Hike', 'value': 'PercentSalaryHike'},
                                        {'label': 'Total Working Years', 'value': 'TotalWorkingYears'},
                                        {'label': 'Years at Company', 'value': 'YearsAtCompany'},
                                        {'label': 'Years since last promotion', 'value': 'YearsSinceLastPromotion'},
                                        {'label': 'Years with curr manager', 'value': 'YearsWithCurrManager'},
                                    ],
                                    placeholder="Select data feature",
                                    style=dict(
                                        width='40%',
                                        verticalAlign="middle"
                                    )
                                    )
                                ],
                                style=dict(display='flex')),
                                html.Div(className='eight columns div-for-charts bg-black',
                                     children=[
                                         dcc.Graph(id='graph', config={'displayModeBar': False}, animate=True),
                                         dcc.Graph(id='graph2', config={'displayModeBar': False}, animate=True)
                                     ])
                                      ])
        ]

)

@app.callback([Output('graph', 'figure'),
               Output('graph2', 'figure')],
              [Input('business_area_dropdown', 'value')])
def getFigure(selectedValue):
    if selectedValue == 'Attrition':
        fig1, fig2 = getAttritionFigure()
        return [fig1, fig2]
    
    elif selectedValue == 'Age':
        fig1 = plot_distribution('Age', False)
        fig2 = barplot('Age', False)
        return [fig1, fig2]
    
    elif selectedValue == 'DistanceFromHome':
        fig1 = plot_distribution('DistanceFromHome', False)
        fig2 = barplot('DistanceFromHome', False)
        return [fig1, fig2]
    
    elif selectedValue == 'MonthlyIncome':
        fig1 = plot_distribution('MonthlyIncome', 100)
        fig2 = plot_distribution('MonthlyRate', 100)
        return [fig1, fig2]
    
    elif selectedValue == 'NumCompaniesWorked':
        fig1 = plot_distribution('NumCompaniesWorked', False)
        fig2 = barplot('NumCompaniesWorked',False)
        return [fig1, fig2]
    
    elif selectedValue == 'PercentSalaryHike':
        fig1 = plot_distribution('PercentSalaryHike', False)
        fig2 = barplot('PercentSalaryHike', False)
        return [fig1, fig2]
    
    elif selectedValue == 'TotalWorkingYears':
        fig1 = plot_distribution('TotalWorkingYears', False)
        fig2 = barplot('TotalWorkingYears', False)
        return [fig1, fig2]
    
    elif selectedValue == 'YearsAtCompany':
        fig1 = plot_distribution('YearsAtCompany', False)
        fig2 = barplot('YearsAtCompany', False)
        return [fig1, fig2]
    
    elif selectedValue == 'YearsSinceLastPromotion':
        fig1 = plot_distribution('YearsSinceLastPromotion', False)
        fig2 = barplot('YearsSinceLastPromotion', False)
        return [fig1, fig2]
    
    elif selectedValue == 'YearsWithCurrManager':
        fig1 = plot_distribution('YearsWithCurrManager', False)
        fig2 = barplot('YearsWithCurrManager', False)
        return [fig1, fig2]
    
    else:
        fig1, fig2 = getAttritionFigure()
        return [fig1, fig2]
    
        

# Run the app
if __name__ == '__main__':
    app.run_server(debug=True)