# Super Simple Test

## Project Info
- **name**: test-simple
- **description**: Simplest possible test
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

## Command
```bash
echo "Message: {message}"
```

## Outputs
- **location**: /outputs
- **type**: stdout
- **mount_to_s3**: false
