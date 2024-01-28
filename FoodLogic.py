from chatterbot.logic import LogicAdapter
from chatterbot.conversation import Statement
from yelp import (build_search_query_basic, build_search_url,
                                  request, format_business_data,
                                  grab_business_id, find_and_print_restaurant_details)

import os

# Get the directory of the current script or module
current_directory = os.path.dirname(os.path.abspath(__file__))

print("Current Directory:", current_directory)
class FoodLogicAdapter(LogicAdapter):
    def __init__(self, chatbot, **kwargs):
        super().__init__(chatbot, **kwargs)

    def can_process(self, statement):
        keywords = ['food', 'restaurant', 'recommendation']
        return any(keyword in statement.text.lower() for keyword in keywords)

    def process(self, input_statement, additional_response_selection_parameters=None):
        location = input("Food Bot🍔: Enter your location\nYou: ")
        type_of_food = input("Food Bot🍔: What are you searching for\nYou: ")

        query = build_search_query_basic(location=location, type_of_food=type_of_food)
        search_url = build_search_url(query)

        response_data = request(search_url)

        if response_data:
            formatted_data = format_business_data(response_data)
            print(formatted_data)

            # Optionally, you can ask the user if they want more details about a specific restaurant
            answer = input("Food Bot🍔: Would you like more details about any of these options? (yes/no)\nYou: ")
            if answer.lower() == 'yes':
                restaurant_name = input("Food Bot🍔: Please enter the name of the restaurant you're interested in\nYou: ")
                business_id = grab_business_id(response_data, restaurant_name)

                if business_id:
                    find_and_print_restaurant_details(build_search_query_basic(location=location, type_of_food=type_of_food))
                else:
                    print("Food Bot🍔: Restaurant not found. Please try again.")

            confidence = 1.0
        else:
            print("Food Bot🍔: No data found! Error occurred, please retry.")
            confidence = 0.0

        response_statement = Statement(text="Placeholder response")  # Customize this as needed
        response_statement.confidence = confidence
        return response_statement
