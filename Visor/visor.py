import dash
from dash import Dash, dcc, html, Input, Output, callback, dash_table, State
import pandas as pd
import ipc


app = Dash(__name__, suppress_callback_exceptions=True)


#ciudades
ciudades = ipc.get_ciudades()
features = ['PRECTOTCORR', 'T2M', 'T2M_MAX', 'T2M_MIN', 'RH2M', 'WS10M']
target = 'IPC_mensual'

app.layout = html.Div([

    dcc.Store(id='df-ciudades-store'),
    dcc.Store(id='portafolio-seleccionado-store'),

    #---------- Header Visor ----------#
    html.Div([
        html.Img(src='https://www.javeriana.edu.co/recursosdb/8091523/8157776/javeriana-web-logo-edu.png/d5eb5e3d-2e95-0d4f-877d-0ed67a254251?t=1676557813805', style={'height': '150px', 'float': 'left'}),
        html.H2('Pontificia Universidad Javeriana - Aprendizaje de Máquina', style={'color': 'black', 'clear': 'left'}),
    ], style={'padding': '5px 10px', 'backgroundColor': 'white', 'color': 'black'}),
    #------------------------------------#

    html.Div([
        html.Div([
            # Contenido de selección
            html.Div([
                # Cuadrado de selección
                html.Div([
                    # Contenido del cuadrado de selección
                    html.Div([
                        # Encabezado de selección
                        html.Div([
                            html.H3('Selección de Ciudades', style={'color': 'white'}),
                        ], style={'padding': '10px', 'backgroundColor': '#1E1E1E', 'color': 'white', 'border-radius': '10px 10px 0 0'}),
                        # Contenido principal de selección
                        html.Div([
                            # Dropdown de selección
                            html.Label('Ciudad:', style={'font-weight': 'bold'}),
                            dcc.Dropdown(
                                id='ciudades-dropdown',
                                options=[{'label': i, 'value': i} for i in ciudades],
                                style={'width': '100%', 'margin-bottom': '15px', 'padding': '5px', 'border-radius': '5px'}
                            ),
                        ], style={'padding': '20px', 'backgroundColor': 'white', 'color': 'black', 'border': '2px solid #1E1E1E', 'border-radius': '0 0 10px 10px', 'box-shadow': '0px 4px 8px rgba(0, 0, 0, 0.1)'}),
                    ], style={'padding': '10px', 'display': 'inline'}),
                ], style={'padding': '10px', 'display': 'inline'}),
            ], style={'padding': '10px', 'display': 'inline'}),

            # Botón Ver
            html.Div([
                html.Button('Ver', id='ver-button', style={
                    'background-color': '#007bff',  # Color azul mejorado
                    'color': 'white',
                    'margin': '10px',
                    'border-radius': '10px',  # Mayor redondez al botón
                    'font-weight': 'bold',  # Hace que el texto sea negrita
                    'border': 'none',  # Quita los bordes
                    'box-shadow': '0px 8px 15px rgba(0, 0, 0, 0.2)',  # Agrega una sombra más pronunciada
                    'cursor': 'pointer',
                    'font-size': '18px',  # Tamaño de fuente más grande
                    'padding': '15px 30px',  # Mayor tamaño del botón
                    'transition': 'background-color 0.3s ease',  # Transición suave para el cambio de color
                }),
            ], style={'display': 'flex', 'justify-content': 'center', 'margin-top': '20px'}),

        ], style={'margin': '20px'}),

        
        #---------- Selección de Características ----------#
        html.Div([
            html.Div([
                html.H3('Características', style={'color': 'white','text-align': 'center'}),
            ], style={'padding': '10px', 'backgroundColor': '#1E1E1E', 'color': 'white', 'border-radius': '10px 10px 0 0'}),
            
            html.Div([
    html.Label('Precipitación'),
    dcc.Checklist(
    id='features-checklist-PRECTOTCORR',
    options=[{'label': 'PRECTOTCORR', 'value': 'PRECTOTCORR'}],
    value=['PRECTOTCORR'],
    style={'margin-bottom': '15px', 'padding': '5px'}
    ),
    html.Label('Temperatura Media'),
    dcc.Checklist(
    id='features-checklist-T2M',
    options=[{'label': 'T2M', 'value': 'T2M'}],
    value=['T2M'],
    style={'margin-bottom': '15px', 'padding': '5px'}
    ),
    html.Label('Temperatura Máxima'),
    dcc.Checklist(
    id='features-checklist-T2M_MAX',
    options=[{'label': 'T2M_MAX', 'value': 'T2M_MAX'}],
    value=['T2M_MAX'],
    style={'margin-bottom': '15px', 'padding': '5px'}
    ),
    html.Label('Temperatura Mínima'),
    dcc.Checklist(
    id='features-checklist-T2M_MIN',
    options=[{'label': 'T2M_MIN', 'value': 'T2M_MIN'}],
    value=['T2M_MIN'],
    style={'margin-bottom': '15px', 'padding': '5px'}
    ),
    html.Label('Presión'),
    dcc.Checklist(
    id='features-checklist-RH2M',
    options=[{'label': 'RH2M', 'value': 'RH2M'}],
    value=['RH2M'],
    style={'margin-bottom': '15px', 'padding': '5px'}
    ),
    html.Label('Velocidad del Viento'),
        dcc.Checklist(
            id='features-checklist-WS10M',
            options=[{'label': 'WS10M', 'value': 'WS10M'}],
            value=['WS10M'],
            style={'margin-bottom': '15px', 'padding': '5px'}
        )
], style={'padding': '20px', 'backgroundColor': 'white', 'color': 'black', 'border': '2px solid #1E1E1E', 'border-radius': '0 0 10px 10px', 'box-shadow': '0px 4px 8px rgba(0, 0, 0, 0.1)'})], style={'width': '300px', 'margin': 'auto', 'margin-top': '20px', 'box-shadow': '0px 4px 8px rgba(0, 0, 0, 0.1)', 'border-radius': '10px'}),


        #------------- Selección de Métricas -------------#
        html.Div([
            html.Div([
                html.H3('Selección de Métricas Random Forest', style={'color': 'white', 'text-align': 'center'}),
            ], style={'padding': '10px', 'backgroundColor': '#1E1E1E', 'color': 'white', 'border-radius': '10px 10px 0 0'}),
            
            html.Div([
                html.Label('Criterion:', style={'font-weight': 'bold'}),
                dcc.Input(id='criterion-input', type='text', placeholder='gini, entropy', style={'margin-bottom': '15px', 'padding': '5px', 'border-radius': '5px', 'width': '100%'}),

                html.Label('Número de Estimadores:', style={'font-weight': 'bold'}),
                dcc.Input(id='n_estimators-input', type='number', placeholder='100, 200, 300', style={'margin-bottom': '15px', 'padding': '5px', 'border-radius': '5px', 'width': '100%'}),

                html.Label('Profundidad Máxima:', style={'font-weight': 'bold'}),
                dcc.Input(id='max_depth-input', type='number', placeholder='None, 5, 10', style={'margin-bottom': '15px', 'padding': '5px', 'border-radius': '5px', 'width': '100%'}),

                html.Label('Muestras Máximas:', style={'font-weight': 'bold'}),
                dcc.Input(id='max_samples-input', type='text', placeholder='None, 0.5, 0.8', style={'margin-bottom': '15px', 'padding': '5px', 'border-radius': '5px', 'width': '100%'}),

                html.Label('División Mínima de Muestras:', style={'font-weight': 'bold'}),
                dcc.Input(id='min_samples_split-input', type='number', placeholder='2, 5, 10', style={'margin-bottom': '15px', 'padding': '5px', 'border-radius': '5px', 'width': '100%'}),

                dcc.Checklist(
                    id='mejor-modelo-checklist',
                    options=[{'label': 'Seleccionar el Mejor Modelo', 'value': 'mejor-modelo'}],
                    style={'margin-bottom': '15px'}
                ),
            ], style={'padding': '20px', 'backgroundColor': 'white', 'color': 'black', 'border': '2px solid #1E1E1E', 'border-radius': '0 0 10px 10px', 'box-shadow': '0px 4px 8px rgba(0, 0, 0, 0.1)'}),
        
        ], style={'width': '300px', 'margin': 'auto', 'margin-top': '20px', 'box-shadow': '0px 4px 8px rgba(0, 0, 0, 0.1)', 'border-radius': '10px'}),
    
    ], style={'display': 'flex', 'flex-wrap': 'wrap', 'gap': '20px', 'backgroundColor': 'white', 'padding': '20px', 'border-radius': '10px', 'box-shadow': '0px 4px 8px rgba(0, 0, 0, 0.1)'}),

    #---------- Contenido Graficas ----------#
    html.Div([
        html.Div([html.H3('Comportamiento de los Datos', style={'color': 'white', 'display': 'block'})], style={'padding': '3px 10px', 'backgroundColor': 'black', 'color': 'white'}),
        html.Div([
            html.Div(id='output-container-graph_serie', style={'padding': '10px'}),
        ], style={'display': 'flex', 'flex-wrap': 'wrap', 'justify-content': 'center', 'align-items': 'center'}),
    ], id='serie-div', style={'display': 'none', 'justify-content': 'center', 'align-items': 'center'}),
    #------------------------------------#

    #---------- Contenido random forest ----------#
    html.Div([
        html.Div([html.H3('Predicción con Random Forest', style={'color': 'white', 'display': 'block'})], style={'padding': '3px 10px', 'backgroundColor': 'black', 'color': 'white'}),
        html.Div([
            html.Div(id='output-container-random-forest', style={'padding': '10px'}),
        ], style={'display': 'flex', 'flex-wrap': 'wrap', 'justify-content': 'center', 'align-items': 'center'}),
    ], id='random-forest-div', style={'display': 'none'})
    #------------------------------------#

], style={'display': 'inline', 'backgroundColor': 'white'})

'''-------------------------------Callbacks ------------------------------- '''
# Actualizar el ciudad seleccionada
@app.callback(
    Output('df-ciudades-store', 'data'),
    Output('output-container-graph_serie', 'children'),
    Output('serie-div', 'style'),
    Input('ciudades-dropdown', 'value'),
    Input('ver-button', 'n_clicks'),
    State('features-checklist-PRECTOTCORR', 'value'),
    State('features-checklist-T2M', 'value'),
    State('features-checklist-T2M_MAX', 'value'),
    State('features-checklist-T2M_MIN', 'value'),
    State('features-checklist-RH2M', 'value'),
    State('features-checklist-WS10M', 'value'),
    prevent_initial_call=True,
)
def update_ciudad(value, n_clicks, PRECTOTCORR, T2M, T2M_MAX, T2M_MIN, RH2M, WS10M):
    ciudad_seleccionada = value
    
    # unir los valores PRECTOTCORR, T2M, T2M_MAX, T2M_MIN, RH2M, WS10M en una lista
    selected_features = []
    if PRECTOTCORR is not None and PRECTOTCORR != []:
        selected_features.extend(PRECTOTCORR)
    if T2M is not None and T2M != []:
        selected_features.extend(T2M)
    if T2M_MAX is not None and T2M_MAX != []:
        selected_features.extend(T2M_MAX)
    if T2M_MIN is not None and T2M_MIN != []:
        selected_features.extend(T2M_MIN)
    if RH2M is not None and RH2M != []:
        selected_features.extend(RH2M)
    if WS10M is not None and WS10M != []:
        selected_features.extend(WS10M)

    # en la lista features_selected insertar como primer valor la variable objetivo
    selected_features.insert(0, target)
    df_datos_ciudad = ipc.get_datos_ciudad(ciudad_seleccionada)
    df_datos_ciudad = df_datos_ciudad[selected_features]

    # Generar los gráficos utilizando las funciones de la librería
    fig_boxplot = ipc.plot_boxplot(df_datos_ciudad, ciudad_seleccionada)
    fig_heatmap = ipc.plot_heatmap(df_datos_ciudad, ciudad_seleccionada)
    fig_histogram = ipc.plot_histogram(df_datos_ciudad, ciudad_seleccionada)
    fig_ipc = ipc.plot_IPC(df_datos_ciudad, ciudad_seleccionada)

    # Actualizar el almacenamiento de datos
    if n_clicks is not None:
        return df_datos_ciudad.to_dict('records'), [
            dcc.Graph(figure=fig_ipc),
            dcc.Graph(figure=fig_boxplot),
            dcc.Graph(figure=fig_histogram),
            dcc.Graph(figure=fig_heatmap),
        ], {'display': 'block', 'justify-content': 'center', 'align-items': 'center'}
    else:
        return df_datos_ciudad.to_dict('records'), [], {'display': 'none', 'justify-content': 'center', 'align-items': 'center'}


@app.callback(
    Output('output-container-random-forest', 'children'),
    Output('random-forest-div', 'style'),
    Input('ver-button', 'n_clicks'),
    State('df-ciudades-store', 'data'),
    State('criterion-input', 'value'),
    State('n_estimators-input', 'value'),
    State('max_depth-input', 'value'),
    State('max_samples-input', 'value'),
    State('min_samples_split-input', 'value'),
    State('mejor-modelo-checklist', 'value'),
    State('features-checklist-PRECTOTCORR', 'value'),
    State('features-checklist-T2M', 'value'),
    State('features-checklist-T2M_MAX', 'value'),
    State('features-checklist-T2M_MIN', 'value'),
    State('features-checklist-RH2M', 'value'),
    State('features-checklist-WS10M', 'value'),
    prevent_initial_call=True,
)
def update_random_forest(n_clicks, data, criterion, n_estimators, max_depth, max_samples, min_samples_split, mejor_modelo, PRECTOTCORR, T2M, T2M_MAX, T2M_MIN, RH2M, WS10M):
    if n_clicks is not None:
        df = pd.DataFrame(data)

        # unir los valores PRECTOTCORR, T2M, T2M_MAX, T2M_MIN, RH2M, WS10M en una lista
        selected_features = []
        if PRECTOTCORR is not None and PRECTOTCORR != []:
            selected_features.extend(PRECTOTCORR)
        if T2M is not None and T2M != []:
            selected_features.extend(T2M)
        if T2M_MAX is not None and T2M_MAX != []:
            selected_features.extend(T2M_MAX)
        if T2M_MIN is not None and T2M_MIN != []:
            selected_features.extend(T2M_MIN)
        if RH2M is not None and RH2M != []:
            selected_features.extend(RH2M)
        if WS10M is not None and WS10M != []:
            selected_features.extend(WS10M)

        if mejor_modelo == ['mejor-modelo']:
            report_df, y_test, y_test_pred, best_model, X_train = ipc.best_random_forest_model(df, selected_features, target)
        else:
            criterion = criterion or 'gini'
            n_estimators = int(n_estimators) if n_estimators else 100
            max_depth = int(max_depth) if max_depth else None
            max_samples = float(max_samples) if max_samples else None
            min_samples_split = int(min_samples_split) if min_samples_split else 2
            
            report_df, y_test, y_test_pred, best_model, X_train = ipc.random_forest_model(df, selected_features, target, criterion, n_estimators, max_depth, max_samples, min_samples_split)

            print(report_df)
        fig_confusion_matrix = ipc.plot_confusion_matrix(y_test, y_test_pred)
        fig_feature_importances = ipc.plot_feature_importances(best_model, X_train)
        
        return [
            dcc.Graph(figure=fig_confusion_matrix),
            dcc.Graph(figure=fig_feature_importances),
           
            html.Div([
                html.Div([
                    html.Div([
                        html.H4('Reporte de Clasificación', style={'color': 'white', 'margin': '0'})
                    ], style={'padding': '10px', 'backgroundColor': '#1E1E1E', 'color': 'white', 'border-radius': '10px 10px 0 0'}),
                    html.Div([
                        dash_table.DataTable(
                            data=report_df.reset_index().to_dict('records'),
                            columns=[{'name': i, 'id': i} for i in ['index'] + list(report_df.columns)],
                            style_table={'width': '100%', 'border-collapse': 'collapse'},
                            style_cell={
                                'textAlign': 'left',
                                'padding': '8px',
                                'border': '1px solid #ddd'
                            },
                            style_header={
                                'backgroundColor': '#f2f2f2',
                                'fontWeight': 'bold',
                                'border': '1px solid #ddd'
                            },
                            style_data_conditional=[
                                {
                                    'if': {'row_index': 'odd'},
                                    'backgroundColor': '#f9f9f9'
                                }
                            ]
                        )
                    ], style={'padding': '20px', 'backgroundColor': 'white', 'color': 'black', 'border': '2px solid #1E1E1E', 'border-radius': '0 0 10px 10px', 'box-shadow': '0px 4px 8px rgba(0, 0, 0, 0.1)'})
                ], style={'margin-top': '20px'})
            ])
            
            ], {'display': 'block'}
    else:
        return [], {'display': 'none'}


if __name__ == '__main__':
    app.run_server(debug=True, port=8050)