import streamlit as st  # pip install streamlit
import pandas as pd
import itertools
from st_keyup import st_keyup
from PIL import Image

# from streamlit_pandas_profiling import st_profile_report

# ---SETTINGS---#

# Set variables

df_display = False
endclient_filtered = pd.DataFrame()
lawfirm_filtered = pd.DataFrame()
attorney_filtered = pd.DataFrame()
judge_filtered = pd.DataFrame()

# convert_amount = {'Amount': 'float64'}


visible_col = dict()
visible_col = {'limited': ['Harvest Case ID', 'Name', 'End Client', 'Lead Attorneys', 'Law Firm Client', 'Judges']}
detail_col = {'detail':
                  ['Name',
                   'Engagement',
                   'Conflict Status',
                   'Law Firm Client',
                   'Industry',
                   'Case Type',
                   'End Client',
                   'Lead Attorneys',
                   'Civil Case Number',
                   'Court',
                   'Judges',
                   'City',
                   'State',
                   'Partys Role',
                   'Core Leads']}

header_list = []
for key, val in detail_col.items():
    header_list.append(val)
flat_heads = list(itertools.chain(*header_list))

# Initialize Radio Buttons - Streamlit

if "visibility" not in st.session_state:
    st.session_state.visibility = "visible"
    st.session_state.disabled = False
    st.session_state.horizontal = True

# Define Functions

# NOT WORKING

# def search_box(column_id, column_name):
#     f = column_id + '_filtered'
#     if (f"input_{column_id}"):
#         df_display = True     
#         thefilter = df_subset[df_subset[column_name].str.lower().str.contains((f'input_{column_id}:').lower(), na=False)]
#         st.write(len(thefilter), "Results found")
#     return thefilter

# Import logo

image = Image.open('Core_Logo_white.png')
show_all_col = []

# Set streamlit metadata and initial options

page_title = "Conflict Check"

st.set_page_config(
    page_title=page_title,
    layout="wide"
)

# CSS 

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

# Display logo
# 
st.image(image, width=80)

# with st.sidebar:
# st.write(df_subset)

# DISPLAY PAGE

'''
## Conflict Checker
'''
show_all_col = st.checkbox('Show All Columns')

# Read in source file

df = pd.DataFrame(pd.read_json('cases.json'))

headers = df.columns.tolist()

# All columns headers for reference:
# ['PID',
#  'Harvest Case ID',
#  'Name',
#  'Engagement',
#  'Conflict Status',
#  'Law Firm Client',
#  'Industry',
#  'Case Type',
#  'End Client',
#  'Lead Attorneys',
#  'Civil Case Number',
#  'Court',
#  'Judges',
#  'City',
#  'State',
#  'Partys Role',
#  'Core Leads']


# Set global pandas display option to show columns based on checkbox selection

if show_all_col:
    df_subset = pd.DataFrame(df)  # .set_index(visible_index)
else:
    df_subset = pd.DataFrame(df, columns=visible_col['limited'])  # .set_index(visible_index)

# Set global pandas display option to show all rows

pd.set_option('display.max_rows', None)

# Conflict search form

# with st.form("entry_form2"):
# submit_button = st.form_submit_button("Submit")

col1, col2 = st.columns(2)

with col1:
    st.text_input("Case Name (Short)", key="fullcase2", placeholder="Party v Party", disabled=False)

with col2:
    st.radio(
        "Entry Type:",
        ["Conflict Check", "Engagement"],
        key="entrytype",
        label_visibility=st.session_state.visibility,
        disabled=st.session_state.disabled,
        horizontal=st.session_state.horizontal,
    )

# Filtering options

col1, col2, col3, col4 = st.columns(4)

with col1:
    input_endclient = st_keyup("Enter End Client")

    if input_endclient:
        endclient_filtered = df_subset[
            df_subset['End Client'].str.lower().str.contains(input_endclient.lower(), na=False)]
        endclient_rows = len(endclient_filtered.index)
        if endclient_rows != 0:
            df_display = True
            st.write(len(endclient_filtered), "End Client results found")

with col2:
    input_lawfirm = st_keyup("Enter Law Firm")

    if input_lawfirm:
        lawfirm_filtered = df_subset[
            df_subset['Law Firm Client'].str.lower().str.contains(input_lawfirm.lower(), na=False)]
        lawfirm_rows = len(lawfirm_filtered.index)
        if lawfirm_rows != 0:
            df_display = True
            st.write(len(lawfirm_filtered), "Law Firm results found")

with col3:
    input_attorney = st_keyup("Enter Lead Attorney")

    if input_attorney:
        attorney_filtered = df_subset[
            df_subset['Lead Attorneys'].str.lower().str.contains(input_attorney.lower(), na=False)]
        attorney_rows = len(attorney_filtered.index)
        if attorney_rows != 0:
            df_display = True
            st.write(len(attorney_filtered), "Attorney results found")

with col4:
    input_judge = st_keyup("Enter Judge")
    # input_judge = "james"  # Prefill for testing purposes

    if input_judge:
        judge_filtered = df_subset[df_subset['Judges'].str.lower().str.contains(input_judge.lower(), na=False)]
        judge_rows = len(judge_filtered.index)
        if judge_rows != 0:
            df_display = True
            st.write(len(judge_filtered), "Judge results found")

if (len(judge_filtered) + len(attorney_filtered) + len(lawfirm_filtered) + len(endclient_filtered)) != 0:
    st.warning("Possible Conflicts", icon="⚠️")

if df_display:
    all_results = pd.concat([endclient_filtered, lawfirm_filtered, attorney_filtered, judge_filtered, ],
                            ignore_index=True, sort=False)
    all_results = all_results.drop_duplicates()  # Research needed
    all_results = all_results.astype({'Harvest Case ID': 'str'})  # convert Amount to str

    num_rows = len(all_results.index)
    df_height = (num_rows + 1) * 35 + 3
    # all_results.set_index(['Harvest Case ID'])

    all_results.insert(0, "Show Profile", False)
    all_results = st.data_editor(all_results.style.format(precision=3, thousands=None), height=df_height,
                                 use_container_width=True)


    def profile_display():
        pass


    # Flip out the side panel if something is checked in the table

    # Create a Streamlit table and get its Styler object
    # table = st.table(df)
    # styler = table._st_container.beta_columns(1)[0].styler

    # Set the font size of the table cells to 16
    # styler.set_cell_font({'font-size': '16px'})

    for cell in all_results["Show Profile"]:
        if cell:
            row_select = all_results[all_results['Show Profile'] == True]
            row_select = pd.DataFrame(row_select, columns=detail_col['detail'])  # .set_index(detail_index)
            result = row_select.T
            with st.sidebar:
                output_list = []
                with st.expander("Profile Review", expanded=True):
                    result.columns = ['Case Profile']
                    for entry in result['Case Profile']:
                        output_list.append(entry)
                    st.write(output_list[0])
                    res = dict(map(lambda i, j: (i, j), flat_heads, output_list))
                    profile_df = pd.DataFrame.from_dict(res, orient='index', columns=['Case Profile'])
                    profile_df = profile_df['Case Profile'].fillna(' ')

                    st.table(profile_df)

                    # result = result.style.format(na_rep=' ')
                    # st.table(result)

# import pandas as pd

# # create a sample dataframe
# df = pd.DataFrame({'A': [1, 2, 3], 'B': [4, 5, 6]})

# # extract the first row as a dataframe and transpose it
# row = pd.DataFrame(df.iloc[0]).T

# # concatenate the original dataframe with the transposed row
# result = pd.concat([row, df], axis=0, ignore_index=True)

# print(result)


# Export button

# if st.button('Export'):
#     json = all_results.to_json('conflict_results.json')
#     excel = all_results.to_excel('conflict_results.xlsx')
