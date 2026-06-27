class ShortTermMemory:
    def __init__(self, max_turns=5):
        self.max_turns=max_turns
        self.messages = []
    
    def add_message(self, role, content):
        self.messages.append({"role": role, "content": f"{content}"})

    def get_messages(self):
        return self.messages[-(self.max_turns * 2):]

    def clear(self):
        self.messages = []

