from ._anvil_designer import PandaTemplate
from anvil import *
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables
import anvil.server
import plotly.graph_objects as go

class Panda(PandaTemplate):
  def __init__(self, **properties):
    # Set Form properties and Data Bindings.
    self.init_components(**properties)

    # Any code you write here will run before the form opens.
    fig = anvil.server.call('create_plots')
    self.plot_1.figure = fig
    self.plot_1.layout.yaxis.title = 'kWh'
    
