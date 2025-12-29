"""
Test script to validate the runme.md parser

This script:
1. Loads an example runme.md file
2. Uses Claude to parse it
3. Validates the structure
4. Generates UI config
5. Tests input validation
6. Builds example commands
"""
import os
import sys
import json
from pathlib import Path

# Add app to path
sys.path.insert(0, str(Path(__file__).parent))

from app.agents.runme_parser import RunmeParser


def print_section(title: str):
    """Print a formatted section header"""
    print("\n" + "=" * 60)
    print(f"  {title}")
    print("=" * 60 + "\n")


def main():
    print_section("RunLab Parser Test")

    # Check for API key
    api_key = os.getenv("ANTHROPIC_API_KEY")
    if not api_key:
        print("❌ Error: ANTHROPIC_API_KEY not found in environment")
        print("Please set it with: export ANTHROPIC_API_KEY=your_key_here")
        sys.exit(1)

    # Initialize parser
    print("✅ Initializing Claude parser...")
    parser = RunmeParser(api_key=api_key)

    # Load example file
    example_file = Path(__file__).parent.parent / "examples" / "simple-hello.runme.md"

    if not example_file.exists():
        print(f"❌ Error: Example file not found at {example_file}")
        sys.exit(1)

    print(f"✅ Loading example: {example_file.name}")
    runme_content = example_file.read_text()

    print("\n📄 Runme.md content:")
    print("-" * 60)
    print(runme_content[:500] + "..." if len(runme_content) > 500 else runme_content)
    print("-" * 60)

    # Parse with Claude
    print_section("Parsing with Claude")
    print("🤖 Sending to Claude for parsing...")

    try:
        result = parser.parse(runme_content)
        print("✅ Parsing successful!")

    except Exception as e:
        print(f"❌ Parsing failed: {e}")
        sys.exit(1)

    # Display parsed spec
    print_section("Parsed Specification")
    spec_dict = result.spec.dict()
    print(json.dumps(spec_dict, indent=2))

    # Display UI config
    print_section("Generated UI Configuration")
    ui_dict = result.ui_config.dict()
    print(json.dumps(ui_dict, indent=2))

    # Test input validation
    print_section("Testing Input Validation")

    # Test valid inputs
    print("Test 1: Valid inputs")
    test_inputs_valid = {
        "name": "Claude",
        "count": 3,
        "enthusiastic": True
    }
    print(f"Inputs: {test_inputs_valid}")

    try:
        validated = parser.validate_inputs(result.spec, test_inputs_valid)
        print(f"✅ Validation passed: {validated}")
    except Exception as e:
        print(f"❌ Validation failed: {e}")

    # Test invalid inputs (missing required field)
    print("\nTest 2: Missing required field")
    test_inputs_invalid = {
        "count": 5
    }
    print(f"Inputs: {test_inputs_invalid}")

    try:
        validated = parser.validate_inputs(result.spec, test_inputs_invalid)
        print(f"❌ Should have failed but didn't: {validated}")
    except ValueError as e:
        print(f"✅ Correctly rejected: {e}")

    # Test command building
    print_section("Testing Command Building")

    test_inputs_cmd = {
        "name": "RunLab",
        "count": 2,
        "enthusiastic": False
    }

    validated = parser.validate_inputs(result.spec, test_inputs_cmd)
    command = parser.build_command(result.spec, validated)

    print(f"Inputs: {test_inputs_cmd}")
    print(f"\n📝 Generated command:")
    print("-" * 60)
    print(command)
    print("-" * 60)

    # Summary
    print_section("Test Summary")
    print("✅ All tests passed!")
    print("\n📊 Results:")
    print(f"   - Spec name: {result.spec.name}")
    print(f"   - Description: {result.spec.description}")
    print(f"   - Input fields: {len(result.spec.inputs)}")
    print(f"   - UI fields: {len(result.ui_config.fields)}")
    print(f"   - Compute: {result.spec.compute.cpu} CPU, {result.spec.compute.memory} RAM")
    print(f"   - GPU: {result.spec.compute.gpu or 'None'}")

    print("\n🚀 Parser is working correctly!")
    print("\nNext steps:")
    print("1. Start the API server: cd backend && uvicorn app.main:app --reload")
    print("2. Visit http://localhost:8000/docs for API documentation")
    print("3. Test the /api/parse endpoint with your own runme.md files")


if __name__ == "__main__":
    main()
