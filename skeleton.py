from chatterbot import ChatBot
from chatterbot.trainers import ChatterBotCorpusTrainer, ListTrainer
import nltk
import ssl
import spacy


try:
    _create_unverified_https_context = ssl._create_unverified_context
except AttributeError:
    pass
else:
    ssl._create_default_https_context = _create_unverified_https_context

# nltk.download()

food_chatbot = ChatBot('FoodBot',
                       logic_adapters=[
                           {"import_path": "chatterbot.logic.BestMatch"
                            "statement_comparison_function": }
                       ])

# Create a new trainer for the chatbot
trainer = ListTrainer(chatbot=food_chatbot)


#Train the chatbot on a custom dataset for food-related queries
custom_food_dataset = [
    'What should I eat?',
    'burgers'
]

#all_data = ['chatterbot.corpus.english']
#all_data.extend(custom_food_dataset)

# Train the chatbot on the custom food dataset
trainer.train("chatterbot.corpus.english")

def get_restaurant_recommendation(location, cuisine):
    pass

def book_reservation(restaurant_name):
    pass


def get_restaurant_recommendation(location, cuisine):
    pass

def has_city_name(response):
    nlp = spacy.load("en_core_web_sm")
    doc = nlp(response)
    return any(ent.label_ == "GPE" for ent in doc.ents)

def extract_city_name(response):
    nlp = spacy.load("en_core_web_sm")
    doc = nlp(response)
    city_names = [ent.text for ent in doc.ents if ent.label_ == "GPE"]
    return city_names

def chat_with_bot():
    print("Food Bot: Hello! I'm FoodBot. Ask me anything about food.")

    while True:
        user_input = input("You: ")
        location = None
        city = None

        if 'where' in user_input:
            if location == None:
                input_city = input('What city would you like')
                # logic to implement yelp API
            elif city == None:
                input_cuisine = input('What are you searching for')
                # logic to implement yelp API

        else:
            location = getting_city(user_input)
            cuisine = getting_cuisine(user_input)

            # function to get_restaurant(location, cuisine)
            response = food_chatbot.get_response(user_input)
            print(f'Food Bot: {response}')

def checking_response(response, value_type='city'):
    if value_type not in ['city', 'cuisine']:
        raise ValueError("Invalid value_type. Use 'city' or 'cuisine'.")
    if value_type == 'city':
        return getting_city(response)
    elif value_type == 'cuisine':
        return getting_cuisine(response)

def getting_city(response):
    if has_city_name(response):
        city_name = extract_city_name(response)
        return city_name
    else:
        return None

def getting_cuisine(response):
    if 'breakfast' in response:
        return 'breakfast'
    elif 'dinner' in response:
        return ('dinner')
    elif 'lunch' in response:
        return 'dinner'
    elif 'restaurant' in response:
        return 'restaurant'
    elif 'boba' in response:
        return 'boba'
    else:
        return None
def main():
    chat_with_bot()

if __name__ == '__main__':
    main()