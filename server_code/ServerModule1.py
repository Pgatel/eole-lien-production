import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables
import anvil.files
from anvil.files import data_files
import anvil.server
import pandas as pd

def csv_to_df(f):
  df = pd.read_csv(data_files[f], sep=';')
  return df

def prepare_data(df):
  df['Month'] = pd.to_datetime(df['Month'])
  return df

@anvil.server.callable
def explore():
  eole_df = csv_to_df('Résumé-2021-2023-Court.csv')
  print(eole_df.head())
  print(eole_df.columns)
  eole_df = prepare_data(eole_df)
  print(eole_df.head())

@anvil.server.callable
def create_plots():
  netflix_df, country_counts = prepare_netflix_data()

  fig1 = go.Figure(
    go.Scattergeo(
      locations=sorted(netflix_df['country'].unique().tolist()), 
      locationmode='country names',  
      text = country_counts['counts'],
      marker= dict(size= country_counts['counts'], sizemode = 'area')))

  fig2 = go.Figure(go.Pie(
    labels=netflix_df['type'], 
    values=netflix_df['type'].value_counts()
  ))
  
  fig3 = go.Figure(
    go.Scatter(
      x=netflix_df['date_added'].dt.year.value_counts().sort_index().index, 
      y=netflix_df['date_added'].dt.year.value_counts().sort_index()
    ))

  return fig1, fig2, fig3