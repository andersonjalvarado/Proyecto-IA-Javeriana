import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import requests
from sklearn.preprocessing import StandardScaler
from sklearn.cluster import DBSCAN
from sklearn.metrics import silhouette_score
from sklearn.neighbors import NearestNeighbors
from itertools import product
from sklearn.decomposition import PCA 
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report, accuracy_score, confusion_matrix
from sklearn.model_selection import GridSearchCV
import plotly.express as px
import plotly.graph_objects as go
import plotly.graph_objects as go
from plotly.subplots import make_subplots

def get_ciudades():
    df_ipc = pd.read_excel('./data/IPC_Por_ciudad_IQY.xlsx',skiprows=range(0,2))
    return df_ipc.columns[1:23].tolist()

def get_datos_ciudad(ciudad):
    df_datos_ciudad = pd.read_excel('./data/datos_ciudades.xlsx', sheet_name=ciudad)
    df_datos_ciudad.index = df_datos_ciudad['Fecha']
    df_datos_ciudad = df_datos_ciudad.drop(columns=['Fecha'])
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
    
    fig.show()

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
        colorscale='RdBu',
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
    
    fig.show()


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
    
    fig.show()

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
    
    fig.show()

