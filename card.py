import streamlit as st
import requests


BASE_URL = "https://sandbox-api.marqeta.com/v3/"

MARQETA_API_KEY = st.secrets["M_KEY"]
MARQETA_API_PWD = st.secrets["M_PWD"]

headers = {
        "Accept": "application/json",
        "Content-Type": "application/json"
    }

def create_card_product(name):
    url = BASE_URL + "cardproducts"

    fulfillment = {
        "payment_instrument": "VIRTUAL_PAN"
    }

    poi = {
        "ecommerce": True
    }

    card_life_cycle = {
        "activate_upon_issue": True
    }

    config = {
        "fulfillment": fulfillment,
        "poi": poi,
         "card_life_cycle": card_life_cycle        
    }

    data = {
        "start_date": "2023-01-01",
        "name": name,
        "config": config
    }
    st.markdown("create card product with name: " + name)
    #st.markdown(name)

    response = requests.post(url, headers=headers, json=data, auth=(MARQETA_API_KEY,MARQETA_API_PWD))
    response_json = response.json()

    #st.markdown(response_json["token"])
    return response_json["token"]


def create_user(first_name, last_name):
    url = BASE_URL + "users"

    data = {
        "first_name": first_name,
        "last_name": last_name
    }

    response = requests.post(url, headers=headers, json=data,auth=(MARQETA_API_KEY,MARQETA_API_PWD))
    response_json = response.json()
    #st.markdown("create user response")
    user_token = response_json["token"] 
    #st.markdown(user_token);
    return user_token

def create_virtual_card(card_product_token, user_token):
    url = BASE_URL + "cards"   
 
    params = {
        "show_cvv_number":"true",
        "show_pan":"true"
    }

    #st.markdown(user_token)    
    #st.markdown(card_product_token)  
    data = {
        "user_token": user_token,
        "card_product_token": card_product_token
    }

    response = requests.post(url, headers=headers, json=data, params=params, auth=(MARQETA_API_KEY,MARQETA_API_PWD))
    #response_json = response.json()
    #return response_json["token"]
    return response

def main():
    st.title("Virtual Card Generator using Marqeta API")
    first_name = st.text_input("First Name")
    last_name = st.text_input("Last Name")
    #card_amount = st.number_input("Card Amount", min_value=0)

    if st.button("Generate Card"):
        user_token = create_user(first_name, last_name)
        name = first_name + " " + last_name + "'s Card"
        card_product_token = create_card_product(name)

        response = create_virtual_card(card_product_token, user_token)
        st.write("Virtual Card Generated Successfully")
        st.write("Response:", response.json())
    
if __name__ == "__main__":
    main()
