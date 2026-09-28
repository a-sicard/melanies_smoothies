# Import python packages
import streamlit as st
import os
# from snowflake.snowpark.context import get_active_session
from snowflake.snowpark.functions import col

# Write directly to the app
st.title(":cup_with_straw: Customize Your Smoothie :cup_with_straw:")
st.write(
  """Choose the fruit you want in your custom smoothie!
  """
)

# fav_fruit = st.selectbox(
#     "What is your favorite fruit?",
#     ("Strawberries", "Bananas", "Peaches"),
# )

# st.write("Your favorite fruit is", fav_fruit)

cnx = st.connection("snowflake")
session = cnx.session()
my_dataframe = session.table("smoothies.public.fruit_options").select(col('FRUIT_NAME'))
# st.dataframe(data=my_dataframe, use_container_width=True)

order_name = st.text_input("Please provide a name for your order")
st.write(order_name)
    
ingredient_list = st.multiselect("Choose up to 5 ingredients", my_dataframe, max_selections=5)
if ingredient_list:  
    ingredient_string = ''
    for fruit in ingredient_list:
        ingredient_string += fruit + ' '
        
    my_insert_stmt = """ insert into smoothies.public.orders(ingredients, NAME_ON_ORDER)
                    values ('""" + ingredient_string + "', '" + order_name + "') """

    time_to_insert = st.button('Submit Order')

    if time_to_insert:
        # st.write(my_insert_stmt)
    
        if ingredient_string and order_name:
            session.sql(my_insert_stmt).collect()
            st.success('Your Smoothie is ordered, ' + order_name + '!', icon="✅")

import requests  
smoothiefroot_response = requests.get("[https://my.smoothiefroot.com/api/fruit/watermelon](https://my.smoothiefroot.com/api/fruit/watermelon)")  
st.text(smoothiefroot_response)
