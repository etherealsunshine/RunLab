# 🚀 RunLab Quickstart

Get up and running with RunLab in 5 minutes!

## Prerequisites

- Python 3.11 or higher
- Anthropic API key ([get one here](https://console.anthropic.com/))
- (Optional) Modal.com account for actual execution

## Step 1: Clone and Setup

```bash
cd RunLab
```

## Step 2: Install Backend Dependencies

```bash
cd backend
pip install -r requirements.txt
```

Or if you use uv (faster):
```bash
uv pip install -r requirements.txt
```

## Step 3: Configure Environment

```bash
cp .env.example .env
```

Edit `.env` and add your Anthropic API key:
```
ANTHROPIC_API_KEY=sk-ant-xxxxx
```

## Step 4: Test the Parser

```bash
# Make sure you're in the backend directory
export ANTHROPIC_API_KEY=your_key_here  # Or use .env file
python test_parser.py
```

You should see:
- ✅ Claude parsing the example runme.md
- ✅ Generated spec and UI config
- ✅ Input validation tests
- ✅ Command building

## Step 5: Start the API Server

```bash
uvicorn app.main:app --reload --port 8000
```

Visit http://localhost:8000/docs for interactive API documentation!

## Step 6: Try It Out

### Option A: Use the Swagger UI

1. Go to http://localhost:8000/docs
2. Click on `POST /api/parse`
3. Click "Try it out"
4. Paste this simple example:

```json
{
  "content": "# Hello World\n\n## Project Info\n- **name**: test-hello\n- **description**: Simple test\n- **version**: 1.0.0\n\n## Container\n- **image**: python:3.11-slim\n- **working_dir**: /app\n\n## Compute Requirements\n- **cpu**: 1\n- **memory**: 1GB\n- **gpu**: none\n- **timeout**: 60\n\n## Inputs\n\n1. **message** (required)\n   - type: string\n   - description: Message to print\n   - example: Hello\n\n## Command\n```bash\npython -c \"print('{message}')\"\n```\n\n## Outputs\n- **location**: /outputs\n- **type**: stdout\n- **mount_to_s3**: false",
  "spec_name": "test-hello"
}
```

5. Execute and see the parsed result!

### Option B: Use curl

```bash
# Parse an example runme.md
curl -X POST "http://localhost:8000/api/parse/file" \
  -H "Content-Type: multipart/form-data" \
  -F "file=@../examples/simple-hello.runme.md"
```

### Option C: Use Python

```python
import requests

# Parse a runme.md
with open("../examples/simple-hello.runme.md") as f:
    content = f.read()

response = requests.post(
    "http://localhost:8000/api/parse",
    json={"content": content, "spec_name": "hello"}
)

result = response.json()
print(f"Parsed spec: {result['spec']['name']}")
print(f"UI fields: {len(result['ui_config']['fields'])}")

# Run a job
job_response = requests.post(
    "http://localhost:8000/api/run",
    json={
        "spec_name": "hello",
        "inputs": {
            "name": "RunLab",
            "count": 3,
            "enthusiastic": True
        }
    }
)

job = job_response.json()
print(f"Job ID: {job['job_id']}")
print(f"Status: {job['status']}")
print(f"Logs:\n{job['logs']}")
```

## What's Next?

### Immediate Next Steps
1. ✅ **Create your own runme.md** - Start with the examples in `examples/`
2. ✅ **Test different input types** - strings, integers, booleans, floats
3. ✅ **Explore the API** - Check out all endpoints at `/docs`

### Build the Frontend
The backend is ready! Now you can:
1. Build a Next.js frontend that:
   - Uploads runme.md files
   - Dynamically renders forms from UI config
   - Submits jobs and shows results
   - Streams logs in real-time

2. Or build a simple CLI tool
3. Or integrate into your existing app

### Enable Real Modal Execution
Right now, the system runs in mock mode. To enable real execution:

1. Sign up for [Modal.com](https://modal.com)
2. Install Modal: `pip install modal`
3. Authenticate: `modal token new`
4. In `app/main.py`, change:
   ```python
   runner = ModalRunner(mock_mode=False)  # Enable real execution
   ```

### Add S3 Output Storage
1. Configure AWS credentials in `.env`
2. Implement S3 upload in `modal_runner.py`
3. Return real S3 URLs in job results

## Example Use Cases

### 1. Stable Diffusion Image Generator
```bash
# Parse the example
curl -X POST "http://localhost:8000/api/parse/file" \
  -F "file=@../examples/stable-diffusion.runme.md"

# Generate an image
curl -X POST "http://localhost:8000/api/run" \
  -H "Content-Type: application/json" \
  -d '{
    "spec_name": "stable-diffusion-xl",
    "inputs": {
      "prompt": "A beautiful sunset over mountains",
      "num_images": 2,
      "steps": 30
    }
  }'
```

### 2. Data Processing Pipeline
Create a `data-pipeline.runme.md`:
- Input: CSV file URL
- Container: Python with pandas
- Compute: 4 CPU, 8GB RAM
- Output: Processed data to S3

### 3. ML Model Training
Create a `train-model.runme.md`:
- Inputs: dataset path, hyperparameters
- Container: PyTorch image
- Compute: A100 GPU, 32GB RAM
- Output: Model checkpoints to S3

## Troubleshooting

### "ANTHROPIC_API_KEY not found"
Make sure you've set the environment variable:
```bash
export ANTHROPIC_API_KEY=your_key_here
```

Or create a `.env` file in the `backend/` directory.

### "Parsing failed"
Check that your runme.md follows the correct format. See `examples/` for reference.

### "ModuleNotFoundError"
Make sure you've installed all dependencies:
```bash
pip install -r requirements.txt
```

## Next Steps

Check out the main [README.md](README.md) for:
- Complete architecture overview
- API endpoint documentation
- How to write runme.md files
- Project roadmap

---

**Built with ❤️ and Claude Code**

Ready to turn any repo into a production app? Let's go! 🚀
