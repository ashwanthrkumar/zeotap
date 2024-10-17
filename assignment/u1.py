import unittest
from ast_logic import create_rule

class TestRuleCreation(unittest.TestCase):
    def test_individual_rules(self):
        rules = [
            ("age > 30", {"type": "operand", "value": "age > 30"}),
            ("salary < 50000", {"type": "operand", "value": "salary < 50000"}),
            ("department == 'Sales'", {"type": "operand", "value": "department == 'Sales'"})
        ]
        
        for rule_string, expected in rules:
            with self.subTest(rule=rule_string):
                ast_tree = create_rule(rule_string)
                self.assertEqual(ast_tree['type'], expected['type'])
                self.assertEqual(ast_tree['value'], expected['value'])

if __name__ == '__main__':
    unittest.main()
