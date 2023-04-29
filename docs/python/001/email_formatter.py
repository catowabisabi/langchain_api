import tkinter as tk
from langchain import PromptTemplate
from langchain.llms import OpenAI
from 

def load_LLM(openai_api_key):
    """Logic for loading the chain you want to use should go here."""
    # Make sure your openai_api_key is set as an environment variable
    llm = OpenAI(temperature=.7, openai_api_key=openai_api_key)
    return llm

def generate_email_response():
    email_input = email_entry.get("1.0", tk.END).strip()
    if len(email_input.split(" ")) > 700:
        response_text.delete("1.0", tk.END)
        response_text.insert(tk.END, "Please enter a shorter email. The maximum length is 700 words.")
        return
    prompt_with_email = prompt.format(tone=tone_choice.get(), dialect=dialect_choice.get(), email=email_input)
    formatted_email = llm(prompt_with_email)
    response_text.delete("1.0", tk.END)
    response_text.insert(tk.END, formatted_email)

prompt = """
    Below is an email that may be poorly worded.
    Your goal is to:
    - Properly format the email
    - Convert the input text to a specified tone
    - Convert the input text to a specified dialect

    Here are some examples different Tones:
    - Formal: We went to Barcelona for the weekend. We have a lot of things to tell you.
    - Informal: Went to Barcelona for the weekend. Lots to tell you.  

    Here are some examples of words in different dialects:
    - American: French Fries, cotton candy, apartment, garbage, cookie, green thumb, parking lot, pants, windshield
    - British: chips, candyfloss, flag, rubbish, biscuit, green fingers, car park, trousers, windscreen

    Example Sentences from each dialect:
    - American: I headed straight for the produce section to grab some fresh vegetables, like bell peppers and zucchini. After that, I made my way to the meat department to pick up some chicken breasts.
    - British: Well, I popped down to the local shop just the other day to pick up a few bits and bobs. As I was perusing the aisles, I noticed that they were fresh out of biscuits, which was a bit of a disappointment, as I do love a good cuppa with a biscuit or two.

    Please start the email with a warm introduction. Add the introduction if you need to.
    
    Below is the email, tone, and dialect:
    TONE: {}
    DIALECT: {}
    EMAIL: {}
    
    YOUR {dialect} RESPONSE:
"""

root = tk.Tk()
root.title("Globalize Email")
root.geometry("800x600")

llm = None

# Top Frame
top_frame = tk.Frame(root)
top_frame.pack(side="top", fill="both")

# Input Frame
input_frame = tk.Frame(top_frame)
input_frame.pack(side="top", padx=20, pady=20)

tone_label = tk.Label(input_frame, text="Choose Tone:")
tone_label.grid(row=0, column=0, padx=10, pady=10)

tone_choice = tk.StringVar(value="Formal")
formal_tone = tk.Radiobutton(input_frame, text="Formal", variable=tone_choice, value="Formal")
formal_tone.grid(row=0, column=1, padx=10, pady=10)

informal_tone = tk.Radiobutton(input_frame, text="Informal", variable=tone_choice, value="Informal")
informal_tone.grid(row=0, column=2, padx=10, pady=10)

dialect_label = tk.Label(input_frame, text="Choose English Dialect:")
dialect_label.grid(row=1, column=0, padx=10, pady=10)

dialect_choice = tk.StringVar(value="American")
american_dialect = tk.Radiobutton(input_frame, text="American", variable=dialect_choice, value="American")
american_dialect.grid(row=1, column=1, padx=10, pady=10)

british_dialect = tk.Radiobutton(input_frame, text="British", variable=dialect_choice, value="British")
british_dialect.grid(row=1, column=2, padx=10, pady=10)

email_label = tk.Label(input_frame, text="Enter Your Email:")
email_label.grid(row=2, column=0, padx=10, pady=10)

email_entry = tk.Text(input_frame, height=5)
email_entry.grid(row=2, column=1, columnspan=2, padx=10, pady=10)

#Button Frame
button_frame = tk.Frame(top_frame)
button_frame.pack(side="top", padx=20, pady=20)

submit_button = tk.Button(button_frame, text="Submit", command=generate_email_response)
submit_button.pack(padx=10, pady=10)

#Response Frame
response_frame = tk.Frame(top_frame)
response_frame.pack(side="top", padx=20, pady=20)

response_label = tk.Label(response_frame, text="Your Converted Email:")
response_label.pack(padx=10, pady=10)

response_text = tk.Text(response_frame, height=10, state="disabled")
response_text.pack(padx=10, pady=10)

#Bottom Frame
bottom_frame = tk.Frame(root)
bottom_frame.pack(side="bottom", pady=20)

#Footer Label
footer_label = tk.Label(bottom_frame, text="Powered by LangChain and OpenAI")
footer_label.pack(side="bottom", padx=10, pady=10)

root.mainloop()
