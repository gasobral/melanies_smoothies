# Import python packages
import requests

import streamlit as st
from snowflake.snowpark.functions import col
import pandas as pd

# Write directly to the app
st.title(f":cup_with_straw: "
         f"Customize Your Smoothie! :cup_with_straw:")
st.write(
  """
  Choose the fruits you want in your custom Smoothie!
  """
)

cnx = st.connection("snowflake")
session = cnx.session()
my_dataframe = session.table("SMOOTHIES.PUBLIC.FRUIT_OPTIONS")\
.select(col('FRUIT_NAME'), col('SEARCH_ON'))

# check result set data
# st.dataframe(data=my_dataframe, use_container_width=True)
# st.stop()

pd_df = my_dataframe.to_pandas()
# check data loaded into pandas data frame
# st.dataframe(pd_df)
# st.stop()

name_on_order = st.text_input('Name on Smoothie')
st.write('The name on your smoothie will be ', name_on_order)

ingredients_list = st.multiselect(
    'Choose up to 5 ingredients',
    my_dataframe,
    max_selections=5
)

if ingredients_list:
    ingredients_string = ' '.join(ingredients_list)
    my_insert_stmt = f"""
    insert into smoothies.public.orders
    (NAME_ON_ORDER, INGREDIENTS)
    values ('{ingredients_string}', '{name_on_order}');
    """
    time_to_insert = st.button('Submit Order')

    if time_to_insert:
        session.sql(my_insert_stmt).collect()
        st.success('Your Smoothie is ordered!', icon="✅")

    for fruit_chosen in ingredients_list:
        search_on = pd_df.loc[pd_df['FRUIT_NAME'] == fruit_chosen, 'SEARCH_ON'].iloc[0]
        st.write(f'The search value for {fruit_chosen} is {search_on}.')

        st.subheader(fruit_chosen + ' Nutrition Information')
        smoothiefroot_response = requests.get("https://my.smoothiefroot.com/api/fruit/" + fruit_chosen)
        sf_df = st.dataframe(data=smoothiefroot_response.json(), use_container_width=True)
