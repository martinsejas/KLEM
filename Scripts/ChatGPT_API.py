import openai
import tkinter as tk

openai.api_key = ' Put your API Here'

def your_script():
    generated_text = "Hello Chatgpt tell me a joke about AI"
    return generated_text

def send_to_gpt(text):
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo", 
        messages=[
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": text}
        ]
    )
    return response['choices'][0]['message']['content']

def update_gui():
    text = your_script()
    response = send_to_gpt(text)
    text_widget.insert(tk.END, response)

root = tk.Tk()

text_widget = tk.Text(root)
text_widget.pack()

button = tk.Button(root, text='Update', command=update_gui)
button.pack()

root.mainloop()
