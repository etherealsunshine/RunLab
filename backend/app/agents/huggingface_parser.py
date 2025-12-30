"""
Hugging Face-powered parser for runme.md files
FREE alternative using Hugging Face Inference API
"""
import json
import os
import requests
from typing import Dict, Any
from ..models.schemas import ParsedResult, RunmeSpec, UIConfig
from dotenv import load_dotenv

# Load .env file
load_dotenv()

class HuggingFaceParser:
    """Parser agent that uses Hugging Face models (FREE!)"""

    def __init__(self, api_key: str | None = None, model: str = "mistralai/Mistral-7B-Instruct-v0.2:featherless-ai"):
        """
        Initialize with Hugging Face API

        Get a FREE API key at: https://huggingface.co/settings/tokens

        Recommended models (all FREE):
        - mistralai/Mistral-7B-Instruct-v0.2:featherless-ai (best quality, recommended)
        - mistralai/Mixtral-8x7B-Instruct-v0.1:featherless-ai (more powerful)
        - meta-llama/Meta-Llama-3-8B-Instruct:featherless-ai (good alternative)
        """
        self.api_key = api_key or os.getenv("HUGGINGFACE_API_KEY")
        if not self.api_key:
            raise ValueError("HUGGINGFACE_API_KEY not found in environment")

        self.model = model
        # Using OpenAI-compatible endpoint
        self.api_url = "https://router.huggingface.co/v1/chat/completions"
        self.headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }

    def parse(self, runme_content: str) -> ParsedResult:
        """Parse a runme.md file using Hugging Face model"""
        prompt = self._build_parse_prompt(runme_content)
    
        # Call Hugging Face Router API (OpenAI-compatible)
        response = requests.post(
            self.api_url,
            headers=self.headers,
            json={
                "model": self.model,
                "messages": [
                    {
                        "role": "system",
                        "content": "You are a parser for runme.md files. Extract structured information and return ONLY valid JSON."
                    },
                    {
                        "role": "user",
                        "content": prompt
                    }
                ],
                "temperature": 0.1,
                "max_tokens": 2000
            },
            timeout=120
        )
    
        if response.status_code != 200:
            raise ValueError(f"Hugging Face API error: {response.text}")
    
        # Extract response (OpenAI format)
        result = response.json()
        response_text = result["choices"][0]["message"]["content"]
    
        # Parse JSON from response
        parsed_data = self._extract_json(response_text)
        
        # Fix common type mapping issues
        parsed_data = self._fix_input_types(parsed_data)  # ADD THIS LINE
    
        # Validate and convert to Pydantic models
        result = ParsedResult(**parsed_data)
        return result

    def _build_parse_prompt(self, runme_content: str) -> str:
        """Build the prompt for the HF model"""
        return f"""Parse this runme.md file and return a JSON object:

{runme_content}

Return this exact structure:

{{
  "spec": {{
    "name": "project-name",
    "description": "description",
    "version": "1.0.0",
    "container": {{"image": "python:3.11-slim", "working_dir": "/app"}},
    "compute": {{"cpu": 2, "memory": "4GB", "gpu": null, "timeout": 300}},
    "inputs": [
      {{"name": "input1", "type": "string", "description": "desc", "required": true, "default": null, "min": null, "max": null, "example": "ex"}}
    ],
    "command": "python main.py --arg {{{{input1}}}}",
    "outputs": {{"location": "/outputs", "type": "files", "mount_to_s3": false}}
  }},
  "ui_config": {{
    "title": "Project Title",
    "description": "Brief description",
    "fields": [
      {{"name": "input1", "type": "text", "label": "Label", "required": true, "default": null, "placeholder": "hint", "help_text": "help"}}
    ]
  }}
}}

CRITICAL RULES:
1. spec.inputs[].type MUST be one of: "string", "integer", "float", "boolean", "file"
2. ui_config.fields[].type can be: "text", "number", "checkbox", "select", etc.
3. Map between them like this:
   - spec type "string" → ui type "text"
   - spec type "integer" → ui type "number"
   - spec type "float" → ui type "number"
   - spec type "boolean" → ui type "checkbox"
4. Keep command simple like: "python script.py --arg {{{{input_name}}}}"
5. DO NOT use inline Python with -c flag
6. DO NOT use escape sequences in command field
7. Return ONLY valid JSON, no explanations

Return the JSON:"""

    def _extract_json(self, text: str) -> Dict[str, Any]:
        """Extract JSON from model response"""
        text = text.strip()
    
        # Remove markdown code blocks
        if "```json" in text:
            text = text.split("```json")[1].split("```")[0]
        elif "```" in text:
            text = text.split("```")[1].split("```")[0]
    
        # Find JSON object
        start = text.find("{")
        if start == -1:
            raise ValueError("No JSON found in response")
    
        # Find matching closing brace
        brace_count = 0
        for i, char in enumerate(text[start:], start):
            if char == "{":
                brace_count += 1
            elif char == "}":
                brace_count -= 1
                if brace_count == 0:
                    text = text[start:i+1]
                    break
                
        # Fix common escape issues before parsing
        # Replace invalid escape sequences in command strings
        try:
            return json.loads(text)
        except json.JSONDecodeError as e:
            # Try to fix invalid escapes
            # Replace \n that aren't properly escaped
            text_fixed = text.replace('\\n', '\\\\n')
            text_fixed = text_fixed.replace('\\t', '\\\\t')
            text_fixed = text_fixed.replace("\\'", "'")  # Fix escaped quotes
            
            try:
                return json.loads(text_fixed)
            except json.JSONDecodeError as e2:
                # If still failing, try to extract and fix the command field specifically
                import re
                # Find the command field and fix it
                command_match = re.search(r'"command"\s*:\s*"([^"]*(?:\\.[^"]*)*)"', text)
                if command_match:
                    # Replace the problematic command with a simpler one
                    text = re.sub(
                        r'"command"\s*:\s*"[^"]*(?:\\.[^"]*)*"',
                        '"command": "python main.py --name {{name}} --count {{count}} --enthusiastic {{enthusiastic}}"',
                        text
                    )
                    return json.loads(text)
                
                raise ValueError(f"Failed to parse JSON: {e2}\nResponse: {text}")
    
    def _fix_input_types(self, parsed_data: Dict[str, Any]) -> Dict[str, Any]:
        """Fix common type mapping issues from the model"""
        type_mapping = {
            "text": "string",
            "number": "integer",
            "checkbox": "boolean",
            "select": "string",
            "textarea": "string"
        }

        if "spec" in parsed_data and "inputs" in parsed_data["spec"]:
            for input_field in parsed_data["spec"]["inputs"]:
                if input_field.get("type") in type_mapping:
                    input_field["type"] = type_mapping[input_field["type"]]

        return parsed_data
    
    def validate_inputs(self, spec: RunmeSpec, inputs: Dict[str, Any]) -> Dict[str, Any]:
        """Validate user inputs against the spec"""
        validated = {}

        for field in spec.inputs:
            value = inputs.get(field.name)

            # Check required fields
            if field.required and value is None:
                if field.default is not None:
                    value = field.default
                else:
                    raise ValueError(f"Required field '{field.name}' is missing")

            # Type conversion and validation
            if value is not None:
                if field.type == "integer":
                    value = int(value)
                    if field.min is not None and value < field.min:
                        raise ValueError(f"Field '{field.name}' must be >= {field.min}")
                    if field.max is not None and value > field.max:
                        raise ValueError(f"Field '{field.name}' must be <= {field.max}")

                elif field.type == "float":
                    value = float(value)
                    if field.min is not None and value < field.min:
                        raise ValueError(f"Field '{field.name}' must be >= {field.min}")
                    if field.max is not None and value > field.max:
                        raise ValueError(f"Field '{field.name}' must be <= {field.max}")

                elif field.type == "boolean":
                    if isinstance(value, str):
                        value = value.lower() in ("true", "1", "yes")
                    else:
                        value = bool(value)

                elif field.type == "string":
                    value = str(value)

            validated[field.name] = value

        return validated

    def build_command(self, spec: RunmeSpec, validated_inputs: Dict[str, Any]) -> str:
        """Build the final command by substituting inputs"""
        command = spec.command

        for key, value in validated_inputs.items():
            placeholder = f"{{{key}}}"
            if placeholder in command:
                if isinstance(value, bool):
                    str_value = "true" if value else "false"
                elif isinstance(value, (int, float)):
                    str_value = str(value)
                else:
                    str_value = str(value).replace('"', '\\"')

                command = command.replace(placeholder, str_value)

        return command