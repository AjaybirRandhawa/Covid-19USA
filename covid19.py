import numpy as np 
import pandas as pd 
import matplotlib.pyplot as plt
import plotly.express as px
import warnings
warnings.filterwarnings('ignore')
import plotly.graph_objects as go
import plotly.express as px


plt.rcParams["figure.figsize"] = (10,5)
pd.options.display.max_columns = 1000
df = pd.read_csv("../input/us-counties-covid-19-dataset/us-counties.csv")
df.head()

#Now drop the fips column
df.drop(columns="fips").describe()

print("Number of counties: ", df.county.nunique())
fig, axis = plt.subplots(2,1, figsize = (12,10))
df.groupby("date").agg({"cases": "sum"}).plot(ax = fig.axes[0])
df.groupby("date").agg({"deaths": "sum"}).plot(ax = fig.axes[1])
fig.axes[0].set_title("Confirmed Cases")
fig.axes[1].set_title("Fatalities")

cols = ['cases', 'deaths']
DF = df[df['date']==max(df['date'])].reset_index()
df1 = DF.groupby(['date'])[['cases','deaths']].sum().reset_index()
values = df1.loc[0,cols]
fig = px.pie(df1,values=values,names=cols)
fig.update_layout(title='Cases to date:'+str(df1['cases'][0]))

df2 = df.groupby('date')[['cases','deaths']].sum().reset_index()
df2 = df2.sort_values(by='date',ascending=True).reset_index()
df2.drop(['index'],axis=1,inplace=True)
df2.head()

splot = go.Figure()
splot.add_trace(go.Scatter(x=df2.index,y=df2.cases,mode='lines',name='Total cases'))
splot.update_layout(title='Rate of infection with respect to time',xaxis_title='Days',yaxis_title='Total cases',template='plotly_dark')
splot.show()

#Deaths with respect to Time
splot3 = go.Figure()
splot3.add_trace(go.Scatter(x=df2.index,y=df2.deaths,mode='lines',name='Deaths',marker_color='red'))
splot3.update_layout(title='Death toll with resepct to time',xaxis_title='Days',yaxis_title='Deaths',template='plotly_dark')

df3 = df.sort_values('cases',ascending=False).reset_index(drop=True)
df3.drop_duplicates(subset='state', keep='first', inplace=True)
df3.drop(['county', 'fips','date'],axis=1,inplace=True)
df3 = df3.reset_index(drop=True)
states_shortform = {'Alabama': 'AL', 
                    'Alaska':'AK',
                    'Arizona':'AZ',
                    'Arkansas':'AR',
                    'California':'CA',
                    'Colorado':'CO',
                    'Connecticut': 'CT',
                    'Delaware':'DE',
                    'District of Columbia': 'DC',
                    'Florida':'FL',
                    'Georgia':'GA',
                    'Guam':'GU',
                    'Hawaii':'HI',
                    'Idaho':'ID',
                    'Illinois':'IL',
                    'Indiana':'IN',
                    'Iowa':'IA',
                    'Kansas':'KS',
                    'Kentucky':'KY',
                    'Louisiana':'LA',
                    'Maine':'ME',
                    'Maryland':'MD',
                    'Massachusetts':'MA',
                    'Michigan':'MI',
                    'Minnesota':'MN',
                    'Mississippi':'MS',
                    'Missouri':'MO',
                    'Montana':'MT',
                    'Nebraska':'NE',
                    'Nevada':'NV',
                    'New Hampshire':'NH',
                    'New Jersey':'NJ',
                    'New Mexico':'NM',
                    'New York':'NY',
                    'North Carolina':'NC',
                    'North Dakota':'ND',
                    'Northern Mariana Islands':'MP',
                    'Ohio':'OH',
                    'Oklahoma':'OK',
                    'Oregon':'OR',
                    'Pennsylvania':'PA',
                    'Puerto Rico':'PR',
                    'Rhode Island':'RI',
                    'South Carolina':'SC',
                    'South Dakota':'SD',
                    'Tennessee':'TN',
                    'Texas':'TX',
                    'Utah':'UT',
                    'Vermont':'VT',
                    'Virginia':'VA',
                    'Virgin Islands':'VG',
                    'Washington':'WA',
                    'West Virginia':'WV',
                    'Wisconsin':'WI',
                    'Wyoming':'WY'
                   }
for state in df3['state']:
    df3['state'] = df3['state'].replace(state,states_shortform[state])
df3

m1 = px.choropleth(df3,locations='state',scope='usa',locationmode='USA-states',color='cases',hover_name='state')
m1.update_layout(title='Confirmed cases in each state')
m1.show()

m2 = px.choropleth(df3,locations='state',scope='usa',locationmode='USA-states',color='deaths',hover_name='state')
m2.update_layout(title='Confirmed deaths in each state')
m2.show()
