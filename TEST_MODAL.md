# 🚀 Testing Modal with RunLab

## Step-by-Step Testing Guide

### 1. Install Modal

```bash
cd backend
pip install modal
```

### 2. Authenticate Modal

```bash
modal setup
```

This opens your browser - just follow the prompts to create a FREE account!

### 3. Test Modal Works Standalone

```bash
cd ..  # back to RunLab root
python3 test_modal_quick.py
```

Expected output:
```
Testing Modal connection...
✅ Initialized. View run at https://modal.com/...
Running on Modal cloud!
✅ Success! Result: Hello RunLab from Modal! 🚀

Modal is working! Ready to enable in RunLab!
```

### 4. Enable Real Modal Execution

Edit `backend/app/main.py` line 57:

**Change this:**
```python
runner = ModalRunner(mock_mode=True)  # Start in mock mode
```

**To this:**
```python
runner = ModalRunner(mock_mode=False)  # Enable real execution! 🚀
```

### 5. Restart Your API Server

```bash
cd backend
# Stop the server (Ctrl+C if running)
uvicorn app.main:app --reload
```

### 6. Test Through the API!

Open another terminal and run:

```bash
cd backend
python3 test_api.py
```

Or manually test in your browser at http://localhost:8000/docs:

#### A. Parse a runme.md file

Click `POST /api/parse/file`, upload `examples/simple-hello.runme.md`

#### B. Run a job (now on real Modal!)

Click `POST /api/run` and use:

```json
{
  "spec_name": "hello-world",
  "inputs": {
    "name": "Modal Cloud",
    "count": 3,
    "enthusiastic": true
  }
}
```

This will **actually run on Modal's infrastructure**! 🎉

### 7. Check Modal Dashboard

Go to https://modal.com/apps to see your running jobs!

---

## Troubleshooting

### "ModuleNotFoundError: No module named 'modal'"
```bash
pip install modal
# or
pip3 install modal
```

### "Not authenticated"
```bash
modal setup
```

### "Insufficient credits"
Check your free tier at https://modal.com/settings/billing
(You get $30/month FREE!)

### Modal runs but gets errors
Check the logs at https://modal.com/apps
The error messages will tell you what's wrong

---

## What Happens When You Run a Job

1. **You submit** via API: `POST /api/run`
2. **RunLab** validates your inputs
3. **RunLab** builds the command
4. **RunLab** creates a Modal function dynamically
5. **Modal** spins up a container in the cloud
6. **Modal** executes your command
7. **Modal** captures the output
8. **RunLab** returns the results to you

All in a few seconds! ⚡

---

## Example: Full Test

```bash
# 1. Parse the simple example
curl -X POST http://localhost:8000/api/parse/file \
  -F "file=@examples/simple-hello.runme.md"

# 2. Run it on Modal!
curl -X POST http://localhost:8000/api/run \
  -H "Content-Type: application/json" \
  -d '{
    "spec_name": "hello-world",
    "inputs": {
      "name": "RunLab User",
      "count": 5,
      "enthusiastic": true
    }
  }'

# You'll get back a job_id and status!
```

---

## Next: Try GPU Execution

Once basic execution works, try the GPU example:

```bash
# Parse the Stable Diffusion example
curl -X POST http://localhost:8000/api/parse/file \
  -F "file=@examples/stable-diffusion.runme.md"

# Run with GPU! (uses your free credits)
curl -X POST http://localhost:8000/api/run \
  -H "Content-Type: application/json" \
  -d '{
    "spec_name": "stable-diffusion-xl",
    "inputs": {
      "prompt": "A beautiful sunset over mountains",
      "num_images": 1,
      "steps": 20
    }
  }'
```

This will run on an **A10G GPU** in the cloud! 🎮

---

## You're Ready! 🎉

✅ Hugging Face parser working (FREE)
✅ API server running
✅ Modal authenticated
✅ Ready for real cloud execution

**Total cost: Still $0!** (Modal free tier)

Go ahead and enable Modal, restart the server, and watch your code run in the cloud! 🚀
