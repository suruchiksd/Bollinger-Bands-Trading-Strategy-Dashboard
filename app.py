import streamlit as st
import yfinance as yf
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt


# Function to fetch stock data
def get_stock_data(symbol, start, end):
    df = yf.download(symbol, start=start, end=end)
    return df


# Function to calculate Bollinger Bands
def bollinger_bands(df, window=20, std_multiplier=2):
    df = df.copy()
    df['SMA'] = df['Close'].rolling(window).mean()
    df['STD'] = df['Close'].rolling(window).std()

    df['Upper Band'] = df['SMA'] + (std_multiplier * df['STD'])
    df['Lower Band'] = df['SMA'] - (std_multiplier * df['STD'])

    # Drop NaN values to ensure alignment
    df.dropna(inplace=True)
    
    return df


# Function to generate Buy/Sell signals
def generate_signals(df):
    # Ensure 'Close' and 'Lower Band' are aligned
    df = df.copy()
    df = df.dropna()  # Remove rows with NaN values
    
    df["Buy Signal"] = df["Close"] < df["Lower Band"]
    df["Sell Signal"] = df["Close"] > df["Upper Band"]
    
    return df


# Function to plot the stock data with Bollinger Bands
def plot_bollinger_bands(df, symbol):
    plt.figure(figsize=(12, 6))
    plt.plot(df.index, df["Close"], label="Close Price", color="blue", alpha=0.5)
    plt.plot(
        df.index, df["Upper Band"], label="Upper Band", color="red", linestyle="dashed"
    )
    plt.plot(
        df.index,
        df["Lower Band"],
        label="Lower Band",
        color="green",
        linestyle="dashed",
    )
    plt.fill_between(
        df.index, df["Upper Band"], df["Lower Band"], color="gray", alpha=0.1
    )
    plt.scatter(
        df.index[df["Buy Signal"]],
        df["Close"][df["Buy Signal"]],
        marker="^",
        color="g",
        label="Buy Signal",
    )
    plt.scatter(
        df.index[df["Sell Signal"]],
        df["Close"][df["Sell Signal"]],
        marker="v",
        color="r",
        label="Sell Signal",
    )
    plt.title(f"Bollinger Bands for {symbol}")
    plt.legend()
    st.pyplot(plt)


# Streamlit UI
st.title("Bollinger Bands Trading Dashboard")

# User input for stock selection and date range
symbol = st.text_input("Enter Stock Symbol (e.g., AAPL, TSLA, MSFT)", "AAPL")
start_date = st.date_input("Start Date", pd.to_datetime("2023-01-01"))
end_date = st.date_input("End Date", pd.to_datetime("today"))

if st.button("Analyze"):
    with st.spinner("Fetching Data..."):
        data = get_stock_data(symbol, start_date, end_date)
        data = bollinger_bands(data)
        data = generate_signals(data)

        st.subheader(f"Stock Data for {symbol}")
        st.write(data.tail())

        # Plot Bollinger Bands
        plot_bollinger_bands(data, symbol)
