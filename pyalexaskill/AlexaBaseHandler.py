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
    def on_processing_error(self, event, context, exc):
        """
        If an unexpected error occurs during the process_request method
        this handler will be invoked to give the concrete handler
        an opportunity to respond gracefully

        :param exc exception instance
        :return: the output of _build_response
        """
        pass

    def on_intent(self, intent_request, session):
        """
        Implement the IntentRequest.  This is called if there is no specific
        on_<intentname>_intent method.  This gives the implementer the choice
        or writing specific on_intent methods, or calling a single method to
        determine what needs to be called.
        :param intent_request:
        :param session:
        :return: the output of _build_response
        """
        pass


    def check_app_id(self, event):
        """
        Check the App id to make sure it is valid.
        :param event:
        :return: True - app id is valid, False - app id is invalid
        """
        valid_app_id = False
        try:
            if self.app_id and event['session']['application']['applicationId'] != self.app_id:
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
        on_a_b(event, context)
        e.g:
        AudioPlayer.PlaybackStarted will be a method
        on_audioplayer_playbackstarted(..)

        :param event:
        :param context:
        :return:speechlet_response, directive, None
        """
        response = None
        self.logger.debug("_handle_amazon_request: event: {0}".format(event))
        request_type = event['request']['type']
        self.logger.debug("_handle_amazon_request: {0}".format(request_type))
        if request_type:
            parts = request_type.split(".")
            if len(parts) == 1:
                request_type_method_name = "on_{0}".format(parts[0].lower())
            elif len(parts) == 2:
                request_type_method_name = "on_{0}_{1}".format(parts[0].lower(), parts[1].lower())
            else:
                raise NotImplementedError("Unexpected request type: {0}".format(request_type))

            self.logger.debug("_handle_amazon_request: {0}".format(request_type_method_name))
            if hasattr(self, request_type_method_name):
                try:
                    response = getattr(self, request_type_method_name)(event, context)
                except:
                    self.logger.error("Traceback Exception {0}".format(traceback.format_exc()))
                    self.logger.error("ERROR: _handle_amazon_request: {0}".format(request_type_method_name))
                    raise
            else:
                # not every request is required to be implemented - particularly for the
                # playbackcontroller requests
                self.logger.warn("_handle_amazon_request: {0} method not found".format(request_type_method_name))
                #raise NotImplementedError("No method with name: {0} exists in class".format(request_type_method_name))

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
            self.logger.debug("_handle_amazon_intent: {0}".format(intent_method_name))

            if hasattr(self, intent_method_name):
                try:
                    response = getattr(self, intent_method_name)(event['request'], event['session'])
                except:
                    self.logger.error("Traceback Exception {0}".format(traceback.format_exc()))
                    self.logger.error("ERROR: _handle_amazon_intent: {0}".format(intent_method_name))
                    raise

            else:
                raise NotImplementedError("No method with name: {0} exists in class".format(intent_method_name))

        return response

    def _handle_custom_intent(self, event, context):
        """
        Method dynamically calls customeintents by taking the intent name,
        lower casing it, and prepending the name with on_

        For example, for the MyCustomIntent, this method will dynamically call
        a method of the form:
        on_mycustomintent(intent_request, session)

        If the class has not method with that name, it will look for a
        method with the name, 'on_intent'.

        If no method with that name exists then an error will be thrown.

        :param event:
        :param context:
        :return: speechlet_response
        """
        response = None

        intent_name = self._get_intent_name(event['request'])
        if intent_name is not None:
            intent_method_name = "on_{0}_intent".format(intent_name.lower())
            self.logger.debug("_handle_custom_intent: {0}".format(intent_method_name))

            if hasattr(self, intent_method_name):
                try:
                    response = getattr(self, intent_method_name)(event['request'], event['session'])
                except:
                    self.logger.error("Traceback Exception {0}".format(traceback.format_exc()))
                    self.logger.error("ERROR: _handle_amazon_intent: {0}".format(intent_method_name))
                    raise

            elif hasattr(self, 'on_intent'):
                try:
                    response = getattr(self, 'on_intent')(event['request'], event['session'])
                except:
                    self.logger.error("Traceback Exception {0}".format(traceback.format_exc()))
                    self.logger.error("ERROR: _handle_custom_intent: {0}".format(intent_method_name))
                    raise
            else:
                raise NotImplementedError("No method with name: {0} exists in class".format(intent_method_name))

        return response

    #--------------------------------------------------------
    #--------------- Main Processing Entry Point  -----------
    #--------------------------------------------------------
    def process_request(self, event, context):
        """
        Helper method to process the input Alexa request and
        dispatch to the appropriate on_ handler
        :param event:
        :param context:
        :return: response from the on_ handler
        """
        self.logger.debug("process_request: event: {0}".format(event))

        try:
            request_type = event['request']['type']
            self.logger.debug("event[request][type]: {0}".format(request_type))
        except:
            request_type = None

        try:
            new_session = event['session']['new']
        except:
            new_session = False

        # if its a new session, run the new session code
        try:
            if not self.check_app_id(event):
                raise NotImplementedError("Invalid Application ID")

            response = None
            if new_session is not False and hasattr(self, 'on_session_started'):
                # then it is a new session, and the concrete class has an on_session_started
                # callback
                getattr(self, 'on_session_started')(event['request'], event['session'])

            # regardless of whether its new, handle the request type
            if request_type == "IntentRequest":
                # Only handle IntentRequest here... all others in the else block
                intent_name = self._get_intent_name(event['request'])
                if intent_name is not None and intent_name.startswith("AMAZON."):
                    response = self._handle_amazon_intent(event, context)
                else:
                    # this is a user specific intent, so let the users concrete
                    # implementation handle it.
                    response = self._handle_custom_intent(event, context)
            else:
                # LaunchRequest, SessionEndedRequest, AudioPlayer requests, etc
                # are handled here.
                self.logger.debug("Calling _handle_amazon_request")
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
        if intent is not None and 'slots' in intent:
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
