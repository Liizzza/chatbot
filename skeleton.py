from chatterbot import ChatBot
from chatterbot.trainers import ChatterBotCorpusTrainer, ListTrainer
import nltk
import ssl
import spacy
import yelp
import collections
collections.Hashable = collections.abc.Hashable

try:
    _create_unverified_https_context = ssl._create_unverified_context
except AttributeError:
    pass
else:
    ssl._create_default_https_context = _create_unverified_https_context

food_chatbot = ChatBot('FoodBot', logic_adapters=[
        "chatterbot.logic.BestMatch"
    ])

trainer = ChatterBotCorpusTrainer(food_chatbot)
datasets_to_train = ['chatterbot.corpus.english.food',
                    'chatterbot.corpus.english.conversations',
                    'chatterbot.corpus.english.greetings',
                    'chatterbot.corpus.english.health'
                     ]

# 'chatterbot.corpus.english.greetings',
#                      'chatterbot.corpus.english.conversations',
#                      'chatterbot.corpus.english.food',
#                      'chatterbot.corpus.english.health'

trainer.train(*datasets_to_train)

trainer_list = ListTrainer(food_chatbot)

trainer_list.train([
    "Hi", "Hello, I am your FoodBot🍔! How can I help you",
    "I am hungry.", "Here are some suggestions: pizza places, burger places, and italian places",
    "Recommend me healthy food.", "There are many places with healthy food! To learn more type 'where should i eat'",
    "Thank you for your help", "No problem. Anything else you need?"
])
# trainer_list.train([
#     "I don't know what to eat", "Are you really hungry?",
#     "Yes I am", "Oh no, would you like me to recommend you places?",
#     "Yes I want suggestions", "Here are some suggestions: pizza places, burger places, and italian places",
#     "I want ones in my area", "For more recommendations ask 'where should I eat'"
#     "Thank you for your help.", "No problem. Anything else you need?"
#     "i am hungry", "excellent! i can recommend you food!"
#     ]
# )
trainer_list.train([
    "Hello! I am hungry", "Would you like recommendations?",
    "I am hungry", "Hi hungry, Im dad. Joking. Would you look food recs?",
    "I want to be healthy", "Perfect! I can help start your search for health restaurants!",
    "I want to be fat", "Im sure we have our own wants. But, I can help recommend healthy alternatives",
    "Hello", "Hello, what can I help you with?"
    "I want help with finding a restaurant", "Of course! please enter what you want to search for.",
    "What's your all-time favorite food", "Speaking of favorite dishes, have you ever tried cooking that special dish at home, and if so, what's your secret ingredient or technique to make it truly exceptional?"
])
trainer_list.train([
    'im hungry', 'Let me help find you a healthy place recommendation!',
    'im hungry', 'Okay! type "search for food in my area"',
    'im hungry', 'Let me recommend you fresh food in you area! Just ask me to search for something'
    'Im hungry', 'Let me find you fresh, healthy food, just ask me to search!',
    'I want fast food', 'Fast food is cheap and easy but unhealthy. Let me recommend you healthier options',
    'i want fast food', 'Fast food is cheap and easy but unhealthy. Let me recommend you healthier options'
])
trainer_list.train([
    'Recommend me food', "Of course! Tell me to help find food in your area",
    "recommend me food", "Of course! Tell me to help"
])

trainer_list.train([
    "Recommend me a boba place", "Of course! Tell me to find a boba place in your area",
    "I want to drink boba", "I will help you find boba in your area, please type 'find boba in my area'",
    "I want coffee", "Of course! I can help you find coffee in your area, please enter 'find coffee in my area'"
    "boba recommendations", "Okay I can help you find some as soon as you specify to find boba in an area",
    "coffee recommendations", "Okay I can help you find some as soon as you specify to find coffee in an area",
    "matcha reccommendations", "Okay! I can help you find some as soon as you specify to find matcha in your area",
    "matcha", "Do you mean, the best thing on earth? I can help you find the universe's gift to the world with an easy search"
])
#
# trainer_list.train([
#     'hi i want food recommendations', 'Of course! I am here to help, what food recommendations do u want.'
#     'I would like you to search for restaurants', "Okay there you go"
#     ]
#     )
# trainer_list.train([
#     'I am not happy with anything you sent me,', "Oh no im so sorry! Would you like to search again?"
#     "Yes, please search for new food", "Okay here!"
# ])
# trainer_list.train([
#     'Hello, I want food recommendations', "Okay would you like me to search for restaurants?",
#     "im hungry", "I can help with that! What would u like."
# ])



agreeing_words = ["YES",'OKAY',"SURE","OK","Y","OKY"]
def chat_with_bot():
    print("Food Bot🍔: Hello! I'm FoodBot. Ask me anything about food.")
    category = None
    location = None
    price = None
    type_of_food = None
    price = None
    limit = 4
    cuisine = None

    while True:
        user_input = input("You: ")

        if 'WHERE' in user_input.upper() or 'SEARCH' in user_input.upper() or 'FIND' in user_input.upper():
            location = input('Food Bot🍔: Enter your location\nYou: ')
            if cuisine is None:
                type_of_food = input('Food Bot🍔: What are you searching for\nYou: ')
            answer = input("Food Bot🍔: Would you like any other criteria?\nYou: ")
            if answer.upper() in agreeing_words:
                answer = input(f"Food Bot🍔:Would you like a specific type of {type_of_food}?\nYou: ")
                if answer.upper() in agreeing_words:
                    category = input("Food Bot🍔: Okay what is it?\nYou: ")
                answer = input(f"Food Bot🍔: Would you like a specific price?\nYou: ")
                if answer.upper() in agreeing_words:
                    price = input("Food Bot🍔: Enter 1,2,3, or 4!\nYou: ")
                    try:
                        price = int(price)
                    except:
                        print("Food Bot🍔: Woops that wasnt a choice!")
                answer = input("Food Bot🍔: Would you like a certain number of options?\nFood Bot: Must be less than twenty!\nYou: ")
                if answer.upper() in agreeing_words:
                    limit = input("Food Bot🍔: Great! Enter your amount\nYou: ")
                    try:
                        limit = int(limit)
                        if limit > 20:
                            print("Food Bot🍔: This was way too much.")
                    except:
                        print("Food Bot🍔: That was not an option!")
            print("Food Bot🍔: Grabbing food data now!")
            query = dict(location = location,
                        type_of_food = type_of_food,
                        category = category,
                        price = price,
                        sort_by = 'best_match',
                        limit = limit
                        )
            yelp.find_and_print_restaurant_details(query)
            answer = input("Food Bot🍔: Would you like to know more about any options?\nYou: ")
            if answer.upper() in agreeing_words:
                answer = input("Food Bot🍔: Great! Please enter the name of the place you want without the exclamation point!\nYou: ")
                query = yelp.build_search_query_basic(location = location,
                                                      type_of_food = type_of_food,
                                                      category = category,
                                                      price = price,
                                                      sort_by = 'best_match',
                                                      limit = limit
                )
                url = yelp.build_search_url(query)
                response = yelp.request(url)
                business_id = yelp.grab_business_id(response,answer)
                if business_id is not None:
                    reviews_query = yelp.build_reviews_query(business_id, limit=4)
                try:
                    print(yelp.find_and_print_rating_details(reviews_query))
                except:
                    print("Food Bot🍔: Woops something went wrong! Please try again later")
        elif 'BYE' in user_input.upper():
            print(f'Food Bot🍔: Goodbye! I hope I helped you find your new favorite place!')
            break
        else:
            response = food_chatbot.get_response(user_input)
            print(f'Food Bot🍔: {response}')
            #
            # feedback = input("Was the response helpful? (yes/no): ")
            # if feedback.lower() == 'yes':
            #     # If the response was helpful, continue the conversation
            #     new_input = input("You: ")
            #     new_response = input("Bot: ")

            #     # Train the chatbot with the new interaction
            #     trainer_list.train([
            #         user_input,
            #         response.text,
            #         new_input,
            #         new_response
            #     ])
            # else:
            #     user_desired = input("What is your desired response?: ")
            #     trainer_list.train([
            #         user_input,
            #         user_desired
            #     ])




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