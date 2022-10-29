class SocketIOResponse:
    def __init__(self, intent, content, next_event):
        self.intent = intent
        self.content = content
        self.next_event = next_event

    def as_dictionary(self):
        return {
            'intent': self.intent,
            'content': self.content,
            'next_event': self.next_event
        }
