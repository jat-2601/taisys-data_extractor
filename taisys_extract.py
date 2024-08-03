# importing the required libraries
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st
import warnings
warnings.filterwarnings("ignore", category=UserWarning, module='openpyxl')


st.title("TCU 2.0 SUMMARY")
uploaded_file_ = st.file_uploader(label=" Upload the master data file ",
                                 accept_multiple_files=False,
                                 help=" Here, upload the downloaded master data file from "
                                      "taisys portal without any changes and file format shall be .xlsx only",
                                 label_visibility="collapsed")
try:
    # reading the file imported
    if uploaded_file_ is not None:
        data = pd.read_excel(uploaded_file_, dtype='object', engine='openpyxl')

        # PRINTING THE MASTER DATA WE IMPORTED
        st.title("MASTER DATA")
        st.write(data)

        # PLOTTING THE BOOTSTRAP VS OPERATIONAL COUNT OF DEVICES AVAILABLE
        try:
            st.title(" BOOTSTRAP VS ON-FIELD DEVICES")
            """
            Visual representing the total count of bootstrap and operational devices count.
            """
            bsvsop = px.bar(data['Network Mode'].value_counts(),
                            title = " BOOTSTRAP VS OPERATIONAL DEVICES COUNT ")
            st.plotly_chart(bsvsop)

            # OPERATIONAL DATA
            st.title("OPERATIONAL DEVICES DATA")
            """
            Here is the data for the on-field or operational devices.
            """
            operational_data = data.iloc[np.where(data['Operational Activation Date'].notnull())]
            st.write(operational_data)

            # MONTHWISE OPERATIONAL ACTIVATIONS PLOt
            st.title("Monthly Operational Activations")
            """
            Below is the plot visualizing the total count of operational activations on the monthly basis.
            """
            # Convert the date column to datetime format
            data['operational_activation_date'] = pd.to_datetime(data['Operational Activation Date'], format='%d-%m-%Y')

            # Extract month and year
            data['operational_month_year'] = data['operational_activation_date'].dt.strftime('%Y-%m')

            # Group by month and year, and count occurrences
            month_counts = data.groupby('operational_month_year').size().reset_index(name='counts')

            # Plot the counts using Plotly
            fig_monthwise = px.bar(month_counts, x='operational_month_year', y='counts',
                                   title=" Monthwise Operational Activation  Counts")
            st.plotly_chart(fig_monthwise)

            # DAYWISE OPERATIONAL ACTIVATIONS PLOT

            # Convert the date column to datetime format
            data['operational_activation_date'] = pd.to_datetime(data['Operational Activation Date'], format='%d-%m-%Y')

            # Extract date (without time)
            data['operational_date'] = data['operational_activation_date'].dt.date

            # Group by date and count occurrences
            daily_counts = data.groupby('operational_date').size().reset_index(name='counts')

            # Plot the counts using Plotly
            fig = px.strip(daily_counts, x='operational_date', y='counts', title=" Daily operational Counts ")
            fig_daily_bar = px.bar(daily_counts, x='operational_date', y='counts', title=" Daily operational Counts ")
            st.title("DAILY OPERATIONAL ACTIVATIONS")
            """
            Below is the plot visualizing the total count of operational activations on the daily basis. hover over the data points
            for better understanding and a count for the activations.
            """
            st.plotly_chart(fig)
            st.plotly_chart(fig_daily_bar)

            # VISUALIZING THE GRAPH FOR STATE WISE ALOCATION OF DEVICES
            stateAllocation = data['State'].value_counts()
            statewise_dvice_allocation =  px.line(stateAllocation, title= "Statewise On road devices")
            st.plotly_chart(statewise_dvice_allocation)


        except Exception as e:
            st.write("Error while displaying the visual.")

except Exception as e:
    st.write("Error while reading the file {}.".format(str(e)))

