class OngoingMessageManager:
    def __init__(self, system_prompt, historical_messages):
        self.messages = [
            {"role": "system", "content": system_prompt},
            *historical_messages,
        ]

    def add_message(self, message):
        self.messages.append(message)

    def add_user_message(self, message):
        self.messages.append({
            "role": "user",
            "content": message,
        })

    def add_assistant_message(self, message):
        self.messages.append({
            "role": "assistant",
            "content": message,
        })

    def add_tool_result(self, result, call_id):
        if not call_id:
            raise ValueError("Tool call ID is required to add a tool result.")
        self.messages.append({
            "role": "tool",
            "content": str(result),
            "tool_call_id": call_id,
        })

    def get_messages(self):
        return self.messages

    def get_intermediate_messages(self):
        return [message for message in self.messages if message["role"] != "user"]
