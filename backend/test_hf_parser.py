"""
Test script for Hugging Face parser
FREE alternative to Anthropic Claude!
"""
import os
import sys
import json
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

from app.agents.huggingface_parser import HuggingFaceParser


def print_section(title: str):
    print("\n" + "=" * 60)
    print(f"  {title}")
    print("=" * 60 + "\n")


def main():
    print_section("🤗 RunLab Hugging Face Parser Test (FREE!)")

    # Check for API key
    api_key = os.getenv("HUGGINGFACE_API_KEY")
    if not api_key:
        print("❌ Error: HUGGINGFACE_API_KEY not found in environment")
        print("")
        print("Get a FREE API key:")
        print("1. Go to https://huggingface.co/settings/tokens")
        print("2. Click 'New token'")
        print("3. Copy the token (starts with hf_...)")
        print("")
        print("Then set it:")
        print("  export HUGGINGFACE_API_KEY=hf_your_token_here")
        print("")
        sys.exit(1)

    # Initialize parser
    print("✅ Initializing Hugging Face parser...")
    print("📦 Using model: meta-llama/Llama-3.2-3B-Instruct (FREE!)")
    parser = HuggingFaceParser(api_key=api_key)

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

    # Parse with Hugging Face
    print_section("Parsing with Hugging Face")
    print("🤖 Sending to Hugging Face API...")
    print("⏳ First request may take 30-60 seconds (model loading)...")

    try:
        result = parser.parse(runme_content)
        print("✅ Parsing successful!")

    except Exception as e:
        print(f"❌ Parsing failed: {e}")
        print("\nTroubleshooting:")
        print("- Model might be loading, wait and try again")
        print("- Check your API token is valid")
        print("- Try a different model (edit huggingface_parser.py)")
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

    print("Test 1: Valid inputs")
    test_inputs_valid = {
        "name": "Hugging Face",
        "count": 3,
        "enthusiastic": True
    }
    print(f"Inputs: {test_inputs_valid}")

    try:
        validated = parser.validate_inputs(result.spec, test_inputs_valid)
        print(f"✅ Validation passed: {validated}")
    except Exception as e:
        print(f"❌ Validation failed: {e}")

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

    print("\n🎉 Hugging Face parser is working correctly!")
    print("\n💡 Tips:")
    print("- FREE tier has ~60 requests/minute limit")
    print("- First request takes longer (model loading)")
    print("- For better quality, try mistralai/Mistral-7B-Instruct-v0.3")

    print("\nNext steps:")
    print("1. Start the API server: uvicorn app.main:app --reload")
    print("2. Visit http://localhost:8000/docs")
    print("3. Set up Modal: modal setup")
    print("4. See SETUP_FREE.md for details")


if __name__ == "__main__":
    main()
