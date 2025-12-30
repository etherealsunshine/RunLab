# 🆓 FREE Setup Guide - No Anthropic Key Needed!

You can use RunLab completely FREE with Hugging Face + Modal!

## Step 1: Get a FREE Hugging Face API Key (2 minutes)

1. Go to https://huggingface.co/
2. Click "Sign Up" (it's free!)
3. Verify your email
4. Go to https://huggingface.co/settings/tokens
5. Click "New token"
   - Name: `runlab`
   - Type: `Read`
6. Copy the token (starts with `hf_...`)

## Step 2: Set Up Your Environment

```bash
cd backend

# Create .env file
cp .env.example .env

# Edit .env and add your token
echo "HUGGINGFACE_API_KEY=hf_your_token_here" >> .env
```

Or export it:
```bash
export HUGGINGFACE_API_KEY=hf_your_token_here
```

## Step 3: Install Dependencies

```bash
pip install -r requirements.txt
```

## Step 4: Test It!

```bash
# Test the parser
python test_parser.py

# Start the server
uvicorn app.main:app --reload
```

Visit http://localhost:8000/docs and you're ready! 🎉

---

## 🚀 Now Let's Set Up Modal (Also FREE to Start!)

Modal has a generous free tier that's perfect for testing!

### 1. Sign Up for Modal

```bash
# Install Modal
pip install modal

# Create account and authenticate (opens browser)
modal setup
```

This will:
1. Open your browser to create a Modal account
2. Authenticate your CLI
3. Create a free workspace

### 2. Test Modal

Let's create a simple test to make sure Modal works:

```bash
# Create a test file
cat > test_modal.py << 'EOF'
import modal

app = modal.App("test")

@app.function()
def hello(name: str):
    return f"Hello {name} from Modal!"

@app.local_entrypoint()
def main():
    result = hello.remote("RunLab")
    print(result)
EOF

# Run it!
modal run test_modal.py
```

You should see: `Hello RunLab from Modal!` ✅

### 3. Enable Real Execution in RunLab

Edit [backend/app/main.py](backend/app/main.py#L57):

```python
# Change this line:
runner = ModalRunner(mock_mode=True)

# To this:
runner = ModalRunner(mock_mode=False)
```

That's it! Now your jobs will actually run on Modal! 🎊

---

## 🎯 What You Get for FREE

### Hugging Face Free Tier:
- ✅ Unlimited API calls to inference API
- ✅ Access to thousands of open source models
- ✅ No credit card required
- ⚠️ Rate limits: ~60 requests/minute (plenty for development!)

**Recommended Models** (all free):
- `meta-llama/Llama-3.2-3B-Instruct` - Fast, good quality (default)
- `mistralai/Mistral-7B-Instruct-v0.3` - Better quality, slower
- `microsoft/Phi-3-mini-4k-instruct` - Very fast, decent quality

### Modal Free Tier:
- ✅ $30/month free credits
- ✅ CPU: 50 free hours/month
- ✅ Full GPU access (uses credits)
- ✅ No credit card required to start
- ✅ Access to A10G, T4, and other GPUs

**What $30 gets you** (approximate):
- ~150 hours of CPU time
- ~30 hours of T4 GPU
- ~10 hours of A10G GPU
- Perfect for testing and small projects!

---

## 🔧 Troubleshooting

### Hugging Face Issues

**"Model is loading"**
```
The first request might take 30-60 seconds while the model loads.
Just wait and try again!
```

**Rate limit errors**
```
Free tier has ~60 requests/minute limit.
Wait a minute and try again.
```

**Model not found**
```
Make sure you're using one of the recommended models.
Check https://huggingface.co/models for available models.
```

### Modal Issues

**"Not authenticated"**
```bash
modal setup  # Run this again
```

**"Insufficient credits"**
```
Check your usage at: https://modal.com/settings/billing
Free tier resets monthly!
```

**Import errors**
```bash
pip install --upgrade modal
```

---

## 🎨 Switching Models

Want to try a different Hugging Face model? Easy!

Edit [backend/app/agents/huggingface_parser.py](backend/app/agents/huggingface_parser.py#L12):

```python
# Default:
parser = HuggingFaceParser(model="meta-llama/Llama-3.2-3B-Instruct")

# Try Mistral (better quality):
parser = HuggingFaceParser(model="mistralai/Mistral-7B-Instruct-v0.3")

# Or Phi-3 (faster):
parser = HuggingFaceParser(model="microsoft/Phi-3-mini-4k-instruct")
```

---

## 📊 Cost Comparison

| Service | Free Tier | Paid | Best For |
|---------|-----------|------|----------|
| **Hugging Face** | ✅ Unlimited (rate limited) | - | Development & Testing |
| **Modal** | ✅ $30/month credits | $0.0001/CPU-sec | Testing & Small Projects |
| **Anthropic Claude** | ❌ No free tier | ~$3/million tokens | Production (if you have key) |

**For your use case**: Hugging Face + Modal free tiers are perfect! 🎉

---

## 🚀 Quick Start Summary

```bash
# 1. Get Hugging Face token
# → https://huggingface.co/settings/tokens

# 2. Set up environment
cd backend
echo "HUGGINGFACE_API_KEY=hf_xxx" >> .env

# 3. Install & test
pip install -r requirements.txt
python test_parser.py

# 4. Start server
uvicorn app.main:app --reload

# 5. Set up Modal (optional)
pip install modal
modal setup

# 6. Enable real execution
# Edit app/main.py: mock_mode=False

# 7. You're done! 🎉
```

---

## 🎓 Next Steps

1. ✅ **Test with examples** - Try the example runme.md files
2. ✅ **Create your own** - Write a custom runme.md
3. ✅ **Build a frontend** - Create a UI for your API
4. ✅ **Deploy** - Use Modal for production

---

**Everything is FREE to start! No credit card needed! 🎊**

Questions? The Hugging Face model might not be as good as Claude for complex parsing, but it works great for simple runme.md files!

If parsing quality is an issue, you can:
1. Use a bigger model (Mistral-7B)
2. Simplify your runme.md format
3. Add few-shot examples to the prompt
4. Eventually upgrade to Claude if needed
