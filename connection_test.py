# streamlit_app.py
import pandas as pd
from gspread_pandas import Spread, Client
import streamlit as st
from streamlit_gsheets import GSheetsConnection
from PIL import Image

# Import logo

image = Image.open('Core_Logo_white.png')
show_all_col = []

st.set_page_config(
    page_title="OC Dashboard",
    layout="wide"
)

st.markdown(
    f'''

            <style>
                .block-container {{
                    padding-top: 2.5rem;
                    }}


                .reportview-container .sidebar-content {{
                    padding-top: 0rem;
                    padding-right: rem;
                    padding-left: rem;
                    padding-bottom: rem;
                    }}

                .css-1o14730 {{
                    # background-color: gray;
                    padding-top: 0rem;
                }}
            </style>
            ''', unsafe_allow_html=True,
)

st.image(image, width=80)

# Create a connection object.
conn = st.connection("gsheets", type=GSheetsConnection)

# df = conn.read(
#     worksheet="Sheet1",
#     # ttl="2m",
#     usecols=[0, 1, 2, 3],
#     nrows=4
# )

# # Print results.
# for row in df.itertuples():
#     st.write(f"On {row.date}, {row.name} passed the :{row.course} course")


spread = Spread('oc_trainining_certificate')
# Display available worksheets

google_sheet_to_df = spread.sheet_to_df()
df = pd.DataFrame(google_sheet_to_df)

display_sheet = st.data_editor(df.style.format(precision=3, thousands=None), use_container_width=True)

# st.dataframe(all_results)

