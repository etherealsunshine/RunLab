# Stable Diffusion Image Generator

## Project Info
- **name**: stable-diffusion-xl
- **description**: Generate high-quality images from text prompts using Stable Diffusion XL
- **version**: 1.0.0

## Container
- **image**: python:3.11-slim
- **working_dir**: /app

## Compute Requirements
- **cpu**: 4
- **memory**: 16GB
- **gpu**: A10G
- **timeout**: 600

## Inputs

1. **prompt** (required)
   - type: string
   - description: The text description of the image you want to generate
   - example: "A serene mountain landscape at sunset, with snow-capped peaks reflecting in a crystal clear lake"

2. **negative_prompt** (optional)
   - type: string
   - description: Things you don't want in the image
   - example: "blurry, low quality, distorted"
   - default: ""

3. **num_images** (optional)
   - type: integer
   - description: Number of images to generate
   - min: 1
   - max: 4
   - default: 1

4. **width** (optional)
   - type: integer
   - description: Image width in pixels
   - min: 512
   - max: 1024
   - default: 1024

5. **height** (optional)
   - type: integer
   - description: Image height in pixels
   - min: 512
   - max: 1024
   - default: 1024

6. **steps** (optional)
   - type: integer
   - description: Number of denoising steps (more steps = better quality but slower)
   - min: 20
   - max: 100
   - default: 50

7. **guidance_scale** (optional)
   - type: float
   - description: How closely to follow the prompt (higher = more literal)
   - min: 1.0
   - max: 20.0
   - default: 7.5

## Command
```bash
python generate.py \
  --prompt "{prompt}" \
  --negative_prompt "{negative_prompt}" \
  --num_images {num_images} \
  --width {width} \
  --height {height} \
  --steps {steps} \
  --guidance_scale {guidance_scale} \
  --output_dir /outputs
```

## Outputs
- **location**: /outputs
- **type**: files
- **mount_to_s3**: true
