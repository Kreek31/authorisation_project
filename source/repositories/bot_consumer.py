import streamlit as st
import json
import jwt
import asyncio
import psycopg2
import threading
from repositories.jwt import decode_jwt
from telegram import Bot
from telegram.ext import ContextTypes
from repositories.connector import get_connection
from settings import TELEGRAM_BOT_TOKEN, SECRET_KEY

bot = Bot(token=TELEGRAM_BOT_TOKEN)

def callback(ch, method, properties, body):
    try:
        user_data = json.loads(body)
        chat_id = user_data.get('chat_id')
        message = "Вы авторизовались под логином: " + str(user_data.get("user_name"))
        if chat_id:
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)
            thread = threading.Thread(target=loop.run_forever, daemon=True)
            thread.start()
            future = asyncio.run_coroutine_threadsafe(bot.send_message(chat_id=chat_id, text=message), loop)
            result = future.result(timeout=5)
            loop.call_soon_threadsafe(loop.stop)
            thread.join()
            loop.stop()
            loop.close()
            print(f"Сообщение отправлено пользователю {chat_id}")
        else:
            print("Отсутствует telegram_chat_id")
        # Завершаем обработку сообщения
        ch.basic_ack(delivery_tag=method.delivery_tag)
        # Останавливаем ожидание новых сообщений
        ch.stop_consuming()
    except Exception as e:
        print("Ошибка при обработке сообщения!!!:", e)
        loop.call_soon_threadsafe(loop.stop)
        loop.stop()
        loop.close()
        ch.basic_ack(delivery_tag=method.delivery_tag)
        ch.stop_consuming()
        # Если ошибка, можно не подтверждать сообщение, чтобы оно было доставлено повторно



async def start(update, context: ContextTypes.DEFAULT_TYPE):
    token = decode_jwt(st.session_state["token"])["token"]
    chat_id = update.effective_chat.id
    # Сохраните chat_id в базу данных (здесь вызов вашей функции сохранения)
    print(f"Получен chat_id: {chat_id}, Тип логина: {token['login']}")

    if token['chat_id'] == None:
        if token['login'] == 'our':
            query = """UPDATE users SET chat_id = %s WHERE user_id = %s"""
        elif token['login'] == 'yandex':
            query = """UPDATE yandex_users SET chat_id = %s WHERE user_id = %s"""

        with get_connection() as conn:
            with conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor) as cur:
                cur.execute(query, [chat_id, token['user_id']])
                conn.commit()
                print("изменения сохранены")
        
        token['chat_id'] = chat_id
        new_token = jwt.encode(token, SECRET_KEY, algorithm='HS256')
        st.session_state.token = new_token
        st.session_state.rerun = True

    
    await update.message.reply_text("Ваш chat_id сохранен! Теперь бот может отправлять вам сообщения.")
    
    # Останавливаем бота после получения первого сообщения
    context.application.stop()
    asyncio.get_running_loop().call_soon_threadsafe(asyncio.get_running_loop().stop)
