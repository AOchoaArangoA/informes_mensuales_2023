
# -*- coding: utf-8 -*-
# """
# Created on Thu Mar  2 12:30:46 2023

# @author: Administrador
# """
# '''
# Crear un programa que se ejecute los 5 y los 20 de cada mes, en donde se realice
# un informe en terminos generales y por cada seres.

#     Ideas de que puede mostrar el informe. 
#         Cantidad de alertas t-1 con la cantidad de alertas t (En este caso se
#                                                               puede usar una 
#                                                               grafica)
#         Principales alertas encontradas, especificando si son de calidad o 
#         seguimiento. 
        
# '''
from datetime import datetime
from dateutil.relativedelta import relativedelta
import pandas as pd 
# import numpy as np
# import seaborn as sns
import matplotlib.pyplot as plt 
import streamlit as st 
# from datetime import datetime
# from funciones_dashboard import cargar_base_actual_anterior, graficos_informes
plt.style.use('fivethirtyeight')
# pd.set_option('max_columns', 200)

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
    
# @st.cache_data
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



st.set_option('deprecation.showPyplotGlobalUse', False)

st.set_page_config( initial_sidebar_state='expanded')
with open('style.css') as f:
    st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)

mes_pasado = datetime.date(datetime.today()- relativedelta(days = 9))



alertas, alertas_anterior, proyectos = cargar_base_actual_anterior('nan', datetime.date(datetime.today()))

anterior_calidad = alertas_anterior[2] # pd.read_excel('{}/alertas_calidad_datos_{}.xlsx'.format(UBI_HISTORIAL_ALERTAS,'2023-03-03' ))
actual_calidad = alertas[2] #pd.read_excel('{}/alertas_calidad_datos.xlsx'.format(UBI_ALERTAS))
base_proyectos = proyectos #pd.read_excel('{}/BASE_DATOS_GOBERNACION.xlsx'.format(UBI))


# base_proyectos_anterior = pd.merge(base_proyectos[['id', 'seres']], anterior_calidad[['alertas_nans', 'id']], on = 'id', how = 'left')
base_proyectos_grafico = pd.merge(base_proyectos[['id', 'seres']], actual_calidad, on = 'id', how = 'left')
base_proyectos_grafico = pd.merge(base_proyectos_grafico, anterior_calidad, on = 'id', how = 'left', suffixes=('_actual', '_anterior')) 
#Graficas Calidad

anterior_seguimiento = pd.merge(alertas_anterior[0], alertas_anterior[1], on = 'id', how = 'outer' )
actual_seguimiento = pd.merge(alertas[0], alertas[1], on = 'id', how = 'outer')


# base_proyectos_anterior = pd.merge(base_proyectos[['id', 'seres']], anterior_calidad[['alertas_nans', 'id']], on = 'id', how = 'left')
base_proyectos_grafico_seguimiento = pd.merge(base_proyectos[['id', 'seres']], actual_seguimiento, on = 'id', how = 'left')
base_proyectos_grafico_seguimiento = pd.merge(base_proyectos_grafico_seguimiento, anterior_seguimiento, on = 'id', how = 'left',
                                              suffixes=('_actual', '_anterior')) 
#Graficas Calidad

por_seres_seguimiento = base_proyectos_grafico_seguimiento.groupby('seres').sum().reset_index()

por_seres = base_proyectos_grafico.groupby('seres').sum().reset_index()

seres_idx = por_seres.seres.value_counts().index
# st.image('https://github.com/AOchoaArangoA/Indice_GC_Conglomerado/blob/main/Gob_Ant2.png', caption = 'Imagen Goberanción de Antioquia', width =1000)
st.markdown('# Alertas plataforma proyectos de inversión 2023')
st.markdown('''
            La oficina privada de la gobernación de antioquia ha desarrollado una plataforma de alertas de calidad y seguimiento para monitorear y
            evaluar las intervenciones de los programas y servicios que se encuentran repositados en la plataforma. Esta página web cuenta con un 
            sistema de seguimiento y monitoreo *mensual* que permite a los responsables del diligenciamiento hacer 
            un seguimiento detallado de los proyectos en donde se presenta un problema de calidad o se presenta un alertamiento en el seguimiento.
            
            El analisis de las alertas se realiza por cada SERES, lo que permite tener informacion segmentada y focalizada. Esto se ve representando
            en la capacidad de tener un alertamiento mas eficiente y efectivo.''')
st.sidebar.header('Filtros')

st.sidebar.subheader('SERES')
seres_select = st.sidebar.selectbox('Seleccionar', seres_idx)

st.sidebar.subheader('Tipo de Alerta')
tipo_select = st.sidebar.selectbox('Seleccionar', ('Calidad', 'Seguimiento'))


if tipo_select == 'Calidad': 
    st.markdown('## Alertas Calidad')
    st.pyplot(graficos_informes(por_seres,seres_select))
    st.markdown('''
                * **Valores Nulos**: Esta alerta presenta la cantidad de proyectos que poseen un valor nulo en algunas de las casillas que son escenciales para el analisis de los proyectos. Las casillas son [subregion', 'municipio', 'actual','annosuscripcion','porcentejecutado_deetapa', 'descripcion_avance']
                * **Cantidad de Palabras Insuficientes**: Esta alerta presenta que la observación del proyecto es menor a 10 palabras. Lo que imposibilita tener un sustento en el seguimiento del proyecto. 
                * **Comparación Año/Etapa**: Esta alerta evidencia la cantidad de intervenciones realizadas en años diferentes a 2022 o 2023, y que se encuentran en etapas de planeación o ejecución. 
                * **Valores Duplicados**: Esta alerta evidencia si hay presencia de proyectos con información duplicada en las columnas de SERES, alcance del proyecto, subregión, municipio, etapa, fuentes de finanaciación, entre otras. 
                * **Porcentaje ejecutado mayor**: Esta alerta evidencia si el proyecto tiene un porcentaje ejecutado mayor al procentaje programado. Esto se considera una incongruencia para el análisis de los proyectos. 
                * **Diferencias Valor Apropiado**: Esta alerta muestra que la suma de las fuentes de financiación es diferente al valor apropiado que se encuentra en la plataforma. 
                ''')

elif tipo_select == 'Seguimiento': 
    st.markdown('## Alertas Seguimiento')
    st.pyplot(graficos_informes(por_seres_seguimiento ,seres_select,  tipo_alerta='Seguimiento'))
    st.markdown('''
                * **Cambios Significativos Valor Apropiado**: Esta alerta compara la información de los proyectos con un archivo anterior. Se desea evidenciar si se presentaron cambios significativos en el valor apropiado de un proyecto. 
                * **Cambios Significativos Porcentaje Ejecutado**: Esta alerta compara la información de los proyectos con un archivo anterior. Se desea evidenciar si se presentaron cambios significativos en el porcentaje ejecutado.
                * **Proyectos Ejecución/Planeación - Finalizados**: Esta alerta compara la información de los proyectos con un archivo anterior. Se desea evidenciar cuantos proyectos pasaron de etapa de planeación/ejecución a finalizados.
                * **Cantidad de Proyectos Finalizados**: Presenta la cantidad de proyectos que se encuentran actualizdos (+/- 2 Meses)
                ''')
