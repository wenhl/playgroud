import stripe
import streamlit as st

stripe.api_key = st.secrets["S_KEY"]


def retrieve_customer(email):
    existing_customers = stripe.Customer.search(query="email:'sarah.kou@example.com'")
    if existing_customers:
        return existing_customers.data[0]
    #else:
    #    return false


def retrieve_payment_method(customer_id):
    payment_method = stripe.PaymentMethod.list(
        limit=3, 
        customer=customer_id,
        type='card'    
    )

    if payment_method:
        return payment_method.data[0]
   # else:
   #     return false

def retrieve_backaound(customer_id):
    bank_account = stripe.Customer.list_sources(
        customer_id,
        object='bank_account',
        limit=1   
    )
    if bank_account:
        return  bank_account.data[0]
    #else:
    #    return false


def create_customer(first_name, last_name, email, payment_method_id):
    existing_customers = stripe.Customer.search(query="email:'sarah.kou@example.com'")
    if existing_customers:
        return existing_customers.data[0]
    else:
        customer = stripe.Customer.create(
            payment_method=payment_method_id,
            email=email,
            name=f"{first_name} {last_name}",
            description=f"{first_name} {last_name} - {email}"
        )
        return customer


def create_token(first_name, last_name, account_number, routing_number):
    token = stripe.Token.create(
        bank_account={
            "country": "US",
            "currency": "usd",
            "account_holder_name": f"{first_name} {last_name}",
            "account_holder_type": "individual",
            "routing_number": routing_number,
            "account_number": account_number
        }
    )
    return token

def create_payment(payment_method_type="card"):
    payment_method = stripe.PaymentMethod.create(
        type=payment_method_type,
        card={
            "number": "4242424242424242",
            "exp_month": 8,
            "exp_year": 2023,
            "cvc": "314"
        }
    )
    return payment_method

def create_bank_account(customer_id, token_id):
    bank_account = stripe.Customer.create_source(
        customer_id,

        source=token_id
    )
    return bank_account

def main():
    st.title("Create Bank Account")

    first_name = st.text_input("First Name", "Sarah")
    last_name = st.text_input("Last Name", "kou")
    email = st.text_input("Email Address", "Sarah.kou@example.com")
    create_bank_account_button = st.button("Create Bank Account")

    if create_bank_account_button:
        customer = retrieve_customer(email)

        if customer:
            #st.write(f"Customer created. with object: {customer}")
            st.write("Customer created with object: ")
            st.write(customer)
            payment_method = retrieve_payment_method(customer.id)
            #st.write(f"Payment method created with object: {payment_method}")
            st.write("Payment method created with object: ")
            st.write(payment_method)
            bank_account = retrieve_backaound(customer.id)
            #st.write(f"Bank account created with object: {bank_account}")
            st.write("Bank account created with object: ")
            st.write(bank_account)

        else:       
            #st.write("Creating payment method...")
            payment_method = create_payment()
            payment_method_id = payment_method.id
            #st.write(f"Payment method created with object: {payment_method}")
            st.write("Payment method created with object: ")
            st.write(payment_method)
        
            #st.write(payment_method)

            #st.write("Creating customer...")
            customer = create_customer(first_name, last_name, email, payment_method_id)
            customer_id = customer.id
            #st.write(f"Customer created. with object: {customer}")
            st.write("Customer created with object: ")
            st.write(customer)

            token = create_token(first_name, last_name, "000123456789", "110000000")
            token_id = token.id
            #st.write(f"Token created with object: {token}")
            st.write("Token created with object: ")
            st.write(token)

            bank_account = create_bank_account(customer_id, token_id)
            #st.write(f"Bank account created with object:  {bank_account}")
            st.write("Bank account created with object: ")
            st.write(bank_account)


if __name__ == "__main__":
    main()