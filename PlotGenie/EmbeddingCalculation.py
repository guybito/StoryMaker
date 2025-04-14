import os
import json
from sentence_transformers import SentenceTransformer

model = SentenceTransformer('all-MiniLM-L6-v2')
genres = ['Romance', 'Adventure', 'Mystery', 'Comedy', 'Dramatic']
input_files = ['cleaned_Climaxes_Surprise_Twists.json', 'cleaned_Complications.json', 'cleaned_Crises.json', 'cleaned_Locale.json'
               ,'cleaned_Obstacles_To_Love.json', 'cleaned_Predicaments.json', 'cleaned_Problems_1.json', 'cleaned_Problems_2.json',
               'cleaned_Problems_3.json', 'cleaned_Problems_4.json', 'cleaned_Problems_5.json', 'cleaned_Problems_6.json',
               'cleaned_Unusual_Female_Characters.json', 'cleaned_Unusual_Male_Characters.json', 'cleaned_Usual_Female_Characters.json',
               'cleaned_Usual_Male_Characters.json']
input_dir = 'Utils'
output_dir = 'with_embeddings'
os.makedirs(output_dir, exist_ok=True)
for filename in input_files:
    input_path = os.path.join(input_dir, filename)
    print(f"Processing {input_path}...")

    # Load data
    with open(input_path, 'r') as f:
        lines = json.load(f)

    # Generate embeddings
    embeddings = model.encode(lines, convert_to_tensor=True, show_progress_bar=True)

    # Combine text and embedding
    output_data = [
        {"text": text, "embedding": embedding.tolist()}
        for text, embedding in zip(lines, embeddings)
    ]

    # Save to new JSON file
    output_filename = filename.replace('.json', '_with_embeddings.json')
    output_path = os.path.join(output_dir, output_filename)

    with open(output_path, 'w') as f:
        json.dump(output_data, f, indent=2)

    print(f"Saved: {output_path}")

embeddings = model.encode(genres, convert_to_tensor=True, show_progress_bar=True)

# Combine genre and its embedding
output_data = [
    {"text": genre, "embedding": embedding.tolist()}
    for genre, embedding in zip(genres, embeddings)
]

# Save to JSON
output_dir = 'with_embeddings'
os.makedirs(output_dir, exist_ok=True)
output_path = os.path.join(output_dir, 'genres_with_embeddings.json')

with open(output_path, 'w') as f:
    json.dump(output_data, f, indent=2)

print(f"Saved: {output_path}")