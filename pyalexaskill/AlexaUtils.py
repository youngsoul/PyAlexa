import logging
import dpath


class AlexaUtils(object):
    """
    Utility Class to help interact with the Lambda event and context objects.


    See the following for Alexa details:
    https://developer.amazon.com/public/solutions/alexa/alexa-skills-kit/docs/handling-requests-sent-by-alexa
    """

    def __init__(self, event, context, app_id=None, log_level=logging.INFO):
        self.logger = logging.getLogger()
        self.logger.setLevel(log_level)
        self.app_id = app_id
        self.event = event
        self.request = event['request']
        self.session = event['session'] if 'session' in event else None
        self.context = context
        self.session_attributes = None # copy of the event session attributes if they exist

    def check_app_id(self):
        """
        Check the App id to make sure it is valid.
        :param event:
        :return: True - app id is valid, False - app id is invalid
        """
        event = self.event
        try:
            if self.app_id and event['session']['application']['applicationId'] != self.app_id:
                valid_app_id = False
            else:
                valid_app_id = True
        except:
            valid_app_id = False

        return valid_app_id

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
        response =  {
            'outputSpeech': {
                'type': 'PlainText',
                'text': speech_output
            },
            'reprompt': {
                'outputSpeech': {
                    'type': 'PlainText',
                    'text': reprompt_text
                }
            },
            'shouldEndSession': should_end_session
        }

        if card_output and card_title:
            response['card'] = {
                            'type': 'Simple',
                            'title': card_title,
                            'content': card_output
                        }

        return response


    def build_response(self, params):
        card_title = params['card_title']
        card_output = params['card_output']
        speech_output = params['speech_output']
        reprompt_text = params['reprompt_text']
        should_end_session = params['should_end_session']
        session_attributes = self.get_session_attributes()

        speechlet = self._build_speechlet_response(card_title,
                                                   card_output,
                                                   speech_output,
                                                   reprompt_text,
                                                   should_end_session)

        return {
            'version': '1.0',
            'sessionAttributes': session_attributes,
            'response': speechlet
        }

    def is_intent(self, intent_name):
        return self.get_intent_name() == intent_name

    def get_intent(self):
        if 'intent' in self.request:
            return self.request['intent']
        else:
            return None

    def get_intent_name(self, default=None):
        intent = self.get_intent()
        if intent is not None and 'name' in intent:
            intent_name = intent['name']
        else:
            intent_name = default

        return intent_name

    def slot_exists(self, slot_name):
        intent = self.get_intent()
        if intent is not None and 'slots' in intent:
            # alexa will send slots with a name but no 'value' element
            # so check that both are there.
            return slot_name in intent['slots'] and 'value' in intent['slots'][slot_name]
        else:
            return False

    def get_slot_value(self, slot_name):
        """

        :param slot_name:  name of the slot
        :return: value of the slot name, or None if there is not slot name
        """
        value = None
        try:
            if self.slot_exists(slot_name):
                intent = self.get_intent()
                value = intent['slots'][slot_name]['value']
            else:
                value = None
        except Exception as exc:
            self.logger.error("Error getting slot value for slot_name={0}".format(slot_name))

        return value

    def get_request_type(self):
        """

        :return:  Alexa request type.
        """
        if self.request:
            return self.request['type']

    def get_session_attributes(self):
        """
        create a copy of all of the session.attributes and return to the caller
        :return: session.attributes
        """
        if self.session_attributes is None:
            if self.session and \
                            'attributes' in self.session:
                self.session_attributes = self.session['attributes'].copy()
            else:
                self.session_attributes = {}

        return self.session_attributes

    def get_session_attribute(self, path, default=None):
        """
        Get a session attribute specified by the path.  For example:

        origin = alexa_util.get_session_attribute('app_context.stations.origin')

        The path is implicity prefixed with:  session.attributes which is part of the Alexa JSON payload.

        :param path: dotted path, from session.attributes where the application can keep conversational
                    session data.
        :param default: if the value is not found, the default value to return.
        :return: the value in the session specified by the path or the default value.
        """
        value = None
        try:
            value = dpath.util.get(self.get_session_attributes(), path, separator='.')
        except:
            if default is not None:
                dpath.util.new(self.get_session_attributes(), path=path, separator='.', value=default )
                value = default

        return value

    def set_session_attribute(self, path, value):
        """
        Either update an existing value or create a new value in the session.attributes.  For example

        alexa_util.set_session_attribute('app_context.stations.origin', origin)

        add app_contet.stations.origin set to the value of origin to the session.attributes of the Alexa conversational
        session data

        :param path: dotted path, from session.attributes, where the application can save conversation session data
        :param value: value to save
        :return: None
        """
        c = dpath.util.set(self.get_session_attributes(), path, separator='.', value=value )
        if c == 0:
            # then this must be new because none were updated
            dpath.util.new(self.get_session_attributes(), path=path, separator='.', value=value)



