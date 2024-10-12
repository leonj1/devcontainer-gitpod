import logging
from datetime import datetime

def convert_devcontainer_to_gitpod(devcontainer_json):
    logging.info(f"{datetime.now().isoformat()} - Starting conversion from devcontainer to gitpod")
    gitpod_yaml = {
        "image": {},
        "tasks": [],
        "vscode": {
            "extensions": []
        }
    }

    # Convert image
    if "image" in devcontainer_json:
        gitpod_yaml["image"] = devcontainer_json["image"]
        logging.info(f"{datetime.now().isoformat()} - Converted image: {devcontainer_json['image']}")

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
                
    if "containerEnv" in devcontainer_json:
        logging.info(f"{datetime.now().isoformat()} - Converting containerEnv to tasks")
        for env, value in devcontainer_json["containerEnv"].items():
            gitpod_yaml["tasks"].append({
                "env": {
                    env: value
                }
            })
            logging.info(f"{datetime.now().isoformat()} - Converted containerEnv: {env}={value}")

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
