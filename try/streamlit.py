import streamlit as st
import pandas as pd
import numpy as np
from google.oauth2 import service_account
from google.cloud import storage
from io import StringIO
import plotly.express as px
import requests
import os
from streamlit_lottie import st_lottie


######################################################
#################### WEB HEADING #####################
######################################################
def load_lottieurl(url: str):
    r = requests.get(url)
    if r.status_code != 200:
        return None
    return r.json()

lottie_book = load_lottieurl("https://assets1.lottiefiles.com/packages/lf20_8vcvc00i.json")
st_lottie(lottie_book, speed=1, height=200, key="initial")
st.title("Email Report Data Visualization")
st.subheader("Besco in the UK")
####################### END #########################
#################### WEB HEADING #####################
######################################################


######################################################
############# Google Cloud Storage (GCS) #############
######################################################
# Notes: 
# All code with comment line starts with GCP would perform certain CRUD action 
# This covers: Retrive and connection
# GCP - Create API client
credentials = service_account.Credentials.from_service_account_info(
    st.secrets["gcp_service_account"]
)
client = storage.Client(credentials=credentials)
# GCP - Bucket name
bucket_name = "db_email_reports_anya"
####################### END #########################
############# Google Cloud Storage (GCS) #############
######################################################

def list_blobs(bucket_name):
    """
    Action : List all the blobs in the bucket
    Parameter: 
        1. bucker_name: Bucket name in GCP which files stored [string]
    """

    # GCP - client.list_blobs : get all files inside the bucket
    blobs = client.list_blobs(bucket_name)

    # The afforementioned function return 'Iterator'. Thus, we implement for loop to generate list to be consumed by st.selectbox
    file_list = []
    for blob in blobs:
        file_list.append(blob.name)
    
    dataframe_file_list = pd.DataFrame(file_list, columns= ['file_name'])
    return dataframe_file_list

######################################################
####################### SIDE BAR #####################
######################################################
# Dropdown
st.sidebar.title("Later")
####################### END #########################
####################### SIDE BAR #####################
######################################################


######################################################
################## VISUALIZATION #####################
######################################################

# GCP - Retrieve file contents
# Uses st.experimental_memo to only rerun when the query changes or after 10 min.
@st.experimental_memo(ttl=600)
def read_file(bucket_name, file_path):
    bucket = client.bucket(bucket_name)
    # CONVERT DATA
    file_ext = os.path.splitext(selected_file)[1]
    if file_ext==".csv":
        content = bucket.blob(file_path).download_as_string().decode("utf-8")
        string_format = StringIO(content)
        return string_format

# Function: Generate Table 
def generate_table(df):
    st.write(df)
files_gcs = list_blobs(bucket_name=bucket_name)
selected_file = st.selectbox(
     "Choose report to analyze and visualize",
     (files_gcs)
     )
content = read_file(bucket_name, selected_file)
df = pd.read_csv(content, sep=",")

row1_1, row1_2 = st.columns(2, gap="large")
with row1_1:
    st.subheader("Data SKU overview")
    generate_table(df)

with row1_2:
    st.subheader("SKU quantity-related data")
    quantity_data = df[["Stock", "Loss", "Return"]]
    st.bar_chart(quantity_data)

row2_1, row2_2 = st.columns(2, gap="large")
with row2_1:
    st.subheader("Total Revenue per SKU")
    revenue_df = pd.DataFrame({"SKU": (df["SKU"]),"Total Revenue": (df["Sales"] * df["Current Price"])})
    st.write(revenue_df)
 
with row2_2:
    fig = px.bar(
       revenue_df,
        x="SKU",
        y="Total Revenue",
        title="Revenue Visualization (in Pounds)",
        color_discrete_sequence=["#9EE6CF"]
        )
    st.plotly_chart(fig, theme="streamlit", use_container_width=True)
####################### END #########################
################## VISUALIZATION #####################
######################################################


######################################################
#############  UPLOADER AND CONVERTER ################
######################################################
def create_download_button(input_file, button_label):
    st.download_button(
            label=button_label,
            data=input_file,
            file_name='GoodSale/converted_df.csv',
            mime='text/csv'
        )

uploaded_file = st.file_uploader("Choose a file")

if uploaded_file is not None:
    # Can be used wherever a "file-like" object is accepted:
    file_extension = os.path.splitext(uploaded_file.name)[1]
   
    # Handling excel file to be converted 
    if file_extension == ".xlsx":
        # Pandas need additional engine due to its incapability to read excell without openpyxl support
        # More details: https://pandas.pydata.org/pandas-docs/stable/reference/api/pandas.read_excel.html
        excel_file = pd.read_excel(uploaded_file, engine='openpyxl')
        st.write(excel_file)
        converted_to_csv = excel_file.to_csv(
                            index=None,
                            header=True)
            
        st.subheader(f"Converter from {file_extension} to CSV")
        create_download_button(converted_to_csv, "Download CSV file from Excel")
    
    # Convert .txt file
    elif file_extension == ".txt":
        text_file = pd.read_csv(uploaded_file)
        st.write(text_file)
        converted_to_csv = text_file.to_csv(
                            index=None,
                            header=True)

        st.subheader(f"Converter from {file_extension} to CSV")
        create_download_button(converted_to_csv, "Download CSV file from Text file")

    elif file_extension == ".csv":
        st.title(uploaded_file.name + file_extension)
        dataframe = pd.read_csv(uploaded_file)
        st.write(dataframe)
    
    else:
        st.title("File format is not supported")
        st.subheader("Please input supported file extension (.xlsx or .csv or .txt)")
####################### END #########################
#############  UPLOADER AND CONVERTER ################
######################################################