import logging
from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import PlainTextResponse, JSONResponse
from fastapi.middleware.cors import CORSMiddleware
import yaml
import json
from converter import convert_devcontainer_to_gitpod

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

app = FastAPI()

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows all origins
    allow_credentials=True,
    allow_methods=["*"],  # Allows all methods
    allow_headers=["*"],  # Allows all headers
)

@app.post("/convert")
async def convert_to_gitpod(request: Request):
    logger.info("Received request to convert devcontainer to Gitpod config")
    try:
        # Get raw request body
        body = await request.body()
        body_str = body.decode()
        
        # Handle empty input
        if not body_str.strip():
            return JSONResponse(
                status_code=422,
                content={
                    "error": "Invalid JSON format",
                    "message": "Empty input",
                    "line_number": 1,
                    "column": 1,
                    "context": "<empty>"
                }
            )
        
        # Try to parse JSON
        try:
            devcontainer_json = json.loads(body_str)
        except json.JSONDecodeError as e:
            logger.error(f"Invalid JSON format: {str(e)}")
            # Get the specific part of the string that caused the error
            lines = body_str.splitlines()
            error_line = lines[e.lineno - 1] if e.lineno and e.lineno <= len(lines) else ""
            error_position = "^".rjust(e.colno) if e.colno else ""
            error_context = f"{error_line}\n{error_position}"
            return JSONResponse(
                status_code=422,
                content={
                    "error": "Invalid JSON format",
                    "message": str(e),
                    "line_number": e.lineno,
                    "column": e.colno,
                    "context": error_context
                }
            )
        
        logger.debug(f"Input devcontainer JSON: {devcontainer_json}")
        
        # Convert to Gitpod YAML
        logger.info("Converting devcontainer JSON to Gitpod YAML")
        gitpod_yaml = convert_devcontainer_to_gitpod(devcontainer_json)
        
        # Convert the result to YAML string
        logger.info("Converting Gitpod config to YAML string")
        gitpod_yaml_str = yaml.dump(gitpod_yaml, default_flow_style=False)
        
        logger.debug(f"Output Gitpod YAML: {gitpod_yaml_str}")
        logger.info("Conversion completed successfully")
        return PlainTextResponse(content=gitpod_yaml_str)
    except Exception as e:
        logger.error(f"Error during conversion: {str(e)}", exc_info=True)
        return JSONResponse(
            status_code=500,
            content={
                "error": "Conversion error",
                "message": str(e)
            }
        )

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
