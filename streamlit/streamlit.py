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

############ LAST COMMIT: 2 January 2023 ###############
##################### NOTE #############################
#####  This Project can be accessed online here: #######
### https://email-collector-goodsale.streamlit.app/ ####
############### Head over to this link #################
#######  To clone the FULL project repository: #########
# https://github.com/anyataa/email_collector_streamlit #
########################################################

######################################################
#################### ALL FUNCTION ####################
######################################################
def load_lottieurl(url: str):
    '''
    Action : List all the blobs in the bucket
    Parameter: 
    1. [string] online lottie file source
    '''
    r = requests.get(url)
    if r.status_code != 200:
        return None
    return r.json()

def create_download_button(input_file, button_label):
    """
    Action : Create download button
    Parameter: 
    1. input_file: [file in csv] file that users want to download
    2. button_label: [string] button label
    """
    return st.download_button(
            label=button_label,
            data=input_file,
            file_name='GoodSale/converted_df.csv',
            mime='text/csv'
        )

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

def generate_table(df):
    """
    Action : Generate table
    Parameter: 
    1. df: [csv format] data frame
    """
    st.write(df)
    
# GCP 
# Uses st.experimental_memo to only rerun when the query changes or after 10 min.
@st.experimental_memo(ttl=600)
def read_file(bucket_name, file_path):
    """
    Action : Retrieve file from GCP
    Parameter: 
    1. bucket_name: [string] name of GCP bucket
    2. file_path: [string] name of the file in GCP
    """

    bucket = client.bucket(bucket_name)
    
    # Convert data
    file_ext = os.path.splitext(selected_file)[1]
    if file_ext==".csv":
        content = bucket.blob(file_path).download_as_string().decode("utf-8")
        string_format = StringIO(content)
        return string_format
######################### END ########################
#################### ALL FUNCTION ####################
######################################################

######################################################
#################### WEB HEADING #####################
######################################################
lottie_book = load_lottieurl("https://assets1.lottiefiles.com/packages/lf20_8vcvc00i.json")
st_lottie(lottie_book, speed=1, height=200, key="initial")
st.title("Email Report Data Visualization")
st.subheader("GoodSale in the UK")
####################### END #########################
#################### WEB HEADING #####################
######################################################


##################### CONFIGURATION ##################
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


######################################################
####################### SIDE BAR #####################
######################################################
# Dropdown
st.sidebar.title("GoodSale Interactive Dashboard")
st.sidebar.subheader("1. Visualization")
st.sidebar.subheader("2. Upload -> Convert -> Download")
####################### END #########################
####################### SIDE BAR #####################
######################################################


######################################################
################## VISUALIZATION #####################
######################################################

st.title("Visualization and Download Report")

files_gcs = list_blobs(bucket_name=bucket_name)
selected_file = st.selectbox(
     "Choose report to analyze and visualize",
     (files_gcs)
     )
content = read_file(bucket_name, selected_file)
df = pd.read_csv(content)

row1_1, row1_2 = st.columns(2, gap="large")
with row1_1:
    create_download_button(df.to_csv(
                            index=None,
                            header=True), "Download SKU overview")
    st.subheader("Data SKU overview")
    generate_table(df)


with row1_2:
    if "Stock" in df:
        quantity_data = df[["Stock", "Loss", "Return"]]
        create_download_button(quantity_data.to_csv(
                              index=None,
                               header=True), "Download quantity data")
        st.subheader("Quantity Visualization")
        st.bar_chart(quantity_data)

    #category data for transaction visualization
    if "category" in df:
        category_data = df[["category"]]
        st.bar_chart(category_data)

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
st.title("Upload -> Convert -> Download")
uploaded_file = st.file_uploader("Choose a file")

if uploaded_file is not None:
    # Can be used wherever a "file-like" object is accepted:
    file_extension = os.path.splitext(uploaded_file.name)[1]
   
    # Convert .xlsx file 
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

    # Read .csv file
    elif file_extension == ".csv":
        st.title(uploaded_file.name + file_extension)
        dataframe = pd.read_csv(uploaded_file)
        st.write(dataframe)
    
    # Ask users to input supported file type
    else:
        st.title("File format is not supported")
        st.subheader("Please input supported file extension (.xlsx or .csv or .txt)")
####################### END #########################
#############  UPLOADER AND CONVERTER ################
######################################################