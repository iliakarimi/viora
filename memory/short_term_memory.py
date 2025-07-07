class ShortTermMemory:
    def __init__(self):
        self.messages = []

    def add_message(self, role, content):
        self.messages.append({"role": role, "content": f"{content}"})

    def get_messages(self):
        return self.messages

    def clear(self):
        self.messages = []
