from flask import Flask, request, jsonify, session
from flask_cors import CORS
from lexer import lexer
from parser import parser
from semantic import check_semantics, execute_queries, log_stream
from database import Database
import logging

app = Flask(__name__)
app.secret_key = 'supersecretkey'
CORS(app, supports_credentials=True)

db_instance = None

@app.route('/connect_db', methods=['POST'])
def connect_db():
    data = request.json
    user = data.get('user')
    password = data.get('password')
    host = data.get('host')
    port = data.get('port')
    database = data.get('database', None)

    try:
        global db_instance
        db_instance = Database(user=user, password=password, host=host, port=port, database=database)
        return jsonify({'message': 'Connection successful'}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 400

@app.route('/run_query', methods=['POST'])
def run_query():
    data = request.json.get('query')
    
    if db_instance is None:
        return jsonify({'error': 'No database connection'}), 400
    
    # Reiniciar el stream de log
    log_stream.truncate(0)
    log_stream.seek(0)

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
    
    if result is None:
        return jsonify({
            'Lexical Analysis': "\n".join(tokens),
            'Syntactic Analysis (Parse Tree)': "Error de sintaxis.",
            'Semantic Errors': "No se realizó el análisis semántico debido a errores sintácticos.",
            'Log': []
        }), 400
    
    # Análisis semántico
    errors = check_semantics(result, db_instance)
    
    if not errors:
        execute_queries(result, db_instance)
    
    # Obtener el log
    log_contents = log_stream.getvalue().strip()
    log_lines = log_contents.split('\n') if log_contents else []
    
    # Formatear la respuesta para una mejor legibilidad
    response = {
        'Lexical Analysis': tokens,
        'Syntactic Analysis (Parse Tree)': result,
        'Semantic Errors': errors,
        'Log': log_lines
    }

    formatted_response = format_response(response)
    
    return jsonify(formatted_response)

def format_response(response):
    formatted = {}
    
    # Formatear el análisis léxico
    formatted['Lexical Analysis'] = "\n".join(response['Lexical Analysis'])
    
    # Formatear el análisis sintáctico
    formatted['Syntactic Analysis (Parse Tree)'] = format_parse_tree(response['Syntactic Analysis (Parse Tree)'])
    
    # Formatear los errores semánticos
    if response['Semantic Errors']:
        formatted['Semantic Errors'] = "\n".join(response['Semantic Errors'])
    else:
        formatted['Semantic Errors'] = "No semantic errors."
    
    # Formatear el log
    formatted['Log'] = "\n".join(response['Log'])
    
    return formatted

def format_parse_tree(parse_tree):
    if parse_tree is None:
        return "No parse tree."
    
    def format_node(node, level=0):
        if isinstance(node, tuple):
            formatted = "\t" * level + str(node[0]) + "\n"
            for child in node[1:]:
                formatted += format_node(child, level + 1)
        elif isinstance(node, list):
            formatted = ""
            for child in node:
                formatted += format_node(child, level)
        else:
            formatted = "\t" * level + str(node) + "\n"
        return formatted
    
    return format_node(parse_tree)

if __name__ == '__main__':
    app.run(debug=True)
