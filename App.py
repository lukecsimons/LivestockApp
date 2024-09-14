import streamlit as st
import pandas as pd
import pyodbc

# Initialize connection.
# Uses st.cache_resource to only run once.
@st.cache_resource
def init_connection():
    return pyodbc.connect(
        "DRIVER={ODBC Driver 17 for SQL Server};SERVER="
        + st.secrets["server"]
        + ";DATABASE="
        + st.secrets["database"]
        + ";UID="
        + st.secrets["username"]
        + ";PWD="
        + st.secrets["password"]
    )

conn = init_connection()

# Perform query.
# Uses st.cache_data to only rerun when the query changes or after 10 min.
# @st.cache_data(ttl=600)
# def run_query(query):
#     with conn.cursor() as cur:
#         cur.execute(query)
#         return cur.fetchall()

query = "SELECT * from animals_imp;"
# Perform query.
df = pd.read_sql(query, conn)

#generate and fill dataframe
col_names = ['Cow_Number', 'Full_Name', 'Dob', 'HerdID', 'NLIS_Tag_Number','Dam_Number','Sire_Number']
df_split = pd.DataFrame(df.values.tolist(), columns=col_names)

#form to search for animals
with st.form("search_form"):
    header = st.columns([2])
    header[0].subheader('Search')

    row1 = st.columns([2])
    animal = st.selectbox("Select an Animal",df_split["Full_Name"])

    search = st.form_submit_button('Search Animals')

if  search:
    st.data_editor(df_split)
else:    
    st.data_editor(df_split)