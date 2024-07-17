import { useState } from 'react';
import Header from './components/Header';
import Sidebar from './components/Sidebar';
import Editor from './components/Editor';
import Footer from './components/Footer';
import WelcomeScreen from './components/WelcomeScreen';

const App = () => {
  const [activeFile, setActiveFile] = useState(null);
  const [tokens, setTokens] = useState([]);

  const handleFileOpen = (fileName) => {
    setActiveFile(fileName);
  };

  const handleTokensUpdate = (newTokens) => {
    setTokens(newTokens);
  };

  return (
    <div className="flex flex-col h-screen bg-[#1c1c1e] text-white">
      <Header />
      <div className="flex flex-1">
        <Sidebar onFileOpen={handleFileOpen} />
        {activeFile ? (
          <Editor fileName={activeFile} onTokensUpdate={handleTokensUpdate} />
        ) : (
          <WelcomeScreen textColor="#00ff00" backgroundColor="#000000" />
        )}
      </div>
      <Footer tokens={tokens} className="flex-grow" />
    </div>
  );
};

export default App;
