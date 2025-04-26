from datasets import load_dataset
import os

# Ensure the output directory exists
output_dir = "sample_transcripts"
os.makedirs(output_dir, exist_ok=True)

# Load 2 examples
dataset = load_dataset('jlh-ibm/earnings_call', split='train[:10]')

for i, example in enumerate(dataset):
    # Assuming text is in 'raw_text' field - verify the field name if needed
    print(example)
    transcript_text = example.get('text', '')
    if transcript_text:
        file_path = os.path.join(output_dir, f"huggingface_sample_{i+1}.txt")
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(transcript_text)
        print(f"Saved sample to {file_path}")
    else:
        print(f"Warning: Could not find 'raw_text' in example {i}")
