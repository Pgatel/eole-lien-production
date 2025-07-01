import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables
import anvil.files
from anvil.files import data_files
import anvil.server
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.graph_objs import Figure, Bar, Layout
from datetime import datetime, date

@anvil.server.callable
def create_plots(s_df):
  data_json = pd.read_json(s_df)
  # Charger les données JSON dans un DataFrame
  eole_df = pd.DataFrame(list(data_json['MWh'].items()), columns=['Month', 'MWh'])
  eole_df.set_index('Month', inplace=True)
  eole_df.index = pd.to_datetime(eole_df.index)

  #  eole_df = eole_df.rename(columns={'Production': 'MWh', })
  # Année de référence = année courante - 3
  annee_debut = pd.Timestamp.today().year - 3

  # Début à partir du 1er janvier de cette année
  date_debut = pd.Timestamp(f"{annee_debut}-01-01")

  # Filtrage du DataFrame
  eole_df_recent = eole_df[eole_df.index >= date_debut]  # Filtrage du DataFrame

  l_production = eole_df_recent['MWh'].to_list()
  r_data = range(len(l_production))
  last = len(l_production) - 1
  st_production = [f'{prod:8.3f}' for prod in l_production]

  s_date = date.today()
  last_hover_template = f'At {s_date}:<BR><BR><b>%{{y:8.3f}} MWh</b><BR>'
  hover_template = ['<b>%{y:8.3f} MWh</b>' if i < last else last_hover_template for i in r_data]
  
  x_vals = [str(m) for m in eole_df_recent.index]
  y_vals = eole_df_recent["MWh"].tolist()

  colors = [[0.0, 'PowderBlue'], [0.33, 'SkyBlue'], [0.66, 'Teal'], [1.0, '#004d4d']]

  fig = Figure(data=[Bar(
            name='Production',
            x=x_vals,
            y=y_vals,
            text=[f"{v:.3f} MWh" for v in y_vals],       # Affichage des valeurs entières
            textposition="inside",                  # Position : "outside", "inside", "auto"
            marker=dict(
              color=y_vals,
              colorscale=colors,
              colorbar=dict(title="MWh")
            )
        )
    ],
    layout=Layout(
        xaxis={"title": "Mois", "tickangle": -90},
        yaxis={"title": "MWh"}
    )
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
