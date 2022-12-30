import streamlit as st
import pandas as pd
import numpy as np
from google.oauth2 import service_account
from google.cloud import storage
from io import StringIO
import plotly.express as px
import os

st.title('Email Report Storage')

'''
Google Cloud Storage (GCS)
Create API client: set connection and provide key credential to form the connection to GCS
Bucket name: the name of folder/bucket to store all the uploaded files

Notes: 
All code with comment line starts with GCP would perform certain CRUD action 
This covers:
GCP - Read (Retrieve)
GCP - Create (Upload)
'''
# Create API client
credentials = service_account.Credentials.from_service_account_info(
    st.secrets["gcp_service_account"]
)
client = storage.Client(credentials=credentials)
# Bucket name
bucket_name = "db_email_reports_anya"
file_path = "mock.csv"

# visualization


# GCP - Retrieve file contents
# Uses st.experimental_memo to only rerun when the query changes or after 10 min.
@st.experimental_memo(ttl=600)
def read_file(bucket_name, file_path):
    bucket = client.bucket(bucket_name)
    content = bucket.blob(file_path).download_as_string().decode("utf-8")
    return content



content = read_file(bucket_name, file_path)

def generate_table(content):

    stringIO = StringIO(content)
    df = pd.read_csv(stringIO, sep=",")
    st.write(df)


generate_table(content)


def list_blobs(bucket_name):
    """Lists all the blobs in the bucket."""

    # Note: Client.list_blobs requires at least package version 1.17.0.
    blobs = client.list_blobs(bucket_name)

    # Note: The call returns a response only when the iterator is consumed.
    for blob in blobs:
        print(blob.name)
        st.write(blob.name)

files_gcs = list_blobs(bucket_name=bucket_name)
# dropdown
clist = list_blobs
# Using object notation
add_selectbox = st.sidebar.selectbox(
    "How would you like to be contacted?",
    ("Email", "Home phone", "Mobile phone")
)

# getting path of the file because st.file_uploader does not return path 
st.title("Get Path")
def file_selector(folder_path='./data'):
    filenames = os.listdir(folder_path)
    selected_filename = st.selectbox('Select a file', filenames)
    if selected_filename is not None:
        st.write(os.path.join(folder_path, selected_filename))
        return os.path.join(folder_path, selected_filename)
file_selector()


# Upload
uploaded_file = st.file_uploader("Choose a file")
if uploaded_file is not None:
    # Can be used wherever a "file-like" object is accepted:
    st.title("Uploaded File Shown Below")
    dataframe = pd.read_csv(uploaded_file)
    st.write(dataframe)
    



    
# try to upload
bucket = client.bucket(bucket_name)
# blob = bucket.blob(uploaded_file.name)
# blob.upload_from_filename(uploaded_file.name)
