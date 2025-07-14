import tkinter as tk
from tkinter import ttk, scrolledtext
import requests
import json

class RecipeAssistant:
    def __init__(self, master):
        self.master = master
        master.title("Nigeria AI Recipe Assistant")
         #Set the window size
        master.geometry("600x500")

        #Add a title label
        self.title_label= ttk.Label(master, text="Nigeria AI Recipe Assistant",font=("Helvetica", 16, "bold"))
        self.title_label.pack(pady=10)

        #Add Instruction label
        self.ingredients_label= ttk.Label(master, text="Enter ingredients you have (separate with commas):")
        self.ingredients_label.pack(pady=5)

        #Add Entry for Ingredients
        self.ingredients_entry = ttk.Entry(master, width=60)
        self.ingredients_entry.pack(pady=5)

        #Button to get recipe
        self.get_recipes_button = ttk.Button(master, text= "Get Recipe Suggestions", command=self.get_recipes)
        self.get_recipes_button.pack(pady=10)

        #Result label and text area
        self.result_label = ttk.Label(master, text= "Recipe Suggestions:")
        self.result_label.pack(pady=5)

        self.results_display = scrolledtext.ScrolledText(master, width=70, height=20, wrap=tk.WORD)
        self.results_display.pack(pady=5)

    def get_recipes(self):
        ingredients = self.ingredients_entry.get()
        if not ingredients:
            self.results_display.insert(tk.END, "Please enter some ingredients first!\n")
            return

        #Clear previous results and show loading
        self.results_display.delete(1.0, tk.END)
        self.results_display.insert(tk.END, "Thinking of Nigerian recipes... Please wait...\n")
        self.master.update()

        # Prepare prompt
        prompt =f"Suggest 3 authentic Nigerian recipes I can make with these ingredients: {ingredients}."\
                f"For each recipe, provide: 1) Recipe name, 2) Full ingredients list, 3) Step-by-step preparation instructions."\
                f"Format each recipe clear with headings."

        try:
            response = self.call_together_api(prompt)
            self.results_display.delete(1.0, tk.END)
            self.results_display.insert(tk.END, response)
        except Exception as e:
            self.results_display.delete(1.0, tk.END)
            self.results_display.insert(tk.END, f"Error: {str(e)}\n")

    def call_together_api(self, prompt):
        url = "https://api.together.xyz/inference"
        api_key = "f9ab7cf01581c657c6950be37c22606bfa56e27a131fd1762c2200350ae399cf"

        headers = {
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json"
        }
        data = {
            "model": "mistralai/Mistral-7B-Instruct-v0.1",
            "prompt": prompt,
            "max_tokens": 1000,
            "temperature": 0.7
        }
        #Make request
        try:
            response = requests.post(url, headers=headers, json=data)
            print("Raw response: ", response.text)

            if response.status_code ==200:
                response_data = response.json()
                print("Parsed response: ", response_data)

                response_text = response_data["output"]["choices"][0]["text"]
                return response_text.strip()
            else:
                return f" API Error: {response.status_code} - {response.text}"

        except Exception as e:
            return f" API Error: {str(e)}"

#Launch the GUI
if __name__ == "__main__":
    root = tk.Tk()
    app = RecipeAssistant(root)
    root.mainloop()











