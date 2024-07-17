import moo from 'moo';

const lexer = moo.compile({
  whitespace: { match: /\s+/, lineBreaks: true },
  keyword: [
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
  ],
  identifier: /[a-zA-Z_][a-zA-Z0-9_]*/,
  string: /"(?:\\["\\]|[^\n"\\])*"/,
  number: /0|[1-9][0-9]*/,
  operator: ['=', '<', '>', '<=', '>=', '!='],
  star: '*',
  lparen: '(',
  rparen: ')',
  semicolon: ';',
  comma: ',',
  unknown: { match: /.+/, lineBreaks: true }
});

export default lexer;
