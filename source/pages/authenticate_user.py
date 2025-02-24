import streamlit as st
from repositories.authenticate import authenticate_user, authenticate_yandex_user, check_user, register_user
from repositories.yandex_auth import process_yandex_auth, get_yandex_auth_url

def show_authenticate_page():
    st.title("Авторизация")
    user_info = process_yandex_auth()
    if (len(user_info) != 0):
        status = authenticate_yandex_user(user_info)
        if "error" in status:
            st.write(status["error"])
        elif "token" in status:
            st.session_state.token = status["token"]
            st.write("Авторизация успешна")
            #print(st.session_state["token"])
            st.rerun()
    with st.form("authorization"):
        username = st.text_input('Логин:', max_chars=50)
        password = st.text_input('Пароль:', type="password")
        authorise_btn = st.form_submit_button('Войти')
        register_btn = st.form_submit_button('Регистрация')
        st.markdown(f"[войти через Yandex]({get_yandex_auth_url()})", unsafe_allow_html=True)
        if authorise_btn:
            status = authenticate_user(username, password)
            if "error" in status:
                st.write(status["error"])
            elif "token" in status:
                st.session_state.token = status["token"]
                st.write("Авторизация успешна")
                #print(st.session_state["token"])
                st.rerun()
                
        if register_btn:
            status = check_user(username)
            if "error" in status:
                st.write(status["error"])
            else:
                st.session_state.token = register_user(username, password)["token"]
                st.write("Авторизация успешна")
                #print(st.session_state["token"])
                st.rerun()
                