"""Quick test to verify Modal is working"""
import modal

app = modal.App("runlab-test")

@app.function()
def hello(name: str):
    print(f"Running on Modal cloud!")
    return f"Hello {name} from Modal! 🚀"

@app.local_entrypoint()
def main():
    print("Testing Modal connection...")
    result = hello.remote("RunLab")
    print(f"✅ Success! Result: {result}")
    print("\nModal is working! Ready to enable in RunLab!")

if __name__ == "__main__":
    app.run()
