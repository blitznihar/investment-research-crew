import json

from investment_research_crew.crews.testcrew.queue_bus import (
    connect,
    setup_topology,
    RESEARCH_Q,
    publish,
    new_envelope,
)
from checkpoint import already_processed, mark_processed
from crew_agents import run_research


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

        topic = msg["payload"]["topic"]
        result = run_research(topic)

        # checkpoint this message as done
        mark_processed(run_id, message_id, step="research", output=result)

        # handoff to writer
        next_msg = new_envelope(
            step="write",
            to="writer",
            payload={"summary_bullets": result, "crash_test": msg["payload"].get("crash_test", False)},
            thread_id=msg["thread_id"],
            run_id=run_id,
        )
        publish("task.write", next_msg)

        ch.basic_ack(delivery_tag=method.delivery_tag)

    ch.basic_consume(queue=RESEARCH_Q, on_message_callback=handler, auto_ack=False)
    print("Research worker consuming...")
    ch.start_consuming()


if __name__ == "__main__":
    main()
