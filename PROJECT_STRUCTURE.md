# RunLab Project Structure

```
RunLab/
├── 📄 README.md                    # Main documentation
├── 📄 QUICKSTART.md                # 5-minute getting started guide
├── 📄 PROJECT_STRUCTURE.md         # This file
├── 🔧 setup.sh                     # Automated setup script
├── 📄 pyproject.toml               # Root project config
├── 📄 main.py                      # Simple test file
│
├── 📁 backend/                     # FastAPI Backend
│   ├── 📄 requirements.txt         # Python dependencies
│   ├── 📄 .env.example             # Environment variable template
│   ├── 📄 .gitignore               # Git ignore rules
│   ├── 🧪 test_parser.py           # Test Claude parser
│   ├── 🧪 test_api.py              # Test API endpoints
│   │
│   └── 📁 app/                     # Main application
│       ├── 📄 __init__.py
│       ├── 🚀 main.py              # FastAPI app entry point
│       │
│       ├── 📁 models/              # Pydantic data models
│       │   ├── 📄 __init__.py
│       │   └── 📄 schemas.py       # All schemas (RunmeSpec, UIConfig, etc.)
│       │
│       ├── 📁 agents/              # AI agents
│       │   ├── 📄 __init__.py
│       │   ├── 🤖 runme_parser.py  # Claude-powered parser
│       │   └── ☁️  modal_runner.py  # Modal.com orchestration
│       │
│       ├── 📁 api/                 # API routes (future)
│       └── 📁 services/            # Business logic (future)
│
├── 📁 examples/                    # Example runme.md files
│   ├── 📄 simple-hello.runme.md    # Simple hello world example
│   └── 📄 stable-diffusion.runme.md # Stable Diffusion example
│
└── 📁 frontend/                    # (Coming soon!)
    └── Next.js app for UI

```

## Key Files Explained

### Backend Core

- **[backend/app/main.py](backend/app/main.py)** - FastAPI application with all endpoints
  - `POST /api/parse` - Parse runme.md content
  - `POST /api/parse/file` - Upload and parse runme.md file
  - `POST /api/run` - Execute a job
  - `GET /api/specs` - List all specs
  - `GET /api/jobs/{job_id}` - Check job status

### AI Agents

- **[backend/app/agents/runme_parser.py](backend/app/agents/runme_parser.py)** - Claude parser
  - Parses runme.md files using Claude
  - Generates UI configurations
  - Validates user inputs
  - Builds executable commands

- **[backend/app/agents/modal_runner.py](backend/app/agents/modal_runner.py)** - Modal integration
  - Orchestrates container execution
  - Handles compute resources (CPU/GPU/Memory)
  - Manages job lifecycle
  - (Currently in mock mode)

### Data Models

- **[backend/app/models/schemas.py](backend/app/models/schemas.py)** - Pydantic models
  - `RunmeSpec` - Parsed specification
  - `UIConfig` - Generated UI configuration
  - `JobRequest` - Job submission request
  - `JobStatus` - Job execution status
  - And more...

### Testing

- **[backend/test_parser.py](backend/test_parser.py)** - Test the Claude parser
  - Load example runme.md
  - Parse with Claude
  - Validate inputs
  - Build commands

- **[backend/test_api.py](backend/test_api.py)** - Test API endpoints
  - Health check
  - Parse runme.md via API
  - Submit jobs
  - Check status

### Examples

- **[examples/simple-hello.runme.md](examples/simple-hello.runme.md)** - Basic example
  - String, integer, and boolean inputs
  - No GPU required
  - Simple Python command

- **[examples/stable-diffusion.runme.md](examples/stable-diffusion.runme.md)** - Advanced example
  - Multiple input types (string, int, float)
  - GPU requirement (A10G)
  - S3 output mounting

## What's Implemented ✅

1. **Complete Backend API** - FastAPI with all core endpoints
2. **Claude-Powered Parser** - Intelligently parses runme.md files
3. **Pydantic Models** - Type-safe data validation
4. **Modal.com Integration** - Ready for container execution
5. **Input Validation** - Automatic validation of user inputs
6. **Command Building** - Template substitution for commands
7. **Example Specs** - Two complete examples
8. **Test Scripts** - Comprehensive testing

## What's Next 🚧

1. **Frontend** - Next.js app with:
   - Dynamic form generation from UI config
   - File upload for runme.md
   - Real-time job status
   - Output display

2. **Real Modal Execution** - Switch from mock mode to actual execution

3. **S3 Integration** - Upload outputs to S3 and return URLs

4. **GitHub Integration** - Clone repos and auto-discover runme.md

5. **WebSocket Support** - Stream logs in real-time

6. **Authentication** - User accounts and API keys

## Development Workflow

```bash
# 1. Setup (one time)
./setup.sh

# 2. Test the parser
cd backend
python test_parser.py

# 3. Start API server
uvicorn app.main:app --reload

# 4. In another terminal, test the API
python test_api.py

# 5. Visit the docs
open http://localhost:8000/docs
```

## Architecture Flow

```
┌─────────────┐
│  User       │
└──────┬──────┘
       │
       ↓
┌─────────────────┐
│  Frontend       │  (Coming Soon!)
│  (Next.js)      │
└──────┬──────────┘
       │ HTTP
       ↓
┌─────────────────┐
│  FastAPI        │  ← You are here!
│  Backend        │
└──────┬──────────┘
       │
       ├─→ Claude API     (Parse runme.md)
       ├─→ Modal.com      (Execute containers)
       └─→ AWS S3         (Store outputs)
```

## File Sizes

- Total Python code: ~1,500 lines
- Models: ~200 lines
- Parser: ~300 lines
- Modal Runner: ~200 lines
- FastAPI App: ~250 lines
- Tests: ~550 lines

## Quick Reference

### Add a new endpoint
Edit [backend/app/main.py](backend/app/main.py:63)

### Add a new input type
Edit [backend/app/models/schemas.py](backend/app/models/schemas.py:14)

### Modify parsing logic
Edit [backend/app/agents/runme_parser.py](backend/app/agents/runme_parser.py:31)

### Change Modal execution
Edit [backend/app/agents/modal_runner.py](backend/app/agents/modal_runner.py:61)

### Create new example
Add to [examples/](examples/)

---

**Ready to build? Start with [QUICKSTART.md](QUICKSTART.md)!**
