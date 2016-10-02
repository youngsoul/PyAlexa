from pyalexaskill.AlexaBaseHandler import AlexaBaseHandler
import abc
import logging

class AlexaAudioBaseHandler(AlexaBaseHandler):
    """
    https://dl.dropboxusercontent.com/u/48134834/BaconBits/climb%20to%20safety.mp3

    Base class for a python Alexa Audio Skill Set.  Concrete implementations
    are expected to implement the abstract methods.

    This base class focuses on the additional intents added by the Audio Playback Support.


    See the following for Alexa details:
    https://developer.amazon.com/public/solutions/alexa/alexa-skills-kit/docs/handling-requests-sent-by-alexa


    http://stackoverflow.com/questions/39157599/simplest-example-for-streaming-audio-with-alexa/39283692#39283692

def lambda_handler(event, context):
    return {
        "response": {
            "directives": [
                {
                    "type": "AudioPlayer.Play",
                    "playBehavior": "REPLACE_ALL",
                    "audioItem": {
                        "stream": {
                            "token": "12345",
                            "url": "https://emit-media-production.s3.amazonaws.com/pbs/the-afterglow/2016/08/24/1700/201608241700_the-afterglow_64.m4a",
                            "offsetInMilliseconds": 0
                        }
                    }
                }
            ],
            "shouldEndSession": True
        }
    }

    https://developer.amazon.com/public/community/post/Tx1DSINBM8LUNHY/New-Alexa-Skills-Kit-ASK-Feature-Audio-Streaming-in-Alexa-Skills

https://developer.amazon.com/public/solutions/alexa/alexa-voice-service/reference/audioplayer

Your skill is not required to respond to AudioPlayer requests but if it does, please be aware that it can only respond with the AudioPlayer directives mentioned earlier (Play, Stop and ClearQueue). The response should not include any of the standard properties such as outputSpeech, just like the AudioPlayer directives.

    """

    def __init__(self, app_id=None, log_level=logging.INFO):
        super(AlexaAudioBaseHandler, self).__init__(app_id, log_level)

    def create_clearqueue_directive(self):
        directive = {
            "version": "1.0",
            "sessionAttributes": {},
            "response": {
                "outputSpeech": {},
                "card": {},
                "reprompt": {},
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

    def create_enqueue_directive(self, token, url, session_attributes=None):
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
                                "expectedPreviousToken": token,
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

    @abc.abstractmethod
    def on_pause_intent(self,intent_request, session):
        raise ValueError("Pause Intent was not implemented")

    @abc.abstractmethod
    def on_resume_intent(self, intent_request, session):
        raise ValueError("Resume Intent was not implemented")

    @abc.abstractmethod
    def on_cancel_intent(self, intent_request, session):
        raise ValueError("Cancel Intent was not implemented")

    @abc.abstractmethod
    def on_loopoff_intent(self, intent_request, session):
        raise ValueError("Loop off Intent was not implemented")

    @abc.abstractmethod
    def on_loopon_intent(self, intent_request, session):
        raise ValueError("Loop on Intent was not implemented")


    @abc.abstractmethod
    def on_next_intent(self, intent_request, session):
        raise ValueError("Next Intent was not implemented")


    @abc.abstractmethod
    def on_previous_intent(self, intent_request, session):
        raise ValueError("Previous Intent was not implemented")


    @abc.abstractmethod
    def on_repeat_intent(self, intent_request, session):
        raise ValueError("Repeat Intent was not implemented")


    @abc.abstractmethod
    def on_shuffleoff_intent(self, intent_request, session):
        raise ValueError("Shuffle Off Intent was not implemented")


    @abc.abstractmethod
    def on_shuffleon_intent(self, intent_request, session):
        raise ValueError("Shuffle on intent was not implemented")

    @abc.abstractmethod
    def on_audioplayer_playbackstarted_request(self, event, context):
        """
        Note: When responding to AudioPlayer requests, you can only respond with AudioPlayer directives. The response cannot include any of the standard properties such as outputSpeech. In addition, some requests limit the directives you can use, such as not allowing Play. Sending a response with unsupported properties causes an error. See the request types below for the limits on each request.
        Use context to get app id and/or user id
            {
              "version": "string",
              "context": {
                "System": {
                  "application": {},
                  "user": {},
                  "device": {}
                }
              },
              "request": {
                "type": "AudioPlayer.PlaybackStarted",
                "requestId": "string",
                "timestamp": "string",
                "token": "string",
                "offsetInMilliseconds": 0,
                "locale": "string"
              }
            }
        :param event:
        :param context:
        :return:
        """
        return None


    @abc.abstractmethod
    def on_audioplayer_playbackfinished_request(self, event, context):
        """
        Note: When responding to AudioPlayer requests, you can only respond with AudioPlayer directives. The response cannot include any of the standard properties such as outputSpeech. In addition, some requests limit the directives you can use, such as not allowing Play. Sending a response with unsupported properties causes an error. See the request types below for the limits on each request.
        Use context to get app id and/or user id
        :param event:
        :param context:
        :return:
        """
        return None


    @abc.abstractmethod
    def on_audioplayer_playbackstopped_request(self, event, context):
        """
        Note: When responding to AudioPlayer requests, you can only respond with AudioPlayer directives. The response cannot include any of the standard properties such as outputSpeech. In addition, some requests limit the directives you can use, such as not allowing Play. Sending a response with unsupported properties causes an error. See the request types below for the limits on each request.
        Your skill cannot return a response to PlaybackStopped
        Use context to get app id and/or user id
        :param event:
        :param context:
        :return:
        """
        return None


    @abc.abstractmethod
    def on_audioplayer_playbacknearlyfinished_request(self, event, context):
        """
        Note: When responding to AudioPlayer requests, you can only respond with AudioPlayer directives. The response cannot include any of the standard properties such as outputSpeech. In addition, some requests limit the directives you can use, such as not allowing Play. Sending a response with unsupported properties causes an error. See the request types below for the limits on each request.
        Use context to get app id and/or user id
        :param event:
        :param context:
        :return:
        """
        return None


    @abc.abstractmethod
    def on_audioplayer_playbackfailed_request(self, event, context):
        """
        Note: When responding to AudioPlayer requests, you can only respond with AudioPlayer directives. The response cannot include any of the standard properties such as outputSpeech. In addition, some requests limit the directives you can use, such as not allowing Play. Sending a response with unsupported properties causes an error. See the request types below for the limits on each request.
        Use context to get app id and/or user id
        :param event:
        :param context:
        :return:
        """
        return None


    @abc.abstractmethod
    def on_playbackcontroller_nextcommandissued_request(self, event, context):
        pass


    @abc.abstractmethod
    def on_playbackcontroller_pausecommandissued_request(self, event, context):
        pass


    @abc.abstractmethod
    def on_playbackcontroller_playcommandissued_request(self, event, context):
        pass


    @abc.abstractmethod
    def on_playbackcontroller_previouscommandissued_request(self, event, context):
        pass
