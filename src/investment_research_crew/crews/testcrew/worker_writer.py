""" Worker for the writer step in the resilient researcher crew.
"""
import json

from queue_bus import connect, setup_topology, WRITER_Q
from checkpoint import already_processed, mark_processed
from crew_agents import run_write

CRASH_ON_PURPOSE = True  # flip this to False after you test resume


def main():
    """
    Docstring for main
    """
    conn = connect()
    ch = conn.channel()
    setup_topology(ch)
    ch.basic_qos(prefetch_count=1)

    def handler(ch, method, properties, body: bytes):
        """
        Docstring for handler
        
        :param ch: Description
        :param method: Description
        :param properties: Description
        :param body: Description
        :type body: bytes
        """
        msg = json.loads(body.decode("utf-8"))
        run_id = msg["run_id"]
        message_id = msg["message_id"]

        if already_processed(run_id, message_id):
            ch.basic_ack(delivery_tag=method.delivery_tag)
            return

        # Optional crash test: simulate failure after research has completed
        if CRASH_ON_PURPOSE and msg["payload"].get("crash_test", False):
            print("Simulating crash BEFORE processing writer step...")
            raise RuntimeError("Intentional crash to test resume")

        bullets = msg["payload"]["summary_bullets"]
        paragraph = run_write(bullets)

        mark_processed(run_id, message_id, step="write", output=paragraph)

        print("\n=== FINAL OUTPUT ===\n")
        print(paragraph)
        print("\n====================\n")

        ch.basic_ack(delivery_tag=method.delivery_tag)

    ch.basic_consume(queue=WRITER_Q, on_message_callback=handler, auto_ack=False)
    print("Writer worker consuming...")
    ch.start_consuming()


if __name__ == "__main__":
    main()
