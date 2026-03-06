import uuid

class UUIDUtils:
    @staticmethod
    def generate_uuid():
        return str(uuid.uuid4())