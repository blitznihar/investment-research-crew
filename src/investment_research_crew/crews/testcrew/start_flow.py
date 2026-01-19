import uuid
from queue_bus import publish, new_envelope


def main():
    run_id = str(uuid.uuid4())
    thread_id = str(uuid.uuid4())

    msg = new_envelope(
        step="research",
        to="research",
        payload={"topic": "Agentic AI in insurance underwriting", "crash_test": False},
        thread_id=thread_id,
        run_id=run_id,
    )
    publish("task.research", msg)

    print("Started flow:")
    print("run_id =", run_id)
    print("thread_id =", thread_id)


if __name__ == "__main__":
    main()
