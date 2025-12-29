# Simple Hello World

## Project Info
- **name**: hello-world
- **description**: A simple hello world example to test the system
- **version**: 1.0.0

## Container
- **image**: python:3.11-slim
- **working_dir**: /app

## Compute Requirements
- **cpu**: 1
- **memory**: 1GB
- **gpu**: none
- **timeout**: 60

## Inputs

1. **name** (required)
   - type: string
   - description: Your name to say hello to
   - example: "World"

2. **count** (optional)
   - type: integer
   - description: How many times to say hello
   - min: 1
   - max: 10
   - default: 1

3. **enthusiastic** (optional)
   - type: boolean
   - description: Add extra exclamation marks
   - default: false

## Command
```bash
python -c "
name = '{name}'
count = {count}
enthusiastic = {enthusiastic}
exclaim = '!!!' if enthusiastic else '!'
for i in range(count):
    print(f'Hello, {{name}}{{exclaim}}')
"
```

## Outputs
- **location**: /outputs
- **type**: stdout
- **mount_to_s3**: false
