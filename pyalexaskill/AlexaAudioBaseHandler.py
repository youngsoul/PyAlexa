from pyalexaskill.AlexaBaseHandler import AlexaBaseHandler
import logging


class AlexaAudioBaseHandler(AlexaBaseHandler):
    """
    Base class for a python Alexa Audio Skill Set.  Concrete implementations
    are expected to implement the abstract methods.

    This base class focuses on the additional intents added by the Audio Playback Support.


    See the following for Alexa details:
    https://developer.amazon.com/public/solutions/alexa/alexa-skills-kit/docs/handling-requests-sent-by-alexa


    http://stackoverflow.com/questions/39157599/simplest-example-for-streaming-audio-with-alexa/39283692#39283692

    https://developer.amazon.com/public/community/post/Tx1DSINBM8LUNHY/New-Alexa-Skills-Kit-ASK-Feature-Audio-Streaming-in-Alexa-Skills

    https://developer.amazon.com/public/solutions/alexa/alexa-voice-service/reference/audioplayer

    Your skill is not required to respond to AudioPlayer requests but if it does, 
    please be aware that it can only respond with the AudioPlayer directives mentioned 
    earlier (Play, Stop and ClearQueue). The response should not include any of the 
    standard properties such as outputSpeech, just like the AudioPlayer directives.

    """

    def __init__(self, app_id=None, log_level=logging.INFO):
        super(AlexaAudioBaseHandler, self).__init__(app_id, log_level)

    def create_clearqueue_directive(self):
        directive = {
            "version": "1.0",
            "sessionAttributes": {},
            "response": {
                "directives": [
                    {
                        "type": "AudioPlayer.ClearQueue"
                    }
                ],
                "shouldEndSession": True
            }
        }
        return directive

    def create_stop_directive(self):
        stop_response = {
                    "version": "1.0",
                    "sessionAttributes": {},
                    "response": {
                        "directives": [
                            {
                                "type": "AudioPlayer.Stop"
                            }
                        ],
                        "shouldEndSession": True
                    }
                }
        return stop_response

    def create_empty_response(self):
        response = {
            "version": "1.0",
            "sessionAttributes": {},
            "response": {
                "outputSpeech": {},
                "card": {},
                "reprompt": {},
                "shouldEndSession": True
            }
        }
        return response

    def create_enqueue_directive(self, current_token, token, url, session_attributes=None):
        directive = {
            "version": "1.0",
            "sessionAttributes": {},
            "response": {
                "directives": [
                    {
                        "type": "AudioPlayer.Play",
                        "playBehavior": "ENQUEUE",  #"REPLACE_ALL",  #"ENQUEUE", "REPLACE_ENQUEUED"
                        "audioItem": {
                            "stream": {
                                "token": token,
                                "expectedPreviousToken": current_token,
                                "url": url,
                                "offsetInMilliseconds": 0
                            }
                        }
                    }
                ],
                "shouldEndSession": True
            }
        }

        if session_attributes is not None:
            directive['sessionAttributes'] = session_attributes

        return directive

    def create_play_directive(self, token, url, behavior="REPLACE_ALL", offset=0, speech_content=None, card_title=None, card_content=None, session_attributes=None):
        directive = {
            "version": "1.0",
            "sessionAttributes": {},
            "response": {
                "outputSpeech": {},
                "card": {},
                "reprompt": {},
                "directives": [
                    {
                        "type": "AudioPlayer.Play",
                        "playBehavior": behavior,  #"REPLACE_ALL",  #"ENQUEUE", "REPLACE_ENQUEUED"
                        "audioItem": {
                            "stream": {
                                "token": token,
                                "url": url,
                                "offsetInMilliseconds": offset
                            }
                        }
                    }
                ],
                "shouldEndSession": True
            }
        }

        if session_attributes is not None:
            directive['sessionAttributes'] = session_attributes

        if speech_content is not None:
            directive['response']['outputSpeech']['type']="PlainText"
            directive['response']['outputSpeech']['text'] = speech_content

        if card_content is not None:
            directive['response']['card']['type']="Simple"
            directive['response']['card']['title']=card_title
            directive['response']['card']['content'] = card_content

        return directive

