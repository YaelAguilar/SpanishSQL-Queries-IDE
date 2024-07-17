const keywords = [
    'SELECCIONAR',
    'DESDE',
    'DONDE',
    'INSERTAR',
    'ACTUALIZAR',
    'BORRAR',
    'EN',
    'VALORES',
    'FIJAR',
    'Y',
    'O',
    'CREAR',
    'BASEDEDATOS',
    'TABLA',
    'ELIMINAR',
    'USAR',
    'VARCHAR',
    'INT'
  ];
  
  const createTokenProvider = (monaco) => {
    monaco.languages.register({ id: 'sql' });
  
    monaco.languages.setMonarchTokensProvider('sql', {
      tokenizer: {
        root: [
          [new RegExp(`\\b(${keywords.join('|')})\\b`, 'i'), 'keyword'],
          [/[a-zA-Z_][a-zA-Z0-9_]*/, 'identifier'],
          [/".*?"/, 'string'],
          [/\d+/, 'number'],
          [/[\*=\>\<\!\<\=\>\=]/, 'operator'],
          [/[;,()]/, 'delimiter'],
          [/\s+/, 'whitespace'],
        ],
      },
    });
  
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
        'editor.background': '#000000', // Black background
      },
    });
  };
  
  export default createTokenProvider;
  