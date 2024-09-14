import streamlit as st
import pandas as pd
import pyodbc

@st.cache_data
def get_animal_data() -> pd.DataFrame:
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

    query = "SELECT * from animals_imp;"
    # Perform query.
    df = pd.read_sql(query, init_connection())

    #generate and fill dataframe
    col_names = ['Cow_Number', 'Full_Name', 'Dob', 'HerdID', 'NLIS_Tag_Number','Dam_Number','Sire_Number']
    df_split = pd.DataFrame(df.values.tolist(), columns=col_names)

    return df_split


#define drop down in side bar
search = st.sidebar.selectbox("Select an Animal",get_animal_data()["Full_Name"])


search, calving = st.tabs(["Search Animals", "Animals Mating/Calving"])

with search:
    st.header('Search')

    df = get_animal_data()

    event = st.dataframe(
        df,
        use_container_width=True,
        hide_index=True,
        on_select="rerun",
        selection_mode="multi-row",       
    )

    st.header("Selected Animals")
    people = event.selection.rows
    filtered_df = df.iloc[people]
    st.dataframe(
        filtered_df,
        use_container_width=True,
    )
    