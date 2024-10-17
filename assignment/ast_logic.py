import ast

class Node:
    def __init__(self, type: str, left=None, right=None, value=None):
        self.type = type
        self.left = left
        self.right = right
        self.value = value

    def __repr__(self):
        return f"Node(type={self.type}, value={self.value})"

def create_rule(rule_string):
    # Replace 'AND' and 'OR' with 'and' and 'or'
    rule_string = rule_string.replace(' AND ', ' and ').replace(' OR ', ' or ')
    tree = ast.parse(rule_string, mode='eval')
    return build_ast(tree.body)

def build_ast(node):
    if isinstance(node, ast.BoolOp):  # AND / OR
        return Node("operator", build_ast(node.values[0]), build_ast(node.values[1]), type(node.op).__name__)
    elif isinstance(node, ast.Compare):  # Comparisons (age > 30)
        left = node.left.id
        op = type(node.ops[0]).__name__
        right = ast.literal_eval(node.comparators[0])

        # Map operator names to Python syntax
        operator_map = {
            'Gt': '>',
            'Lt': '<',
            'GtE': '>=',
            'LtE': '<=',
            'Eq': '==',
            'NotEq': '!=',
        }
        
        if isinstance(right, str):
            right = f'"{right}"'  # Enclose string values in quotes

        op = operator_map.get(op, op)  # Replace operator with its Python equivalent
        return Node("operand", value=f"{left} {op} {right}")

def combine_rules(asts):
    if len(asts) == 1:
        return asts[0]
    root = asts[0]
    for other_ast in asts[1:]:
        root = Node("operator", root, other_ast, "And")  # Combine with AND by default
    return root

def evaluate_ast(node, data):
    if node['type'] == "operator":
        left_eval = evaluate_ast(node['left'], data)
        right_eval = evaluate_ast(node['right'], data)
        if node['value'] == "And":
            return left_eval and right_eval
        elif node['value'] == "Or":
            return left_eval or right_eval
    elif node['type'] == "logical":
        # You can define the logic for "logical" nodes here
        if node['value'] == "Not":
            return not evaluate_ast(node['left'], data)
    elif node['type'] == "operand":
        # Ensure the operator is properly formatted and can be evaluated safely
        expression = node['value'].replace(" ", "")  # Remove spaces for safety
        return eval(expression, {}, data)  # Pass data as local scope
    else:
        raise ValueError(f"Unknown node type: {node['type']}")
