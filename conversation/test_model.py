from ollama import chat

stream = chat(
            model="llama3.2:1b",  
            messages=[{'role': 'user', 'content': '你是谁？'}],
            stream=False
        )

# print(stream['message']['content'])
print(stream)
# for chunk in stream:
#     print(chunk, end='', flush=True)