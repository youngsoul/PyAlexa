#!/usr/bin/env python
import os
import random
import sys
import getopt
import string

"""
Script will create an AWS Lambda function deployment.

It expects there to be a deployments directory and it will create a
deployment of the form:

deployment_n

where n is incremented for each deployment based on the existing deployment
directories

If the AWS Lambda function has dependencies those dependencies are expected
to be in the requirements.txt file.

The implementation files are expected to be in the root project directory, and
this command does not currently support deeply nested file structures.

"""

main_file_template = """
import logging
from {0} import {1}


#  Main entry point for the Lambda function.
#  In the AWS Lamba console, under the 'Configuration' tab there is an
#  input field called, 'Handler'.  That should be:  main.lambda_handler

#  Handler: main.lambda_handler
#  Role: lambda_basic_execution



logger = logging.getLogger()
logger.setLevel(logging.INFO)


def lambda_handler(event, context):
    logging.info("Executing main lambda_handler for {1} class")

    deployment_handler = {1}()
    handler_response = deployment_handler.process_request(event, context)

    return handler_response

"""


def main(argv):
    default_deployment_handler_filename = 'YourDeploymentHandler'
    default_deployment_handler_classname = 'YourDeploymentHandler'

    root_project_dir = ''
    main_file_name = 'main_template_' + ''.join(random.choice(string.ascii_lowercase + string.digits) for _ in range(5)) + '.py'

    try:
        opts, args = getopt.getopt(argv, "hr:f:c:", ["root=", "filename=", "classname="])
    except getopt.GetoptError:
        print('create_aws_main.py -r <root project dir> -n <filename>')
        print('if -r option not supplied it will look for PWD environment variable')
        print('if -f option not supplied the name will be main_template_<random>.py')
        print('if -c classname of handler, default is AlexaDeploymentTestHandler')
        sys.exit(2)
    for opt, arg in opts:
        if opt == '-h':
            print('create_aws_main.py -r <root project dir>')
            print('if -r option not supplied it will look for PWD environment variable')
            print('if -f option not supplied the name will be main_template_<random>.py')
            print('if -c classname of handler, default is AlexaDeploymentTestHandler')
            sys.exit()
        elif opt in ("-r", "--root"):
            root_project_dir = arg
        elif opt in ("-f", "--filename"):
            main_file_name = arg
        elif opt in ("-c", "--classname"):
            default_deployment_handler_filename = arg
            default_deployment_handler_classname = arg

    if not root_project_dir:
        root_project_dir = os.environ.get("PWD")
        if root_project_dir is None:
            root_project_dir = os.getcwd()
            if root_project_dir is None:
                raise ValueError("Must supply -r or --root option")

    with open(os.path.join(root_project_dir, main_file_name), "w") as text_file:
        text_file.write(main_file_template.format(default_deployment_handler_filename, default_deployment_handler_classname))

    print("Created main template file: {}".format(main_file_name))
if __name__ == "__main__":
    main(sys.argv[1:])
