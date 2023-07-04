import streamlit as st
from streamlit_chat import message
from streamlit_extras.colored_header import colored_header
from streamlit_extras.add_vertical_space import add_vertical_space

import src.chatbot as  chatbot 

import streamlit_authenticator as stauth


#import yaml
#from yaml.loader import SafeLoader


st.set_page_config(page_title="MedHelp")


#with open('Project3_intranet/data/config.yaml', 'r') as file:
#    config = yaml.load(file, Loader=SafeLoader)


#authenticator = stauth.Authenticate(
#    config['credentials'],
#    config['cookie']['name'],
#    config['cookie']['key'],
#    config['cookie']['expiry_days'],
#    config['preauthorized']
#)

#name, authentication_status, username = authenticator.login('Login', 'main')

@st.cache_resource
def get_chatbot():
    return chatbot.Chatbot()

chatbot = get_chatbot()

#def handle_logout():
#    authenticator.logout('Logout', 'main', key='unique_key')
#    st.session_state.clear()
#    st.experimental_singleton.clear()



#if st.session_state["authentication_status"]:
#    patients = config['credentials']['usernames'][username]['patients']
        

with st.sidebar:
    st.title("MedHelp")
    #st.sidebar.button('Logout', on_click=handle_logout)
    st.write(f'Välkommen *King👑👑*')
    st.markdown('''
    ## About
    
    Ett första försök att bygga en chatt-bot för läkare och patienter med GPT modeller,
    gjort i sammarbete mellan AI-Sweden och Sahlgrenska Universitetssjukhus
    under GPT Summer Internship 2023.

    Gjort av:

    - Henrik Johansson
    - Oskar Pauli
    - Felix Nilsson

    🔗 [Projektsida](https://my.ai.se/projects/287)

    💡  Note: Bara dummy-data används, fortfarande i ett tidigt stadie
    ''')

add_vertical_space(5)

if 'generated' not in st.session_state:
    st.session_state['generated'] = ["Välkommen till MedHelp! Hur kan jag hjälpa dig?"]

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

def generate_response(prompt):
    response = chatbot.get_chat_response(prompt)
    return response

with bot_container:
    if user_input:
        response = generate_response(user_input)
        st.session_state.past.append(user_input)
        st.session_state.generated.append(response)
    
    if st.session_state['generated']:
        for i in range(len(st.session_state['generated'])):
            message(st.session_state['past'][i], is_user=True, key=str(i) + '_user')
            message(st.session_state["generated"][i], key=str(i))

#elif st.session_state["authentication_status"] is False:
#    st.error('Username/password is incorrect')
#elif st.session_state["authentication_status"] is None:
#    st.warning('Please enter your username and password')
