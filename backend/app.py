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
    
    # Formatear la respuesta para una mejor legibilidad
    response = {
        'Lexical Analysis': tokens,
        'Syntactic Analysis (Parse Tree)': result,
        'Semantic Errors': errors
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
