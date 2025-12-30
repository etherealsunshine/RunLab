# 👋 START HERE - Super Quick Setup!

## You Want FREE Everything? Let's Do It! 🎉

### Step 1: Get a FREE Hugging Face Token (2 mins)

1. Go here: https://huggingface.co/settings/tokens
2. Sign up (free!)
3. Click "New token" → Name it "runlab" → Create
4. Copy the token (starts with `hf_...`)

### Step 2: Set It Up (1 min)

```bash
cd backend

# Set your token
export HUGGINGFACE_API_KEY=hf_paste_your_token_here

# Install stuff
pip install -r requirements.txt
```

### Step 3: Test It! (30 seconds)

```bash
python test_hf_parser.py
```

You should see it parse an example file! ✅

### Step 4: Start the Server (10 seconds)

```bash
uvicorn app.main:app --reload
```

Visit: **http://localhost:8000/docs**

🎊 **YOU'RE DONE!** The backend is working!

---

## Now Let's Add Modal (Optional but Cool!)

### Step 1: Install Modal

```bash
pip install modal
```

### Step 2: Set Up Account (2 mins)

```bash
modal setup
```

This opens your browser to create a FREE Modal account (no credit card!).

### Step 3: Test It

```bash
# Quick test
cat > test.py << 'EOF'
import modal
app = modal.App("test")

@app.function()
def hello():
    return "Hello from Modal!"

@app.local_entrypoint()
def main():
    print(hello.remote())
EOF

modal run test.py
```

Should print: `Hello from Modal!` ✅

### Step 4: Enable in RunLab

Edit `backend/app/main.py` line 57:

```python
# Change this:
runner = ModalRunner(mock_mode=True)

# To this:
runner = ModalRunner(mock_mode=False)
```

Restart your server and now jobs run on real Modal cloud! 🚀

---

## 🎯 Quick Test

Open http://localhost:8000/docs

1. Click `POST /api/parse`
2. Click "Try it out"
3. Paste this:

```json
{
  "content": "# Test\n\n## Project Info\n- **name**: test\n- **description**: Test\n- **version**: 1.0.0\n\n## Container\n- **image**: python:3.11-slim\n- **working_dir**: /app\n\n## Compute Requirements\n- **cpu**: 1\n- **memory**: 1GB\n- **gpu**: none\n- **timeout**: 60\n\n## Inputs\n\n1. **msg** (required)\n   - type: string\n   - description: Message\n\n## Command\n```bash\necho '{msg}'\n```\n\n## Outputs\n- **location**: /outputs\n- **type**: stdout\n- **mount_to_s3**: false"
}
```

4. Click Execute

You should see parsed JSON! 🎉

5. Now click `POST /api/run`
6. Paste:

```json
{
  "spec_name": "test",
  "inputs": {
    "msg": "Hello RunLab!"
  }
}
```

7. Execute

You get a job result! If Modal is enabled, it actually ran in the cloud! ☁️

---

## 📚 More Info

- **FREE Setup**: See [SETUP_FREE.md](SETUP_FREE.md)
- **Modal Setup**: See [MODAL_SETUP.md](MODAL_SETUP.md)
- **Full Guide**: See [QUICKSTART.md](QUICKSTART.md)
- **API Docs**: http://localhost:8000/docs (when server is running)

---

## ❓ Questions?

**Parser not working?**
- Make sure you set `HUGGINGFACE_API_KEY`
- First request takes 30-60 seconds (model loading)
- Free tier: ~60 requests/minute

**Modal not working?**
- Run `modal setup` again
- Check `modal token current`

**Server won't start?**
- Make sure you're in `backend/` directory
- Try `pip install -r requirements.txt` again

---

## 🎉 That's It!

You now have:
- ✅ FREE AI parser (Hugging Face)
- ✅ FREE cloud execution (Modal)
- ✅ Working API
- ✅ Example runme.md files

**Total cost: $0** 🎊

Next step: Build a frontend or create your own runme.md files!

---

**Stuck? Check the other guides in this repo!**

- Too long to read? This file is your friend!
- Want details? Check SETUP_FREE.md
- Need help with Modal? See MODAL_SETUP.md
- General questions? See README.md
