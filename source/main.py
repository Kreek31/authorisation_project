import streamlit as st
import pika
import asyncio
from telegram.ext import Application, CommandHandler
from repositories.bot_consumer import callback, start
from repositories.jwt import decode_jwt
from pages.authenticate_user import show_authenticate_page
from pages.authenticate_success import show_success_page
from settings import TELEGRAM_BOT_TOKEN



# Главная логика приложения с навигацией
def main():
    if "token" not in st.session_state:
        show_authenticate_page()
    else:
        token = decode_jwt(st.session_state["token"])["token"]
        show_success_page()

        if token['chat_id'] == None:
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)
            app = Application.builder().token(TELEGRAM_BOT_TOKEN).build()
            app.add_handler(CommandHandler("start", start))
            app.run_polling()
            if 'rerun' in st.session_state:
                print('rerunning')
                del st.session_state['rerun']
                st.rerun()

        connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost', port=5672))
        channel = connection.channel()
        channel.queue_declare(queue='registration_queue', durable=True)
        channel.basic_consume(queue='registration_queue', on_message_callback=callback)
        print("Ожидание сообщений...")
        channel.start_consuming()


if __name__ == "__main__":
    main()