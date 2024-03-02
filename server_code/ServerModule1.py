import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables
import anvil.files
from anvil.files import data_files
import anvil.server
import pandas as pd
import plotly.graph_objects as go

@anvil.server.callable
def create_plots():
  file = data_files['Résumé-2021-2023-Court.csv']
  eole_df = pd.read_csv(file, sep=';')
  eole_df['Month'] = pd.to_datetime(eole_df['Month'], dayfirst=True)
  figure = go.Figure(
    go.Bar(
      x=eole_df['Month'],
      y=eole_df['Total (MWh)'],
    ))
  figure.update_layout(
      margin=dict(t=10, b=30, l=10, r=10),
      xhoverformat = '%Y-%m')
  return figure

  