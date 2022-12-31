import streamlit as st
import pandas as pd
import numpy as np
from google.oauth2 import service_account
from google.cloud import storage
from io import StringIO
import plotly.express as px
import os


st.title("Email Report Storage")


# Google Cloud Storage (GCS)
# Create API client: set connection and provide key credential to form the connection to GCS
# Bucket name: the name of folder/bucket to store all the uploaded files

# Notes: 
# All code with comment line starts with GCP would perform certain CRUD action 
# This covers:
# GCP - Read (Retrieve)
# GCP - Create (Upload)


# Create API client
credentials = service_account.Credentials.from_service_account_info(
    st.secrets["gcp_service_account"]
)
client = storage.Client(credentials=credentials)
# Bucket name
bucket_name = "db_email_reports_anya"


def list_blobs(bucket_name):
    """Lists all the blobs in the bucket."""

    # client.list_blobs : get all files inside the bucket
    blobs = client.list_blobs(bucket_name)

    # The call return 'Iterator'. Thus, we implement for loop to generate list to be consumed by st.selectbox
    file_list = []
    for blob in blobs:
        file_list.append(blob.name)
    
    dataframe_file_list = pd.DataFrame(file_list, columns= ['file_name'])
    return dataframe_file_list

# SIDE BAR
# Dropdown
st.sidebar.title("Later")
# SIDE BAR DONE

# GCP - Retrieve file contents
# Uses st.experimental_memo to only rerun when the query changes or after 10 min.
@st.experimental_memo(ttl=600)
def read_file(bucket_name, file_path):
    bucket = client.bucket(bucket_name)
    content = bucket.blob(file_path).download_as_string().decode("utf-8")
    string_format = StringIO(content)
    return string_format


# Function: Generate Table 
def generate_table(df):
    st.write(df)

# Visualization structure
row1_1, row1_2 = st.columns(2, gap="large")

with row1_1:
    files_gcs = list_blobs(bucket_name=bucket_name)
    selected_file = st.selectbox(
    "Desired data for monitoring and visualizing",
    (files_gcs)
    )
    content = read_file(bucket_name, selected_file)
    df = pd.read_csv(content, sep=",")
    generate_table(df)

with row1_2:
    generate_table(df)

row2_1, row2_2 = st.columns(2, gap="large")
with row2_1:
    st.subheader("Total Return Over the SKU")
    analyse_file = list_blobs(bucket_name=bucket_name)
    analyse_visual = st.selectbox(
        "Desired data for monitoring and visualizing", (files_gcs), key=1
        )
    loss_df = df
    st.write(loss_df)

with row2_2:
    st.subheader("Non- determined")
    st.bar_chart(df)

# Upload and visualize
uploaded_file = st.file_uploader("Choose a file")
if uploaded_file is not None:
    # Can be used wherever a "file-like" object is accepted:
    st.title("Uploaded File Shown Below")
    dataframe = pd.read_csv(uploaded_file)
    st.write(dataframe)
    
