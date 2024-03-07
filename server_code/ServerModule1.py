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
  data = app_tables.productionmensuelle.search()
  data_list = [dict(row) for row in data]
  eole_df = pd.DataFrame(data_list)
  eole_df.set_index('Month', inplace=True)
       
  # Make the plot!
  lt_production = eole_df.itertuples(index=False)
  print(lt_production)
  lc_production = eole_df['Production']
  print(lc_production)
  st_production = [f'{prod:8.3f}' for prod in eole_df['Production'].to_list()]
  sc_production = [prod for prod in lc_production]
  fig2 = px.bar(eole_df, x=eole_df.index, y="Production", color=sc_production,
                barmode="group",
                text=st_production,
                color_continuous_scale='mint',
               )
  fig2.update_layout(font_family='Arial', title_font_size=24,
                     margin={'l': 10, 'r': 10, 't': 10, 'b': 10})
  fig2.update_xaxes(tickangle=90, dtick='M1')
  fig2.update_yaxes(dtick=100, title='MWh')
  return fig2

@anvil.server.callable
def get_production(): 
  rows = app_tables.productionmensuelle.search()
  return rows

@anvil.server.callable
def set_production(year, month, production, complete): 
  date0 = date(year=year, month=month, day=1)
  print(f'month={date0} production={production}')
  row = app_tables.productionmensuelle.get(Month=date0)
  if row is None:
    app_tables.productionmensuelle.add_row(Month=date0, Production=production, Complete=complete)
  else:
    print(f"month={row['Month']} Production={row['Production']}")
    row['Production'] = production
    row['Complete'] = complete
