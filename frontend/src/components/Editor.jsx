import PropTypes from 'prop-types';
import MonacoEditor from '@monaco-editor/react';
import lexer from '../lexer';
import createTokenProvider from '../monaco-tokens-provider';

const Editor = ({ fileName, onTokensUpdate }) => {
  const handleEditorChange = (value) => {
    lexer.reset(value);
    let tokenList = [];
    let token;
    while ((token = lexer.next())) {
      tokenList.push(token);
    }
    onTokensUpdate(tokenList);
  };

  const handleEditorWillMount = (monaco) => {
    createTokenProvider(monaco);
    monaco.editor.defineTheme('customDarkTheme', {
      base: 'vs-dark',
      inherit: true,
      rules: [
        { token: 'keyword', foreground: '00ff00' }, // Phosphorescent green
        { token: 'identifier', foreground: 'ffffff' }, // White
        { token: 'string', foreground: 'ce9178' }, // Orange
        { token: 'number', foreground: 'CB02FD' }, // Intense purple
        { token: 'operator', foreground: '87cefa' }, // Light Blue
        { token: 'delimiter', foreground: '87cefa' }, // Light Blue
        { token: 'whitespace', foreground: 'd4d4d4' }, // Light Gray
      ],
      colors: {
        'editor.background': '#000000', // Black background
      },
    });
  };

  return (
    <section className="flex-1 p-4 bg-black">
      <h2 className="text-white text-xl mb-4">{fileName}</h2>
      <MonacoEditor
        height="90%"
        theme="customDarkTheme"
        defaultLanguage="sql"
        defaultValue={`-- Escribe tu código SQL aquí para ${fileName}...`}
        options={{
          minimap: { enabled: false },
          automaticLayout: true,
        }}
        onChange={handleEditorChange}
        beforeMount={handleEditorWillMount}
      />
    </section>
  );
};

Editor.propTypes = {
  fileName: PropTypes.string.isRequired,
  onTokensUpdate: PropTypes.func.isRequired,
};

export default Editor;
