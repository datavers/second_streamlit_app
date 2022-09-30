import streamlit
import pandas as pd
import requests as re
import snowflake.connector
from urllib.error import URLError

my_fruit_list = pd.read_csv('https://uni-lab-files.s3.us-west-2.amazonaws.com/dabw/fruit_macros.txt')

streamlit.header('Breakfast Menu')
streamlit.text('🥣 Omega 3 & Blueberry Oatmeal')
streamlit.text('🥗 Kale, Spinach & Rocket Smoothie')
streamlit.text('🐔 Hard-Boiled Free-Range Egg')
streamlit.text('🥑🍞 Avocado Toast')

streamlit.header('🍌🥭 Build Your Own Fruit Smoothie 🥝🍇')

# Let's put a pick list here so they can pick the fruit they want to include 
my_fruit_list = my_fruit_list.set_index('Fruit')

#streamlit.multiselect("Pick some fruits:", list(my_fruit_list.index))
# streamlit.multiselect("Pick some fruits:", list(my_fruit_list.index), ["Apple","Avocado"])
# Előre kijelölt elemeket tartalmaz, mint Apple és Avocado
# streamlit.dataframe(my_fruit_list)

fruits_selected = streamlit.multiselect("Pick some fruits:", list(my_fruit_list.index))
fruits_to_show = my_fruit_list.loc[fruits_selected]
streamlit.dataframe(fruits_to_show)

def get_fruityvice_data(this_fruit_choice):
    fruityvice_response = re.get("https://fruityvice.com/api/fruit/"+ fruit_choice)
    # normalized version of the json file
    fruityvice_normalized = pd.json_normalize(fruityvice_response.json())
    return fruityvice_normalized

streamlit.header("Fruityvice Fruit Advice!")
try:
  fruit_choice = streamlit.text_input('What fruit would you like information about?','Kiwi')
  if not fruit_choice:
      streamlit.error("Please select a fruit to get information")
  else:
    back_from_function = get_fruityvice_data(fruit_choice)
    streamlit.write('The user entered ', fruit_choice)
    # draw the table
    streamlit.dataframe(back_from_function)
except URLError as e:
  streamlit.error()

add_my_fruit = streamlit.text_input('What fruit would you like to add', 'jackfruit')
# Ez nem működik így: streamlit.text('Thanks for adding ', add_my_fuit)

streamlit.header("The fruit load list:")
#Snowflake related functions
def get_fruit_load_list():
    with my_cnx.cursor() as my_cur:
        my_cur.execute("SELECT * FROM fruit_load_list")
        return my_cur.fetchall()

# Add a button to load fruit list
if streamlit.button('Get Fruit Load list'):
    my_cnx = snowflake.connector.connect(**streamlit.secrets["snowflake"])
    my_data_rows = get_fruit_load_list()
    streamlit.dataframe(my_data_rows)

# my_data_row = my_cur.fetchone()
# Allow to the end user to add a fruit to the list
def insert_row_snowflake(new_fruit):
    with my_cnx.cursor() as my_cur:
        my_cur.execute("INSERT INTO fruit_load_list VALUES ('from streamlit')")
        return "Thanks for adding" + new_fruit
    
add_my_fruit = streamlit.text_input('What fruit would you like to add')
if streamlit.button('Add a fruit to the Load list'):
    my_cnx = snowflake.connector.connect(**streamlit.secrets["snowflake"])
    back_from_function = insert_row_snowflake(add_my_fruit)
    streamlit.text(back_from_function)
