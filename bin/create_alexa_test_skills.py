#!/usr/bin/env python
import os
import sys
import getopt

"""
Script will create a test intent schema and sample utterance file..

"""


intent_template = """{
  "intents": [
    {
      "intent": "DeploymentIntent",
      "slots": []
    }
  ]
}
"""

utterance_template = """DeploymentIntent what is the deployment status
DeploymentIntent what is the status
DeploymentIntent provide the deployment status
"""

def _mkdirp(directory):
    if not os.path.isdir(directory):
        os.makedirs(directory)


def main(argv):
    root_project_dir=None

    try:
        opts, args = getopt.getopt(argv, "hr:", ["root="])
    except getopt.GetoptError:
        print 'create_alexa_test_skills.py -r <root project dir>'
        print 'if -r option not supplied it will look for PWD environment variable'
        sys.exit(2)
    for opt, arg in opts:
        if opt == '-h':
            print 'create_alexa_test_skills.py -r <root project dir>'
            print 'if -r option not supplied it will look for PWD environment variable'
            print '<include files> are relative to root project dir'
            sys.exit()
        elif opt in ("-r", "--root"):
            root_project_dir = arg

    if not root_project_dir:
        root_project_dir = os.environ.get("PWD")
        if root_project_dir is None:
            raise ValueError("Must supply -r or --root option")


    root_deployments_dir = "{0}/alexa_skills/deployment_test2".format(root_project_dir)
    _mkdirp(root_deployments_dir)

    with open("{0}/{1}".format(root_deployments_dir, "deployment_intent_schema.json"), "w") as text_file:
        text_file.write(intent_template)

    with open("{0}/{1}".format(root_deployments_dir, "sample_utterance.txt"), "w") as text_file:
        text_file.write(utterance_template)

if __name__ == "__main__":
    main(sys.argv[1:])
