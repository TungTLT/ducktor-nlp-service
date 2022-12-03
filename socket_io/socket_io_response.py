class SocketIOResponse:
    def __init__(self, content, next_event='', action_code='', suggest_messages=None, extra_data=None):
        if suggest_messages is None:
            suggest_messages = []

        self.content = content
        self.next_event = next_event
        self.action_code = action_code
        self.suggest_messages = suggest_messages
        self.extra_data = extra_data

    def as_dictionary(self):
        return {
            'content': self.content,
            'next_event': self.next_event,
            'action_code': self.action_code,
            'suggest_messages': self.suggest_messages,
            'extra_data': self.extra_data
        }
