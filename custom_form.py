# Import python packages
import streamlit as st
from snowflake.snowpark.context import get_active_session
from snowflake.snowpark.functions import col

# Write directly to the app
st.title(f":cup_with_straw: "
         f"Customize Your Smoothie! :cup_with_straw:")
st.write(
  """
  Choose the fruits you want in your custom Smoothie!
  """
)

session = get_active_session()
my_dataframe = session.table("SMOOTHIES.PUBLIC.FRUIT_OPTIONS")\
.select(col('FRUIT_NAME'))

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