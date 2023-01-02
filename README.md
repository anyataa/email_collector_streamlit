
# GoodSale Email Collector Interactive Dashboard
<p align="center"><img src="https://media.giphy.com/media/Y48tUO0hMtxaFLfIc8/giphy.gif"></p>
<p align="center">
  <a href="https://email-collector-goodsale.streamlit.app/#sku-quantity-related-data">Website</a> •
  <a href="#features">Features</a> •
  <a href="https://www.linkedin.com/in/anya-tamara-akbar-74555514a/">Linkedin</a> •
  <a href="https://github.com/anyataa/email_collector_streamlit/issues">Issues</a> •
  <a href="#license">License</a>
</p>

Head over to my deployed GoodSale Interactive Dashboard [website](https://email-collector-goodsale.streamlit.app/#sku-quantity-related-data) for a demo.  
The source code of this project is available online on my [github](https://github.com/anyataa/email_collector_streamlit/edit/main/README.md#features).    

# Features
* Visualize data in tabular format
* Visualize data in bar format
* Download data visualization
* Convert .txt to .csv
* Convert .xlsx (excel) to csv
* Download converted .csv file 

# Main Tech Stack
* Google Cloud Platform 
file storage for the reports only in .csv format to maintain unify files in the main data base
* Github
to store the repository and to support future colaborativity possibility
* Streamlit 
to visualize the data and CI/CD by connecting the streamlit app and GitHub repository

# Business Problem 
GoodSale is a national retailer with stores across the UK. You are the Assistant Sales Manager at the
headquarters. Every morning, you receive emails from the regional offices with the sales reports from
the previous business day. As some offices still use a legacy system, the report you received may be
attached as Excel or CSV files. Occasionally, the report may be included in the email as plain text. You
need to integrate the data from these reports into a central file stored in your computer. After that,
you will analyze the data and then create a summary report that will be sent to the sales manager,
via email.

# GoodSale Application Overview

This application supports two main function:
* Data visualization
Managers able to visualize the quantity of stocks and download the visualization to support their report. This interactive dashboard could ease managers in accessing and visualizing the report data anywhere and anythime. Furthermore, the data being centralized in GCP which makes this application scallable. Lastly, the data is secured in the cloud which makes the data more prone to any accidental loss due to system failures. 

* Upload - Convert - Download
This features aimed for database admin to ease the process of saving the data to GCP 
## Getting Started

# Repository and File Description
### [folder](https://github.com/anyataa/email_collector_streamlit/tree/main/data) data
mock data for testing purpose
### [folder](https://github.com/anyataa/email_collector_streamlit/tree/main/streamlit) streamlit
main folder for files related to streamlit
* [folder](https://github.com/anyataa/email_collector_streamlit/tree/main/streamlit/env) env
Python environment contains list of packages and modules used for this application development
* [file](https://github.com/anyataa/email_collector_streamlit/blob/main/streamlit/requirements.txt) requirements.txt 
this file contains list of modules required modules that needs to be installed by Streamlit deployment pipeline
* [file] (https://github.com/anyataa/email_collector_streamlit/blob/main/streamlit/streamlit.py) streamlit.py
main file where all codes exist from upload mechanism to visualization. More details regarding the code structure explained in comment-mechanism inside the file
*[file](https://github.com/anyataa/email_collector_streamlit/blob/main/.gitignore) .gitignore
prevent file that contains data-sensitive information being pushed to github. In this case, .toml file contains GCP credential access


# License
[MIT](https://tldrlegal.com/license/mit-license)

## Contributing
GoodSale Interactive Dashboard is a personal project but your are welcome to contribute and submit a pull request!
