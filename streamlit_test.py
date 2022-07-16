from pytest import mark
import streamlit as st
from yahoo_fin.stock_info import get_data
from yahoo_fin.stock_info import get_quote_data
import plotly.graph_objects as go
import altair as alt
import pandas as pd

def get_worth(input):
    
    price = get_data(input, start_date="1/1/1900", end_date="12/31/2100", index_as_date = True, interval="1d")
    
    price['year'] = price.index.year
    price['month'] = price.index.month
    
    merged_data = pd.merge(price, dollar_index, on=['year', 'month'])
    merged_data['worth'] = merged_data['close'] * merged_data['CUUR0000SA0R']
    merged_data.set_index(price.index, inplace=True)
    
    shares_outstanding = get_quote_data(input)['sharesOutstanding']
    
    merged_data['cap'] = merged_data['worth'] * shares_outstanding
        
    return merged_data.loc[:,'cap']
    
def dollar_index_preprocessing():
    dollar_index = pd.read_csv('/Volumes/GoogleDrive-111094423641400606317/My Drive/projects/22_05_Quantamental_project/data/indicator/CUUR0000SA0R.csv')
    dollar_index['DATE'] = pd.to_datetime(dollar_index['DATE'])
    dollar_index['year'] = dollar_index['DATE'].dt.year
    dollar_index['month'] = dollar_index['DATE'].dt.month
    dollar_index.drop('DATE', axis=1, inplace=True)
    dollar_index.loc[len(dollar_index)] = [dollar_index.iloc[-1,0], dollar_index.iloc[-1,1], dollar_index.iloc[-1,2]+1]
    
    return dollar_index

# dollar index preprocessing
dollar_index = dollar_index_preprocessing()


st.title("Super Screener")
col1, col2 = st.columns(2)
input_a = col1.text_input("Ticker A").upper()
input_b = col2.text_input("Ticker B").upper()


if input_a != '':
    worth_a = get_worth(input_a)
    price_chart = st.line_chart(worth_a)
    # fig = go.Figure()
    # fig.add_trace(go.Scatter(x=market_cap_a.index, y=market_cap_a))
    # chart = st.plotly_chart(fig)

if input_b != '':
    worth_b = get_worth(input_b)
    price_chart.add_rows(worth_b)
    # fig.add_trace(go.Scatter(x=market_cap_b.index, y=market_cap_b))
    # chart.
    



