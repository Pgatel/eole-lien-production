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
    anvil.server.call('reset_sqlalchemy_session')
    s_df = anvil.server.call('get_months')
    s_total = anvil.server.call('get_sum_per_year')

    l_total = s_total.strip('[]').replace('"', '').split(', ')
    fig = anvil.server.call('create_plots', s_df)
    self.plot_1.figure = fig
    l_year = [i for i in range(2022, 2026)]
    self.total1.text = "Total {}: {} MWh".format(l_year[0], l_total[0])
    self.total2.text = "Total {}: {} MWh".format(l_year[1], l_total[1])
    self.total3.text = "Total {}: {} MWh".format(l_year[2], l_total[2])
    self.total4.text = "Total {}: {} MWh".format(l_year[3], l_total[3])

  def button_day_click(self, **event_args):
    """This method is called when the button is clicked"""
    open_form('EoleLienProductionDay')
