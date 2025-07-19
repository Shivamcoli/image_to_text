import React, { useState, useEffect } from 'react';
import axios from 'axios';
import './App.css';

function App() {
  const [image, setImage] = useState(null);
  const [language, setLanguage] = useState('en');
  const [translatedText, setTranslatedText] = useState('');
  const [languages, setLanguages] = useState({});

  // Fetch languages on initial render
  useEffect(() => {
    axios.get('http://127.0.0.1:8000/languages')
      .then((res) => setLanguages(res.data))
      .catch((err) => console.error('Error loading languages:', err));
  }, []);

  const handleImageChange = (e) => {
    setImage(e.target.files[0]);
  };

  const handleLanguageChange = (e) => {
    setLanguage(e.target.value);
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    if (!image) return;

    const formData = new FormData();
    formData.append('file', image);
    formData.append('target_lang', language);  // ✅ MUST MATCH FastAPI parameter name


    try {
      const response = await axios.post('http://127.0.0.1:8000/translate', formData);
      setTranslatedText(response.data.translated_text);
    } catch (error) {
      console.error('Translation failed:', error);
    }
  };

  return (
    <div className="wrapper">
      <div className={translatedText ? 'split-layout' : 'center-layout'}>
        <div className="form-box">
          <h1 className="title">
            <img src="https://img.icons8.com/color/48/image.png" alt="icon" />
            Image to Text Translator
          </h1>
          <form onSubmit={handleSubmit}>
            <input type="file" accept="image/*" onChange={handleImageChange} />
            <label>Target Language:</label>
            <select value={language} onChange={handleLanguageChange}>
              {Object.entries(languages).map(([langName, langCode]) => (
                <option key={langCode} value={langCode}>
                  {langName.charAt(0).toUpperCase() + langName.slice(1)}
                </option>
              ))}
            </select>
            <button type="submit">Translate</button>
          </form>
        </div>

        {translatedText && (
          <div className="output-box">
            <h2>Translated Text</h2>
            <div className="translated-text">{translatedText}</div>
          </div>
        )}
      </div>
    </div>
  );
}

export default App;
