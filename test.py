from gpt4free import you
chat = []

while True:
    prompt = input("You: ")
    if prompt == 'q':
        break
    response = you.Completion.create(
        prompt=prompt,
        chat=[])

    print("Bot:", response.text)

    chat.append({"question": prompt, "answer": response.text})