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
from YourDeploymentHandler import YourDeploymentHandler


#  Main entry point for the Lambda function.
#  In the AWS Lamba console, under the 'Configuration' tab there is an
#  input field called, 'Handler'.  That should be:  main.lambda_handler

#  Handler: main.lambda_handler
#  Role: lambda_basic_execution



logger = logging.getLogger()
logger.setLevel(logging.INFO)


def lambda_handler(event, context):
    logging.info("Executing main lambda_handler for YourDeploymentHandler class")

    deployment_handler = YourDeploymentHandler()
    handler_response = deployment_handler.process_request(event, context)

    return handler_response

"""


def main(argv):
    root_project_dir = ''
    main_file_name = 'main_template_' + ''.join(random.choice(string.ascii_lowercase + string.digits) for _ in range(5)) + '.py'

    try:
        opts, args = getopt.getopt(argv, "hr:", ["root="])
    except getopt.GetoptError:
        print 'create_aws_main.py -r <root project dir>'
        print 'if -r option not supplied it will look for PWD environment variable'
        sys.exit(2)
    for opt, arg in opts:
        if opt == '-h':
            print 'create_aws_main.py -r <root project dir>'
            print 'if -r option not supplied it will look for PWD environment variable'
            sys.exit()
        elif opt in ("-r", "--root"):
            root_project_dir = arg

    if not root_project_dir:
        root_project_dir = os.environ.get("PWD")
        if root_project_dir is None:
            raise ValueError("Must supply -r or --root option")

    with open("{0}/{1}".format(root_project_dir, main_file_name), "w") as text_file:
        text_file.write(main_file_template)

if __name__ == "__main__":
    main(sys.argv[1:])
