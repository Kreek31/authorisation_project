import json
import pika

def publish_registration_event(user_data):
    connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost', port=5672))
    channel = connection.channel()
    # Объявляем очередь, если её ещё нет (durable – для сохранности сообщений)
    channel.queue_declare(queue='registration_queue', durable=True)
    # Преобразуем данные в JSON
    message = json.dumps(user_data)
    channel.basic_publish(
        exchange='',
        routing_key='registration_queue',
        body=message,
        properties=pika.BasicProperties(
            delivery_mode=2,  # Сообщение будет сохраняться на диск
        )
    )
    connection.close()