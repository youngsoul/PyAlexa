#!/usr/bin/env python
import os
import random
import sys
import getopt
import string

"""
Script will create a concrete implementation of the Alexa Handler.

"""

handler_file_template = """
from pyalexaskill.AlexaAudioBaseHandler import AlexaAudioBaseHandler
import logging
import random


class MyAudioException(Exception):
    pass


class AlexaBwBHandler(AlexaAudioBaseHandler):

    def _build_audio_response(self, speech, title, card):
        session_attributes = {}
        card_title = title
        card_output = card
        speech_output = speech
        # If the user either does not reply to the welcome message or says something
        # that is not understood, they will be prompted again with this text.
        reprompt_text = ""
        should_end_session = True

        speechlet = self._build_speechlet_response(card_title, card_output, speech_output, reprompt_text, should_end_session)

        return self._build_response(session_attributes, speechlet)

    def __init__(self, app_id=None, log_level=logging.INFO):

        self.songs = []
        self.songs.append({
            'name': '',
            'url': '',
            'token': ''
        })
        self.songs.append({
            'name': '',
            'url': '',
            'token': ''
        })
        #add more songs here
        super(AlexaBwBHandler, self).__init__(app_id, log_level)

    def on_system_exceptionencountered(self, event, context):
        try:
            self.logger.error("ERROR: on_system_exceptionencountered: {0}".format(event))
            self.logger.error("ERROR: Type: {0}".format(event['error']['type']))
            self.logger.error("ERROR: Msg: {0}".format(event['error']['message']))
        except:
            pass

        return None

    def on_invalid_response(self, event, context):
        self.logger.error("on_invalid_response: {0}".format(event))
        return self.create_empty_response()

    def on_startover_intent(self, intent_request, session):
        return self._play_song()

    def on_stop_intent(self, intent_request, session):
        self.logger.debug("AlexaBwBHandler.on_stop_intent")
        return self.create_stop_directive()

    def check_app_id(self, event):
        return super(AlexaBwBHandler, self).check_app_id(event)

    def on_processing_error(self, event, context, exc):
        session_attributes = {}
        speech_output = "I am having difficulty fulfilling your request"

        reprompt_text = "I did not hear you, you can ask for train schedules like, ask Chicago Trains when the next train from starting station names goes to ending station name."
        should_end_session = True

        card_output = speech_output
        speechlet = self._build_speechlet_response('BwB Error',
                                                   card_output,
                                                   speech_output,
                                                   reprompt_text,
                                                   should_end_session)

        return self._build_response(session_attributes, speechlet)


    def on_launchrequest(self, event, context):
        self.logger.debug("Executing on_launch")
        return self._play_song()

    def _enqueue_song(self, current_token):
        song = random.choice(self.songs)
        url = song['url']
        token = song['token']
        self.logger.debug("_enqueue_song: {0}".format(song['name']))
        enqueue_response = self.create_enqueue_directive(current_token, token, url)
        self.logger.debug("Enqueue Response: {0}".format(enqueue_response))
        return enqueue_response

    def _play_song(self, silent=False):
        song = random.choice(self.songs)
        url = song['url']
        token = song['token']
        if silent:
            speech = ""
        else:
            speech = "Playing {0}".format(song['name'])
        card = "Playing {0}".format(song['name'])
        self.logger.debug("_play_song: {0}".format(song['name']))
        session_attributes = {
            'song': song
        }

        play_response = self.create_play_directive(token, url, "REPLACE_ALL", 0, speech, "BwB", card, session_attributes)
        self.logger.debug("Play Response: {0}".format(play_response))
        return play_response

    def on_help_intent(self, intent_request, session):
        session_attributes = {}
        card_output = "You can hear the sizzling sounds of Better with Bacon by saying, play some bacon"
        speech_output = card_output
        card_title = "Better with Bacon"

        reprompt_text = "I did not hear you, {0}".format(speech_output)
        should_end_session = False
        speechlet = self._build_speechlet_response(card_title,
                                                   card_output,
                                                   speech_output,
                                                   reprompt_text,
                                                   should_end_session)

        return self._build_response(session_attributes, speechlet)

    def on_next_intent(self, intent_request, session):
        return self._play_song()

    def on_audioplayer_playbackfailed(self, event, context):
        self.logger.debug("Executing on_audioplayer_playbackfailed_request")
        try:
            self.logger.debug(event)
        except:
            pass

    def on_resume_intent(self, intent_request, session):
        self.logger.debug("Executing on_resume_intent")
        try:
            self.logger.debug(intent_request)
            self.logger.debug(session)
            return self._play_song(silent=True)
        except:
            raise MyAudioException("An error occurred trying to resume audio")


    def on_previous_intent(self, intent_request, session):
        return self._play_song(silent=True)

    def on_shuffleoff_intent(self, intent_request, session):
        return self._build_audio_response("Shuffle off is not yet supported", "BwB", 'Shuffle off is not yet supported')

    def on_shuffleon_intent(self, intent_request, session):
        return self._build_audio_response("Shuffle on is not yet supported", "BwB", 'Shuffle on is not yet supported')

    def on_audioplayer_playbackstarted(self, event, context):
        self.logger.debug("Executing on_audioplayer_playbackstarted_request")
        return None


    def on_loopoff_intent(self, intent_request, session):
        return self._build_audio_response("Loop off is not yet supported", "BwB", 'Loop off is not yet supported')

    def on_playbackcontroller_pausecommandissued(self, event, context):
        try:
            self.logger.debug("Executing on_playbackcontroller_pausecommandissued_request")
            self.logger.debug(event)
        except:
            pass

        return None

    def on_audioplayer_playbackstopped(self, event, context):
        self.logger.debug("Executing on_audioplayer_playbackstopped_request")
        try:
            self.logger.debug("Executing on_audioplayer_playbackstopped_request: event: {0}".format(event))

        except:
            pass

        return None

    def on_pause_intent(self, intent_request, session):
        self.logger.debug("Executing on_pause_intent")
        try:
            self.logger.debug("AlexaBwBHandler.on_pause_intent: intent_request: {0}".format(intent_request))
            self.logger.debug("AlexaBwBHandler.on_pause_intent: session: {0}".format(session))
        except:
            pass

        response = self.create_stop_directive()
        self.logger.debug("on_pause_intent response: {0}".format(response))
        return response

    def on_audioplayer_playbacknearlyfinished(self, event, context):
        self.logger.debug("Executing on_audioplayer_playbacknearlyfinished_request")
        current_token = event['request']['token']
        return self._enqueue_song(current_token)

    def on_loopon_intent(self, intent_request, session):
        return self._build_audio_response("Loop on is not yet supported", "BwB", 'Loop on is not yet supported')

    def on_cancel_intent(self, intent_request, session):
        self.logger.debug("Executing on_cancel_intent")
        return self.create_stop_directive()

    def on_repeat_intent(self, intent_request, session):
        return self._play_song()

    def on_playbaconintent_intent(self, intent_request, session):
        self.logger.debug("Executing on_playbacon_intent")
        return self._play_song()

"""


def main(argv):
    root_project_dir = ''
    template_file_name = 'AlexaHandler_template_' + ''.join(
        random.choice(string.ascii_lowercase + string.digits) for _ in range(5)) + '.py'

    try:
        opts, args = getopt.getopt(argv, "hr:", ["root="])
    except getopt.GetoptError:
        print 'create_alexa_handler.py -r <root project dir>'
        print 'if -r option not supplied it will look for PWD environment variable'
        sys.exit(2)
    for opt, arg in opts:
        if opt == '-h':
            print 'create_alexa_handler.py -r <root project dir>'
            print 'if -r option not supplied it will look for PWD environment variable'
            sys.exit()
        elif opt in ("-r", "--root"):
            root_project_dir = arg

    if not root_project_dir:
        root_project_dir = os.environ.get("PWD")
        if root_project_dir is None:
            raise ValueError("Must supply -r or --root option")

    with open("{0}/{1}".format(root_project_dir, template_file_name), "w") as text_file:
        text_file.write(handler_file_template)


if __name__ == "__main__":
    main(sys.argv[1:])
