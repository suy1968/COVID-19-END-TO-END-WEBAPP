import pandas as pd 
import streamlit as st
import random
import matplotlib.pyplot as plt 
import matplotlib.colors as mcolors
import numpy as np
import operator

st.title("COVID-19 Analysis and Visualisation")
st.markdown("A realtime Analysis and Visualization of Coronavirus")

page =  st.sidebar.selectbox('What you wanna see?',['Quick Analysis','Detailed Analysis','Victims per Country'])

@st.cache
def confirmcase_get_data():
    url = "https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_time_series/time_series_covid19_confirmed_global.csv"
    return pd.read_csv(url)
confirm_case_df = confirmcase_get_data()

@st.cache
def deaths_get_data():
    url = "https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_time_series/time_series_covid19_deaths_global.csv"
    return pd.read_csv(url)
deaths_df = deaths_get_data()

@st.cache
def recoveries_get_data():
    url = "https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_time_series/time_series_covid19_recovered_global.csv"
    return pd.read_csv(url)
recoveries_df = recoveries_get_data()

cols = confirm_case_df.keys()
confirm_case_df_index = confirm_case_df.set_index('Country/Region')
deaths_df_index = deaths_df.set_index('Country/Region')
recoveries_df_index = recoveries_df.set_index('Country/Region')

recent_confirmed = confirm_case_df_index.loc[:, cols[-5]:cols[-1]]
recent_deaths = deaths_df_index.loc[:, cols[-5]:cols[-1]]
recent_recoveries = recoveries_df_index.loc[:, cols[-5]:cols[-1]]
#function starts here
confirmed = confirm_case_df.loc[:, cols[4]:cols[-1]]
deaths = deaths_df.loc[:, cols[4]:cols[-1]]
recoveries = recoveries_df.loc[:, cols[4]:cols[-1]]

dates = confirmed.keys()
world_cases = []
total_deaths = []
mortality_rate = []
recovery_rate = []
total_recovered = []
total_active = []
china_cases = []
italy_cases = []
us_cases = []
spain_cases = []
india_cases = []
for i in dates:
    confirmed_sum = confirmed[i].sum()
    death_sum = deaths[i].sum()
    recovered_sum = recoveries[i].sum()
    
    world_cases.append(confirmed_sum)
    total_deaths.append(death_sum)
    total_recovered.append(recovered_sum)
    total_active.append(confirmed_sum-death_sum-recovered_sum)
    
    #calculate rates
    
    mortality_rate.append(death_sum/confirmed_sum)
    recovery_rate.append(recovered_sum/confirmed_sum)
    
    #country wise datas
    china_cases.append(confirm_case_df[confirm_case_df['Country/Region']=='China'][i].sum())
    italy_cases.append(confirm_case_df[confirm_case_df['Country/Region']=='Italy'][i].sum())
    us_cases.append(confirm_case_df[confirm_case_df['Country/Region']=='US'][i].sum())
    spain_cases.append(confirm_case_df[confirm_case_df['Country/Region']=='Spain'][i].sum())
    india_cases.append(confirm_case_df[confirm_case_df['Country/Region']=='India'][i].sum())

def daily_increase(data):
    d = []
    for i in range(len(data)):
        if i == 0:
            d.append(data[0])
        else:
            d.append(data[i]-data[i-1])
    return d

world_daily_increase = daily_increase(world_cases)
china_daily_increase = daily_increase(china_cases)
italy_daily_increase = daily_increase(italy_cases)
us_daily_increase = daily_increase(us_cases)
spain_daily_increase = daily_increase(spain_cases)
india_daily_increase = daily_increase(india_cases)

day_since_first_case = np.array([i for i in range(len(dates))]).reshape(-1, 1)

world_cases = np.array(world_cases).reshape(-1 , 1)
total_deaths = np.array(total_deaths).reshape(-1 , 1)
total_recovered = np.array(total_recovered).reshape(-1 , 1)

days_in_future = 20
future_forecast = np.array([i for i in range(len(dates)+days_in_future)]).reshape(-1 , 1)
adjusted_dates = future_forecast[:-20]

country_confirm_cases = []
no_cases = []
latest_confirmed = confirm_case_df[dates[-1]]
latest_deaths = deaths_df[dates[-1]]
latest_recoveries = recoveries_df[dates[-1]]

unique_countries =  list(confirm_case_df['Country/Region'].unique())
country_confirm_cases = []
no_cases = []
for i in unique_countries:
    cases = latest_confirmed[confirm_case_df['Country/Region']==i].sum()
    if cases > 0:
        country_confirm_cases.append(cases)
    else:
        no_cases.append(i)
        
for i in no_cases:
    unique_countries.remove(i)

unique_countries = [k for k, v in sorted(zip(unique_countries, country_confirm_cases), key = operator.itemgetter(1), reverse=True)]
for i in range(len(unique_countries)):
    country_confirm_cases[i] = latest_confirmed[confirm_case_df['Country/Region']==unique_countries[i]].sum()

    
# Only show 10 countries with the most confirmed cases, the rest are grouped into the other category
visual_unique_countries = [] 
visual_confirmed_cases = []
others = np.sum(country_confirm_cases[10:])

for i in range(len(country_confirm_cases[:10])):
    visual_unique_countries.append(unique_countries[i])
    visual_confirmed_cases.append(country_confirm_cases[i])
    
visual_unique_countries.append('Others')
visual_confirmed_cases.append(others)

if page == 'Quick Analysis':
    st.header("Recent confirmed cases all over the world")
    st.markdown("The below table shows the list of recent confirmed cases all over the world country wise")

    st.dataframe(recent_confirmed)

    st.header("Recent cases all over the world")
    st.markdown("The below table shows the list of recent deaths due to Corona Virus all over the world country wise")

    st.dataframe(recent_deaths)

    st.header("Recent  Recoveries all over the world")
    st.markdown("The below table shows the list of recent recoveries of Corona Virus all over the world country wise")

    st.dataframe(recent_recoveries)

    #PLOTTING THE DATA
    st.header("Number of CoronaVirus cases overtime!")
    st.markdown("The below chart visualises the increase of Corona Virus cases over time!")

    adjusted_dates = adjusted_dates.reshape(1, -1)[0]
    plt.figure(figsize=(16, 9))
    plt.plot(adjusted_dates, world_cases)
    plt.title('# of Coronavirus Cases Over Time', size=30)
    plt.xlabel('Days Since 22/1/2020', size=30)
    plt.ylabel('# of Cases', size=30)
    plt.xticks(size=20)
    plt.yticks(size=20)
    st.pyplot()

    st.header("Daily increase of Corona Virus")
    st.markdown("The below chart visualises the daily increase of Corona Virus cases all over the  World")

    plt.figure(figsize=(16,9))
    plt.bar(adjusted_dates, world_daily_increase)
    plt.title("World Daily increase in confirmed cases",size=30)
    plt.xlabel('Days since 22/1/2020', size=30)
    plt.ylabel('Number of Cases', size=30)
    plt.xticks(size=30)
    plt.yticks(size=30)
    st.pyplot()

    st.header("Number of Corona Virus  cases in major countries")
    st.markdown("The below chart visualises the number of Corona Virus cases in major countries")

    plt.figure(figsize=(16,9))
    plt.plot(adjusted_dates, china_cases)
    plt.plot(adjusted_dates, italy_cases)
    plt.plot(adjusted_dates, us_cases)
    plt.plot(adjusted_dates, spain_cases)
    plt.plot(adjusted_dates, india_cases)
    plt.title('# of Coronavirus Cases', size=30)
    plt.xlabel('Days Since 22/1/2020', size=30)
    plt.ylabel('# of Cases', size=30)
    plt.legend(['China', 'Italy', 'US', 'Spain' , 'India'], prop={'size': 20})
    plt.xticks(size=20)
    plt.yticks(size=20)
    st.pyplot()

    st.header("Countries that are most affected by Corona Virus")
    st.markdown("Only showing 10 countries with the most confirmed cases, the rest are grouped into the other category")

    plt.figure(figsize=(16, 9))
    plt.barh(visual_unique_countries, visual_confirmed_cases)
    plt.title('# of Covid-19 Confirmed Cases in Countries/Regions', size=20)
    plt.xticks(size=20)
    plt.yticks(size=20)
    st.pyplot()
elif page == 'Detailed Analysis':
    st.markdown('This page provides you the detailed visualisations of Corona Virus')
    st.header("Confirmed cases all over the world")
    st.markdown("The below table shows the list of all the Confirmed cases all over the world country wise from January 22,2020")

    st.dataframe(confirm_case_df)

    st.header("Deaths all over the world")
    st.markdown("The below table shows the list of all the Deaths due to Corona Virus all over the world country wise from January 22,2020")
    st.dataframe(deaths_df)

    st.header("Recoveries  all over the world")
    st.markdown("The below table shows the list of all the Recoveries of Corona Virus cases  all over the world country wise from January 22,2020")
    st.dataframe(recoveries_df)



    st.header("Comparision between Coronavirus deaths vs Coronavirus recoveries")
    st.markdown("The below chart visualises the number of Corona Virus cases in major countries")

    plt.figure(figsize=(16,9))
    plt.plot(total_recovered, total_deaths)
    plt.title('# of Coronavirus Deaths vs. # of Coronavirus Recoveries', size=30)
    plt.xlabel('# of Coronavirus Recoveries', size=30)
    plt.ylabel('# of Coronavirus Deaths', size=30)
    plt.xticks(size=20)
    plt.yticks(size=20)
    st.pyplot()

    st.header("Number of Corona Virus recoveries")
    st.markdown("The below chart visualises the number of Corona Virus recoveries all over the world")

    plt.figure(figsize=(16,9))
    plt.plot(adjusted_dates, total_recovered, color='green')
    plt.title('# of Coronavirus Cases Recovered Over Time', size=30)
    plt.xlabel('Days Since 22/1/2020', size=30)
    plt.ylabel('# of Cases', size=30)
    plt.xticks(size=20)
    plt.yticks(size=20)
    st.pyplot()

    st.header("Number of Corona Virus deaths")
    st.markdown("The below chart visualises the number of Corona Virus deaths all over the world")

    plt.figure(figsize=(16, 9))
    plt.plot(adjusted_dates, total_deaths, color='red')
    plt.title('# of Coronavirus Deaths Over Time', size=30)
    plt.xlabel('Days Since 1/22/2020', size=30)
    plt.ylabel('# of Deaths', size=30)
    plt.xticks(size=20)
    plt.yticks(size=20)
    st.pyplot()

    st.header("Mortality rate of Coronavirus")
    st.markdown("The below chart visualises the number of Corona Virus deaths all over the world")

    mean_mortality_rate = np.mean(mortality_rate)
    plt.figure(figsize=(16, 9))
    plt.plot(adjusted_dates, mortality_rate, color='orange')
    plt.axhline(y = mean_mortality_rate,linestyle='--', color='black')
    plt.title('Mortality Rate of Coronavirus Over Time', size=30)
    plt.legend(['mortality rate', 'y='+str(mean_mortality_rate)], prop={'size': 20})
    plt.xlabel('Days Since 1/22/2020', size=30)
    plt.ylabel('Mortality Rate', size=30)
    plt.xticks(size=20)
    plt.yticks(size=20)
    st.pyplot()
else:
    #PRINTING THE COUNTRY SPECIFIC DATA

    latest_confirmed = confirm_case_df[dates[-1]]
    latest_deaths = deaths_df[dates[-1]]
    latest_recoveries = recoveries_df[dates[-1]]

    unique_countries =  list(confirm_case_df['Country/Region'].unique())

    country_confirm_cases = []
    no_cases = []
    for i in unique_countries:
        cases = latest_confirmed[confirm_case_df['Country/Region']==i].sum()
        if cases > 0:
            country_confirm_cases.append(cases)
        else:
            no_cases.append(i)
        
    for i in no_cases:
        unique_countries.remove(i)

    unique_countries = [k for k, v in sorted(zip(unique_countries, country_confirm_cases), key = operator.itemgetter(1), reverse=True)]
    for i in range(len(unique_countries)):
        country_confirm_cases[i] = latest_confirmed[confirm_case_df['Country/Region']==unique_countries[i]].sum()
     
       # number of cases per country/region
    st.markdown('This page shows the list of countries that are affected by Corona Virus and the number of victims in each countries')
    st.subheader('Confirmed Cases by Countries/Regions:')
    for i in range(len(unique_countries)):
        st.write(f'{unique_countries[i]}: {country_confirm_cases[i]} cases')




