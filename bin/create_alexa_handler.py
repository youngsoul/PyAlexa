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
from pyalexaskill.AlexaBaseHandler import AlexaBaseHandler


class AlexaDeploymentTestHandler(AlexaBaseHandler):

    # Sample concrete implementation of the AlexaBaseHandler to test the
    # deployment scripts and process.
    # All on_ handlers call the same test response changing the request type
    # spoken.


    def __init__(self):
        super(self.__class__, self).__init__()


    def _test_response(self, msg):
        session_attributes = {}
        card_title = "Test Response"
        card_output = "Test card output"
        speech_output = "Welcome to the Python Alexa Test Deployment for request type {0}.  It seems to have worked".format(
            msg)
        # If the user either does not reply to the welcome message or says something
        # that is not understood, they will be prompted again with this text.
        reprompt_text = "Reprompt text for the Alexa Test Deployment"
        should_end_session = True

        speechlet = self._build_speechlet_response(card_title, card_output, speech_output, reprompt_text,
                                                   should_end_session)

        return self._build_response(session_attributes, speechlet)


    def on_processing_error(self, event, context, exc):
        return self._test_response("on processing error")


    def on_launch(self, launch_request, session):
        return self._test_response("on launch")


    def on_session_started(self, session_started_request, session):
        return self._test_response("on session started")


    def on_intent(self, intent_request, session):
        return self._test_response("on intent")


    def on_session_ended(self, session_end_request, session):
        return self._test_response("on session end")

"""


def main(argv):
    root_project_dir = ''
    template_file_name = 'AlexaHandler_template_' + ''.join(random.choice(string.ascii_lowercase + string.digits) for _ in range(5)) + '.py'

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
