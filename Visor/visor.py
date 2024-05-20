import dash
from dash import Dash, dcc, html, Input, Output, callback, dash_table, State
from dash.exceptions import PreventUpdate
import pandas as pd
import ipc


app = Dash(__name__, suppress_callback_exceptions=True)


#ciudades
ciudades = ipc.get_ciudades()


app.layout = html.Div([
    dcc.Store(id='df-ciudades-store'),
    dcc.Store(id='portafolio-seleccionado-store'),

    #---------- Header Visor ----------#
    html.Div([
        html.Img(src='https://www.javeriana.edu.co/recursosdb/8091523/8157776/javeriana-web-logo-edu.png/d5eb5e3d-2e95-0d4f-877d-0ed67a254251?t=1676557813805', style={'height':'150px', 'float':'left'}),
        html.H4('Pontificia Universidad Javeriana - Analítica de Datos', style={'color': 'black', 'clear':'left'}),
    ], style={'padding': '5px 10px', 'backgroundColor': 'white', 'color': 'black'}),
    #------------------------------------#

    #---------- Contenido Selección ----------#
    html.Div([

        html.Div([  
            #---------- Cuadrado Seleccion ----------#
            ### contenido Selección ###
            html.Div([ 
                 ### header Selección ###
                html.Div([ 
                    html.H3('Selección de Ciudades', style={'color': 'white'}),
                ], style={'padding': '5px 10px', 'backgroundColor': 'black', 'color': 'white'}),
                #######################
                html.Div([
                    ### dropdown Selección ###
                    html.Label('Ciudad:'),
                    dcc.Dropdown(
                        id='ciudades-dropdown',
                        options=[{'label': i, 'value': i} for i in ciudades],
                        style={'width': '300px','margin-bottom': '10px'},  
                    ),

                    

                    ########### Botones ###########
                    html.Div([
                        ### Botón Ver ###
                        html.Button('Ver', id='ver-button', style={
                            'background-color': 'blue',
                            'color': 'white', 
                            'margin': '10px',
                            'border-radius': '5px',  # Agrega redondez al botón
                            'font-weight': 'bold',  # Hace que el texto sea negrita
                            'border': 'none',  # Quita los bordes
                            'box-shadow': '0px 8px 15px rgba(0, 0, 0, 0.1)',  # Agrega sombra
                            'cursor': 'pointer'
                        }),
                    
                    ], style={'display': 'flex'})
                ], style={'padding': '10px', 'backgroundColor': 'white', 'color': 'black', 'border': '1px solid ' + 'black'}),      
            ], style={'padding': '10px','display': 'inline'}),
                
        ], style={'padding': '10px','display': 'inline'}),
    ], style={'display': 'flex', 'padding':'10px','justify-content': 'flex-start', 'align-items': 'flex-start', 'backgroundColor': 'white'}),

    #        #------------- Portafolio Seleccionado -------------#
    #         html.Div([
    #             html.Div([
    #                 html.Div([     
    #                     html.Div([ 
    #                             html.H3('Portafolio Seleccionado',id='port-selection-header', style={'color': 'white', 'display': 'block'}),
    #                         ], style={'padding': '3px 10px', 'backgroundColor': 'black', 'color': 'white'}),

    #                     html.Div(id='output-select', style={'padding': '0px 0px 20px 1px'}),

    #                 ], id='parent-div-select',style={'display': 'none', 'padding': '5px','justify-content': 'flex-start', 'align-items': 'flex-start', 'backgroundColor': 'white'}),

    #                 #------------- Restricciones Portafolio Seleccionado -------------#
    #                 html.Div([     
    #                     html.Div([ 
    #                             html.H3('Restricciones del Portafolio',id='port-const-header', style={'color': 'white', 'display': 'block'}),
    #                         ], style={'padding': '3px 10px', 'backgroundColor': 'black', 'color': 'white'}),

    #                     html.Div(id='output-constraints', style={'padding': '0px 0px 20px 1px'}),

    #                 ], id='parent-div-cons',style={'display': 'none', 'padding': '5px','justify-content': 'flex-start', 'align-items': 'flex-start', 'backgroundColor': 'white'}),
    #             ], style={'display': 'flex'}),
    #             #---------------------------------------------------#
    #             # Text below the two Divs
    #             html.P("*Volver a Optimizar cuando se actualicen los valores", 
    #                     id='informacion_opt',
    #                     style={'display': 'none',
    #                             'padding': '10px 0', 
    #                             'font-weight': 'bold', 
    #                             'color': 'black'}),
    #         ],style={'display': 'inline-block'}),
    # ], style={'display': 'flex', 'padding':'10px','justify-content': 'flex-start', 'align-items': 'flex-start', 'backgroundColor': 'white'}),

    #---------- Contenido Graficas ----------#
    html.Div([
        html.Div([html.H3('Comportamiento de los Datos',style={'color': 'white','display': 'block'}), ], style={'padding': '3px 10px', 'backgroundColor': 'black', 'color': 'white'}),
        html.Div([
            html.Div(id='output-container-graph_serie', style={'padding': '10px'}),
        ], style={'display': 'flex', 'flex-wrap': 'wrap', 'justify-content': 'center', 'align-items': 'center'}),
    ], id='serie-div'),
    #------------------------------------#

    #---------- Contenido random forest ----------#
    html.Div([
        html.Div([html.H3('Predicción con Random Forest', style={'color': 'white', 'display': 'block'})],
                style={'padding': '3px 10px', 'backgroundColor': 'black', 'color': 'white'}),
        html.Div([
            html.Div(id='output-container-random-forest', style={'padding': '10px'}),
        ], style={'display': 'flex', 'flex-wrap': 'wrap', 'justify-content': 'center', 'align-items': 'center'}),
    ], id='random-forest-div', style={'display': 'none'})


    # #---------- Contenido Optimización ----------#
    # html.Div([
    #     html.Div([html.H3('Optimización',style={'color': 'white','display': 'block'}),
    #             ], style={'padding': '3px 10px', 'backgroundColor': 'black', 'color': 'white'}),
    #     html.Div([
    #         html.Div(id='output-container-opt-u', style={'padding': '1px 10px 20px 1px'}), 
    #         html.Div(id='output-container-met-ut', style={'padding': '1px 10px 20px 1px'}), 
    #     ], style={'display': 'flex','justify-content': 'center', 'align-items': 'center'}),
    #     html.Button('Exportar', id='export-button', style={
    #                 'display': 'block', 
    #                 'background-color': colores_corporativos['yellow'],
    #                 'color': 'black', 
    #                 'margin': '10px',
    #                 'border-radius': '5px',  
    #                 'font-weight': 'bold',  
    #                 'border': 'none',  
    #                 'box-shadow': '0px 8px 15px rgba(0, 0, 0, 0.1)',  
    #                 'cursor': 'pointer'
    #             }),
    #     # Text below the two Divs
    #             html.P("Exportado en Excel correctamente", 
    #                     id='export_opt',
    #                     style={'display': 'none',
    #                             'padding': '10px', 
    #                             'font-style': 'italic',  
    #                             'color': colores_corporativos['green1']}),
    # ], id='optimization-div', style={'display': 'none', 'justify-content': 'center', 'align-items': 'center'}),
    # #------------------------------------#

    # #---------- Contenido Gráficas ----------#
    # html.Div([
    #     ## titulo de las graficas ##
    #     html.Div([html.H3('Gráficas',style={'color': 'white','display': 'block'}),
    #             ], style={'padding': '3px 10px', 'backgroundColor': 'black', 'color': 'white'}),     
    #     ## Allocation ##
    #     html.Div([
    #         html.Div(id='output-container-graph_allocation', style={'padding': '10px'}),
    #     ], style={'display': 'flex','justify-content': 'center', 'align-items': 'center'}),
    #     ## Frontera eficiente ##
    #     html.Div([
    #         html.Div(id='output-container-graph_ef', style={'padding': '10px'}),
    #     ], style={'display': 'flex','justify-content': 'center', 'align-items': 'center'}),
    #     ## Retornos historicos ##
    #     html.Div([
    #         html.Div(id='output-container-graph_returns', style={'padding': '10px'}),
    #     ], style={'display': 'flex','justify-content': 'center', 'align-items': 'center'}),
    # ], id='graphs-div', style={'display': 'none', 'justify-content': 'center', 'align-items': 'center'}),
    #------------------------------------#
], style={'display': 'inline','backgroundColor': 'white'})


'''-------------------------------Callbacks ------------------------------- '''

# Actualizar el ciudad seleccionada
# @app.callback(
#     Output('df-ciudades-store', 'data'),
#     Input('ciudades-dropdown', 'value'),
#     prevent_initial_call=True,
# )
# def update_ciudad(value):  
#     ciudad_seleccionada = value
#     print(ciudad_seleccionada)
    
#     df_datos_ciudad = ipc.get_datos_ciudad(ciudad_seleccionada)
#     print(df_datos_ciudad)

#     # Actualizar el almacenamiento de datos
#     return df_datos_ciudad.to_dict('records')


@app.callback(
    Output('df-ciudades-store', 'data'),
    Output('output-container-graph_serie', 'children'),
    Output('serie-div', 'style'),
    Input('ciudades-dropdown', 'value'),
    Input('ver-button', 'n_clicks'),
    prevent_initial_call=True,
)
def update_ciudad(value, n_clicks):
    ciudad_seleccionada = value
    #print(ciudad_seleccionada)
    df_datos_ciudad = ipc.get_datos_ciudad(ciudad_seleccionada)
    #print(df_datos_ciudad)

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
            dcc.Graph(figure=fig_heatmap),
            dcc.Graph(figure=fig_histogram),
        ], {'display': 'block', 'justify-content': 'center', 'align-items': 'center'}
    else:
        return df_datos_ciudad.to_dict('records'), [], {'display': 'none', 'justify-content': 'center', 'align-items': 'center'}


@app.callback(
    Output('output-container-random-forest', 'children'),
    Output('random-forest-div', 'style'),
    Input('ver-button', 'n_clicks'),
    State('df-ciudades-store', 'data'),
    prevent_initial_call=True,
)
def update_random_forest(n_clicks, data):
    if n_clicks is not None:
        df = pd.DataFrame(data)
        report_df, y_test, y_test_pred, best_model, X_train = ipc.random_forest_model(df)
        fig_confusion_matrix = ipc.plot_confusion_matrix(y_test, y_test_pred)
        fig_feature_importances = ipc.plot_feature_importances(best_model, X_train)
        
        return [
            dcc.Graph(figure=fig_confusion_matrix),
            dcc.Graph(figure=fig_feature_importances),
            html.Div([
                html.H4('Classification Report'),
                dash_table.DataTable(
                    data=report_df.to_dict('records'),
                    columns=[{'name': i, 'id': i} for i in report_df.columns],
                )
            ])
        ], {'display': 'block'}
    else:
        return [], {'display': 'none'}

# # Generar optimización
# @app.callback( [Output('output-container-opt-u', 'children'), 
#                 Output('output-container-met-ut', 'children')], 
#                 [Input('ver-button', 'n_clicks'), 
#                  Input('optimizacion-dropdown', 'value')],
#                 State('port-opt-3col', 'data'), 
#                 State('my-table-constraints', 'data'), 
#                 State('df-ciudades-store', 'data'), 
#                 prevent_initial_call=True) 
# def update_optimization(n_clicks, value_opt, data, data_cons, df_portafolios_seleccion_data): 
#     #archivo retornos consolidados
#     df_retornos_consolidados = leer_archivo_optimizacion(ruta_opt + 'RETORNOS SAA/ENCUESTA_RETORNO_BAYESIANO.xlsm', 'RETORNOS CONSOLIDADOS')

#     df_seleccion = pd.DataFrame(data)

#     df_portafolios_seleccion = pd.DataFrame(df_portafolios_seleccion_data)

#     # convierte los valores de las ultimas 3 columnas a numerico de df_seleccion
#     df_seleccion.iloc[:, -3:] = df_seleccion.iloc[:, -3:].apply(pd.to_numeric, errors='coerce')

#     # variable para renta fija 
#     is_RFL = False
#     #Verificar el tipo de portafolio y guardar en una variable si es RFL para desagregar los R
#     if(df_portafolios_seleccion['Type_Portfolio'].unique()[0] == 'RENTA FIJA LOCAL'):
#         is_RFL = True

#     # los valores en los indices
#     indices_opt = df_portafolios_seleccion.index.to_list()
#     #display(indices_opt)
#     # Se filtra el Datafreme de retonos solo para los indices que se van a optimizar
#     df_ret_opt = df_ret_diarios_aj[indices_opt]

#     #verificar si el portafolio tiene cobertura
#     df_cons_IND_USDCOP = None
#     if asset_management.check_hedge(df_portafolios_seleccion):
#         df_cons_IND_USDCOP = df_retornos_consolidados[df_retornos_consolidados['ID AM MONEDA LOCAL'] == 'IND_MON_USDCOP_USD_001']
#         df_cons_IND_USDCOP = df_cons_IND_USDCOP.set_index('ID AM MONEDA LOCAL').reset_index()   

#     # Limites de los activos
#     limites_li_ls = df_seleccion[['Inferior','Superior']]/100
#     limites_li_ls = list(limites_li_ls.itertuples(index=False,name=None))
#     #display(limites_li_ls)

#     # Pesos del Benchmark
#     #w_bench = df_seleccion['Benchmark']/100

#     # Se filtra el Datafreme de retornos consolidados solo para los indices que se van a optimizar
#     df_retornos_consolidados = df_retornos_consolidados[df_retornos_consolidados['ID AM MONEDA LOCAL'].isin(indices_opt)]
#     df_retornos_consolidados = df_retornos_consolidados.set_index('ID AM MONEDA LOCAL').loc[indices_opt].reset_index()

#     """ Metricas para la optimización """
#     # Retornos esperados
#     retorno_esperado = df_retornos_consolidados['RETORNO BAYESIANO MONEDA LOCAL']
#     retorno_esperado.index = df_retornos_consolidados['ID AM MONEDA LOCAL']

#     # Volatilidad
#     escala_diaria = 252
#     # if value_vol == 'Hist':
#     vector_volatilidad = df_ret_opt.std()*np.sqrt(escala_diaria)
#     # elif value_vol == 'EWMA':
#     #     window = '9M'
#     #     escala_9m = 9/12
#     #     retornos_9m = transform_benchmark_al_dia(df_vu_bench[indices_opt], window = window)
#     #     decay_factor = 0.94
#     #     df_vol_ewma = asset_management.calculate_ewma_vol(returns=retornos_9m, decay_factor=decay_factor, escala_anual=escala_9m)


#     # Si hay cobertura se agregan los valores de retorno, volatilidad y duracion del indice de cobertura
#     if df_cons_IND_USDCOP is not None:
#         df_ret_IND_USDCOP = df_ret_diarios_aj['IND_MON_USDCOP_USD_001']
#         volatilidad_IND_USDCOP = df_ret_IND_USDCOP.std()*np.sqrt(52)
#         df_cons_IND_USDCOP['VOLATILIDAD'] = volatilidad_IND_USDCOP  

#     # Duracion
#     vector_duracion = df_retornos_consolidados['DURACION']
#     vector_duracion.index = df_retornos_consolidados['ID AM MONEDA LOCAL']

#     # Fechas
#     fechas = df_retornos_consolidados[['FECHA','FECHA_PRONOSTICO']]
#     fechas.index = df_retornos_consolidados['ID AM MONEDA LOCAL']

#     # Matriz de varianza-covarianza redondeado a 3 decimales
#     matriz_varcov = df_ret_opt.cov()*escala_diaria
    

#     """ Resticciones para la optimización """
#     # df_restricciones = leer_archivo_optimizacion(ruta_opt + '/OPTIMIZACIONES/INDICES_OPT.xlsx', 'Restricciones') 
#     # df_restricciones = df_restricciones.loc[df_restricciones['Ticket_Portfolio'] == ciudad_seleccionada]
#     df_restricciones = pd.DataFrame(data_cons)

#     # convierte los valores de todas las columnas a numerico
#     df_restricciones = df_restricciones.apply(pd.to_numeric, errors='coerce')
#     #print('######################################################')
#     #display(df_restricciones)

#     # Número de activos
#     num_assets = len(indices_opt)

#     # Pesos iniciales
#     w_ini = np.ones(num_assets)/np.sum(np.ones(num_assets))

#     # Maximo Tracking Error
#     maximo_te = df_restricciones['max_traking_error'].values[0]/100

#     #Minima duracion
#     min_dur = df_restricciones['Duracion_Inferior'].values[0]

#     #Maxima duracion
#     max_dur = df_restricciones['Duracion_Superior'].values[0]

#     # Coeficiente de averción al riesgo
#     coef_avr = df_restricciones['Aversion'].values[0]

#     #cobertura maxima en USD
#     cob_usd = asset_management.check_hedge(df_portafolios_seleccion)
#     #print(cob_usd)

#     restricciones = [{'type': 'eq', 'fun': lambda x: np.sum(x)-1},                                                                                                             # Suma de las pesos debe ser 1
#                      {'type': 'ineq', 'fun': lambda x: maximo_te - asset_management.tracking_error(x, df_portafolios_seleccion['Benchmark'], matriz_varcov)},                   # Limite de TE
#                     #{'type': 'ineq', 'fun': lambda x: asset_management.port_return(df_portafolios_seleccion['Values'], retorno_esperado) - asset_management.port_return(x,retorno_esperado)},     # retorno opt > retono benchmark                                                            
#                     ]

#     #Si hay cobertura se agregan restricciones adicionales
#     if cob_usd > 0:             
#         restricciones.append({'type': 'ineq', 'fun': lambda x: cob_usd - np.sum(x[np.where(retorno_esperado.index.str.contains('COBCOP'))[0]])})                               # Limite de cobertura en USD

#     #verificar si el portafolio es de Renta Fija para agregar restricciones adicionales
#     if is_RFL:
#         restricciones.append({'type': 'ineq', 'fun': lambda x: max_dur - asset_management.duration_func(x, vector_duracion)})                                                  # Limite de duracion
#         restricciones.append({'type': 'ineq', 'fun': lambda x: asset_management.duration_func(x, vector_duracion) - min_dur })                                                 # Limite de duracion    """ Optimización del portafolio """

#     """ Optimización del portafolio """
#     if value_opt == 'Information Ratio':
#         w_opt = asset_management.max_ir(w_ini, df_seleccion['Benchmark']/100, retorno_esperado, matriz_varcov, restricciones, limites_li_ls)
#     elif value_opt == 'Sharpe Ratio':
#         w_opt = asset_management.max_sharpe(w_ini, retorno_esperado, matriz_varcov, restricciones, limites_li_ls)
#     else:
#         w_opt = asset_management.max_mu(w_ini, retorno_esperado, matriz_varcov, coef_avr, restricciones, limites_li_ls)

    
#     #Si hay cobertura se agregan los valores de retorno, volatilidad y duracion del indice de cobertura
#     if cob_usd > 0:
#             retorno_ma = retorno_esperado.copy()
#             retorno_ma[df_cons_IND_USDCOP['ID AM MONEDA LOCAL'].values[0]] = df_cons_IND_USDCOP['RETORNO BAYESIANO MONEDA LOCAL'].values[0]
#             volatilidad_ma = vector_volatilidad.copy()
#             volatilidad_ma[df_cons_IND_USDCOP['ID AM MONEDA LOCAL'].values[0]] = df_cons_IND_USDCOP['VOLATILIDAD'].values[0]
#             duracion_ma = vector_duracion.copy()
#             duracion_ma[df_cons_IND_USDCOP['ID AM MONEDA LOCAL'].values[0]] = df_cons_IND_USDCOP['DURACION'].values[0]
#             #fechas = pd.concat([fechas, df_cons_IND_USDCOP[['ID AM MONEDA LOCAL','FECHA','FECHA_PRONOSTICO']].set_index('ID AM MONEDA LOCAL')], axis=0)
#             df_opt_u = asset_management.benchmark_vs_strategy(df_portafolios_seleccion, w_opt, retorno_ma, volatilidad_ma,duracion_ma)
#     else:
#         df_opt_u = asset_management.benchmark_vs_strategy(df_portafolios_seleccion, w_opt, retorno_esperado, vector_volatilidad,vector_duracion)

#     #verificar si el portafolio es de Renta Fija Local para desagregar los R
#     if is_RFL:
#         df_RFL = leer_archivo_optimizacion(ruta_opt +'/OPTIMIZACIONES/INDICES_OPT.xlsx', 'Renta_Fija')
#         df_opt_u = asset_management.desaggregate_RFL(df_opt_u, df_RFL)

#     df_met_ut = asset_management.portfolio_metrics(w_opt, df_seleccion['Benchmark']/100, retorno_esperado, matriz_varcov,vector_duracion)

#     return (dash_table.DataTable(id='my-table-opt',
#                                 data=df_opt_u.to_dict('records'), 
#                                 columns=[{'name': i, 'id': i} for i in df_opt_u.columns],
#                                 style_header={
#                                     'backgroundColor': 'black',
#                                     'color': 'white',
#                                 },
#                                 style_data={
#                                     'border': '1px solid' + 'black'}
#                                 ),
#             dash_table.DataTable(id='my-table-met',
#                                 data=df_met_ut.to_dict('records'), 
#                                 columns=[{'name': i, 'id': i} for i in df_met_ut.columns],
#                                 style_header={
#                                     'backgroundColor': 'black',
#                                     'color': 'white',
#                                     },
#                                 style_data={
#                                     'border': '1px solid' + 'black'}
#                                 )
#         )

# #guardar archivo de optimización
# @app.callback(
#     Output('export_opt', 'style'),
#     [Input('ver-button', 'n_clicks'),
#      Input('export-button', 'n_clicks')],
#     [State('my-table-opt', 'data'),
#      State('my-table-met', 'data'),
#      State('portafolio-seleccionado-store', 'data')],
#     prevent_initial_call=True,
# )
# def export_optimization(optimize_button, export_button, data_opt, data_met, ciudad_seleccionada):
#     ctx = dash.callback_context
#     button_id = ctx.triggered[0]['prop_id'].split('.')[0]

#     if button_id == 'ver-button':
#         return {'display': 'none',
#                 'padding': '10px', 
#                 'font-style': 'italic',  
#                 'color': colores_corporativos['green1']}
#     elif button_id == 'export-button':
#         df_opt_u = pd.DataFrame(data_opt)
#         df_met_ut = pd.DataFrame(data_met)
#         df_concat = pd.concat([df_opt_u, df_met_ut], axis=1)
#         df_concat.to_excel(ruta_opt + f'/data/{ciudad_seleccionada}_opt.xlsx', sheet_name='OPTIMIZACION', index=False)
        
#         return {'display': 'block',
#                 'padding': '10px', 
#                 'font-style': 'italic',  
#                 'color': colores_corporativos['green1']}

# # Mostrar div selección
# @app.callback(
#     Output('parent-div-select', 'style'),
#     #Input('df-portafolios-seleccionados-store', 'data'),
#     Input('ciudades-dropdown', 'value'),
#     #Input('port-opt-3col', 'data'),
#     prevent_initial_call=True,
# )
# def show_headers(data):
#     return {'display': 'block', 'padding': '5px','justify-content': 'flex-start', 'align-items': 'flex-start', 'backgroundColor': 'white'}

# # Mostrar div restricciones
# @app.callback(
#     Output('parent-div-cons', 'style'),
#     Input('ciudades-dropdown', 'value'),
#     #Input('my-table-constraints', 'data'),
#     prevent_initial_call=True,
# )
# def show_headers(data):
#     return {'display': 'block', 'padding': '5px','justify-content': 'flex-start', 'align-items': 'flex-start', 'backgroundColor': 'white'}

# #mostrar mensaje informativo
# @app.callback(
#     Output('informacion_opt', 'style'),
#     Input('ciudades-dropdown', 'value'),
#     prevent_initial_call=True,
# )
# def show_info(data):
#     return {'display': 'block',
#             'padding': '10px 20px', 
#             'font-weight': 'bold', 
#             'color': 'black',
#             'backgroundColor': '#fff3cd',  # color de fondo similar a alert-warning
#             'borderColor': '#ffeeba',  # color de borde similar a alert-warning
#             'borderRadius': '4px',  # radio de borde similar a alert-warning
#             'marginBottom': '1rem'}  # margen inferior similar a alert-warning

# #Mostrar boton Resetear
# @app.callback(
#     Output('ver-button', 'style'),
#     Input('ver-button', 'n_clicks'),
#     prevent_initial_call=True,
# )
# def show_headers(data):
#     return {'display': 'block', 'background-color': colores_corporativos['yellow'],
#             'color': 'black', 'margin': '10px',
#             'border-radius': '5px',  # Agrega redondez al botón
#             'font-weight': 'bold',  # Hace que el texto sea negrita
#             'border': 'none',  # Quita los bordes
#             'box-shadow': '0px 8px 15px rgba(0, 0, 0, 0.1)',  # Agrega sombra
#             'cursor': 'pointer'
#             }

# # Mostrar los contenidos de la optimización
# @app.callback(
#     [Output('optimization-div', 'style'), 
#      Output('graphs-div', 'style'),
#      Output('serie-div', 'style')],
#      Input('ver-button', 'n_clicks'),
#     prevent_initial_call=True,
# )
# def show_headers(n_clicks):
#     return (
#         {'display': 'inline', 'justify-content': 'center', 'align-items': 'center'},
#         {'display': 'inline', 'justify-content': 'center', 'align-items': 'center'},
#         {'display': 'inline', 'justify-content': 'center', 'align-items': 'center'}
#     )

# # Actualizar las gráficas
# Serie de tiempo IPC
# @app.callback(
#     Output('output-container-graph_serie', 'children'),
#     Input('ver-button', 'n_clicks'),
#     State('df-ciudades-store', 'data'), 
#     prevent_initial_call=True,
# )
# def update_graphs_ipc(n_clicks,df_ciudades_seleccion_data):

#     df_ciudad_seleccion = pd.DataFrame.from_dict(df_ciudades_seleccion_data)
    
#     df_ciudad_seleccion.index = df_ciudad_seleccion['Fecha']
#     df_ciudad_seleccion = df_ciudad_seleccion.drop(columns=['Fecha'])
#     print(df_ciudad_seleccion)
#     fig = ipc.plot_IPC(df_ciudad_seleccion,'newiva')
    
#     return dcc.Graph(figure=fig)

# # Retornos Historicos
# @app.callback(
#     Output('output-container-graph_returns', 'children'),
#     Input('ver-button', 'n_clicks'),
#     State('df-ciudades-store', 'data'), 
#     prevent_initial_call=True,
# )
# def update_graphs_returns(n_clicks,df_portafolios_seleccion_data):

#     df_portafolios_seleccion = pd.DataFrame(df_portafolios_seleccion_data)
#     indices_opt = df_portafolios_seleccion.index.to_list()
#     # Se filtra el Datafreme de retonos solo para los indices que se van a optimizar
#     df_ret_opt = df_ret_diarios_aj[indices_opt]

#     assets = df_portafolios_seleccion['Asset'].to_list()

#     fig = asset_management.plot_historic_returns(df_ret_opt,assets)
    
#     return dcc.Graph(figure=fig)

# # Allocation
# @app.callback(
#     Output('output-container-graph_allocation', 'children'),
#     Input('my-table-opt', 'data'),
#     State('port-opt-3col', 'data'),
#     prevent_initial_call=True,
# )
# def update_graphs_allocation(opt_data,data):
    
#     df_seleccion = pd.DataFrame(data)
#     df_opt = pd.DataFrame(opt_data)

#     if(df_opt['Activo'].tail(1).values[0] == 'Exposición COP - USD'):
#         df_opt = df_opt.iloc[:-1]

#     asset_management.aggregate_RFL(df_opt)
    
#     activos = df_opt['Activo'].to_list()  

#     #benchmark_aux = df_opt['Benchmark'].to_list()
#     #de df_seleccion filtra las valores de la columna Benchmark que sean iguales a benchmark_aux
#     #benchmark = df_seleccion[df_seleccion['Benchmark'].isin(benchmark_aux)]['Benchmark'].to_list()
    
#     benchmark = df_seleccion['Benchmark'].to_list()
#     estrategia = df_opt['Estrategia'].to_list()
    
#     fig = asset_management.plot_allocation(estrategia, benchmark, activos)
    
#     return dcc.Graph(figure=fig)



if __name__ == '__main__':
    app.run_server(debug=True, port=8050)