#!/usr/bin/env python

import subprocess

"""
Script to generate all of the necessary elements for a simple test Alexa deployment.

"""
handler_cmd = "create_alexa_handler.py -c TestDeployment -t true"
print("Execute: {0}".format(handler_cmd))
return_code = subprocess.call(handler_cmd, shell=True)

main_cmd = "create_aws_main.py -c TestDeployment -f TestLambdaMain.py"
print("Execute: {0}".format(main_cmd))
return_code = subprocess.call(main_cmd, shell=True)

skill_assets_cmd = "create_alexa_test_skills.py"
print("Execute: {0}".format(skill_assets_cmd))
return_code = subprocess.call(skill_assets_cmd, shell=True)

lambda_zip_package_cmd = "create_aws_lambda.py -i 'TestLambdaMain.py,TestDeployment.py'"
print("Execute: {0}".format(lambda_zip_package_cmd))
return_code = subprocess.call(lambda_zip_package_cmd, shell=True)

