from pymongo import MongoClient
from bson.objectid import ObjectId
import json

# Initialize MongoDB connection
client = MongoClient("mongodb://localhost:27017/")
db = client['rule_engine_db']
rules_collection = db['rules']

def save_rule_to_db(rule_string, rule_ast):
    """
    Save the rule string and its abstract syntax tree (AST) to the database.
    
    Args:
        rule_string (str): The rule as a string.
        rule_ast (Node): The abstract syntax tree representation of the rule.
    
    Returns:
        ObjectId: The ID of the inserted document.
    """
    # Convert the AST to a dictionary format for storage
    rule_ast_dict = json.dumps(rule_ast.__dict__, default=str)
    rule_doc = {"rule": rule_string, "ast": rule_ast_dict}
    
    # Insert the document into the collection
    result = rules_collection.insert_one(rule_doc)
    return result.inserted_id

def get_rule_from_db(rule_id):
    """
    Retrieve a rule document from the database using its ID.
    
    Args:
        rule_id (str): The ID of the rule to retrieve.
    
    Returns:
        dict: The AST of the rule if found.
    
    Raises:
        ValueError: If the rule is not found.
    """
    rule_doc = rules_collection.find_one({"_id": ObjectId(rule_id)})
    if rule_doc:
        # Deserialize the AST back to its original structure
        return json.loads(rule_doc['ast'])
    else:
        raise ValueError("Rule not found")
