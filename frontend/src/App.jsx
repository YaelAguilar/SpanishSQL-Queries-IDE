import { useState } from 'react';
import Header from './components/Header';
import Sidebar from './components/Sidebar';
import Editor from './components/Editor';
import Footer from './components/Footer';
import WelcomeScreen from './components/WelcomeScreen';

const App = () => {
  const [activeFile, setActiveFile] = useState(null);
  const [logs, setLogs] = useState([]);

  const handleFileOpen = (fileName) => {
    setActiveFile(fileName);
  };

  const handleLogUpdate = (newLogs) => {
    setLogs(Array.isArray(newLogs) ? newLogs : []);
  };

  return (
    <div className="flex flex-col h-screen bg-[#1c1c1e] text-white">
      <Header />
      <div className="flex flex-1">
        <Sidebar onFileOpen={handleFileOpen} />
        {activeFile ? (
          <Editor
            fileName={activeFile}
            onLogUpdate={handleLogUpdate}
          />
        ) : (
          <WelcomeScreen textColor="#00ff00" backgroundColor="#000000" />
        )}
      </div>
      <Footer logs={logs} className="flex-grow" />
    </div>
  );
};

export default App;
