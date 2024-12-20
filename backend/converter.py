import logging
from datetime import datetime

def convert_devcontainer_to_gitpod(devcontainer_json):
    logging.info(f"{datetime.now().isoformat()} - Starting conversion from devcontainer to gitpod")
    gitpod_yaml = {
        "image": {},
        "tasks": [],
        "vscode": {
            "extensions": []
        },
        "ports": []
    }

    # Convert image
    if "image" in devcontainer_json:
        gitpod_yaml["image"] = devcontainer_json["image"]
        logging.info(f"{datetime.now().isoformat()} - Converted image: {devcontainer_json['image']}")

    # Convert forwardPorts to ports
    if "forwardPorts" in devcontainer_json:
        gitpod_yaml["ports"] = [{"port": port} for port in devcontainer_json["forwardPorts"]]
        logging.info(f"{datetime.now().isoformat()} - Converted {len(devcontainer_json['forwardPorts'])} ports")

    # Convert environment variables
    if "containerEnv" in devcontainer_json or "remoteEnv" in devcontainer_json:
        logging.info(f"{datetime.now().isoformat()} - Converting environment variables")
        env_vars = {}
        
        def convert_env_var(value):
            # Convert ${localEnv:VAR} to ${VAR}
            if isinstance(value, str) and "${localEnv:" in value:
                return value.replace("${localEnv:", "${")
            # Convert ${containerEnv:VAR} to ${VAR}
            if isinstance(value, str) and "${containerEnv:" in value:
                return value.replace("${containerEnv:", "${")
            return value
        
        if "containerEnv" in devcontainer_json:
            for key, value in devcontainer_json["containerEnv"].items():
                env_vars[key] = convert_env_var(value)
            logging.info(f"{datetime.now().isoformat()} - Added containerEnv variables")
            
        if "remoteEnv" in devcontainer_json:
            for key, value in devcontainer_json["remoteEnv"].items():
                env_vars[key] = convert_env_var(value)
            logging.info(f"{datetime.now().isoformat()} - Added remoteEnv variables")
            
        if env_vars:
            gitpod_yaml["env"] = env_vars
            logging.info(f"{datetime.now().isoformat()} - Added combined environment variables")

    # Convert features to tasks
    if "features" in devcontainer_json:
        logging.info(f"{datetime.now().isoformat()} - Converting features to tasks")
        for feature, value in devcontainer_json["features"].items():
            if isinstance(value, dict) and "version" in value:
                gitpod_yaml["tasks"].append({
                    "name": f"Install {feature}",
                    "command": f"sudo apt-get update && sudo apt-get install -y {feature}={value['version']}"
                })
                logging.info(f"{datetime.now().isoformat()} - Added task to install {feature} version {value['version']}")
            else:
                version = "latest" if not isinstance(value, dict) or "version" not in value else value["version"]
                gitpod_yaml["tasks"].append({
                    "name": f"Install {feature}",
                    "command": f"sudo apt-get update && sudo apt-get install -y {feature}={version}"
                })
                logging.info(f"{datetime.now().isoformat()} - Added task to install {feature} version {version}")
                
    # Convert settings
    # if condition to check if the following exists: "customizations": {"vscode": {"settings"}}
    if "customizations" in devcontainer_json and "vscode" in devcontainer_json["customizations"] and "settings" in devcontainer_json["customizations"]["vscode"]:
        gitpod_yaml["vscode"]["settings"] = {"# Note": "VS Code settings should be configured separately in Gitpod"}
        logging.info(f"{datetime.now().isoformat()} - Added note about VS Code settings")

    # Convert extensions
    if "customizations" in devcontainer_json and "vscode" in devcontainer_json["customizations"] and "extensions" in devcontainer_json["customizations"]["vscode"]:
        gitpod_yaml["vscode"]["extensions"] = devcontainer_json["customizations"]["vscode"]["extensions"]
        logging.info(f"{datetime.now().isoformat()} - Converted {len(devcontainer_json['customizations']['vscode']['extensions'])} extensions")

    # Convert postCreateCommand
    if "postCreateCommand" in devcontainer_json:
        gitpod_yaml["tasks"].append({
            "name": "Post-create command",
            "command": devcontainer_json["postCreateCommand"]
        })
        logging.info(f"{datetime.now().isoformat()} - Added post-create command")

    logging.info(f"{datetime.now().isoformat()} - Conversion completed successfully")
    return gitpod_yaml
