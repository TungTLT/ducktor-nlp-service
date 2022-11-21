class SocketIOResponse:
    def __init__(self, intent, content, next_event='', action_code='', suggest_messages= []):
        self.intent = intent
        self.content = content
        self.next_event = next_event
        self.action_code = action_code
        self.suggest_messages = suggest_messages

    def as_dictionary(self):
        return {
            'intent': self.intent,
            'content': self.content,
            'next_event': self.next_event,
            'action_code': self.action_code,
            'suggest_messages': self.suggest_messages
        }
