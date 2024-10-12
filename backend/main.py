from fastapi import FastAPI, HTTPException, Body
import yaml
from converter import convert_devcontainer_to_gitpod

app = FastAPI()

@app.post("/convert")
async def convert_to_gitpod(devcontainer_json: dict = Body(...)):
    try:
        # Convert to Gitpod YAML
        gitpod_yaml = convert_devcontainer_to_gitpod(devcontainer_json)
        
        # Convert the result to YAML string
        gitpod_yaml_str = yaml.dump(gitpod_yaml, default_flow_style=False)
        
        return {"gitpod_yaml": gitpod_yaml_str}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
