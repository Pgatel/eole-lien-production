import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables
import anvil.files
from anvil.files import data_files
import anvil.server
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
from datetime import date

@anvil.server.callable
def create_plots():
  file = data_files['Résumé-2021-2023-Court.csv']
  eole_df = pd.read_csv(file, sep=';')
  eole_df['Month'] = pd.to_datetime(eole_df['Month'], dayfirst=True)
     
    # Make the plot!
  fig2 = px.bar(eole_df, x="Month", y="Total (MWh)", color="Total (MWh)",
                barmode="group",
                text="Total (MWh)",
                color_continuous_scale='blugrn',
               )
  fig2.update_layout(font_family='Arial', title_font_size=24,
                     margin={'l': 10, 'r': 10, 't': 10, 'b': 10})
  fig2.update_xaxes(tickangle=90, dtick='M1')
  fig2.update_yaxes(dtick=100, title='kWh')
  return fig2

@anvil.server.callable
def get_production(): 
  rows = app_tables.productionmensuelle.search()
  return rows

@anvil.server.callable
def set_production(year, month, production): 
  date0 = date(year=year, month=month, day=1)
  print(f'month={date0} production={production}')
  row = app_tables.productionmensuelle.get(Month=date0)
  if row is None:
    app_tables.productionmensuelle.add_row(Month=date0, Production=production)
  else:
    print(f"month={row['Month']} Production={row['Production']}")
    row['Production'] = production

