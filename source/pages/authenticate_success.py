import streamlit as st
from repositories.jwt import decode_jwt
from repositories.rabbitmq_producer import publish_registration_event
from settings import TELEGRAM_BOT_TAG

def get_bot_url(parameter):
    return (f"https://t.me/{TELEGRAM_BOT_TAG}?start={parameter}")

def show_success_page():
    token = decode_jwt(st.session_state["token"])["token"]
    st.title("Авторизация успешна")
    st.write("Авторизация успешна")
    st.markdown(f"[начать чат с ботом]({get_bot_url(token['login'])})", unsafe_allow_html=True)
    print("Токен пользователя после авторизации: ", token)
    if token['chat_id'] != None:
        publish_registration_event(token)
        print("добавлено сообщение в очередь")
                