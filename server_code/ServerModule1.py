import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables
import anvil.files
from anvil.files import data_files
import anvil.server
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, date

@anvil.server.callable
def create_plots(s_df):
  l_total = [2501, 3251, 5625, 6525]
  data_json = pd.read_json(s_df)
  # Charger les données JSON dans un DataFrame
  eole_df = pd.DataFrame(list(data_json['MWh'].items()), columns=['Month', 'MWh'])
  eole_df.set_index('Month', inplace=True)
  l_production = eole_df['MWh'].to_list()
  print(l_production)
  st_production = [f'{prod:8.3f}' for prod in l_production]
  r_data = range(len(l_production))
  last = len(l_production) - 1
  st_production = [f'{prod:8.3f}' for prod in l_production]

  s_date = date.today()
  last_hover_template = f'At {s_date}:<BR><BR><b>%{{y:8.3f}} MWh</b><BR>'
  hover_template = ['<b>%{y:8.3f} MWh</b>' if i < last else last_hover_template for i in r_data]
  
  eole_df = eole_df.rename(columns={'Production': 'MWh', })
  
  fig = px.bar(eole_df, x=eole_df.index, y="MWh", color='MWh',
               barmode="group",
               text=st_production,
               color_continuous_scale=['PowderBlue', 'SkyBlue', 'Teal', '#004d4d'],
              )
  fig.update_layout(font_family='Arial', title_font_size=24,
                    margin={'l': 10, 'r': 10, 't': 10, 'b': 10}, 
                    hovermode='x unified', hoverlabel=dict(bgcolor='white'),
                   )
  fig.update_traces(hovertemplate=hover_template, hovertext=st_production)
  fig.update_xaxes(dtick='M1', tickformat='%b-%Y')

  last_hover_template = f'Partial<BR>At {s_date}:<BR><BR><b>%{{y:8.3f}} MWh</b><BR>'
  hover_template = ['<b>%{y:8.3f} MWh</b>' if i < last else last_hover_template for i in r_data]
  color_lines = [l_production[i] if i < last else 'gold' for i in r_data]
  normal_marker = dict(line=dict(width=1, color='Teal'), )
  last_marker = dict(line=dict(width=2, color='red'), )
  fig.update_traces(hovertemplate=hover_template, hovertext=st_production,
                  marker=dict(line=dict(width=1, color='White'), ), )

  markers = fig.data[0].marker
  markers = go.bar.Marker(color=color_lines, colorscale=['PowderBlue', 'SkyBlue', 'Teal', '#004d4d'])
  markers.colorbar = go.bar.marker.ColorBar(bgcolor='white', title=dict(font=dict(family='Arial', size=12), text='MWh'),
                                          outlinecolor='White')
  fig.data[0].marker = markers

  fig.update_xaxes(showspikes=True, spikecolor="green", spikesnap="cursor", spikemode="across")
  fig.update_yaxes(showspikes=True, spikecolor="orange", spikethickness=2)
  fig.update_layout(spikedistance=1000, hoverdistance=100)
  return fig, l_total

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
