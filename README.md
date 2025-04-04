# AI Lyrics Generator


This full-stack AI music platform combines a custom-trained lyric generation model with state-of-the-art music synthesis tools. The system features:

🧠 Custom AI Lyrics Engine
Our proprietary fine-tuned language model generates original song lyrics based on user prompts (artist or title), with real-time editing capabilities.

🎵 Intelligent Music Backing
Integrated third-party audio models transform lyrics into styled accompaniments matching user-selected genres.

🛠️ Full Creative Control

Lyrics Workshop: Edit generated text with syntax highlighting

Export options: PDF lyrics sheets / WAV audio downloads

Parameter tuning: BPM, key, instrumentation preferences

⚙️ Tech Stack
Flask backend (Python) + React frontend with seamless audio pipeline integration

## Developers

- **Ruoming Zhang**  
- **Sinian Liu**  
- **Yujing Liu**  
- **Xinyi Wei**  

## Requirements

- Python 
- Flask
- React
- Tailwind
- torch
- transformers
- Anything LLM
- scipy

## Preview
![image](https://github.com/user-attachments/assets/266e2205-b35d-43d9-afed-f543e32839e6)

## Installation
git clone https://github.com/MintFlavor23/ai-music-generator.git

### 2. Backend Requirements

### 1️⃣ Place your [app.py](backend/app.py) to your backend root directory
```sh
cd backend
```
### 2️⃣ Make sure you have the following dependencies installed:
```sh
pip install flask flask-cors transformers torch scipy
```
### 3️⃣ run flask server:
```sh
python app.py
```
>Dont forget to wait for debuger pin show up

### 4️⃣ Test the API using curl:
```sh
curl -X POST "http://127.0.0.1:5000/generate-lyrics" -H "Content-Type: application/json" -d "{\"music_style\": \"rock\", \"theme\": \"adventure\", \"length\": 250, \"emotion\": \"exciting\", \"structure\": \"verse-chorus-verse\"}"
```
### 5️⃣ Test the API using curl for music:
```sh
curl -X POST "http://127.0.0.1:5000/generate-music" -H "Content-Type: application/json" -d "{\"des\": \"Upbeat pop track with a driving beat and bright, uplifting chords. Inspired by modern synth-pop.\"}"
```
>[!NOTE]
>⚡Adjust the split to fill the needs:  
Feel free to change ***\n*** to any symbol to suit your needs
```
lines = generated_text.strip().split("\n")
```
### 3. Frontend Development Guide:

```sh
cd ai-music-frontend
npm install
npm start
```

Open your browser and go to  http://localhost:3000

### 1️⃣ Enter descriptions into the input boxes
```
const [formData, setFormData] = useState({
    music_style: "rock",
    theme: "adventure",
    length: 250,
    emotion: "exciting",
    structure: "verse-chorus-verse",
    acompaniment: "Upbeat pop track with a driving beat and bright, uplifting chords. Inspired by modern synth-pop."
});
```
### 2️⃣ Click 'generate Lyrics' button
Now wait for the output to show on the right side

### 4. Anything LLM
You need to prepare:
1. api_key
2. workspace
3. replace yours in the code
```sh
api_key = "5R2QZJF-ZMZ42BB-PKKFSQX-TCDB0TX"
workspace_id = "genm"
baseurl = "http://localhost:3001/api/v1"
chat_url = f"{baseurl}/workspace/{workspace_id}/chat" 
```

## App Usage
1. Enter your desired parameters in the input box, or leave them blank if not needed.
2. Click "Generate Lyrics" to display the output editor on the right.
3. Once the AI finishes generating the lyrics, you can edit them directly in the editor.
4. Use the first button in the bottom-right corner to copy the text and the second button to export it as a PDF.

## License
[MIT License](./LICENSE)
