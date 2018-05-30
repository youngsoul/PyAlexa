<h2> test editSample project to demonstrate how to create a lambda function in 
Python that can be used in an Alexa Skill.</h2>

This project is not meant to be a tutorial on Alexa development.  For that
please see the Amazon documentation at:

Youtube video for this project.
<code>
https://www.youtube.com/watch?v=WFWAK175p2g
</code>

<code>
https://developer.amazon.com/public/solutions/alexa/alexa-skills-kit
</code>

<h2>AlexaBaseHandler class</h2>

The AlexaBaseHandler class is an abstract class that provides the necessary
framework to build the necessary response hooks for an Alexa application.

<h3>process_request</h3>
This method will take the 2 parameters that are sent to the lambda function
and determine which of the Alexa handlers to invoke.  

<h3>_build_speechlet_response</h3>
This method ( from the Alexa color example ) will put together the speechlet portion
into a properly formatted json message.  This is typically called by the 
concrete implementations of the AlexaBaseHandler.

<h3>_build_response</h3>
This method (from the Alexa color example ) will construct a properly formatted
response message so the Amazon Echo knows what to respond with.

<h2>AlexaDeploymentHandler class</h2>
This class is a reference implementation that does nothing useful.  All Alexa
handlers are handled the same way.

<h2>main.py</h2>
This file contains the main entry point of the lambda function that is called
for the Alexa skill.

<h3>lambda_handler(event, context)</h3>
This method ( which can be called anything, you just need to configure it in 
the lambda handler ), is the method that is called with the 2 parameters.

This method will typically instantiate an concrete implementation of the
AlexaBaseHandler and delegate to the process_request method.

<h2>requirements.txt</h2>
This file is the standard Python requirements file.  This file is used by the
create_deployment.py script to install the necessary 3rd party libraries that
your Alexa skill might need.  Any library specified in the requirements.txt
file will be installed into your deployment directory.

<h2>create_aws_lambda</h2>
This script creates a zip file per the Amazon lambda specification, such that
it is suitable to upload as your lambda function implementation.

option: -r [Optional]  to specify root directory of project.  Default is the current directory

<h2>create_aws_main</h2>

option: -r [Optional] to specify root directory of project.  Default is the current directory
option: -f [Optional] filename to use for the main lambda entry point. e.g. my_main.py
option: -c [Optional] classname of the handler to instantiate in the main entry point.

This script creates a template main entry point

All deployments are stored in the deployments subdirectory and follow the naming
convention of 'deployment_n' and 'deployment_n.zip', where 'n' is automatically
calculated to the next largest 'n' in the directory.  Right now it does this
based on the name of the subdirectories of deployments - NOT - the names of 
the zip files.

The deployment script will create a deployment directory and zip file for
everything in the requirements.txt file AND the files in the <code>deployment_files</code>
variable in the create_deployment.py file.  

When this script is done running, there should be a 'deployment_n.zip' file in the deployments directory.
It is that file that needs to be upload to the Amazon Lambda console.

<h2>create_alexa_handler</h2>

option: -r [Optional] to specify root directory of project.  Default is the current directory
option: -t [Optional] true, then include a test deployment method
option: -c [Optional] classname of the handler to instantiate in the main entry point.

<h2>create_alexa_test_skills</h2>

This will create a simple utterance and schema file.

<h3>Useful links:</h3>

http://docs.aws.amazon.com/lambda/latest/dg/python-programming-model-handler-types.html
http://docs.aws.amazon.com/lambda/latest/dg/lambda-python-how-to-create-deployment-package.html


https://hynek.me/articles/sharing-your-labor-of-love-pypi-quick-and-dirty/
