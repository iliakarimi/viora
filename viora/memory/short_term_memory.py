class ShortTermMemory:
    def __init__(self, max_turns=5):
        self.max_turns=max_turns
        self.agent_messages = []
        self.user_messages = []
    
    def add_message(self, content):
        self.user_messages.append({"role": "user", "content": f"{content}"})
        self.agent_messages.append({"role": "assistant", "content": f"{content}"})

    def get_user_messages(self):
        return self.user_messages[-(self.max_turns * 2):]
    
    def get_agent_messages(self):
        return self.agent_messages[-(self.max_turns * 2):]

    def clear(self):
        self.messages = []
