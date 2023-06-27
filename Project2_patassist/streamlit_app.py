import streamlit as st
from streamlit_chat import message
from streamlit_extras.colored_header import colored_header
from streamlit_extras.add_vertical_space import add_vertical_space
from embeddings.chatbot import get_chat_response

import streamlit_authenticator as stauth

import yaml
from yaml.loader import SafeLoader

st.set_page_config(page_title="P-Assist")

with open('patientrecords/config.yaml', 'r') as file:
    config = yaml.load(file, Loader=SafeLoader)

authenticator = stauth.Authenticate(
    config['credentials'],
    config['cookie']['name'],
    config['cookie']['key'],
    config['cookie']['expiry_days'],
    config['preauthorized']
)

name, authentication_status, username = authenticator.login('Login', 'main')

id = username[1:]

def handle_logout():
    authenticator.logout('Logout', 'main', key='unique_key')
    st.session_state.clear()


if st.session_state["authentication_status"]:
    
    with st.sidebar:
        st.title("P-Assist")
        st.sidebar.button('Logout', on_click=handle_logout)
        st.write(f'Välkommen *{st.session_state["name"]}*')
        st.markdown('''
        ## About
        Ett första försök att bygga en chatt-bot för patienter
    
    💡  Note: Bara dummy-data används, fortfarande i ett tidigt stadie
        ''')

    add_vertical_space(5)

    if 'generated' not in st.session_state:
        st.session_state['generated'] = ["Välkommen till Assistenten! Hur kan jag hjälpa dig?"]

    if 'past' not in st.session_state:
        st.session_state['past'] = ["Hejsan!"]

    user_container = st.container()
    colored_header(label='', description='', color_name='blue-30')
    bot_container = st.container()

    def get_text():
        input_text = st.text_input("You: ", "", key="input")
        return input_text

    with user_container:
        user_input = get_text()

    def generate_response(prompt, id):
        response = get_chat_response(prompt, id)
        return response

    with bot_container:
        if user_input:
            response = generate_response(user_input, id)
            st.session_state.past.append(user_input)
            st.session_state.generated.append(response)
        
        if st.session_state['generated']:
            for i in range(len(st.session_state['generated'])):
                message(st.session_state['past'][i], is_user=True, key=str(i) + '_user')
                message(st.session_state["generated"][i], key=str(i))

elif st.session_state["authentication_status"] is False:
        st.error('Username/password is incorrect')
elif st.session_state["authentication_status"] is None:
        st.warning('Please enter your username and password')



