# 🚀 Modal Setup Guide

Modal is awesome for running containers in the cloud with GPU support!

## Why Modal?

- ✅ $30/month FREE credits
- ✅ No credit card to start
- ✅ Auto-scaling
- ✅ GPU access (T4, A10G, A100, H100)
- ✅ Super fast cold starts
- ✅ Pay only for what you use

## Step 1: Install Modal

```bash
pip install modal
```

## Step 2: Create Account & Authenticate

```bash
modal setup
```

This will:
1. Open your browser
2. Ask you to create a Modal account (FREE!)
3. Authenticate your CLI
4. Create a workspace

**No credit card required!** 🎉

## Step 3: Test Modal

Let's make sure it works:

```bash
# Create a simple test
cat > test_modal.py << 'EOF'
import modal

app = modal.App("runlab-test")

@app.function()
def square(x: int):
    print(f"Computing {x}^2...")
    return x ** 2

@app.local_entrypoint()
def main():
    print("Testing Modal...")
    result = square.remote(10)
    print(f"Result: {result}")
    print("✅ Modal is working!")
EOF

# Run it!
modal run test_modal.py
```

You should see:
```
Computing 10^2...
Result: 100
✅ Modal is working!
```

## Step 4: Test with GPU

Let's test GPU access:

```bash
cat > test_modal_gpu.py << 'EOF'
import modal

app = modal.App("runlab-gpu-test")

@app.function(gpu="T4")
def check_gpu():
    import subprocess
    result = subprocess.run(["nvidia-smi"], capture_output=True, text=True)
    return result.stdout

@app.local_entrypoint()
def main():
    print("Testing GPU access...")
    output = check_gpu.remote()
    print(output)
    if "Tesla T4" in output or "T4" in output:
        print("✅ GPU is working!")
    else:
        print("⚠️  GPU might not be available")
EOF

modal run test_modal_gpu.py
```

## Step 5: Enable Real Execution in RunLab

Now that Modal is set up, let's enable it in RunLab!

Edit [backend/app/main.py](backend/app/main.py):

```python
# Find this line (around line 57):
runner = ModalRunner(mock_mode=True)

# Change it to:
runner = ModalRunner(mock_mode=False)
```

That's it! Now when you submit jobs through the API, they'll actually run on Modal! 🎊

## Step 6: Test RunLab with Real Modal Execution

```bash
# Start your API server
cd backend
uvicorn app.main:app --reload
```

Then in another terminal:

```bash
# Parse an example
curl -X POST http://localhost:8000/api/parse/file \
  -F "file=@../examples/simple-hello.runme.md"

# Run it on Modal!
curl -X POST http://localhost:8000/api/run \
  -H "Content-Type: application/json" \
  -d '{
    "spec_name": "hello-world",
    "inputs": {
      "name": "Modal Cloud",
      "count": 3,
      "enthusiastic": true
    }
  }'
```

Your code will run on Modal's cloud infrastructure! 🚀

---

## 🎯 Understanding Modal Execution

When you run a job with `mock_mode=False`, here's what happens:

1. **RunLab** receives your job request
2. **RunLab** creates a Modal function dynamically with:
   - Your specified container image
   - CPU/memory/GPU requirements
   - Command to execute
3. **Modal** spins up a container in the cloud
4. **Modal** runs your command
5. **Modal** sends back the output
6. **RunLab** returns the results to you

All this happens in seconds! ⚡

---

## 📊 Free Tier Limits

Modal's free tier includes:

- **$30/month** in free credits
- Credits reset monthly
- No credit card required to start

**What this gets you** (approximate):

| Resource | $/hour | Hours/$30 |
|----------|--------|-----------|
| CPU (1 core) | $0.0002 | ~150,000 hours 😱 |
| CPU (8 cores) | $0.0016 | ~18,750 hours |
| T4 GPU | $0.30 | ~100 hours |
| A10G GPU | $1.00 | ~30 hours |
| A100 GPU (40GB) | $3.00 | ~10 hours |

**For development**: The free tier is MORE than enough! 🎉

---

## 🔧 Troubleshooting

### "modal: command not found"
```bash
pip install --upgrade modal
```

### "Not authenticated"
```bash
modal setup
```

### "Insufficient credits"
Check your usage:
```bash
modal profile current
```

Or visit: https://modal.com/settings/billing

### Container fails to start
Check the logs in the Modal dashboard:
https://modal.com/apps

---

## 🎨 Advanced: Custom Container Images

Modal supports any Docker image! You can use:

```python
# Python with specific packages
modal.Image.debian_slim().pip_install("torch", "transformers")

# Custom Dockerfile
modal.Image.from_dockerfile("./Dockerfile")

# Pre-built images
modal.Image.from_registry("pytorch/pytorch:2.0.0-cuda11.7-cudnn8-runtime")
```

RunLab uses the image specified in your runme.md!

---

## 📚 Resources

- **Modal Docs**: https://modal.com/docs
- **Modal Examples**: https://github.com/modal-labs/modal-examples
- **Modal Discord**: https://discord.gg/modal
- **Pricing**: https://modal.com/pricing

---

## 🚀 Quick Reference

```bash
# Setup
modal setup

# Deploy an app
modal deploy app.py

# Run a function
modal run app.py

# View logs
modal logs app-name

# Check token
modal token current

# Check profile
modal profile current
```

---

## 🎓 What's Next?

Now that Modal is set up, you can:

1. ✅ **Run real workloads** - Your jobs execute on actual cloud infrastructure
2. ✅ **Use GPUs** - Specify `gpu: "T4"` in your runme.md
3. ✅ **Scale up** - Modal auto-scales based on demand
4. ✅ **Deploy** - Move from development to production seamlessly

**Modal + Hugging Face = Completely FREE development environment!** 🎊

---

## 💡 Pro Tips

1. **Start with CPU** - Test your code with CPU first, then add GPU
2. **Use smaller models** - For testing, use smaller/faster models
3. **Monitor credits** - Keep an eye on your free tier usage
4. **Cache images** - Modal caches container images for faster cold starts
5. **Use volumes** - For persistent data, use Modal volumes

---

**You're all set! Your RunLab setup is now complete!** 🎉

Everything is FREE:
- ✅ Hugging Face API (free tier)
- ✅ Modal execution ($30/month free credits)
- ✅ Open source everything else

**No credit card needed to start building!** 🚀
