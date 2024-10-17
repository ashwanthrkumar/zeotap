from flask import Flask, request, jsonify
from ast_logic import create_rule, combine_rules, evaluate_ast
from database import save_rule_to_db, get_rule_from_db
import re

app = Flask(__name__)

def parse_rule(rule):
    # Tokenize the input rule
    tokens = re.findall(r'[\w\'"]+|[=<>!]+|AND|OR|\(|\)', rule)
    output = []
    operators = []

    precedence = {
        'OR': 1,
        'AND': 2,
        '(': 0
    }

    def is_operator(token):
        return token in precedence

    def to_ast(left, operator, right):
        return {
            "type": "operator",
            "value": operator,
            "left": left,
            "right": right
        }

    for token in tokens:
        if token == '(':
            operators.append(token)
        elif token == ')':
            while operators and operators[-1] != '(':
                operator = operators.pop()
                right = output.pop()
                left = output.pop()
                output.append(to_ast(left, operator, right))
            operators.pop()  # Pop the '('
        elif is_operator(token):
            while (operators and operators[-1] != '(' and 
                   precedence[operators[-1]] >= precedence[token]):
                operator = operators.pop()
                right = output.pop()
                left = output.pop()
                output.append(to_ast(left, operator, right))
            operators.append(token)
        else:  # Token is an operand
            output.append({"type": "operand", "value": token.strip()})

    # Final pass to clear remaining operators
    while operators:
        operator = operators.pop()
        right = output.pop()
        left = output.pop()
        output.append(to_ast(left, operator, right))

    return output[0] if output else None




@app.route('/create_rule', methods=['POST'])
def create_rule_endpoint():
    # Retrieve the rule expression from the request
    rule_expression = request.json.get('rule')
    
    # Parse the rule expression into an AST
    try:
        ast = parse_rule(rule_expression)
        # Optionally save the AST to a database
        # save_rule_to_db(ast)  # Uncomment to save
        return jsonify({"ast": ast}), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 400  # Return error if parsing fails

@app.route('/combine_rules', methods=['POST'])
def combine_rules_endpoint():
    rule_ids = request.json.get('rule_ids')
    rules = [get_rule_from_db(rule_id) for rule_id in rule_ids]
    combined_ast = combine_rules(rules)
    return jsonify({"combined_ast": combined_ast.__dict__})

@app.route('/evaluate_rule', methods=['POST'])
def evaluate_rule_endpoint():
    rule_ast = request.json.get('ast')
    user_data = request.json.get('user_data')
    result = evaluate_ast(rule_ast, user_data)
    return jsonify({"result": result})

if __name__ == '__main__':
    app.run(debug=True)
