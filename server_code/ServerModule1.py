import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables
import anvil.files
from anvil.files import data_files
import anvil.server
import pandas as pd
import plotly.graph_objects as go

def csv_to_df(f):
  df = pd.read_csv(data_files[f], sep=';')
  return df

def prepare_data():
  eole_df = csv_to_df()
  eole_df['Month'] = pd.to_datetime(eole_df['Month'])
  counts = pd.DataFrame(eole_df['Total (MWh)']).value_counts()
  print(counts)
  return eole_df, counts

@anvil.server.callable
def explore():
  eole_df = csv_to_df('Résumé-2021-2023-Court.csv')
  print(eole_df)
  print(eole_df.columns)
  eole_df = prepare_data()
  print(eole_df)
  return eole_df

@anvil.server.callable
def create_plots(df):
  eole_df, counts = prepare_data()
  fig3 = go.Figure(
    go.Scatter(
      x=eole_df['Month'].dt.year.value_counts().sort_index().index, 
      y=eole_df['Total (MWh)']
    ))
  return fig3
  