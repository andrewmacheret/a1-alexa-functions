#!/usr/bin/env python2.7

from urllib import quote
import json
from requests import get
import pprint
pp = pprint.PrettyPrinter(indent=4)

def lambda_handler(event, context):
    """ Route the incoming request based on type (LaunchRequest, IntentRequest,
    etc.) The JSON body of the request is provided in the event parameter.
    """
    print("event.session.application.applicationId=" +
          event['session']['application']['applicationId'])

    if event['session']['new']:
        on_session_started({'requestId': event['request']['requestId']},
                           event['session'])

    if event['request']['type'] == "LaunchRequest":
        return on_launch(event['request'], event['session'])
    elif event['request']['type'] == "IntentRequest":
        return on_intent(event['request'], event['session'])
    elif event['request']['type'] == "SessionEndedRequest":
        return on_session_ended(event['request'], event['session'])


def on_session_started(session_started_request, session):
    """ Called when the session starts """

    print("on_session_started requestId=" + session_started_request['requestId']
          + ", sessionId=" + session['sessionId'])


def on_launch(launch_request, session):
    """ Called when the user launches the skill without specifying what they
    want
    """

    print("on_launch requestId=" + launch_request['requestId'] +
          ", sessionId=" + session['sessionId'])
    # Get's the help section

    return get_welcome_response()


def on_intent(intent_request, session):
    """ Called when the user specifies an intent for this skill """

    print("on_intent requestId=" + intent_request['requestId'] +
          ", sessionId=" + session['sessionId'])

    intent = intent_request['intent']
    intent_name = intent_request['intent']['name']

    # Sends the request to one of our intents
    if intent_name == "Pun":
        return get_pun_response()
    elif intent_name == "ShowerThought":
        return get_shower_thought_response()
    elif intent_name == "MathFact":
        return get_math_fact_response(intent)
    elif intent_name == "AMAZON.HelpIntent":
        return get_welcome_response()
    else:
        print(intent_name)
        return build_response({},  build_speechlet_response(None, 'not ok'))

def on_session_ended(session_ended_request, session):
    # When the User decides to end the session, this is the function that is
    # called.
    print("on_session_ended requestId=" + session_ended_request['requestId'] +
          ", sessionId=" + session['sessionId'])
    # add cleanup logic here

# --------------- Functions that control the skill's behavior ------------


def get_welcome_response():
    """ Helps the User Find out what they can say, and how to use
            the program, Sends a Card with that data as well"""
    session_attributes = {}
    card_title = "Andy"
    speech_output = "Ask Andy for a pun, a shower thought, or a math fact."
    reprompt_text = "Please ask me for a pun."
    should_end_session = False
    return build_response(session_attributes, build_speechlet_response(
        card_title, speech_output, reprompt_text, should_end_session))


def handle_session_end_request():
    print('handle_session_end_request')
    should_end_session = True
    return build_response({}, build_speechlet_response(
        None, None, None, should_end_session))


def get_pun_response():

    response = get('https://pun.andrewmacheret.com')
    data = response.json()
    pp.pprint(data)

    pun = data['pun']

    speech = build_speechlet_response("Andy - Pun", pun)
    return build_response({}, speech)

def get_shower_thought_response():
    #curl -s -L -A 'asdf' -X GET 'https://www.reddit.com/r/Showerthoughts/random.json'  

    response = get('https://remote-apis.andrewmacheret.com/reddit/Showerthoughts/random.json')
    data = response.json()
    pp.pprint(data)
    shower_thought = data[0]['data']['children'][0]['data']['title']

    speech = build_speechlet_response("Andy - Shower Thought", shower_thought)
    return build_response({}, speech)

def get_math_fact_response(intent):
    number = None
    pp.pprint(intent)
    number = intent['slots']['number'].get('value')
    numberString = int(number) if number is not None else 'random'

    response = get(
        'http://numbersapi.com/%s' % (numberString),
        headers={ 'User-Agent': 'Andy' }
    )
    math_fact = response.text

    speech = build_speechlet_response("Andy - Math Fact", math_fact)
    return build_response({}, speech)


# --------------- Helpers that build all of the responses ----------------


def build_speechlet_response(title, output, reprompt_text="", should_end_session=True):
    if output == None:
        return {
            'shouldEndSession': should_end_session
        }
    elif title == None:
        return {
            'outputSpeech': {
                'type': 'PlainText',
                'text': output
            },
            'reprompt': {
                'outputSpeech': {
                    'type': 'PlainText',
                    'text': reprompt_text
                }
            },
            'shouldEndSession': should_end_session
        }
    else:
        return {
            'outputSpeech': {
                'type': 'PlainText',
                'text': output
            },
            'card': {
                'type': 'Simple',
                'title':  title,
                        'content': output
            },
            'reprompt': {
                'outputSpeech': {
                    'type': 'PlainText',
                    'text': reprompt_text
                }
            },
            'shouldEndSession': should_end_session
        }


def build_response(session_attributes, speechlet_response):
    return {
        'version': '1.0',
        'sessionAttributes': session_attributes,
        'response': speechlet_response
    }


