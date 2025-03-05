#!/usr/bin/env python
# coding: utf-8

# In[4]:


# ИМПОРТ ВСЕХ БИБЛИОТЕК
import math as m
import time
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
import streamlit as st
import altair as alt
####### ФУНКЦИИИ

#Считывание данных
@st.cache_data
def load_data():
    return pd.read_csv("https://raw.githubusercontent.com/aiedu-courses/all_datasets/main/Population.csv", delimiter=';')

# Функция для создания сообщения 0 - ассистент, 1 - пользователь // можно и не 1)))

def chat(text, x):
    if x == 0:
        st.chat_message("assistant").write(text)
    else:
        st.chat_message("user").write(text)
       
# Коэффициент корреляции Пирсона между населением двух стран
@st.cache_data
def Pirson(B, C, df):
    Country1 = df.loc[B][1:].astype(float)
    Country2 = df.loc[C][1:].astype(float)
    Corr = Country1.corr(Country2)
    return Corr
    
# Население страны в конкретном году
@st.cache_data
def population_year(year):
    
       start_year = 1960
       index_year = int(year - start_year)
       popu = Country1[index_year]
       
       st.write(f'💁‍♀️*Население* {Name1} *в* {year} *году* - {popu:,.0f}')
    
# Создание таблицы страна - коэф. корреляции Пирсона
@st.cache_data
def correlationPir(B,country,df):
    correlation = []
    for i in range(0,266):
        correlation.append(Pirson(B, i,df)) # СЧИТАЮ ККП для Болгарии и i-ой страны + добавляю ККП в массив    
    corr_data = pd.DataFrame({         # таблица Страна - ККП
            'Country': country,
            'Pirson Correlation':correlation
       })
    corr_data = corr_data.sort_values(by='Pirson Correlation',ascending=False)
    return corr_data

# Функция сохранения графика:
def save(name, fig):
    file_name = name
    fullpath = f"C:/Users/Никита/Desktop/{file_name}.png"
    if file_name:  
     try:
        fig.savefig(fullpath,dpi=300, bbox_inches='tight')
        st.write('*График сохранен на рабочем столе*')
     except Exception as noway:
        st.write(f'Ошибка {noway}')
        fig.savefig('C:/Users/Никита/Desktop/heatmap.png',dpi=300,bbox_inches='tight', pad_inches='0.5')
        st.write('*График сохранен на рабочем столе как default.png*')

# Смена изображения
@st.cache_data
def image_setter(x):
    name =  ['https://i.pinimg.com/originals/84/8d/7c/848d7c6b1d27d9c484463b2e16cb406b.gif',
             'https://i.pinimg.com/originals/85/05/05/8505051384604a66d6af0f6662e7dd44.gif',
             'https://i.pinimg.com/originals/67/34/b0/6734b0c9b53211b35430606fffb385ad.gif',
             'https://i.pinimg.com/originals/f2/eb/43/f2eb4304c9c154cb56fdfc20c0641114.gif',
             'https://i.pinimg.com/originals/76/7d/68/767d687e4a8b796f54553c0b0fe641a3.gif',
             'https://i.pinimg.com/originals/2a/df/bf/2adfbfcda9ac11be42f243367f2f6fd7.gif',
             'https://i.pinimg.com/originals/e2/4d/bb/e24dbbe9ce331da8424d88f14eba3891.gif',
             'https://i.pinimg.com/originals/f3/58/57/f3585768009c22148ce472033e93ac2e.gif',
             'https://i.pinimg.com/originals/39/f9/78/39f978cf23dfbe5d0f0c389e7c35a82e.gif',
             'https://i.pinimg.com/originals/d9/84/39/d984395bfb4cbd10a7e4d764ae760c67.gif'
    ]
    url = name[int(x)]
    st.image(url)
    
######## ЗАГРУЗКА ДАННЫХ
st.set_page_config(layout="centered", page_title="Население страны", page_icon="📈") # Макет
df = load_data()
years = df.columns[1:].astype(int) # МАССИВ ИЗ ГОДОВ
country = df['Country Name'].values # МАССИВ СТРАН
counts = len(years) # ЧИСЛО ГОДОВ)))

# СОЗДАНИЕ ЧАТА

# стартовый диалог
if 'x' not in st.session_state:
    st.session_state.x = 0
if 'name' not in st.session_state:
    st.session_state.name =''
if 'image' not in st.session_state:
    st.session_state.image = int(0)
    
if st.session_state.x == 0:
    chat('**Привет, выбери страну**',0)
    user_name = st.selectbox('Выбери страну',options=country, index=None)
    if user_name != None:
      st.session_state.x = 1
      st.session_state.name= user_name
if st.session_state.x == 1:
    Name1 = st.session_state.name
    st.session_state.x = 2
    chat(f'**Я выбрал {Name1}**', 1)   
    time.sleep(0.5)
    chat("**Отлично, теперь выбери нужные пункты в :rainbow[МЕНЮ] слева**", 0)
# Выбор данных и создание сайдбара
if st.session_state.x == 2:
    Name1 = st.session_state.name
    
    Country1 = df[df['Country Name'] == Name1].values[0][1:].astype(int)
    B = df.loc[df['Country Name'] == Name1].index[0] # индекс страны 1
    with st.sidebar:
        with st.container(key='g'):
            st.write('Первое приложение на streamlit😶‍🌫️🥶 \n *tg*: @jktm18📱⌨️ \n *gmail*:kulikov123451@gmail.com📧🖥️')
        with st.form('my form'):
             with st.container(key='j'): 
               image_setter(st.session_state.image)
               
               with st.expander(':rainbow[**МЕНЮ**]', expanded=False):
                            
                            show_heatmap = st.checkbox("Показать тепловую карту")
                            population_plot=st.checkbox("Показать график зависимости населения от года")
                            year = st.slider("Выбери год😈", min_value=int(df.columns[1]), max_value=int(df.columns[-1])) # ВЫБОР ГОДА
                            with st.container():
                              show_population = st.checkbox("Показать население страны в выбранный год")
                              mean_std = st.checkbox("Показать среднее население страны по годам")
                              population_max = st.checkbox("Показать максимальное население") 
                            
                            submitted = st.form_submit_button("Подтвердить",type='primary')
        with st.container(border=True,key='y'):
           submitted_two = st.toggle('🔙:violet[Смена страны]')
           submitted_three = st.toggle('🌃:violet[Про дата сет]')
            
    #Информация о датасете
    if submitted_three:
         st.write('***Набор данных представляет из себя распределение :red[населения стран] по :blue[годам]***')
         st.write(df)
        
    # Смена страны     
    if submitted_two:
                st.session_state.x = 0
                st.session_state.name=None
                st.rerun()
   
    # Кнопка подтвердить
    if submitted:
          if st.session_state.image < 9:
                  st.session_state.image +=1
          else:
              st.session_state.image = 0
   
          #Население в конкретный год
          if show_population:
              
              population_year(year)
              
          #Среднее значение населения   
          if mean_std:
            
            mean1 = np.mean(Country1)
            std1 = np.std(Country1)
            st.write(f'💁*Среднее население страны*: {mean1:,.0f} ± {std1:,.0f}')

          #Максимальное значение населения    
          if population_max:
              
            pop_max = np.max(Country1)
            st.write(f'💁‍♂️*Максимальное население страны*: {pop_max:,.0f}')

          # Тепловая карта    
          if show_heatmap:
              
              data = correlationPir(B,country,df)
              data = data[data['Country'] != 'Not classified']
              st.subheader('Heatmap: Pirson Correlation(Country)')
              heatmap = alt.Chart(data).mark_rect().encode(
                  y=alt.Y('Country:O', sort=alt.SortField('Pirson Correlation', order='descending')), 
                  color='Pirson Correlation:Q'
              ).properties(
                  width=800,
                  height=500,
                  )
            
              st.altair_chart(heatmap,use_container_width=False)
              
          # График населения
          if population_plot:
              data =pd.DataFrame({'Years':years, 'Population':Country1})
              st.subheader('Graph: Population(Years)')
              s = st.line_chart(data,x='Years', y='Population', x_label='Год',y_label='Население')
              
                    
                    


# In[ ]:




