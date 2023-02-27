import streamlit as st
import requests



BASE_URL = "https://sandbox-api.marqeta.com/v3/"

MARQETA_API_KEY = st.secrets["M_KEY"]
MARQETA_API_PWD = st.secrets["M_PWD"]
M_FUND_TOKEN = st.secrets["M_FUND_TOKEN"]
M_MID = st.secrets["M_MID"]


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
    #st.markdown("create card product with name: " + name)
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


def fund_card(user_token):
    url = BASE_URL + "gpaorders"
    data = {
        "user_token": user_token,
        "amount": "1000.00",
        "currency_code": "USD",
        "funding_source_token": M_FUND_TOKEN
    }

    response = requests.post(url, headers=headers, json=data, auth=(MARQETA_API_KEY,MARQETA_API_PWD))

    return response

def create_transaction(amount, card_token):
    url = BASE_URL + "simulate/authorization"
    data = {
        "amount": amount,
        "mid": M_MID,
        "card_token": card_token
    }

    response = requests.post(url, headers=headers, json=data,auth=(MARQETA_API_KEY,MARQETA_API_PWD))

    return response





def main():
    st.title("Generate Card and Use Card")
    st.markdown("To generate virtual payment cards using the Marqeta API, you first need to create a user, then create a card product that defines the card's characteristics, and finally create the virtual cards for the user based on the card product.")

    col1, col2 = st.columns(2)
    #col1.write("Enter brand name and User's first Name and Last name and click 'Generate Card' button")
    brand_name = col1.text_input("Brand Name")
    first_name = col1.text_input("First Name")
    last_name =  col1.text_input("Last Name")

    #amount = col1.number_input("Amount", min_value=0.01, max_value=1000000.00, step=0.01)
    
    trans_amount = col1.number_input("After generate the card, we can simularte authorization with a Merchant(mid as 123456890) and amount", min_value=10)

    generate_card = col1.button("Generate Card and Use Card")

    if  generate_card:
        user_token = create_user(first_name, last_name)
        name =  brand_name + "'s Card"
        card_product_token = create_card_product(name)

        response = create_virtual_card(card_product_token, user_token)
        card_number = response.json()["pan"]
        card_token = response.json()["token"]

        #card_image_url, card_number = generate_prepaid_card(brand_name, amount)
        #col2.image(card_image_url, use_column_width=True)
        #col2.write(brand_name)
        #col2.write("Prepaid Card Number: {}".format(card_number))

        col2.markdown("1 -- Virtual Card Generated Successfully")
        col2.markdown("     Primary Account Nunber is: " + card_number) 
        col2.markdown("     Card Token is: " + card_token) 
        col2.markdown("     User Token is: " + user_token) 
        col2.markdown("     Card Product Token is: " + user_token) 

        #transaction = col2.button("Simulate authorization")

        #if transaction:
        #col2.write("Card Token is: " + card_token) 
        fund_response = fund_card(user_token)

        trans_response = create_transaction(trans_amount, card_token)
        #memo = trans_response.json()["response"]["memo"]
        #col2.write("message: " + memo)
        col2.write("2 -- Funding User Account - Response:") 
        col2.write(fund_response.json())
        col2.write("3 -- Transaction with Merchant: " + M_MID + " - Response: ")
        col2.write(trans_response.json())
    
if __name__ == "__main__":
    main()
