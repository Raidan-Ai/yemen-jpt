import uuid


def generate_event_id() -> str:
    """"Return a new event identifier.""""
    return str(uuid.uuid4())
