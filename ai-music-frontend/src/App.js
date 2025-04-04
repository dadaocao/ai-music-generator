import React, { useState } from 'react';
import { Sparkles, Music } from 'lucide-react';

const LyricsGenerator = () => {
  const [form, setForm] = useState({
    artist: '',
    title: '',
    music_style: '',
    theme: '',
    emotion: '',
    structure: '',
    length: '',
  });

  const [lyrics, setLyrics] = useState('');
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState('');

  const handleInputChange = (e) => {
    const { name, value } = e.target;
    setForm({
      ...form,
      [name]: value,
    });
  };

  const generateContent = async () => {
    setIsLoading(true);
    setError('');

    try {
      const response = await fetch('http://127.0.0.1:5000/generate-content', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(form), // 直接发送整个表单
      });

      if (!response.ok) {
        throw new Error('Failed to generate content');
      }

      const data = await response.json();
      setLyrics(data.lyrics);
      console.log('Generated music:', data.music);
    } catch (err) {
      setError('Error generating content. Please try again.');
      console.error('Error:', err);
    } finally {
      setIsLoading(false);
    }
  };


  return (
    <div className="max-w-7xl mx-auto min-h-screen p-6 mt-28 pb-20">
      <div className="flex flex-col items-center mb-12">
        <h1 className="text-5xl font-bold text-gray-800">AI Lyrics & Music Generator</h1>
        <h3 className="text-xl font-bold text-gray-400 mt-4">Create your customized lyrics and accompaniment!</h3>
      </div>

      <div className="grid grid-cols-2 gap-8">
        {/* Input Form */}
        <div>
          <h2 className="text-xl font-bold text-gray-700 mb-4">Generate Lyrics & Music</h2>
          <input
            type="text"
            name="artist"
            value={form.artist}
            onChange={handleInputChange}
            placeholder="Artist (e.g. Taylor Swift, BTS)"
            className="w-full p-3 border rounded-lg mb-4"
          />
          <input
            type="text"
            name="title"
            value={form.title}
            onChange={handleInputChange}
            placeholder="Title (e.g. Love Story)"
            className="w-full p-3 border rounded-lg mb-4"
          />
          <input
            type="text"
            name="music_style"
            value={form.music_style}
            onChange={handleInputChange}
            placeholder="Music Style (e.g. Pop, Rock)"
            className="w-full p-3 border rounded-lg mb-4"
          />
          <input
            type="text"
            name="theme"
            value={form.theme}
            onChange={handleInputChange}
            placeholder="Theme (e.g. Love, Journey)"
            className="w-full p-3 border rounded-lg mb-4"
          />
          <input
            type="text"
            name="emotion"
            value={form.emotion}
            onChange={handleInputChange}
            placeholder="Emotion (e.g. Happy, Sad)"
            className="w-full p-3 border rounded-lg mb-4"
          />
          <input
            type="text"
            name="structure"
            value={form.structure}
            onChange={handleInputChange}
            placeholder="Structure (e.g. Verse-Chorus-Verse)"
            className="w-full p-3 border rounded-lg mb-4"
          />
          <input
            type="text"
            name="length"
            value={form.length}
            onChange={handleInputChange}
            placeholder="Length (e.g. 3 minutes)"
            className="w-full p-3 border rounded-lg mb-4"
          />
        </div>
      </div>

      {/* Generate Button */}
      <div className="flex justify-center mt-8">
        <button
          onClick={generateContent}
          disabled={isLoading}
          className="px-8 py-3 bg-green-500 text-white rounded-lg w-full max-w-xs flex items-center justify-center"
        >
          {isLoading ? 'Generating...' : 'Generate Lyrics & Music'}
          {!isLoading && <Sparkles className="w-5 h-5 ml-2" />}
        </button>
      </div>

      {/* Error Message */}
      {error && <div className="mt-4 text-center text-red-500">{error}</div>}

      {lyrics && (
        <div
          style={{
            maxHeight: '300px', // 设置最大高度
            overflowY: 'auto', // 启用上下滑动条
            padding: '1rem',
            borderRadius: '0.5rem',
            backgroundColor: '#f9fafb',
          }}
        >
          <h3
            style={{
              fontSize: '1.25rem',
              fontWeight: 'bold',
              color: '#4b5563',
              marginBottom: '0.5rem',
            }}
          >
            Generated Lyrics:
          </h3>
          <pre
            style={{
              whiteSpace: 'pre-wrap', // 保持文本格式
              color: '#1f2937',
            }}
          >
            {lyrics}
          </pre>
        </div>
      )}


    </div>
  );
};

export default LyricsGenerator;