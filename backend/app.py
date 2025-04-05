from flask import Flask, request, jsonify
from transformers import GPT2LMHeadModel, AutoTokenizer, AutoProcessor, MusicgenForConditionalGeneration
import torch
import scipy.io.wavfile
import numpy as np
import logging
from flask_cors import CORS
import os
import base64
import time
import zipfile

app = Flask(__name__)
CORS(app)

# extact the model
model_dir = "../my_lyrics_model"
zip_path = "../../../../my_lyrics_model-20250403T000854Z-001.zip"

if not os.path.exists(model_dir):
    with zipfile.ZipFile(zip_path, "r") as zip_ref:
        zip_ref.extractall(model_dir)

# load models
device = "cuda" if torch.cuda.is_available() else "cpu"
tokenizer = AutoTokenizer.from_pretrained(model_dir)
lyrics_model = GPT2LMHeadModel.from_pretrained(model_dir).to(device)

processor = AutoProcessor.from_pretrained("facebook/musicgen-small")
music_model = MusicgenForConditionalGeneration.from_pretrained("facebook/musicgen-small").to(device)


def generate_lyrics(prompt, max_length=250, temperature=0.8):
    inputs = tokenizer(prompt, return_tensors="pt").to(device)

    with torch.no_grad():
        output = lyrics_model.generate(
            **inputs,
            max_length=max_length,
            temperature=temperature,
            top_k=50,
            top_p=0.95,
            do_sample=True
        )

    generated_text = tokenizer.decode(output[0], skip_special_tokens=True)
    return generated_text.replace(prompt, "").strip()


def generate_music_audio(des):
    print("Generating music...")
    start_time = time.time()

    # Input preprocessing
    inputs = processor(text=[des], padding=True, return_tensors="pt").to(music_model.device)

    # Model generation
    with torch.no_grad():
        audio_tokens = music_model.generate(
            **inputs,
            max_new_tokens=512,
            do_sample=True,
            temperature=1.2,
            top_k=50,
            top_p=0.95
        )

    print(f"Music generated in {time.time() - start_time:.2f} seconds")

    # Tensor processing
    if isinstance(audio_tokens, torch.Tensor):
        audio_array = audio_tokens[0].cpu().numpy()
    else:
        raise TypeError("Unexpected type for audio_tokens")

    if audio_array.size == 0:
        raise ValueError("Generated audio is empty")

    # Audio post-processing
    audio_array = np.clip(audio_array, -1.0, 1.0)
    if len(audio_array.shape) > 1:
        audio_array = np.mean(audio_array, axis=0)

    scaled_audio = (audio_array * 32767).astype(np.int16)
    sampling_rate = min(max(getattr(music_model.config, "sampling_rate", 32000), 1), 65535)

    # Write to WAV file
    save_path = os.path.join(os.getcwd(), "generated_music.wav")
    scipy.io.wavfile.write(save_path, rate=sampling_rate, data=scaled_audio)

    # Encode to Base64
    with open(save_path, 'rb') as f:
        wav_data = f.read()

    return base64.b64encode(wav_data).decode('utf-8'), sampling_rate



@app.route('/generate-content', methods=['POST'])
def generate_content():
    try:
        data = request.json
        music_style = data.get("music_style", "pop")
        theme = data.get("theme", "love")
        emotion = data.get("emotion", "happy")
        structure = data.get("structure", "Verse-Chorus")

        prompt = f"Write a {emotion} {music_style} song about {theme}. Structure: {structure}. Here are the lyrics:\n\n[Verse 1]"

        print("Generating lyrics...")
        lyrics = generate_lyrics(prompt)
        print("Lyrics generated.")

        return jsonify({
            "lyrics": lyrics
        })

    except Exception as e:
        logging.exception("Error in generate-content:")
        return jsonify({"error": str(e)}), 500


@app.route('/generate-music', methods=['POST'])
def generate_music():
    try:
        data = request.json
        des = data.get("des", "")

        if not des:
            return jsonify({"error": "Missing music description"}), 400

        audio_base64, sampling_rate = generate_music_audio(des)
        return jsonify({
            "audio_data_base64": audio_base64,
            "sampling_rate": sampling_rate
        })

    except Exception as e:
        logging.exception("Error in generate-music:")
        return jsonify({"error": str(e)}), 500

        
if __name__ == '__main__':
    app.run(debug=True, port=5000, threaded=True)
