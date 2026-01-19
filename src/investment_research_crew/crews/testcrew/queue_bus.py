"""_summary_

Returns:
    _type_: _description_
"""

import json
import os
import uuid
from datetime import datetime, timezone

import pika

RABBITMQ_URL = os.getenv("RABBITMQ_URL", "amqp://guest:guest@localhost:5672/")

EXCHANGE = "crew.topic"

RESEARCH_Q = "agent.research.in"
WRITER_Q = "agent.writer.in"
DLQ = "agent.dlq"


def now_iso() -> str:
    """
    Docstring for now_iso

    :return: Description
    :rtype: str
    """
    return datetime.now(timezone.utc).isoformat()


def connect() -> pika.BlockingConnection:
    """
    Docstring for connect

    :return: Description
    :rtype: BlockingConnection
    """
    params = pika.URLParameters(RABBITMQ_URL)
    return pika.BlockingConnection(params)


def setup_topology(channel) -> None:
    """
    Docstring for setup_topology

    :param channel: Description
    """
    channel.exchange_declare(exchange=EXCHANGE, exchange_type="topic", durable=True)

    channel.exchange_declare(exchange="dlx", exchange_type="topic", durable=True)
    channel.queue_declare(queue=DLQ, durable=True)
    channel.queue_bind(exchange="dlx", queue=DLQ, routing_key="#")

    args = {"x-dead-letter-exchange": "dlx"}
    channel.queue_declare(queue=RESEARCH_Q, durable=True, arguments=args)
    channel.queue_declare(queue=WRITER_Q, durable=True, arguments=args)

    channel.queue_bind(exchange=EXCHANGE, queue=RESEARCH_Q, routing_key="task.research")
    channel.queue_bind(exchange=EXCHANGE, queue=WRITER_Q, routing_key="task.write")


def publish(routing_key: str, message: dict) -> None:
    """
    Docstring for publish

    :param routing_key: Description
    :type routing_key: str
    :param message: Description
    :type message: dict
    """
    conn = connect()
    ch = conn.channel()
    setup_topology(ch)

    body = json.dumps(message).encode("utf-8")
    ch.basic_publish(
        exchange=EXCHANGE,
        routing_key=routing_key,
        body=body,
        properties=pika.BasicProperties(
            delivery_mode=2,  # persistent
            content_type="application/json",
            message_id=message.get("message_id"),
        ),
    )
    conn.close()


def new_envelope(step: str, to: str, payload: dict, thread_id: str, run_id: str) -> dict:
    """
    Docstring for new_envelope

    :param step: Description
    :type step: str
    :param to: Description
    :type to: str
    :param payload: Description
    :type payload: dict
    :param thread_id: Description
    :type thread_id: str
    :param run_id: Description
    :type run_id: str
    :return: Description
    :rtype: dict
    """
    return {
        "message_id": str(uuid.uuid4()),
        "thread_id": thread_id,
        "run_id": run_id,
        "step": step,
        "to_agent": to,
        "attempt": 1,
        "created_at": now_iso(),
        "payload": payload,
    }
