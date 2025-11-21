from vllm import LLM, SamplingParams
from PIL import Image
import requests
from io import BytesIO

# 1. Define model path and load the model
model_path = "ibm-granite/granite-vision-3.3-2b"
model = LLM(model=model_path) # You may need to specify revision="untied" or dtype="float32" based on hardware

# 2. Define sampling parameters
sampling_params = SamplingParams(
    temperature=0.2,
    max_tokens=64,
)

# 3. Load the image (can be a local path or URL)
image_path = "notebooks/data/DENVER-25CAP-00000-04SUF-ID.jpeg" # Replace with your JPEG file path
try:
    image = Image.open(image_path)
except FileNotFoundError:
    print(f"Error: The file '{image_path}' was not found.")
    exit()

# 4. Format the prompt with the image placeholder
image_token = "<image>"
system_prompt = "<|system|>\nA chat between a curious user and an artificial intelligence assistant."
user_prompt = "Describe the image in detail." # Your specific task here

full_prompt = f"{system_prompt}\n<|user|>\n{image_token}\n{user_prompt}<|end_of_user|>\n<|assistant|>"

# 5. Generate the output
outputs = model.generate(
    inputs=[full_prompt],
    sampling_params=sampling_params,
    images=[image]
)

# 6. Print the generated text
for output in outputs:
    print(f"Generated text: {output.outputs[0].text}")