Changelog
=========

The third digit is only for regressions.


----

0.0.1 (2016-23-03)
------------------

Changes:
^^^^^^^^

Initial Release and implementation

0.0.5 (2016-23-03)
------------------

Changes:
~~~~~~~~
* changed create_aws_deployment.py to create_aws_lambda.py
* changed module name from pyalexa-skill to pyalexaskill

0.0.6 (2016-24-03)
------------------

Changes:
~~~~~~~~
* add create_alexa_handler.py script to create a handler template

0.0.7 (2016-25-03)
------------------

Changes:
~~~~~~~~
* changed the handler template generator

0.0.8 (2016-25-03)
------------------

Changes:
~~~~~~~~
* remove the shebang in the create_xyz scripts so now the user has to specify which python to use

0.0.9 (2016-25-03)
------------------

Changes:
~~~~~~~~
* log exception in the process_request method


0.1.0 (2016-25-03)
------------------

Changes:
~~~~~~~~
* put the shebang back

0.1.1 (2016-27-03)
------------------

Changes:
~~~~~~~~
* add app_id to base handler, and check app_id in process_request if it is not None


0.1.2 (2016-28-03)
------------------

Changes:
~~~~~~~~
* documentation update


0.1.3 (2016-29-03)
------------------

Changes:
~~~~~~~~
* add script command create_alexa_test_skills.py to add sample intent schema and sample utterances to go along with the sample Alexa handler that is created.

0.1.5 (2016-4-04)
-----------------

Changes:
~~~~~~~~
* added abstract methods for the built-in intents

0.1.6 (2016-4-20)
-----------------

Changes:
~~~~~~~~
* updated the handler template to include the new intents

0.1.7 (2016-4-20)
-----------------

Changes:
~~~~~~~~
* provide better sample implementations in the template

0.1.9 (2016-5-21)
-----------------

Changes:
~~~~~~~~
* updated create_aws_lambda.py to not save the deployment directory, instead delete it
* keeps track of next deployment number in a dot file ( .deployment_number.txt )
* prints the name and location of the created deployment zip.

0.1.10 (2016-9-03)
------------------

Changes:
~~~~~~~~
* update create_aws_lambda.py to allow for files in directories below the root directory
and they will be copied into a corresponding deployment directory.

0.2.0 (2016-x-xx)
------------------

Changes:
~~~~~~~~
* many of the abstract methods were removed, because with the AudioPlayer capability, also
  came additional intents and request types.  Instead of trying to keep up with these, I have
  opted for dynamically calling methods based on a convention for the intent and request
  names.
* added audio intent handling and generically call amazon intents, custom intents and audio requests
* BREAKING CHANGE: on_start_over_intent needs to be renamed to on_startover_intent
* BREAKING CHANGE: on_launch needs to be renamed to on_launchrequest and are passed event, context
* BREAKING CHANGE: on_session_ended needs to be renamed to on_sessionendedrequest and are passed event, context
* added ability to include requirements-test.txt which create_aws_lambda.py will install as:
    pip install -i https://testpypi.python.org/pypi <requirements line> -t <deployment_dir>
   to allow for test packages to be added to a Lambda function zip file.
* added log level specification to ctor
* added on_invalid_response_request abstract method
* added create_alexa_audio_handler.py to create a starter template for audio applications
