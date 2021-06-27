import os
import requests
import pandas as pd
from datetime import date

# Bokeh
from bokeh.plotting import figure
from bokeh.models.annotations import Title
from bokeh.embed import components
from bokeh.models import ColumnDataSource
#from bokeh.models.tools import HoverTool

# Get Key from Heroku config
alpha_key =  os.environ['ALPHA_KEY']

def fetch_stock_data(ticker,price_options):
  url = 'https://www.alphavantage.co/query?function=TIME_SERIES_DAILY_ADJUSTED&symbol={}&apikey={}'.format(ticker, alpha_key)
  response = requests.get(url)
  response_json = response.json()
  
  # Price options mapping
  options_dict = {'Open':'1. open',
               'High':'2. high',
               'Low':'3. low',
               'Close':'4. close',
               'Adjusted Close':'5. adjusted close'
               }
  
  # IBM color palette, should be colorblind accessible
  colors_dict = {'Open':'#648FFF',
               'High':'#785EF0',
               'Low':'#DC267F',
               'Close':'#FE6100',
               'Adjusted Close':'#FFB000'
               }
  
  # Initialize plot title
  if len(price_options) > 1:
    title = "Stock prices for {}: ".format(ticker) # else set later
  p = None # initialize so that we can test if plot exists yet
  print(price_options)
  
  # Build as many timeseries as requested in price options
  for option in price_options:
    price_type = options_dict[option]

    # Flatten to list of tuples
    response_list = [(date.fromisoformat(idx), float(value[price_type]))
                   for (idx, value) in response_json['Time Series (Daily)'].items()]

    # Put into pandas and bokeh
    prices = pd.DataFrame(data=response_list, columns=['Date', 'Price'])
    source = ColumnDataSource(data=prices)

    # create a new Bokeh plot with a title and axis labels
    option_string = (''.join([ch for ch in option if ch.isalpha()  or ch == ' '])).capitalize() + ' '
    if len(price_options) > 1:
      title += option_string + ' | '
    else:
      title = "{}prices for {}: ".format(option_string,ticker)
    
    if p is None: # just set up figure once
      if len(price_options) > 1:
        p = figure(x_axis_label='Date', x_axis_type="datetime",
                   y_axis_label='Price (USD)',toolbar_location="right") 
      else:
        y_axis_label = "{} price (USD)".format(option_string)
        p = figure(x_axis_label='Date', x_axis_type="datetime",
                   y_axis_label=y_axis_label,toolbar_location="right")
        
    p.line(x='Date', y='Price',
         source=source, line_width=2,
         color=colors_dict[option], alpha=0.6,legend_label=option)
  
  # Final figure formatting
  t = Title(); t.text = title # Can't just directly set plot title...
  p.title = t
  p.title.text_font_size = "18px"
  p.legend.location = "bottom_right"
  p.legend.click_policy="hide"
  p.xaxis.axis_label_text_font_size = "16pt"
  p.yaxis.axis_label_text_font_size = "16pt"
  p.xaxis.major_label_text_font_size = "12pt"
  p.yaxis.major_label_text_font_size = "12pt"


  # get components to embed in template
  script, div = components(p)
  return script, div, ticker
