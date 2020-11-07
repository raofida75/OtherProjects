import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
import streamlit as st
sns.set_style('darkgrid')

# loading the names of countries 
countries=pd.read_json('https://api.covid19api.com/countries')
country_names = list(countries['Country'])


################################# INTRO #################################
st.title('COVID-19 TRACKER APP')

st.write('''
[Covid 19 API](https://documenter.getpostman.com/view/10808728/SzS8rjbc?version=latest#00030720-fae3-4c72-8aea-ad01ba17adf8)
is used to get this dataset.
''')

st.write('Coronavirus is officially a pandemic. Since the first case in december the disease has spread fast reaching almost every corner of the world.'+
         'Some governments are taking measures to prevent a sanitary collapse to be able to take care of all these people.'+
         'I\'m tackling this challenge here. Let\'s see how some countries/regions are doing!')
############################### INTRO DONE ###############################


##################### Widgets #################################
st.sidebar.subheader('Create/Filter Search')
case_type = st.sidebar.selectbox('Case Type',
                     ['Case type', 'Confirmed', 'Deaths', 'Recovered'])

st.sidebar.write('Search by Country')
country1 = st.sidebar.selectbox('Select country name',
                     list(np.append(['Select a country'], country_names)))

country2 = st.sidebar.selectbox('Compare with another country',
                     list(np.append(['Select another country'], country_names)))

from streamlit.script_runner import RerunException
if st.sidebar.button('Refresh Data'):
  raise RerunException(st.script_request_queue.RerunData(None))
####################### Widgets completed ###########################


####################### BAR PLOT ####################################
if country2 == 'Select another country' and country1 == 'Select a country':
    
    all = pd.read_csv('https://api.covid19api.com/summary',header=None).T
    new = pd.DataFrame()
    new['x'] = all[0].str.split(':').str[0]
    new['y'] = all[0].str.split(':').str[1]
    new=new.set_index('x')
    new['y'] = new['y'].str.strip('}')
    st.subheader('Total Cases: {}, Total Deaths: {}, Total Recovered: {}'
              .format(new['y'][2],new['y'][4],new['y'][6] ))
    fig= plt.figure(figsize=(5,3))
    plt.bar(list(new[2:7:2].index),new[2:7:2]['y'].astype('int'))
    plt.tight_layout()
    st.pyplot(fig)
##################### BAR PLOT DONE #################################   
    

###################### FOR 1 COUNTRY ##############################
if case_type != 'Case type':
    
    if country2 == 'Select another country':    
        if country1 != 'Select a country':
            slug1 =  countries['Slug'][np.where(np.array(country_names)==country1)[0][0]]
            url1 = pd.read_json('https://api.covid19api.com/dayone/country/'+slug1)
            if url1.shape[0] != 0:
                st.subheader('Total {0} cases in {1} are {2}'
                    .format(case_type,country1,url1[case_type].iloc[-1]))
                fig = plt.figure(figsize=(5,3))
                sns.lineplot(url1['Date'].dt.month,url1[case_type])
                plt.xlabel('Month Number')
                st.pyplot(fig)
            else:
                st.write('No cases were reported in '+ country1)
        else:
            st.sidebar.text('Select a country')
    
############################ FOR COMPARISON B/W TWO COUNTRIES #######################   
    if country2 != 'Select another country' and country1 != 'Select a country':
        slug2 = countries['Slug'][np.where(np.array(country_names)==country2)[0][0]]
        url2 = pd.read_json('https://api.covid19api.com/dayone/country/'+slug2)
        slug1 =  countries['Slug'][np.where(np.array(country_names)==country1)[0][0]]
        url1 = pd.read_json('https://api.covid19api.com/dayone/country/'+slug1)
        
        if url1.shape[0] == 0:
            st.sidebar.write('No case were reported in '+ country1)
        elif url2.shape[0] == 0:
            st.sidebar.write('No case were reported in '+ country2)
        else:
            st.subheader('Total {0} cases in {1} are {2}'
                    .format(case_type,country1,url1[case_type].iloc[-1]))
            st.subheader('Total {0} cases in {1} are {2}'
                    .format(case_type,country2,url2[case_type].iloc[-1]))
            
            fig = plt.figure(figsize=(6,4))
            sns.lineplot(url1['Date'].dt.month, url1[case_type])
            sns.lineplot(url2['Date'].dt.month,url2[case_type])
            plt.xlabel('Month Number')
            plt.legend([country1, country2])
            st.pyplot(fig)

################################ LINE PLOTS DONE #####################################

