from pytest import mark
import streamlit as st
from yahoo_fin.stock_info import get_data
from yahoo_fin.stock_info import get_quote_data
import plotly.graph_objects as go
import altair as alt
import pandas as pd
from datetime import datetime

def get_worth(input):
    
    price = get_data(input, start_date="1/1/1900", end_date="12/31/2100", index_as_date = True, interval="1wk")
    
    price['year'] = price.index.year
    price['month'] = price.index.month
    
    merged_data = pd.merge(price, dollar_index, on=['year', 'month'])
    merged_data['worth'] = merged_data['close'] * merged_data['CUUR0000SA0R']
    merged_data.set_index(price.index, inplace=True)
    
    shares_outstanding = get_quote_data(input)['sharesOutstanding']
    merged_data['cap'] = merged_data['worth'] * shares_outstanding / (1000000000 * dollar_index.iloc[-1,0])
    merged_data.rename(columns={'cap':input}, inplace=True)
        
    return merged_data.loc[:,input]
    
def dollar_index_preprocessing():
    dollar_index = pd.read_csv('/Volumes/GoogleDrive-111094423641400606317/My Drive/projects/22_05_Quantamental_project/data/indicator/CUUR0000SA0R.csv')
    dollar_index['DATE'] = pd.to_datetime(dollar_index['DATE'])
    dollar_index['year'] = dollar_index['DATE'].dt.year
    dollar_index['month'] = dollar_index['DATE'].dt.month
    dollar_index.drop('DATE', axis=1, inplace=True)
    dollar_index.loc[len(dollar_index)] = [dollar_index.iloc[-1,0], dollar_index.iloc[-1,1], dollar_index.iloc[-1,2]+1]
    
    return dollar_index


def get_worth_and_merge(worth, input):
    worth_tmp = get_worth(input)
    worth = pd.merge(worth, worth_tmp, left_index=True, right_index=True , how='outer')
    return worth

# dollar index preprocessing
dollar_index = dollar_index_preprocessing()


st.title("Screener")
col1, col2 = st.columns(2)
col3, col4 = st.columns(2)
input_a = col1.text_input("Ticker A").upper()
input_b = col2.text_input("Ticker B").upper()
input_c = col3.text_input("Ticker C").upper()
input_d = col4.text_input("Ticker D").upper()

worth = None

if input_a != '': worth = pd.DataFrame(get_worth(input_a))

other_inputs = [input_b, input_c, input_d]

for other_input in other_inputs :
    if other_input != '': worth = get_worth_and_merge(worth, other_input)

if type(worth) == pd.DataFrame:
    
    min_time = min(worth.index)
    max_time = max(worth.index)
    start_date, end_date = st.slider('Select Timeline', 
                                     value = (datetime(min_time.year, min_time.month, min_time.day), 
                                              datetime(max_time.year, max_time.month, max_time.day)),
                                     format="YY/MM/DD"
                                     )
    worth_in_time = worth[start_date:end_date]
    
    st.line_chart(worth_in_time)
    



