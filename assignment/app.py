from flask import Flask, request, jsonify
from ast_logic import create_rule, combine_rules, evaluate_ast
from database import save_rule_to_db, get_rule_from_db

app = Flask(__name__)

@app.route('/create_rule', methods=['POST'])
def create_rule_endpoint():
    rule_string = request.json.get('rule')
    rule_ast = create_rule(rule_string)
    rule_id = save_rule_to_db(rule_string, rule_ast)
    return jsonify({"rule_id": str(rule_id), "ast": rule_ast.__dict__})

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
