import uuid

import secrets


def random_code():

    return secrets.token_hex(16)
def generate_uuid():

    return str(uuid.uuid4())