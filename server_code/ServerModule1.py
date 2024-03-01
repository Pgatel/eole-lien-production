import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables
import anvil.files
from anvil.files import data_files
import anvil.server
import pandas as pd

def csv_to_df(f):
  df = pd.read_csv(data_files[f], index_col=0, sep=';')
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
