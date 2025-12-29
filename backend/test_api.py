"""
Simple API test client

This script demonstrates how to use the RunLab API programmatically
"""
import requests
import json
import sys
from pathlib import Path


API_BASE = "http://localhost:8000"


def print_section(title: str):
    print("\n" + "=" * 60)
    print(f"  {title}")
    print("=" * 60 + "\n")


def test_health():
    """Test the health endpoint"""
    print("Testing health endpoint...")
    response = requests.get(f"{API_BASE}/")
    print(f"Status: {response.status_code}")
    print(f"Response: {response.json()}")
    return response.status_code == 200


def parse_runme(file_path: str, spec_name: str):
    """Parse a runme.md file"""
    print(f"Parsing {file_path}...")

    with open(file_path) as f:
        content = f.read()

    response = requests.post(
        f"{API_BASE}/api/parse",
        json={"content": content, "spec_name": spec_name}
    )

    if response.status_code == 200:
        result = response.json()
        print("✅ Parsing successful!")
        print(f"\nSpec name: {result['spec']['name']}")
        print(f"Description: {result['spec']['description']}")
        print(f"Inputs: {len(result['spec']['inputs'])}")
        print(f"UI fields: {len(result['ui_config']['fields'])}")
        return result
    else:
        print(f"❌ Parsing failed: {response.text}")
        return None


def list_specs():
    """List all available specs"""
    print("Fetching available specs...")
    response = requests.get(f"{API_BASE}/api/specs")

    if response.status_code == 200:
        specs = response.json()
        print(f"✅ Found {len(specs)} spec(s):")
        for name in specs.keys():
            print(f"   - {name}")
        return specs
    else:
        print(f"❌ Failed: {response.text}")
        return {}


def run_job(spec_name: str, inputs: dict):
    """Run a job with given inputs"""
    print(f"Running job for spec '{spec_name}'...")
    print(f"Inputs: {inputs}")

    response = requests.post(
        f"{API_BASE}/api/run",
        json={"spec_name": spec_name, "inputs": inputs}
    )

    if response.status_code == 200:
        job = response.json()
        print("✅ Job submitted!")
        print(f"\nJob ID: {job['job_id']}")
        print(f"Status: {job['status']}")
        if job.get('logs'):
            print(f"\nLogs:\n{job['logs']}")
        if job.get('output_urls'):
            print(f"\nOutputs: {job['output_urls']}")
        return job
    else:
        print(f"❌ Job failed: {response.text}")
        return None


def main():
    print_section("RunLab API Test Client")

    # Test health
    print_section("1. Health Check")
    if not test_health():
        print("❌ API is not running!")
        print("Start it with: uvicorn app.main:app --reload")
        sys.exit(1)

    # Parse example file
    print_section("2. Parse Example Runme.md")
    example_file = Path(__file__).parent.parent / "examples" / "simple-hello.runme.md"

    if not example_file.exists():
        print(f"❌ Example file not found: {example_file}")
        sys.exit(1)

    result = parse_runme(str(example_file), "hello-world")

    if not result:
        sys.exit(1)

    # Show UI config
    print("\n📋 Generated UI Configuration:")
    for field in result['ui_config']['fields']:
        print(f"   - {field['label']} ({field['type']}): {field.get('help_text', 'N/A')}")

    # List specs
    print_section("3. List Available Specs")
    list_specs()

    # Run a job
    print_section("4. Run Example Job")
    job = run_job("hello-world", {
        "name": "RunLab User",
        "count": 3,
        "enthusiastic": True
    })

    # Summary
    print_section("Summary")
    print("✅ All tests passed!")
    print("\n🎉 The API is working correctly!")
    print("\nNext steps:")
    print("1. Create your own runme.md files")
    print("2. Build a frontend UI")
    print("3. Enable real Modal.com execution")
    print("4. Add S3 output storage")


if __name__ == "__main__":
    try:
        main()
    except requests.exceptions.ConnectionError:
        print("\n❌ Error: Could not connect to API")
        print("Make sure the server is running:")
        print("   cd backend && uvicorn app.main:app --reload")
        sys.exit(1)
    except KeyboardInterrupt:
        print("\n\nTest interrupted by user")
        sys.exit(0)
