import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables
import anvil.files
from anvil.files import data_files
import anvil.server
import pandas as pd
import plotly.express as px
from datetime import date

@anvil.server.callable
def create_plots():
  data = app_tables.productionmensuelle.search()
  data_list = [dict(row) for row in data]
  eole_df = pd.DataFrame(data_list)
  eole_df.set_index('Month', inplace=True)
  
  st_production = [f'{prod:8.3f}' for prod in eole_df['Production'].to_list()]
  eole_df = eole_df.rename(columns={'Production': 'MWh', })

  fig = px.bar(eole_df, x=eole_df.index, y="MWh", color='MWh',
               barmode="group",
               text=st_production, hover_data={'MWh'},
               color_continuous_scale='mint',
              )
  fig.update_traces(hovertemplate=('<b>%{y:8.3f} MWh</b>'))
  fig.update_layout(font_family='Arial', title_font_size=24,
                    margin={'l': 10, 'r': 10, 't': 10, 'b': 10}, 
                    hovermode='x unified', hoverlabel=dict(bgcolor='white'),
                   )
  fig.update_xaxes(dtick='M1', tickformat='%b-%Y')
  fig.update_yaxes(dtick=100, title='MWh')
  return fig

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
