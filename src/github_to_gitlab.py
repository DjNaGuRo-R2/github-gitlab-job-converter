def browseDict(keyElt, dictionary):
    NOT_FOUND = ""
    for key, value in dictionary.items():        
        if (key == keyElt):
            return (keyElt, value)
        if (isinstance(value,dict)):
            result = browseDict(keyElt, value)
            if(result != NOT_FOUND):
                return result
    return NOT_FOUND  

def get_variables(dictionary):
    variables = {}
    _, value = browseDict("workflow_call", dictionary)
    inputs = value.get("inputs", "")
    secrets = value.get("secrets", "")
    if(inputs):
        for key, value in inputs.items():
            variables[key] = value.get("default", "")
    if(secrets):
        for key, value in secrets.items():
            variables[key] = value.get("default", "")
    return variables

def get_docker_image(job):
    container = job.get("container", "")
    if(container):
        if(isinstance(container, str)):
            return container
        elif(isinstance(container, dict)):
            return container.get("image", "")
    return ""
    
def get_runs_on(job):
    return job.get("runs-on", "")

def get_steps(job):
    return job.get("steps", [])

def get_artifacts(steps):
    artifacts = {}
    for elt in steps:
        if "actions/upload-artifact" in elt.get("uses", ""):
            artifacts["name"] = elt["with"].get("name", "")
            artifacts["paths"] = elt["with"].get("path", "").splitlines()
            artifacts["expire_in"] = elt["with"].get("retention-days", "")
            when = elt.get("if", "")
            if when == "failure()":
                artifacts["when"] = "on_failure"
            elif when == "always()":
                artifacts["when"] = "always"
            else:
                artifacts["when"] = "on_success"
                
    return artifacts
    
def get_cache(steps):
    cache = {}
    for elt in steps:
        if "actions/cache" in elt.get("uses", ""):
            cache["key"] = elt["with"].get("key", "")
            cache["paths"] = elt["with"].get("path", "").splitlines()
    return cache

def get_script(steps):
    script = []
    for step in steps:
        if "run" in step:
            lines = step.get("run").splitlines()
            for line in lines:
                script.append(line)
    return script

def github_calleable_workflow_to_gitlab(workflow_content):
    _,jobs = browseDict("jobs", workflow_content)
    gitlab_cicd_content = {}
    variables = get_variables(workflow_content)
    for job_name, job in jobs.items():
        gitlab_cicd_content[job_name] = {}
        image = get_docker_image(job)
        if image:
            gitlab_cicd_content[job_name]["image"] = image
        gitlab_cicd_content[job_name]["variables"] = variables
        steps = get_steps(job)
        cache = get_cache(steps)
        if cache:
            gitlab_cicd_content[job_name]["cache"] = cache
        script = get_script(steps)
        gitlab_cicd_content[job_name]["script"] = script
        artifacts = get_artifacts(steps)
        if artifacts:
            gitlab_cicd_content[job_name]["artifacts"] = artifacts
    return gitlab_cicd_content