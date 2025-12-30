# Python Simple Test

## Project Info
- **name**: python-simple
- **description**: Simple Python test
- **version**: 1.0.0

## Container
- **image**: python:3.12-slim
- **working_dir**: /tmp

## Compute Requirements
- **cpu**: 1
- **memory**: 512MB
- **gpu**: none
- **timeout**: 60

## Inputs

1. **message** (required)
   - type: string
   - description: Message to print
   - example: "Hello World"

2. **repeat** (optional)
   - type: integer
   - description: How many times to repeat
   - min: 1
   - max: 5
   - default: 1

## Command
```bash
for i in $(seq 1 {repeat}); do echo "{message}"; done
```

## Outputs
- **location**: /outputs
- **type**: stdout
- **mount_to_s3**: false
