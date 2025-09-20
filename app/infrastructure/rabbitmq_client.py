import pika
import json
from ..domain.models import Clientes

RABBITMQ_HOST = 'localhost'
QUEUE_NAME = 'clientes.fila.v2'

def publicar_cliente(novo_cliente: Clientes):
    cliente: dict = {
        "cpf": novo_cliente.cpf,
        "nome": novo_cliente.nome,
        "sistema": novo_cliente.sistema
    }

    connection = pika.BlockingConnection(pika.ConnectionParameters(host=RABBITMQ_HOST))
    channel = connection.channel()

    # Declara fila (idempotente)
    channel.queue_declare(queue=QUEUE_NAME, durable=True)

    mensagem = json.dumps(cliente)
    channel.basic_publish(
        exchange='',
        routing_key=QUEUE_NAME,
        body=mensagem,
        properties=pika.BasicProperties(
            delivery_mode=2,
            content_type='application/json'
        )
    )
    print(f"Mensagem publicada na fila: {mensagem}")

    connection.close()