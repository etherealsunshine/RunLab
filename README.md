# 🚀 AI DevOps Runner

> Run any GitHub repo with AI-generated UI and automatic cloud provisioning

Inspired by Modal.com's capabilities, this tool lets you create a `runme.md` file that Claude reads to automatically:
- Generate a bespoke user interface
- Provision compute resources (CPU/GPU)
- Run containers with proper orchestration
- Stream outputs to S3
- Handle all the DevOps complexity

## 🎯 The Vision

**Instead of writing:**
- Custom deployment scripts
- Docker compose files
- Frontend forms
- API endpoints
- Infrastructure code

**You write:**
A simple `runme.md` that describes what inputs you need, what container to run, and what compute resources you want.

**Claude handles:**
- Parsing your requirements
- Generating the UI
- Orchestrating the execution
- Managing outputs

## 🏗️ Architecture

```
┌─────────────┐
│  runme.md   │  ← Developer writes this
└──────┬──────┘
       │
       ↓
┌─────────────────────┐
│  Claude AI Agent    │  ← Parses & understands
│  (runme_parser.py)  │
└──────┬──────────────┘
       │
       ↓
┌─────────────────────┐
│  FastAPI Backend    │  ← Validates & orchestrates
└──────┬──────────────┘
       │
       ↓
┌─────────────────────┐
│  Modal.com          │  ← Runs containers with GPU
│  (modal_runner.py)  │
└──────┬──────────────┘
       │
       ↓
┌─────────────────────┐
│  S3 Storage         │  ← Stores outputs
└─────────────────────┘
```

## 🚀 Quick Start

### Prerequisites

- Python 3.11+
- Anthropic API key
- Modal.com account (optional for now, mocked in development)
- AWS account (optional for S3 storage)

### Installation

```bash
# Clone the repo
git clone <your-repo>
cd ai-devops-runner

# Set up backend
cd backend
pip install -r requirements.txt

# Configure environment
cp .env.example .env
# Edit .env and add your ANTHROPIC_API_KEY
```

### Test the Parser

```bash
cd backend
export ANTHROPIC_API_KEY=your_key_here
python test_parser.py
```

This will:
1. Load the example `runme.md`
2. Use Claude to parse it
3. Generate UI configuration
4. Validate inputs
5. Build commands

### Run the API Server

```bash
cd backend
uvicorn app.main:app --reload --port 8000
```

Visit: http://localhost:8000/docs for the interactive API documentation

## 📝 Writing a runme.md

Here's the structure:

```markdown
# AI Agent Runner Specification

## Project Info
- **name**: my-awesome-app
- **description**: What your app does
- **version**: 1.0.0

## Container
- **image**: python:3.11-slim
- **working_dir**: /app

## Compute Requirements
- **cpu**: 4
- **memory**: 8GB
- **gpu**: T4  # or "none" if not needed
- **timeout**: 300

## Inputs
1. **prompt** (required)
   - type: string
   - description: The main input
   - example: "Hello world"

2. **count** (optional)
   - type: integer
   - min: 1
   - max: 10
   - default: 1

## Command
```bash
python main.py --prompt "{prompt}" --count {count}
```

## Outputs
- **location**: /outputs
- **type**: files
- **mount_to_s3**: true
```

## 🎨 How It Works

### 1. Parse Phase
```python
# Claude reads runme.md and extracts:
{
  "name": "my-app",
  "inputs": [
    {"name": "prompt", "type": "string", "required": true},
    {"name": "count", "type": "integer", "min": 1, "max": 10}
  ],
  "command": "python main.py --prompt {prompt} --count {count}",
  "compute": {"cpu": 4, "memory": "8GB", "gpu": "T4"}
}
```

### 2. UI Generation Phase
```python
# Claude generates UI config:
{
  "fields": [
    {
      "name": "prompt",
      "type": "text",
      "label": "Prompt",
      "required": true
    },
    {
      "name": "count",
      "type": "number",
      "label": "Count",
      "min": 1,
      "max": 10,
      "default": 1
    }
  ]
}
```

### 3. Execution Phase
```python
# User submits inputs → API validates → Modal runs container
POST /api/run
{
  "spec_name": "my-app",
  "inputs": {"prompt": "test", "count": 5}
}

# Returns:
{
  "job_id": "uuid",
  "status": "completed",
  "output_urls": ["https://s3.../output.png"]
}
```

## 📡 API Endpoints

### `POST /api/parse`
Upload a `runme.md` file, get parsed spec + UI config

### `POST /api/run`
Execute a job with user inputs

### `GET /api/specs`
List all available specs

### `GET /api/jobs/{job_id}`
Check job status

## 🔧 Project Structure

```
ai-devops-runner/
├── backend/
│   ├── app/
│   │   ├── main.py              # FastAPI app
│   │   ├── agents/
│   │   │   ├── runme_parser.py  # Claude parser
│   │   │   └── modal_runner.py  # Modal orchestration
│   │   ├── models/
│   │   │   └── schemas.py       # Pydantic models
│   │   └── services/
│   ├── test_parser.py           # Test the parser
│   ├── requirements.txt
│   └── .env.example
├── frontend/                     # Coming soon!
│   └── (Next.js app)
└── examples/
    └── runme.md                  # Example specification
```

## 🎯 Current Status

✅ **Completed:**
- runme.md specification format
- Claude AI parser agent
- Pydantic models for type safety
- FastAPI backend structure
- Input validation
- Command builder
- Modal.com integration skeleton

🚧 **In Progress:**
- Modal.com actual execution
- S3 output handling
- GitHub integration

📋 **Next Steps:**
1. Build the Next.js frontend
2. Real Modal.com deployment
3. GitHub repo fetching
4. WebSocket for streaming logs
5. User authentication

## 🤝 Contributing

Want to help? Here are some ideas:
- Add support for more input types (file uploads, etc.)
- Build the frontend UI
- Add real-time log streaming
- Implement job queuing
- Add support for private repos
- Create example runme.md files for popular tools

## 🎓 Examples

Check out `examples/runme.md` for a Stable Diffusion example!

## 📄 License

MIT

## 🙏 Acknowledgments

- Inspired by Modal.com's incredible platform
- Built with Claude AI
- FastAPI for the backend
- Next.js for the frontend (coming soon!)

---

**Built with ❤️ and AI**

Ready to turn any repo into a production app? Let's go! 🚀