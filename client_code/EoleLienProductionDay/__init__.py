from ._anvil_designer import EoleLienProductionDayTemplate
from anvil import *
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables
import anvil.server
from datetime import datetime, timedelta, date


class EoleLienProductionDay(EoleLienProductionDayTemplate):
  def __init__(self, **properties):
    # Set Form properties and Data Bindings.
    self.init_components(**properties)

    # Any code you write here will run before the form opens.
    to_day = date.today()
    self.this_day = to_day.timetuple().tm_yday
    self.this_year = to_day.year
    self.max_day = self.this_day
    self.max_year = self.this_year
    min_date = datetime.strptime(self.date_picker_1.min_date, '%d-%m-%Y')
    self.min_day = min_date.timetuple().tm_yday
    self.min_year = min_date.year

    self.date_picker_1.date = to_day.strftime('%d-%m-%Y')
    self.date_picker_1.max_date = to_day.strftime("%Y-%m-%d")

    """ 
    plot_day is a server call given by the service anvil_service_db
    running on Hostinger
    """
    fig = anvil.server.call('plot_day', self.this_day, self.this_year)
    self.plot_1.figure = fig


  def date_picker_1_change(self, **event_args):
    """This method is called when the selected date changes"""
    choosen_date = self.date_picker_1.date
    self.this_year = choosen_date.year
    self.this_day = choosen_date.timetuple().tm_yday
    
    fig = anvil.server.call('plot_day', self.this_day, self.this_year)
    self.plot_1.figure = fig

  def backward_click(self, **event_args):
    """This method is called when the button is clicked"""
    if self.this_day == self.min_day and self.this_year == self.min_year:
      return
    self.this_day -= 1
    if self.this_day == 0:
      self.this_day = 365
      self.this_year -= 1
    this_date = date(self.this_year, 1, 1) + timedelta(days=self.this_day - 1)
    self.date_picker_1.date = this_date.strftime('%d-%m-%Y')
    fig = anvil.server.call('plot_day', self.this_day, self.this_year)
    self.plot_1.figure = fig

  def forward_click(self, **event_args):
    """This method is called when the button is clicked"""
    if self.this_day == self.max_day and self.this_year == self.max_year:
      return
    self.this_day += 1
    if self.this_day == 366:
      self.this_day = 1
      self.this_year += 1
    this_date = date(self.this_year, 1, 1) + timedelta(days=self.this_day - 1)
    self.date_picker_1.date = this_date.strftime('%d-%m-%Y')
    fig = anvil.server.call('plot_day', self.this_day, self.this_year)
    self.plot_1.figure = fig

  def button_month_click(self, **event_args):
    """This method is called when the button is clicked"""
    #open_form('EoleLienProduction')
    fig = anvil.server.call('plot_month')
    self.plot_1.figure = fig

