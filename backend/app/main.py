"""
RunLab FastAPI Application

Main entry point for the API that orchestrates:
- Parsing runme.md files with Claude
- Generating UI configurations
- Running jobs on Modal.com
- Tracking job status
"""
from fastapi import FastAPI, HTTPException, File, UploadFile
from fastapi.middleware.cors import CORSMiddleware
from typing import Dict, List
import os

from .models.schemas import (
    ParsedResult,
    ParseRequest,
    JobRequest,
    JobStatus,
)
from .agents.runme_parser import RunmeParser
from .agents.huggingface_parser import HuggingFaceParser
from .agents.modal_runner import ModalRunner


# Initialize FastAPI app
app = FastAPI(
    title="RunLab API",
    description="AI-powered DevOps runner that turns any repo into a production app",
    version="0.1.0"
)

# CORS middleware for frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Configure this properly in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Global state (in production, use a database)
parsed_specs: Dict[str, ParsedResult] = {}

# Choose parser based on available API key
# Priority: HUGGINGFACE_API_KEY (free!) > ANTHROPIC_API_KEY
if os.getenv("HUGGINGFACE_API_KEY"):
    print("🤗 Using Hugging Face parser (FREE!)")
    parser = HuggingFaceParser()
elif os.getenv("ANTHROPIC_API_KEY"):
    print("🤖 Using Claude parser")
    parser = RunmeParser()
else:
    print("⚠️  No API key found! Set HUGGINGFACE_API_KEY or ANTHROPIC_API_KEY")
    parser = None

runner = ModalRunner(mock_mode=False)  # Start in mock mode


@app.get("/")
async def root():
    """Health check endpoint"""
    return {
        "status": "running",
        "service": "RunLab API",
        "version": "0.1.0"
    }


@app.post("/api/parse", response_model=ParsedResult)
async def parse_runme(request: ParseRequest):
    """
    Parse a runme.md file and generate UI configuration

    This endpoint uses AI (Hugging Face or Claude) to understand the runme.md specification
    and generates both the structured spec and UI config.
    """
    if parser is None:
        raise HTTPException(
            status_code=503,
            detail="No AI parser available. Please set HUGGINGFACE_API_KEY or ANTHROPIC_API_KEY"
        )

    try:
        # Parse the content
        result = parser.parse(request.content)

        # Store the parsed spec
        spec_name = request.spec_name or result.spec.name
        parsed_specs[spec_name] = result

        return result

    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Parsing failed: {str(e)}")


@app.post("/api/parse/file", response_model=ParsedResult)
async def parse_runme_file(file: UploadFile = File(...)):
    """
    Upload and parse a runme.md file

    Alternative endpoint that accepts file upload
    """
    try:
        content = await file.read()
        content_str = content.decode("utf-8")

        # Extract name from filename (e.g., "my-app.runme.md" -> "my-app")
        spec_name = file.filename.replace(".runme.md", "").replace(".md", "")

        result = parser.parse(content_str)
        parsed_specs[spec_name] = result

        return result

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"File parsing failed: {str(e)}")


@app.get("/api/specs", response_model=Dict[str, ParsedResult])
async def list_specs():
    """
    List all available parsed specifications

    Returns all specs that have been parsed and are ready to run
    """
    return parsed_specs


@app.get("/api/specs/{spec_name}", response_model=ParsedResult)
async def get_spec(spec_name: str):
    """Get a specific parsed specification by name"""
    if spec_name not in parsed_specs:
        raise HTTPException(status_code=404, detail=f"Spec '{spec_name}' not found")

    return parsed_specs[spec_name]


@app.post("/api/run", response_model=JobStatus)
async def run_job(request: JobRequest):
    """
    Execute a job with user inputs

    This validates inputs, builds the command, and executes on Modal.com
    """
    # Get the spec
    if request.spec_name not in parsed_specs:
        raise HTTPException(
            status_code=404,
            detail=f"Spec '{request.spec_name}' not found. Parse it first using /api/parse"
        )

    parsed_result = parsed_specs[request.spec_name]
    spec = parsed_result.spec

    try:
        # Validate inputs
        validated_inputs = parser.validate_inputs(spec, request.inputs)

        # Build command
        command = parser.build_command(spec, validated_inputs)

        # Run on Modal
        job_status = runner.run_job(spec, command, validated_inputs)

        return job_status

    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Job execution failed: {str(e)}")


@app.get("/api/jobs/{job_id}", response_model=JobStatus)
async def get_job_status(job_id: str):
    """Get the status of a running or completed job"""
    job = runner.get_job_status(job_id)

    if not job:
        raise HTTPException(status_code=404, detail=f"Job '{job_id}' not found")

    return job


@app.delete("/api/specs/{spec_name}")
async def delete_spec(spec_name: str):
    """Delete a parsed specification"""
    if spec_name not in parsed_specs:
        raise HTTPException(status_code=404, detail=f"Spec '{spec_name}' not found")

    del parsed_specs[spec_name]
    return {"status": "deleted", "spec_name": spec_name}


# Development mode settings
if os.getenv("ENVIRONMENT") == "development":
    @app.get("/api/debug/specs")
    async def debug_specs():
        """Debug endpoint to see raw parsed specs"""
        return {
            name: {
                "spec": result.spec.dict(),
                "ui_config": result.ui_config.dict()
            }
            for name, result in parsed_specs.items()
        }
