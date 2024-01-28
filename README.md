# Chatterbot Yelp Recommender

This project utilizes a chatterbot and the Yelp API to provide restaurant recommendations. 

## Overview

The `gui.py` module launches a graphical interface for the chatbot. Users can enter keywords about what type of cuisine, price range, etc. they are looking for, and the chatbot will query the Yelp API to find matching restaurants. Users can then ask for more details on a restaurant to read reviews, see photos, get contact information, etc.

## Usage

To use this application:

1. Sign up for a [Yelp Fusion API Key](https://www.yelp.com/developers/documentation/v3)
2. Add your API Key to `yelp.py`
3. Run `python gui.py` to launch the graphical interface
4. Chat with the bot to get restaurant recommendations based on keywords
5. Select a restaurant to see more details pulled from Yelp

## Dependencies

This project requires the following libraries:

- ChatterBot
- Ssl
  
Install missing dependencies using `pip install -r requirements.txt`.

## Customizing

The bot conversation logic is defined in `chatbot.py`. You can modify this to change dialog flow, responses, etc. Commented out is a way to train the bot rhough responses,
as well as more starters for conversation flows.

The Yelp API queries are made in `yelp.py`. Modify the search parameters here.

The graphical interface is powered by Tkinter in `gui.py`. Customize the UI by editing this file.
