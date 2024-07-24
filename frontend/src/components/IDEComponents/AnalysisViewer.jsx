import { useState } from 'react';
import PropTypes from 'prop-types';

const AnalysisViewer = ({ lexicalAnalysis, syntacticAnalysis, semanticErrors, onClose }) => {
  const [visibleSection, setVisibleSection] = useState('none');

  const handleButtonClick = (section) => {
    setVisibleSection(visibleSection === section ? 'none' : section);
  };

  return (
    <div className="bg-gray-800 p-4 rounded shadow-lg text-white fixed top-0 left-0 w-full h-full flex flex-col z-50">
      <div className="flex justify-between mb-4">
        <div>
          <button className="bg-blue-500 hover:bg-blue-700 text-white font-bold py-2 px-4 rounded mr-2" onClick={() => handleButtonClick('lexical')}>
            Análisis Léxico
          </button>
          <button className="bg-green-500 hover:bg-green-700 text-white font-bold py-2 px-4 rounded mr-2" onClick={() => handleButtonClick('syntactic')}>
            Análisis Sintáctico
          </button>
          <button className="bg-red-500 hover:bg-red-700 text-white font-bold py-2 px-4 rounded mr-2" onClick={() => handleButtonClick('semantic')}>
            Análisis Semántico
          </button>
        </div>
        <button className="bg-gray-500 hover:bg-gray-700 text-white font-bold py-2 px-4 rounded" onClick={onClose}>
          Cerrar
        </button>
      </div>
      <div className="bg-gray-700 p-4 rounded flex-grow overflow-y-auto">
        {visibleSection === 'lexical' && (
          <pre className="whitespace-pre-wrap">{lexicalAnalysis}</pre>
        )}
        {visibleSection === 'syntactic' && (
          <pre className="whitespace-pre-wrap">{syntacticAnalysis}</pre>
        )}
        {visibleSection === 'semantic' && (
          <pre className="whitespace-pre-wrap">{semanticErrors}</pre>
        )}
        {visibleSection === 'none' && (
          <div className="text-center text-gray-400">Seleccione una opción para ver el análisis</div>
        )}
      </div>
    </div>
  );
};

AnalysisViewer.propTypes = {
  lexicalAnalysis: PropTypes.string.isRequired,
  syntacticAnalysis: PropTypes.string.isRequired,
  semanticErrors: PropTypes.string.isRequired,
  onClose: PropTypes.func.isRequired,
};

export default AnalysisViewer;
