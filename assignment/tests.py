import unittest
from ast_logic import create_rule, evaluate_ast, combine_rules

class TestRuleEngine(unittest.TestCase):

    def setUp(self):
        self.data = {"age": 35, "department": "Sales"}
        self.rule_string = "age > 30 and department == 'Sales'"
        self.rule_ast = create_rule(self.rule_string)

    def test_create_rule(self):
        self.assertIsNotNone(self.rule_ast)
        self.assertEqual(self.rule_ast.type, "operator")
        self.assertEqual(self.rule_ast.value, "And")

    def test_evaluate_rule(self):
        result = evaluate_ast(self.rule_ast, self.data)
        self.assertTrue(result)

    def test_combine_rules(self):
        rule1 = create_rule("age > 30")
        rule2 = create_rule("department == 'Sales'")
        combined = combine_rules([rule1, rule2])
        self.assertEqual(combined.value, "And")
        self.assertIsNotNone(combined)

if __name__ == '__main__':
    unittest.main()
