import { useState } from 'react';
import PropTypes from 'prop-types';
import MonacoEditor from '@monaco-editor/react';
import lexer from '../../lexer';
import createTokenProvider from '../../monaco-tokens-provider';

const Editor = ({ fileName, onLogUpdate, onAnalysisUpdate }) => {
  const [query, setQuery] = useState('');

  const runQuery = async () => {
    try {
      const response = await fetch('http://localhost:5000/run_query', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ query }),
      });

      const data = await response.json();

      if (!response.ok) {
        console.error('Errors:', data['Semantic Errors']);
      }

      console.log('Tokens:', data['Lexical Analysis']);
      console.log('Parse Tree:', data['Syntactic Analysis (Parse Tree)']);
      console.log('Semantic Errors:', data['Semantic Errors']);
      console.log('Log:', data['Log']);

      onLogUpdate(data['Log'].split('\n'));

      onAnalysisUpdate(data['Lexical Analysis'], data['Syntactic Analysis (Parse Tree)'], data['Semantic Errors']);
    } catch (error) {
      console.error('Error running query:', error);
      onLogUpdate([`Error: ${error.message}`]);
    }
  };

  const handleEditorChange = (value) => {
    setQuery(value);
    lexer.reset(value);
  };

  const handleEditorWillMount = (monaco) => {
    createTokenProvider(monaco);
    monaco.editor.defineTheme('customDarkTheme', {
      base: 'vs-dark',
      inherit: true,
      rules: [
        { token: 'keyword', foreground: '00ff00' }, // Green
        { token: 'identifier', foreground: 'ffffff' }, // White
        { token: 'string', foreground: 'ce9178' }, // Light Red
        { token: 'number', foreground: 'CB02FD' }, // Purple
        { token: 'operator', foreground: '87cefa' }, // Light Blue
        { token: 'delimiter', foreground: '87cefa' }, // Light Blue
        { token: 'whitespace', foreground: 'd4d4d4' }, // Gray
      ],
      colors: {
        'editor.background': '#000000', // Black
      },
    });
  };

  return (
    <section className="flex-1 p-4 bg-black">
      <h2 className="text-white text-xl mb-4">{fileName}</h2>
      <MonacoEditor
        height="80%"
        theme="customDarkTheme"
        defaultLanguage="sql"
        defaultValue={`-- Your SQL code here...`}
        options={{
          minimap: { enabled: false },
          automaticLayout: true,
        }}
        onChange={handleEditorChange}
        beforeMount={handleEditorWillMount}
      />
      <button
        onClick={runQuery}
        className="mt-4 p-2 bg-green-500 text-white rounded hover:bg-green-700"
      >
        Run Query
      </button>
    </section>
  );
};

Editor.propTypes = {
  fileName: PropTypes.string.isRequired,
  onLogUpdate: PropTypes.func.isRequired,
  onAnalysisUpdate: PropTypes.func.isRequired,
};

export default Editor;
