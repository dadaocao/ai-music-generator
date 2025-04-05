import React, { useState } from 'react';
import { Sparkles } from 'lucide-react';
import MusicGenerator from './MusicGenerator';

const LyricsGenerator = () => {
  const [form, setForm] = useState({
    artist: '',
    title: '',
    music_style: '',
    theme: '',
    emotion: '',
    structure: '',
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
    setLyrics('');

    try {
      const response = await fetch('http://127.0.0.1:5000/generate-content', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(form),
      });

      if (!response.ok) {
        throw new Error('Failed to generate content');
      }

      const data = await response.json();
      setLyrics(data.lyrics);
    } catch (err) {
      setError('Error generating content. Please try again.');
      console.error('Error:', err);
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div className="fixed inset-0 overflow-y-auto">
      <div className="max-w-7xl mx-auto min-h-screen p-6 mt-28 pb-20">
        <div className="flex flex-col items-center mb-12">
          <h1 className="text-5xl font-bold text-gray-800">AI Lyrics & Music Generator</h1>
          <h3 className="text-xl font-bold text-gray-400 mt-4">Create your customized lyrics and accompaniment!</h3>
        </div>

        <div className="grid grid-cols-2 gap-8">
          <div>
            <h2 className="text-xl font-bold text-gray-700 mb-4">Generate Lyrics & Music</h2>
            {["artist: Taylor Swift, BTS", "title: Love Story", "music_style: Pop, R&B", "theme: Love, Friendship", "emotion: Happy, Sad", "structure: AABA"].map((field) => (
              <input
                key={field}
                type="text"
                name={field}
                value={form[field]}
                onChange={handleInputChange}
                placeholder={field.replace("_", " ").replace(/\b\w/g, l => l.toUpperCase())}
                className="w-full p-3 border rounded-lg mb-4"
              />
            ))}
          </div>
        </div>

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

        {error && <div className="mt-4 text-center text-red-500">{error}</div>}

        {lyrics && (
          <>
            {/* <div className="mt-8 p-4 rounded-md bg-gray-100">
            <h3 className="text-xl font-bold text-gray-700 mb-2">Generated Lyrics:</h3>
            <pre className="whitespace-pre-wrap text-gray-800">{lyrics}</pre>
          </div> */}
            <div
              style={{
                maxHeight: '300px',
                overflowY: 'auto',
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
                  whiteSpace: 'pre-wrap',
                  color: '#1f2937',
                }}
              >
                {lyrics}
              </pre>
            </div>

            <div className="mt-10">
              <MusicGenerator
                description={`A ${form.emotion} ${form.music_style} instrumental with ${form.structure.toLowerCase()} structure, inspired by ${form.theme}.`}
              />
            </div>
          </>
        )}
      </div>
    </div>
  );
};

export default LyricsGenerator;
