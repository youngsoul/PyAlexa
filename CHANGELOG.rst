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
