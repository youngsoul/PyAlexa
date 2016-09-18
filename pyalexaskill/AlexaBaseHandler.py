import abc
import logging
import traceback

class AlexaBaseHandler(object):
    """
    Base class for a python Alexa Skill Set.  Concrete implementations
    are expected to implement the abstract methods.

    See the following for Alexa details:
    https://developer.amazon.com/public/solutions/alexa/alexa-skills-kit/docs/handling-requests-sent-by-alexa
    """

    __metaclass__ = abc.ABCMeta

    def __init__(self, app_id=None, log_level=logging.INFO):
        self.logger = logging.getLogger()
        self.logger.setLevel(log_level)
        self.app_id = app_id

    @abc.abstractmethod
    def on_launch(self, launch_request, session):
        """
        Implement the LaunchRequest.  Called when the user issues a:
        Alexa, open <invocation name>
        :param launch_request:
        :param session:
        :return: the output of _build_response
        """
        pass

    @abc.abstractmethod
    def on_session_started(self, session_started_request, session):
        pass

    @abc.abstractmethod
    def on_intent(self, intent_request, session):
        """
        Implement the IntentRequest
        :param intent_request:
        :param session:
        :return: the output of _build_response
        """
        pass

    @abc.abstractmethod
    def on_help_intent(self, intent_request, session):
        """
        Implement the built in help intent.
        :param intent_request:
        :param session:
        :return:
        """
        raise ValueError("Help Intent was not implemented")

    @abc.abstractmethod
    def on_stop_intent(self, intent_request, session):
        """
        Implement the built in stop intent.
        :param intent_request:
        :param session:
        :return:
        """
        raise ValueError("Stop Intent was not implemented")

    @abc.abstractmethod
    def on_cancel_intent(self, intent_request, session):
        """
        Implement the built in cancel intent.
        :param intent_request:
        :param session:
        :return:
        """
        raise ValueError("Cancel Intent was not implemented")

    @abc.abstractmethod
    def on_no_intent(self, intent_request, session):
        """
        Implement the built in no (or negative) intent.
        :param intent_request:
        :param session:
        :return:
        """
        raise ValueError("Answer No Intent was not implemented")

    @abc.abstractmethod
    def on_yes_intent(self, intent_request, session):
        """
        Implement the built in yes (or positive) intent.
        :param intent_request:
        :param session:
        :return:
        """
        raise ValueError("Answer Yes Intent was not implemented")

    @abc.abstractmethod
    def on_repeat_intent(self, intent_request, session):
        """
        Implement the built in repeat intent.
        :param intent_request:
        :param session:
        :return:
        """
        raise ValueError("Answer Repeat Intent was not implemented")

    @abc.abstractmethod
    def on_startover_intent(self, intent_request, session):
        """
        Implement the built in start over intent.
        :param intent_request:
        :param session:
        :return:
        """
        raise ValueError("Start Over Intent was not implemented")

    @abc.abstractmethod
    def on_session_ended(self, session_end_request, session):
        """
        Implement the SessionEndRequest
        :param session_end_request:
        :param session:
        :return: the output of _build_response
        """
        pass

    @abc.abstractmethod
    def on_processing_error(self, event, context, exc):
        """
        If an unexpected error occurs during the process_request method
        this handler will be invoked to give the concrete handler
        an opportunity to respond gracefully

        :param exc exception instance
        :return: the output of _build_response
        """
        pass

    @abc.abstractmethod
    def on_invalid_response_request(self, event, context):
        pass

    def check_app_id(self, event):
        """
        Check the App id to make sure it is valid.
        :param event:
        :return: True - app id is valid, False - app id is invalid
        """
        valid_app_id = False
        try:
            if (self.app_id and event['session']['application']['applicationId'] != self.app_id):
                valid_app_id = False
            else:
                valid_app_id = True
        except:
            valid_app_id = False

        return valid_app_id

    def _handle_amazon_request(self, event, context):
        """
        Method dynamically calls AMAZON built in requests.  For example, with the
        new Audio Playback, there call requests of the form:
        AudioPlayer.PlaybackStarted
        AudioPlayer.PlaybackFinished
        To keep this generic, this method will dynamically call method of the form:

        A.B
        on_a_b_request(event, context)
        e.g:
        AudioPlayer.PlaybackStarted will be a method
        on_audioplayer_playbackstarted_request(..)

        :param event:
        :param context:
        :return:speechlet_response, directive, None
        """
        response = None
        self.logger.info("_handle_amazon_request: event: {0}".format(event))
        request_type = event['request']['type']
        self.logger.info("_handle_amazon_request: {0}".format(request_type))
        if request_type:
            parts = request_type.split(".")
            if len(parts) == 1:
                request_type_method_name = "on_{0}_request".format(parts[0].lower())
            elif len(parts) == 2:
                request_type_method_name = "on_{0}_{1}_request".format(parts[0].lower(), parts[1].lower())
            else:
                raise ValueError("Unexpected request type: {0}".format(request_type))
            self.logger.info("_handle_amazon_request: {0}".format(request_type_method_name))
            if hasattr(self, request_type_method_name):
                try:
                    response = getattr(self, request_type_method_name)(event, context)
                except:
                    self.logger.error("Traceback Exception {0}".format(traceback.format_exc()))
                    self.logger.error("ERROR: _handle_amazon_request: {0}".format(request_type_method_name))
            else:
                self.logger.error("_handle_amazon_request: {0} method not found".format(request_type_method_name))
                raise ValueError("No method with name: {0} exists in class".format(request_type_method_name))

        return response

    def _handle_amazon_intent(self, event, context):
        """
        Method dynamically calls AMAZON built in intents.
        For example, for the AMAZON.YesIntent, this method will dynamically call
        a method of the form:
        on_yes_intent(intent_request, session)

        This allows for this base class to be extensible to handle the new
        Amazon Alexa Streaming Playback support without having to specially
        look for the streaming intent names.
        :param event:
        :param context:
        :return: speechlet_response
        """
        response = None

        intent_name = self._get_intent_name(event['request'])
        if intent_name is not None and intent_name.startswith("AMAZON."):
            intent_method_name = "on_{0}_intent".format(intent_name.split(".")[1].replace("Intent","").lower())
            self.logger.info("_handle_amazon_intent: {0}".format(intent_method_name))

            if hasattr(self, intent_method_name):
                try:
                    response = getattr(self, intent_method_name)(event['request'], event['session'])
                except:
                    self.logger.error("Traceback Exception {0}".format(traceback.format_exc()))
                    self.logger.error("ERROR: _handle_amazon_intent: {0}".format(intent_method_name))

            else:
                raise ValueError("No method with name: {0} exists in class".format(intent_method_name))

        return response


    def process_request(self, event, context):
        """
        Helper method to process the input Alexa request and
        dispatch to the appropriate on_ handler
        :param event:
        :param context:
        :return: response from the on_ handler
        """
        self.logger.debug("process_request: event: {0}".format(event))
        self.logger.debug("process_request: context: {0}".format(context))

        try:
            request_type = event['request']['type']
            self.logger.info("event[request][type]: {0}".format(request_type))
        except:
            request_type = None

        try:
            new_session = event['session']['new']
        except:
            new_session = False

        # if its a new session, run the new session code
        try:
            if not self.check_app_id(event):
                raise ValueError("Invalid Application ID")

            response = None
            if new_session is not False:
                self.on_session_started({'requestId': event['request']['requestId']}, event['session'])

                # regardless of whether its new, handle the request type
            if request_type == "LaunchRequest":
                response = self.on_launch(event['request'], event['session'])
            elif request_type == "IntentRequest":
                intent_name = self._get_intent_name(event['request'])
                if intent_name is not None and intent_name.startswith("AMAZON."):
                    response = self._handle_amazon_intent(event, context)
                else:
                    # this is a user specific intent, so let the users concrete
                    # implementation handle it.
                    response = self.on_intent(event['request'], event['session'])
            elif request_type == "SessionEndedRequest":
                response = self.on_session_ended(event['request'], event['session'])
            elif request_type is not None:
                self.logger.info("Calling _handle_amazon_request")
                response = self._handle_amazon_request(event, context)

        except Exception as exc:
            self.logger.error("Error in process_request: {0}".format(traceback.format_exc()))
            self.logger.error(exc.message)
            response = self.on_processing_error(event, context, exc)

        return response

    # --------------- Helpers that build all of the responses ----------------------
    def _build_speechlet_response(self, card_title, card_output, speech_output, reprompt_text, should_end_session):
        """
        Internal helper method to build the speechlet portion of the response
        :param card_title:
        :param card_output:
        :param speech_output:
        :param reprompt_text:
        :param should_end_session:
        :return:
        """
        return {
            'outputSpeech': {
                'type': 'PlainText',
                'text': speech_output
            },
            'card': {
                'type': 'Simple',
                'title': card_title,
                'content': card_output
            },
            'reprompt': {
                'outputSpeech': {
                    'type': 'PlainText',
                    'text': reprompt_text
                }
            },
            'shouldEndSession': should_end_session
        }

    def _build_response(self, session_attributes, speechlet_response):
        """
        Internal helper method to build the Alexa response message
        :param session_attributes:
        :param speechlet_response:
        :return: properly formatted Alexa response
        """
        return {
            'version': '1.0',
            'sessionAttributes': session_attributes,
            'response': speechlet_response
        }

    def _is_intent(self, intent_name, intent_request):
        return self._get_intent_name(intent_request) == intent_name

    def _get_intent(self, intent_request):
        if 'intent' in intent_request:
            return intent_request['intent']
        else:
            return None

    def _get_intent_name(self, intent_request):
        intent = self._get_intent(intent_request)
        intent_name = None
        if intent is not None and 'name' in intent:
            intent_name = intent['name']

        return intent_name

    def _slot_exists(self, slot_name, intent_request):
        intent = self._get_intent(intent_request)
        if intent is not None:
            return slot_name in intent['slots']
        else:
            return False

    def _get_slot_value(self, slot_name, intent_request):
        value = None
        try:
            if self._slot_exists(slot_name, intent_request):
                intent = self._get_intent(intent_request)
                value = intent['slots'][slot_name]['value']
            else:
                value = None
        except Exception as exc:
            self.logger.error("Error getting slot value for slot_name={0}".format(slot_name))

        return value
