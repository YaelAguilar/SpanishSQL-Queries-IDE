import { useState } from 'react';
import Header from './components/Header';
import Sidebar from './components/Sidebar';
import Editor from './components/Editor';
import Footer from './components/Footer';
import WelcomeScreen from './components/WelcomeScreen';
import AnalysisViewer from './components/AnalysisViewer';

const App = () => {
  const [activeFile, setActiveFile] = useState(null);
  const [logs, setLogs] = useState([]);
  const [analysis, setAnalysis] = useState({
    lexical: '',
    syntactic: '',
    semantic: '',
  });
  const [showAnalysisViewer, setShowAnalysisViewer] = useState(false);

  const handleFileOpen = (fileName) => {
    setActiveFile(fileName);
  };

  const handleLogUpdate = (newLogs) => {
    setLogs(Array.isArray(newLogs) ? newLogs : []);
  };

  const handleAnalysisUpdate = (lexical, syntactic, semantic) => {
    setAnalysis({ lexical, syntactic, semantic });
  };

  const handleOpenAnalysisViewer = () => {
    setShowAnalysisViewer(true);
  };

  const handleCloseAnalysisViewer = () => {
    setShowAnalysisViewer(false);
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
            onAnalysisUpdate={handleAnalysisUpdate}
          />
        ) : (
          <WelcomeScreen textColor="#00ff00" backgroundColor="#000000" />
        )}
      </div>
      <Footer logs={logs} className="flex-grow" />
      <button
        onClick={handleOpenAnalysisViewer}
        className="bg-blue-500 hover:bg-blue-700 text-white font-bold py-2 px-4 rounded fixed bottom-4 right-4 z-50"
      >
        Ver Análisis
      </button>
      {showAnalysisViewer && (
        <AnalysisViewer
          lexicalAnalysis={analysis.lexical}
          syntacticAnalysis={analysis.syntactic}
          semanticErrors={analysis.semantic}
          onClose={handleCloseAnalysisViewer}
        />
      )}
    </div>
  );
};

export default App;
