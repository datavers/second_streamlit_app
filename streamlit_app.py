import streamlit
import pandas as pd
import requests as r

fruitvice_response = r.get("https://fruityvice.com/api/fruit/watermelon")

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

streamlit.header("Fruityvice Fruit Advice!")
# normalized version of the json file
fruityvice_normalized = pandas.json_normalize(fruityvice_response.json())
# draw the table
streamlit.dataframe(fruityvice_normalized)
