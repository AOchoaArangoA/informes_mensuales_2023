# -*- coding: utf-8 -*-
"""
Created on Tue Mar 21 13:26:23 2023

@author: Administrador
"""

from datetime import datetime, timedelta
from dateutil.relativedelta import relativedelta
import pandas as pd 
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt 
import streamlit as st 
from datetime import datetime
plt.style.use('fivethirtyeight')
pd.set_option('max_columns', 200)

mes_pasado = datetime.date(datetime.today()- relativedelta(days = 9))

#Ubicacion del archivo de los proyectos actuales
UBI = 'D:\Gestion\OneDrive - Gobernacion de Antioquia\Base_Datos'
#Ubicacion de los archivos de las alertas actuales
UBI_ALERTAS = 'D:/Gestion/OneDrive - Gobernacion de Antioquia/Base_Datos/alertas_plataforma'
#Ubicacion del historial de las alertas
UBI_HISTORIAL_ALERTAS = 'D:/Gestion/OneDrive - Gobernacion de Antioquia/Base_Datos/alertas_plataforma/historial_alertas'



def graficos_informes(df, seres, tipo_alerta = 'Calidad' ):
    df_plot = df[df['seres'] == seres]
    
    if tipo_alerta == 'Calidad': 
        
        
        
        alertas = ['alertas_nans', 'alertas_palabras', 'alerta_cruzado',
               'alerta_duplicados', 'alerta_programado_ejecutado',
               'alerta_valor_apropiado']
        nombre = ['Valores Nulos', 'Cantidad de Palabras Insuficiente', 'Comparación Año/Etapa',
                  'Valores Duplicados', 'Porcentaje Ejecutado Mayor',
                  'Diferencias Valor Apropiado']
        
        dict_from_list = dict(zip(alertas, nombre))
        
        
        fila = 2
        cols = 3
    elif tipo_alerta == 'Seguimiento': 
        alertas = ['alertas_valorapropiado', 'alertas_porcejecutado',
                   'alerta_ejecucion_planeacion', 'alerta_actualizacion']
        nombre = ['Cambios Significativos \nValor Apropiado', 'Cambios Significativos \nPorcentaje Ejecutado',
                  'Proyectos Ejecucion/Planeación - Finalizado', 'Cantidad de Proyectos Actualizados']
        
        fila = 2
        cols = 2
        
        dict_from_list = dict(zip(alertas, nombre))
    count=0
    fig, ax = plt.subplots(fila, cols)
    for row, contenido in enumerate(ax):
        for column in range(len(contenido)):
            df_plot[['{}_anterior'.format(alertas[count]), '{}_actual'.format(alertas[count])]].plot.bar( ax = ax[row, column],
                                                                                              subplots=False, ylim = 0,
                                                                                              color = ['#416864', '#00a6a2'])
            if alertas[count] == 'alerta_actualizacion': 
                ax[row, column].text(-0.5 ,1 , '*Significado\nContrario*')
                
            ax[row, column].bar_label(container= ax[row, column].containers[1],label_type='center')
            ax[row, column].bar_label(container= ax[row, column].containers[0],label_type='center')
            ax[row, column].set_title(label = '{}'.format(dict_from_list[alertas[count]]), fontsize = 15 )
            ax[row, column].legend(['Anterior', 'Actual'], loc = 4, fontsize = 'medium')
            count += 1
    

    fig.set_figheight(10)
    fig.set_figwidth(12)
    fig.suptitle('SERES:\n{}'.format(seres), fontsize=16)    
    
    fig.text(0, 0, 
         '{} Base Seguimiento:{}'.format(tipo_alerta, mes_pasado), 
         style = 'italic',
         fontsize = 10,
         color = "black")
    plt.show()

def cargar_base_actual_anterior(nombre_alerta, fecha):
    
    # hoy = datetime.date(datetime.now())
    if fecha.year > 2023: 
        print('Problema con la fecha. Se encuentra en una año mayor al 2023')
        return None
    
    lista_alertas_anterior = []
    # if fecha.day == 5 or fecha.day == 20: 
    if True:
        alertas_seguimiento_anterior_cambios = pd.read_excel('{}/alertas_seguimiento_{}.xlsx'.format(UBI_HISTORIAL_ALERTAS, mes_pasado), 
                                                     sheet_name = 'alertas_cambios')
        lista_alertas_anterior.append(alertas_seguimiento_anterior_cambios)
        
        ###################
        
        alertas_seguimiento_anterior_actualizacion = pd.read_excel('{}/alertas_seguimiento_{}.xlsx'.format(UBI_HISTORIAL_ALERTAS, mes_pasado),
                                                                   sheet_name = 'alertas_actualizacion')
        lista_alertas_anterior.append(alertas_seguimiento_anterior_actualizacion)
        
        ###################
        alertas_calidad_datos_anterior = pd.read_excel('{}/alertas_calidad_datos_{}.xlsx'.format(UBI_HISTORIAL_ALERTAS, mes_pasado))
        lista_alertas_anterior.append(alertas_calidad_datos_anterior)
    
    lista_alertas = []
    alertas_calidad_datos = pd.read_excel('{}/alertas_calidad_datos.xlsx'.format(UBI_ALERTAS))
    alertas_seguimiento_cambios = pd.read_excel('{}/alertas_seguimiento.xlsx'.format(UBI_ALERTAS), sheet_name = 'alertas_cambios')
    alertas_seguimiento_actualizacion = pd.read_excel('{}/alertas_seguimiento.xlsx'.format(UBI_ALERTAS), sheet_name = 'alertas_actualizacion')
    
    
    lista_alertas.append(alertas_seguimiento_cambios)
    lista_alertas.append(alertas_seguimiento_actualizacion)
    lista_alertas.append(alertas_calidad_datos)
    
    base_datos_proyectos = pd.read_excel('{}/BASE_DATOS_GOBERNACION.xlsx'.format(UBI))
    return lista_alertas, lista_alertas_anterior, base_datos_proyectos
