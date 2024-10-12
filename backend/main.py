from fastapi import FastAPI, HTTPException, Request
import json
import yaml
from converter import convert_devcontainer_to_gitpod

app = FastAPI()

@app.post("/convert")
async def convert_to_gitpod(request: Request):
    try:
        # Get the raw JSON content from the request body
        devcontainer_json = await request.json()
        
        # Convert to Gitpod YAML
        gitpod_yaml = convert_devcontainer_to_gitpod(devcontainer_json)
        
        # Convert the result to YAML string
        gitpod_yaml_str = yaml.dump(gitpod_yaml, default_flow_style=False)
        
        return {"gitpod_yaml": gitpod_yaml_str}
    except json.JSONDecodeError:
        raise HTTPException(status_code=400, detail="Invalid JSON content")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
