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
![alt text](/readme_demo.jpg)

## Installation

### 1. Clone Repository
git clone https://github.com/dadaocao/ai-music-generator.git

### 2. Backend Configurations

```sh
cd backend
pip install flask flask-cors transformers torch scipy
python app.py
```

### 3. Frontend Configurations:

```sh
cd ai-music-frontend
npm install
npm start
```
Open your browser and go to  http://localhost:3000

## App Usage
1. Enter your desired parameters in the input box, or leave them blank if not needed.
2. Click "Generate Lyrics" to display the output editor on the right.
3. Once the AI finishes generating the lyrics, you can edit them directly in the editor.
4. Use the first button in the bottom-right corner to copy the text and the second button to export it as a PDF.

## License
[MIT License](./LICENSE)
