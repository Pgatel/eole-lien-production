from ._anvil_designer import EoleLienProductionTemplate
from anvil import *
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables
import anvil.server
import plotly.graph_objects as go

class EoleLienProduction(EoleLienProductionTemplate):
  def __init__(self, **properties):
    # Set Form properties and Data Bindings.
    self.init_components(**properties)

    # Any code you write here will run before the form opens.
    fig = anvil.server.call('create_plots')
    self.plot_1.figure = fig

  def button_day_click(self, **event_args):
    """This method is called when the button is clicked"""
    open_form('EoleLienProductionDay')
