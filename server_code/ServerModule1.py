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
def create_plots():
  data = app_tables.productionmensuelle.search()
  data_list = [dict(row) for row in data]
  eole_df = pd.DataFrame(data_list)
  eole_df.set_index('Month', inplace=True)
  l_production = eole_df['Production'].to_list()
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
  fig.update_yaxes(dtick=100, title='MWh')

  last_complete = eole_df['Complete'][last]
  print(last_complete)
  last_hover_template = f'Partial<BR>At {s_date}:<BR><BR><b>%{{y:8.3f}} MWh</b><BR>'
  hover_template = ['<b>%{y:8.3f} MWh</b>' if i < last or last_complete else last_hover_template for i in r_data]
  color_lines = [l_production[i] if i < last or last_complete else 'gold' for i in r_data]
  normal_marker = dict(line=dict(width=1, color='Teal'), )
  last_marker = dict(line=dict(width=2, color='red'), )
  lines = [normal_marker if i < len(st_production)-1 else last_marker for i in r_data]
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

@anvil.server.callable
def plot_day(day):
  data = app_tables.productionday.search(Day=day)
  print(data)
  l_date = [row['Date'] for row in data]
  l_power = [row['Power'] for row in data]
  dict_data = {'Date': l_date, 'Power': l_power}
  
  eole_df = pd.DataFrame(dict_data)
  eole_df.set_index('Date', inplace=True)
  
  st_power = [f'{prod:4.0f}' for prod in l_power]
  r_data = range(len(l_power))
  last = len(l_power) - 1

  fig = go.Figure()
  fig.add_trace(go.Scatter(x=eole_df.index, y=eole_df['Power'], name='Power', mode='lines+markers',
                           line={'color': 'purple'}))
  fig.update_layout(font_family='Arial', title_font_size=24,
                    margin={'l': 10, 'r': 10, 't': 10, 'b': 10},
                    hovermode='x unified', hoverlabel=dict(bgcolor='white'),
                    )
  fig.update_xaxes(tickangle=45, tickformat="%H:%M")
  fig.update_traces(textposition='bottom right', )

  fig.update_xaxes(showspikes=True, spikecolor="green", spikesnap="cursor", spikemode="across")
  fig.update_yaxes(showspikes=True, spikecolor="blue", spikethickness=2)
  fig.update_layout(spikedistance=1000, hoverdistance=100)
  return fig
