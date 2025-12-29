"""
Claude-powered parser for runme.md files
Uses Claude to intelligently parse specifications and generate UI configurations
"""
import json
import os
from typing import Dict, Any
from anthropic import Anthropic
from ..models.schemas import ParsedResult, RunmeSpec, UIConfig


class RunmeParser:
    """Parser agent that uses Claude to understand runme.md files"""

    def __init__(self, api_key: str | None = None):
        self.api_key = api_key or os.getenv("ANTHROPIC_API_KEY")
        if not self.api_key:
            raise ValueError("ANTHROPIC_API_KEY not found in environment")
        self.client = Anthropic(api_key=self.api_key)

    def parse(self, runme_content: str) -> ParsedResult:
        """
        Parse a runme.md file and generate both spec and UI config

        Args:
            runme_content: The raw markdown content of runme.md

        Returns:
            ParsedResult containing the spec and UI configuration
        """
        prompt = self._build_parse_prompt(runme_content)

        response = self.client.messages.create(
            model="claude-sonnet-4-5-20250929",
            max_tokens=4000,
            temperature=0,
            messages=[
                {
                    "role": "user",
                    "content": prompt
                }
            ]
        )

        # Extract JSON from response
        response_text = response.content[0].text
        parsed_data = self._extract_json(response_text)

        # Validate and convert to Pydantic models
        result = ParsedResult(**parsed_data)
        return result

    def _build_parse_prompt(self, runme_content: str) -> str:
        """Build the prompt for Claude to parse the runme.md"""
        return f"""You are a parser agent for runme.md files. Your job is to extract structured information and generate a UI configuration.

Here is the runme.md content:

{runme_content}

Parse this file and return a JSON object with the following structure:

{{
  "spec": {{
    "name": "project-name",
    "description": "project description",
    "version": "1.0.0",
    "container": {{
      "image": "docker-image-name",
      "working_dir": "/app"
    }},
    "compute": {{
      "cpu": 4,
      "memory": "8GB",
      "gpu": "T4 or null",
      "timeout": 300
    }},
    "inputs": [
      {{
        "name": "input_name",
        "type": "string|integer|float|boolean|file",
        "description": "what this input is for",
        "required": true,
        "default": null,
        "min": null,
        "max": null,
        "example": "example value"
      }}
    ],
    "command": "the command template with {{input_name}} placeholders",
    "outputs": {{
      "location": "/outputs",
      "type": "files|stdout|both",
      "mount_to_s3": true
    }}
  }},
  "ui_config": {{
    "title": "Human-readable title",
    "description": "Brief description for users",
    "fields": [
      {{
        "name": "input_name",
        "type": "text|number|checkbox|file|textarea",
        "label": "User-friendly label",
        "required": true,
        "default": null,
        "min": null,
        "max": null,
        "placeholder": "helpful placeholder",
        "help_text": "additional context"
      }}
    ]
  }}
}}

IMPORTANT RULES:
1. Extract ALL information from the runme.md accurately
2. For the UI config, create user-friendly labels and help text
3. Map input types correctly:
   - string → text or textarea (use textarea for long text)
   - integer/float → number
   - boolean → checkbox
   - file → file
4. Preserve the command template with curly brace placeholders like {{input_name}}
5. If GPU is specified as "none" or not needed, set gpu to null
6. Return ONLY valid JSON, no markdown formatting or explanations

Return the JSON now:"""

    def _extract_json(self, text: str) -> Dict[str, Any]:
        """Extract JSON from Claude's response"""
        # Try to find JSON in the response
        text = text.strip()

        # Remove markdown code blocks if present
        if text.startswith("```"):
            lines = text.split("\n")
            text = "\n".join(lines[1:-1])

        if text.startswith("```json"):
            text = text[7:]
        if text.endswith("```"):
            text = text[:-3]

        text = text.strip()

        try:
            return json.loads(text)
        except json.JSONDecodeError as e:
            raise ValueError(f"Failed to parse JSON from Claude response: {e}\nResponse: {text}")

    def validate_inputs(self, spec: RunmeSpec, inputs: Dict[str, Any]) -> Dict[str, Any]:
        """
        Validate user inputs against the spec

        Args:
            spec: The parsed RunmeSpec
            inputs: User-provided inputs

        Returns:
            Validated and type-converted inputs

        Raises:
            ValueError: If validation fails
        """
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
        """
        Build the final command by substituting inputs into the command template

        Args:
            spec: The parsed RunmeSpec
            validated_inputs: Validated user inputs

        Returns:
            The final command string ready to execute
        """
        command = spec.command

        # Replace {input_name} placeholders with actual values
        for key, value in validated_inputs.items():
            placeholder = f"{{{key}}}"
            if placeholder in command:
                # Handle different types appropriately
                if isinstance(value, bool):
                    str_value = "true" if value else "false"
                elif isinstance(value, (int, float)):
                    str_value = str(value)
                else:
                    # String values - escape quotes
                    str_value = str(value).replace('"', '\\"')

                command = command.replace(placeholder, str_value)

        return command
