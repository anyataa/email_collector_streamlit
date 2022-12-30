import streamlit as st
import pandas as pd
import numpy as np
from google.oauth2 import service_account
from google.cloud import storage
from io import StringIO
import plotly.express as px


st.title('Email Report Storage')


# Create API client.
credentials = service_account.Credentials.from_service_account_info(
    st.secrets["gcp_service_account"]
)
client = storage.Client(credentials=credentials)


# visualization


# Retrieve file contents.
# Uses st.experimental_memo to only rerun when the query changes or after 10 min.
@st.experimental_memo(ttl=600)
def read_file(bucket_name, file_path):
    bucket = client.bucket(bucket_name)
    content = bucket.blob(file_path).download_as_string().decode("utf-8")
    return content

bucket_name = "db_email_reports_anya"
file_path = "mock.csv"

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



# Upload
uploaded_file = st.file_uploader("Choose a file")
if uploaded_file is not None:
   

    # Can be used wherever a "file-like" object is accepted:
    dataframe = pd.read_csv(uploaded_file)
    st.write(dataframe)