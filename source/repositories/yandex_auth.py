import streamlit as st
import streamlit.components.v1 as components
import requests
from settings import YANDEX_CLIENT_ID

def get_yandex_auth_url():
    return (f"https://oauth.yandex.ru/authorize?response_type=token&client_id={YANDEX_CLIENT_ID}")

def process_yandex_auth():
    components.html(
            """
            <script>
                console.log("Компонент загружен. Родительский URL: " + window.parent.location.href);
                if (window.parent.location.hash) {
                    const hashParams = window.parent.location.hash.substring(1);
                    console.log("Hash params from parent: " + hashParams);
                    const newUrl = window.parent.location.origin + window.parent.location.pathname + "?" + hashParams;
                    console.log("Новый URL для родителя: " + newUrl);
                    window.parent.history.replaceState(null, null, newUrl);
                    window.parent.location.reload();
                }
            </script>
            """,
            height=0,
        )
    if "access_token" in st.query_params:
        token = st.query_params["access_token"]
        # print("Получен OAuth токен:", token)

        response = requests.get(
            "https://login.yandex.ru/info",
            params={
                "oauth_token": token,
                "format": "json"
            }
        )
        user_info = response.json()
        # print("ответ на get запрос: ", user_info)
        return user_info
    else:
        return {}