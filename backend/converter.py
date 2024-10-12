def convert_devcontainer_to_gitpod(devcontainer_json):
    gitpod_yaml = {
        "image": {},
        "tasks": [],
        "vscode": {
            "extensions": []
        }
    }

    # Convert image
    if "image" in devcontainer_json:
        gitpod_yaml["image"]["file"] = devcontainer_json["image"]

    # Convert features to tasks
    if "features" in devcontainer_json:
        for feature, value in devcontainer_json["features"].items():
            if isinstance(value, dict) and "version" in value:
                gitpod_yaml["tasks"].append({
                    "name": f"Install {feature}",
                    "command": f"sudo apt-get update && sudo apt-get install -y {feature}={value['version']}"
                })
            else:
                gitpod_yaml["tasks"].append({
                    "name": f"Install {feature}",
                    "command": f"sudo apt-get update && sudo apt-get install -y {feature}"
                })

    # Convert settings
    if "settings" in devcontainer_json:
        # In Gitpod, VS Code settings are typically handled differently
        # For this example, we'll just add a comment
        gitpod_yaml["vscode"]["settings"] = {"# Note": "VS Code settings should be configured separately in Gitpod"}

    # Convert extensions
    if "extensions" in devcontainer_json:
        gitpod_yaml["vscode"]["extensions"] = devcontainer_json["extensions"]

    # Convert postCreateCommand
    if "postCreateCommand" in devcontainer_json:
        gitpod_yaml["tasks"].append({
            "name": "Post-create command",
            "command": devcontainer_json["postCreateCommand"]
        })

    return gitpod_yaml
