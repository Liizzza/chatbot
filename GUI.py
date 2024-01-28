import tkinter as tk
import yelp
from skeleton import food_chatbot

keyword_yes = ['yes','sure','ok','okay','yeah','k','of course']
class ChompBot:
    def __init__(self, master):
        self.master = master
        master.title("ChompBot")

        # Set the background color
        master.config(bg="#a3ccae")

        # Make the text box scalable and set the background color
        self.conversation = tk.Text(master, wrap=tk.WORD, width=60, height=20, font=("Helvetica", 12), bg="#a3ccae", state=tk.DISABLED)
        self.conversation.pack(padx=10, pady=10)

        # Increase the width of the entry box
        self.entry = tk.Entry(master, width=60, font=("Helvetica", 12))
        self.entry.pack(padx=10, pady=10)
        self.entry.bind("<Return>", lambda event: self.process_input())

        self.entry.focus()

        # Variables to store user responses
        self.location = None
        self.category = None
        self.type_of_food = None
        self.keywords = None
        self.price_range = None
        self.options = None
        self.business_name = None

        self.waiting_for_specific_type = False

        # Flag to track when in the search loop
        self.in_search_loop = False

        self.print_prompt("Hello! I am ChompBot🍔 and here to help you!")

    def print_prompt(self, prompt):
        self.conversation.config(state=tk.NORMAL)
        self.conversation.insert(tk.END, f"ChompBot🍔: {prompt}\n")
        self.conversation.config(state=tk.DISABLED)

    def process_input(self):
        user_input = self.entry.get()
        # Display user's input immediately
        self.conversation.config(state=tk.NORMAL)
        self.conversation.insert(tk.END, f"You: {user_input}\n")
        self.conversation.config(state=tk.DISABLED)
        self.conversation.see(tk.END)

        # Your custom processing logic goes here
        # For example, you can print the input to the console
        print("Processing user input:", user_input)

        if "bye" in user_input.lower() or "see you" in user_input.lower():
            self.print_prompt(
                "ChompBot🍔: Goodbye! I hope I helped assist you!"
            )
            self.master.destroy()


        elif "find" in user_input.lower() or "search" in user_input.lower() or 'where' in user_input.lower():
            self.in_search_loop = True
            self.print_prompt("Please enter your location")
            self.entry.delete(0, tk.END)
        elif self.in_search_loop:
            if not self.location:
                self.location = user_input
                self.entry.delete(0, tk.END)
                self.print_prompt("What are you searching for?")
            elif not self.category:
                self.category = user_input
                self.entry.delete(0, tk.END)
                self.print_prompt(f"Please enter a specific type of category for the search!")
            elif not self.type_of_food:
                self.type_of_food = user_input
                if self.type_of_food == "no":
                    self.type_of_food = ''
                self.entry.delete(0, tk.END)
                self.print_prompt("Please enter a specific price? Type 1,2,3, or 4. One being least expensive")
            elif not self.price_range:
                self.price_range = user_input
                self.entry.delete(0, tk.END)
                try:
                    self.price_range = int(self.price_range)
                    if self.price_range < 1 or self.price_range >4:
                        self.print_prompt("Too high or Too low! Please enter how many options you would like: ")
                        self.price_range = None
                        self.entry.delete(0, tk.END)
                    else:
                        self.print_prompt(
                            "Please enter how many options you want! Must be less than twenty")
                except ValueError:
                    self.print_prompt("Invalid Number for price")
                    self.print_prompt("Please enter how many options you want! Must be less than twenty")

            elif not self.options:
                self.options = user_input
                self.entry.delete(0, tk.END)
                try:
                    self.options = int(self.options)
                    if self.options < 1 or self.options >20:
                        self.print_prompt("Too high or Too low!")
                except ValueError:
                    self.print_prompt("Invalid number")

                self.entry.delete(0, tk.END)
                self.conversation.config(state = tk.NORMAL)
                self.conversation.insert(tk.END,
                                         f"ChompBot🍔: Searching {self.category} in {self.location}")

                business_search_query = yelp.build_search_query_basic(
                    location = self.location,
                    type_of_food = self.type_of_food,
                    category = self.category,
                    price = self.price_range,
                    sort_by = "best_match",
                    limit = self.options
                )

                business_url = yelp.build_search_url(business_search_query)
                business_dict = yelp.request(business_url)
                business_string = yelp.format_business_data(business_dict)
                self.conversation.insert(tk.END,business_string + '\n')

                self.print_prompt(
                    "ChompBot🍔: Would you like to learn more about any business? Either type the name or press enter"
                )

            elif not self.business_name:
                self.business_name = user_input
                self.entry.delete(0,tk.END)
                if len(self.business_name.strip()) == 0:
                    self.location = None
                    self.category = None
                    self.keywords = None
                    self.price_range = None
                    self.in_search_loop = False
                    self.business_name = None
                else:
                    business_search_query = yelp.build_search_query_basic(
                        location = self.location,
                        type_of_food = self.type_of_food,
                        category = self.category,
                        price = self.price_range,
                        sort_by = "best_match",
                        limit = self.options
                    )
                    url = yelp.build_search_url(business_search_query)
                    print(url)
                    response = yelp.request(url)
                    business_id = yelp.grab_business_id(response, self.business_name)
                    print(business_id)

                    if business_id is not None:
                        review_url = yelp.build_reviews_url(business_id)
                        reviews_dict = yelp.request(review_url)
                        reviews_string = yelp.format_reviews_data(reviews_dict)
                        self.conversation.config(state = tk.NORMAL)
                        self.conversation.insert(tk.END, f"ChompBot🍔: {reviews_string}\n")
                    else:
                        self.print_prompt("ChompBot🍔: Sorry business id couldnt be found")

                self.conversation.config(state = tk.DISABLED)

            else:
                self.location = None
                self.category = None
                self.keywords = None
                self.price_range = None
                self.in_search_loop = False
                self.business_name = None

        else:
            self.conversation.config(state=tk.NORMAL)
            bot_response = food_chatbot.get_response(user_input)
            self.conversation.insert(tk.END, f"ChompBot🍔: {bot_response}\n")
            self.conversation.config(state=tk.DISABLED)
            self.entry.delete(0, tk.END)

        self.entry.focus()

if __name__ == "__main__":
    root = tk.Tk()
    app = ChompBot(root)
    root.mainloop()

