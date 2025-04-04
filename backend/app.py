# 04.03
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

# **解压模型**
model_dir = "../my_lyrics_model"
zip_path = "../../../../my_lyrics_model-20250403T000854Z-001.zip"

if not os.path.exists(model_dir):
    with zipfile.ZipFile(zip_path, "r") as zip_ref:
        zip_ref.extractall(model_dir)

# **加载自训练的歌词生成模型**
device = "cuda" if torch.cuda.is_available() else "cpu"
tokenizer = AutoTokenizer.from_pretrained(model_dir)
lyrics_model = GPT2LMHeadModel.from_pretrained(model_dir).to(device)

# **加载音乐生成模型**
processor = AutoProcessor.from_pretrained("facebook/musicgen-small")
music_model = MusicgenForConditionalGeneration.from_pretrained("facebook/musicgen-small").to(device)


def generate_lyrics(prompt, max_length=250, temperature=0.8):
    """ 生成歌词文本 """
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
    """ 生成音乐音频数据并返回 base64 编码 """
    print("Generating music...")
    start_time = time.time()

    inputs = processor(text=[des], padding=True, return_tensors="pt").to(music_model.device)

    with torch.no_grad():
        audio_tokens = music_model.generate(
            **inputs,
            max_new_tokens=512,
            do_sample=True,
            temperature=1.2,
            top_k=50,
            top_p=0.95
        )

    end_time = time.time()
    print(f"Music generated in {end_time - start_time:.2f} seconds")

    # **确保 `audio_tokens` 是可解码的**
    if isinstance(audio_tokens, torch.Tensor):
        audio_tokens = audio_tokens.cpu().numpy()

    if audio_tokens.size == 0:
        raise ValueError("Generated audio is empty")

    # **采样率处理**
    sampling_rate = getattr(music_model.config, "sampling_rate", 32000)
    sampling_rate = min(max(sampling_rate, 1), 65535)

    # **转换成 16-bit PCM**
    audio_array = np.clip(audio_tokens, -1.0, 1.0)
    if len(audio_array.shape) > 1:
        audio_array = np.mean(audio_array, axis=0)
    scaled_audio = (audio_array * 32767).astype(np.int16)

    # **保存到文件**
    save_directory = os.path.join(os.getcwd(), "generated_music.wav")
    scipy.io.wavfile.write(save_directory, rate=sampling_rate, data=scaled_audio)

    # **转换为 base64**
    with open(save_directory, 'rb') as f:
        wav_data = f.read()
    return base64.b64encode(wav_data).decode('utf-8'), sampling_rate


@app.route('/generate-content', methods=['POST'])
def generate_content():
    """ 统一接口：同时生成歌词和音乐 """
    try:
        data = request.json
        music_style = data.get("music_style", "pop")
        theme = data.get("theme", "love")
        emotion = data.get("emotion", "happy")

        prompt = f"Write a {emotion} {music_style} song about {theme}. Here are the lyrics:\n\n[Verse 1]"

        print("Generating lyrics...")
        start_time = time.time()
        lyrics = generate_lyrics(prompt)
        end_time = time.time()
        print(f"Lyrics generated in {end_time - start_time:.2f} seconds")

        # **生成音乐**
        music_desc = f"A {emotion} {music_style} instrumental inspired by {theme}"
        # audio_base64, sampling_rate = generate_music_audio(music_desc)

        return jsonify({
            "lyrics": lyrics,
            # "music": {
            #     "sampling_rate": sampling_rate,
            #     "audio_data_base64": audio_base64
            # }
        })

    except Exception as e:
        logging.exception("Error in generate-content:")
        return jsonify({"error": str(e)}), 500


if __name__ == '__main__':
    app.run(debug=True, port=5000, threaded=True)