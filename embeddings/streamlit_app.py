import streamlit as st
from streamlit_chat import message
from streamlit_extras.colored_header import colored_header
from streamlit_extras.add_vertical_space import add_vertical_space
from chatbot import get_chat_response

st.set_page_config(page_title="Assistenten")

with st.sidebar:
    st.title("Assistenten")
    st.markdown('''
    ## About
    Ett första försök att bygga en chatt-bot för läkare
    
    💡 Note: Bara dummy-data används, fortfarande i ett tidigt stadie
    ''')

add_vertical_space(5)

if 'generated' not in st.session_state:
    st.session_state['generated'] = ["Välkommen till Assisten!"]

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
    response = get_chat_response(prompt)
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
