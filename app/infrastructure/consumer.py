import pika

QUEUE_NAME = "clientes.fila.v2"

connection = pika.BlockingConnection(pika.ConnectionParameters("localhost"))
channel = connection.channel()

channel.queue_declare(queue=QUEUE_NAME, durable=True)

def callback(ch, method, properties, body):
    print(f"📥 Mensagem recebida: {body.decode()}")

channel.basic_consume(queue=QUEUE_NAME, on_message_callback=callback, auto_ack=True)

print("🔄 Aguardando mensagens. Pressione CTRL+C para sair.")
channel.start_consuming()