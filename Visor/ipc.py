import pandas as pd
import numpy as np
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report, accuracy_score, confusion_matrix
from sklearn.model_selection import GridSearchCV
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots

def get_ciudades():
    df_ipc = pd.read_excel('./data/IPC_Por_ciudad_IQY.xlsx',skiprows=range(0,2))
    return df_ipc.columns[1:23].tolist()

def get_datos_ciudad(ciudad):
    df_datos_ciudad = pd.read_excel('./data/datos_ciudades.xlsx', sheet_name=ciudad)
    df_datos_ciudad['Fecha'] = pd.to_datetime(df_datos_ciudad['Fecha']).dt.to_period('M')
    df_datos_ciudad.set_index('Fecha', inplace=True)
    return df_datos_ciudad

def plot_boxplot(df, nom_ciudad):
    """
    Genera un boxplot de un DataFrame utilizando Plotly.
    
    Args:
        df (DataFrame): El DataFrame.
        nom_ciudad (str): Nombre de la ciudad.
    """
    int_cols = df.select_dtypes(exclude='object').columns
    
    fig = go.Figure()
    
    for col in int_cols:
        fig.add_trace(go.Box(y=df[col], name=col))
    
    fig.update_layout(
        title=f'Boxplot de {nom_ciudad}',
        yaxis=dict(title='Valores'),
        boxmode='group',
        height=600,
        width=800
    )
    
    return fig

def plot_heatmap(df, nom_ciudad):
    """
    Genera un heatmap de correlación de un DataFrame utilizando Plotly.
    
    Args:
        df (DataFrame): El DataFrame.
        nom_ciudad (str): Nombre de la ciudad.
    """
    corr_matrix = df.corr()
    
    fig = go.Figure(data=go.Heatmap(
            z=corr_matrix.values,
            x=corr_matrix.columns,
            y=corr_matrix.index,
            colorscale='Blues',
            zmid=0,
            zmin=-1,
            zmax=1,
            text=corr_matrix.values,
            texttemplate="%{text:.2f}",
            textfont=dict(size=12),
            hovertemplate='Correlación entre %{x} y %{y}: %{text:.2f}<extra></extra>'
        ))
    
    fig.update_layout(
        title=f'Heatmap de Correlación de {nom_ciudad}',
        xaxis_title='Variables',
        yaxis_title='Variables',
        width=800,
        height=800
    )
    
    return fig


def plot_histogram(df, nom_ciudad):
    """
    Genera un histograma de un DataFrame utilizando Plotly.
    
    Args:
        df (DataFrame): El DataFrame.
        nom_ciudad (str): Nombre de la ciudad.
    """
    int_cols = df.select_dtypes(exclude='object').columns
    num_cols = len(int_cols)
    
    num_rows = (num_cols + 1) // 2
    num_cols = 2
    
    fig = make_subplots(rows=num_rows, cols=num_cols, subplot_titles=int_cols)
    
    for i, col in enumerate(int_cols):
        row = (i // 2) + 1
        col_num = (i % 2) + 1
        
        fig.add_trace(go.Histogram(x=df[col], name=col, nbinsx=30), row=row, col=col_num)
        fig.update_xaxes(title_text=col, row=row, col=col_num)
        fig.update_yaxes(title_text='Frecuencia', row=row, col=col_num)
    
    fig.update_layout(
        title=f'Histograma de {nom_ciudad}',
        height=num_rows * 400,
        width=800,
        showlegend=False
    )
    
    return fig

def plot_IPC(df, nom_ciudad):
    """
    Genera un gráfico de IPC de un DataFrame utilizando Plotly.
    
    Args:
        df (DataFrame): El DataFrame.
        nom_ciudad (str): Nombre de la ciudad.
    """
    fechas = df.index.astype(str).tolist()
    
    fig = go.Figure()
    
    fig.add_trace(go.Scatter(x=fechas, y=df.iloc[:, 0], mode='lines', name=df.columns[0]))
    
    fig.update_layout(
        title=f'Serie Temporal de IPC Mensual - {nom_ciudad}',
        xaxis_title='Fecha',
        yaxis_title='IPC Mensual',
        width=800,
        height=400
    )
    
    return fig


def plot_confusion_matrix(y_test, y_test_pred):
    """
    Genera una matriz de confusión utilizando Plotly.
    
    Args:
        y_test (array): Valores reales de la variable objetivo.
        y_test_pred (array): Valores predichos de la variable objetivo.
    """
    labels = ['Bajo', 'Medio', 'Alto']
    conf_matrix = confusion_matrix(y_test, y_test_pred)
    
    fig = go.Figure(data=go.Heatmap(
        z=conf_matrix,
        x=labels,
        y=labels,
        colorscale='Blues',
        text=conf_matrix,
        texttemplate="%{text}",
        textfont=dict(size=20),
        hovertemplate='Predicted: %{x}<br>Actual: %{y}<br>Count: %{text}<extra></extra>'
    ))
    
    fig.update_layout(
        title='Confusion Matrix',
        xaxis_title='Predicted',
        yaxis_title='Actual',
        width=700,
        height=600
    )
    
    return fig

def plot_feature_importances(best_model, X_train):
    """
    Visualiza la importancia de las características utilizando Plotly.
    
    Args:
        best_model: El modelo entrenado.
        X_train (DataFrame): El conjunto de entrenamiento.
    """
    feature_importances = pd.DataFrame(best_model.feature_importances_, index=X_train.columns, columns=['importance'])
    feature_importances = feature_importances.sort_values('importance', ascending=False)
    
    fig = go.Figure(data=[go.Bar(
        x=feature_importances.index,
        y=feature_importances['importance'],
        text= np.round(feature_importances['importance'],2),
        textposition='auto',
        hovertemplate='Característica: %{x}<br>Importancia: %{y}<extra></extra>'
    )])
    
    fig.update_layout(
        title='Importancia de las Características',
        xaxis_title='Características',
        yaxis_title='Importancia',
        width=800,
        height=600
    )
    
    return fig

def best_random_forest_model(df, features, target):
    """
    Realiza un modelo predictivo utilizando Random Forest.
    
    Args:
        df (DataFrame): El DataFrame con los datos.
        features (list): Las características a utilizar.
        target (str): La variable objetivo.
    Returns:
        DataFrame: El classification_report del modelo.
    """
    df['IPC_Category'] = pd.qcut(df[target], q=3, labels=[0, 1, 2])
    
    scaler = StandardScaler()
    df[features] = scaler.fit_transform(df[features])

    X = df[features]
    y = df['IPC_Category']

    # Dividir el conjunto de datos en entrenamiento y prueba
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    rf = RandomForestClassifier(random_state=42)

    # Definir los hiperparámetros a ajustar
    param_grid = {
        'criterion': ['gini', 'entropy'],
        'n_estimators': [100, 200, 300],
        'max_depth': [None, 5, 10],
        'max_samples': [None, 0.5, 0.8],
        'min_samples_split': [2, 5, 10]
    }

    # Realizar la búsqueda de hiperparámetros con validación cruzada
    grid_search = GridSearchCV(estimator=rf,
                               param_grid=param_grid,
                               cv=5,
                               scoring='accuracy')

    grid_search.fit(X_train, y_train)

    # Obtener el mejor modelo y sus hiperparámetros
    best_model = grid_search.best_estimator_
    best_params = grid_search.best_params_

    y_test_pred = best_model.predict(X_test)
    test_accuracy = accuracy_score(y_test, y_test_pred)

    # Generar el classification_report
    report = classification_report(y_test, y_test_pred, output_dict=True)
    report_df = pd.DataFrame(report).transpose()

    return report_df, y_test, y_test_pred, best_model, X_train

def random_forest_model(df, features, target, criterion, n_estimators, max_depth, max_samples, min_samples_split):
    """
    Realiza un modelo predictivo utilizando Random Forest.
    
    Args:
        df (DataFrame): El DataFrame con los datos.
        features (list): Las características a utilizar.
        target (str): La variable objetivo.
        criterion (str): El criterio de división.
        n_estimators (int): El número de árboles.
        max_depth (int): La profundidad máxima de los árboles.
        max_samples (float): La proporción de muestras a utilizar.
        min_samples_split (int): El número mínimo de muestras para dividir un nodo.
    Returns:
        DataFrame: El classification_report del modelo.
    """

    #estandarizar df
    df = standardize(df)

    df['IPC_Category'] = pd.qcut(df[target], q=3, labels=[0, 1, 2])

    X = df[features]
    y = df['IPC_Category']

    # Dividir el conjunto de datos en entrenamiento y prueba
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    rf = RandomForestClassifier(random_state=42,
                                criterion=criterion,
                                n_estimators=n_estimators,
                                max_depth=max_depth,
                                max_samples=max_samples,
                                min_samples_split=min_samples_split)

    rf.fit(X_train, y_train)
    y_test_pred = rf.predict(X_test)

    # Generar el classification_report
    report = classification_report(y_test, y_test_pred, output_dict=True)
    report_df = np.round(pd.DataFrame(report).transpose(),3)

    return report_df, y_test, y_test_pred, rf, X_train

def standardize(df):
    """
    Estandariza un DataFrame.
    Args:
        df (DataFrame): El DataFrame.
    Returns:
        DataFrame: El DataFrame estandarizado.
    """
    scaler = StandardScaler()
    df_scaled = scaler.fit_transform(df)
    df_scaled = pd.DataFrame(df_scaled, columns=df.columns)
    return df_scaled