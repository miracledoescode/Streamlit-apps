import streamlit as st
import plotly.express as px
import os
import json
import pandas as pd


st.set_page_config(page_title="Simple Finance App ", page_icon="💰", layout="wide")

def load_transactions(file):
	try:
		df = pd.read_csv(file)
		df.columns = [col.strip() for col in df.columns]
		df["AMOUNT in naira"] = df["AMOUNT in naira"].astype(float)
		st.write(df)
		return df
	except Exception as e:
		st.error(f"Error processing file: {str(e)}")
		return None

def main():
	st.title("Simple finance Dashboard")
	
	uploaded_file = st.file_uploader("Upload your transactions Csv file", type=["csv"])
	
	if uploaded_file is not None:
		df = load_transactions(uploaded_file)
		
if __name__ == "__main__":
	main()