import logging
from fastapi import FastAPI, HTTPException
from fastapi.responses import PlainTextResponse
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
import yaml
from converter import convert_devcontainer_to_gitpod

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class DevContainerConfig(BaseModel):
    """DevContainer configuration model."""
    name: str = Field(..., description="Name of the devcontainer")

app = FastAPI()

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows all origins
    allow_credentials=True,
    allow_methods=["*"],  # Allows all methods
    allow_headers=["*"],  # Allows all headers
)

@app.post("/convert", response_class=PlainTextResponse)
async def convert_to_gitpod(config: DevContainerConfig):
    logger.info("Received request to convert devcontainer to Gitpod config")
    try:
        devcontainer_json = config.dict()
        logger.debug(f"Input devcontainer JSON: {devcontainer_json}")
        
        # Convert to Gitpod YAML
        logger.info("Converting devcontainer JSON to Gitpod YAML")
        gitpod_yaml = convert_devcontainer_to_gitpod(devcontainer_json)
        
        # Convert the result to YAML string
        logger.info("Converting Gitpod config to YAML string")
        gitpod_yaml_str = yaml.dump(gitpod_yaml, default_flow_style=False)
        
        logger.debug(f"Output Gitpod YAML: {gitpod_yaml_str}")
        logger.info("Conversion completed successfully")
        return gitpod_yaml_str
    except Exception as e:
        logger.error(f"Error during conversion: {str(e)}", exc_info=True)
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
