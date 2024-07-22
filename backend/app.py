from flask import Flask, request, jsonify
from flask_cors import CORS
from lexer import lexer
from parser import parser
from semantic import check_semantics, execute_queries

app = Flask(__name__)
CORS(app)

@app.route('/run_query', methods=['POST'])
def run_query():
    data = request.json.get('query')
    
    # Análisis léxico
    lexer.input(data)
    tokens = []
    while True:
        tok = lexer.token()
        if not tok:
            break
        tokens.append(str(tok))
    
    # Análisis sintáctico
    result = parser.parse(data)
    
    # Análisis semántico
    errors = check_semantics(result)
    
    if not errors:
        execute_queries(result)
    
    # Respuesta con todos los resultados
    response = {
        'tokens': tokens,
        'parse_tree': result,
        'semantic_errors': errors
    }
    
    if errors:
        return jsonify(response), 400
    
    return jsonify(response)

if __name__ == '__main__':
    app.run(debug=True)
