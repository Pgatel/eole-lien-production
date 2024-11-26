from ._anvil_designer import EoleLienProductionTemplate
from anvil import *
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables
import anvil.server
import plotly.graph_objects as go
def error_handler(err):
  alert(str(err), title="An error has occurred")

class EoleLienProduction(EoleLienProductionTemplate):

  def __init__(self, **properties):
    # Set Form properties and Data Bindings.
    self.init_components(**properties)
    set_default_error_handling(error_handler)

    # Any code you write here will run before the form opens.
    s_df = anvil.server.call('get_months')
    fig = anvil.server.call('create_plots', s_df)
    self.plot_1.figure = fig

  def button_day_click(self, **event_args):
    """This method is called when the button is clicked"""
    open_form('EoleLienProductionDay')
