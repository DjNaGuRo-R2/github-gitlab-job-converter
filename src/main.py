from github_to_gitlab import github_calleable_workflow_to_gitlab
#from yaml import load, dump
import yaml

JOB_NAME = "cypress_run_2"
INPUT_JOB_FILE = f"../Inputs/github/{JOB_NAME}.yml"
OUTPUT_JOB_FILE = f"../Outputs/gitlab/{JOB_NAME}.yml"

try:
    from yaml import CLoader as Loader, CDumper as Dumper
except ImportError:
    from yaml import Loader, Dumper

with open(INPUT_JOB_FILE, 'r') as input_job_file:
    yaml_content = yaml.load(input_job_file, Loader=Loader)

# Convertion from GitHub Actions to GitLab CI/CD for a calleable workflow
gitlab_cicd_content = github_calleable_workflow_to_gitlab(yaml_content)

with open(OUTPUT_JOB_FILE, 'w') as job_file:
    yaml.dump(gitlab_cicd_content, job_file)
