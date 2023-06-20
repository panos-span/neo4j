import pandas as pd
from neo4j import GraphDatabase

actions = pd.read_csv('mooc_actions.tsv', delimiter='\t', names=['ACTIONID', 'USERID', 'TARGETID', 'TIMESTAMP'],
                      skiprows=1)
action_features = pd.read_csv('mooc_action_features.tsv', delimiter='\t',
                              names=['ACTIONID', 'FEATURE0', 'FEATURE1', 'FEATURE2', 'FEATURE4'], skiprows=1)
action_labels = pd.read_csv('mooc_action_labels.tsv', delimiter='\t', names=['ACTIONID', 'LABEL'], skiprows=1)

# Merge the dataframes on ACTIONID
actions = actions.merge(action_features, on='ACTIONID').merge(action_labels, on='ACTIONID')

uri = "bolt://localhost:7687"  # replace with your Neo4j URI
username = input("Enter your Neo4j username: ")
password = input("Enter your Neo4j password: ")

driver = GraphDatabase.driver(uri, auth=(username, password))

with driver.session() as session:
    # Create user nodes
    users = list(actions['USERID'].unique())
    session.run("UNWIND $ids AS id CREATE (:User {id: id})", ids=users)

    # Create target nodes
    targets = list(actions['TARGETID'].unique())
    session.run("UNWIND $ids AS id CREATE (:Target {id: id})", ids=targets)

    # Create action relationships
    actions_dict = actions.to_dict('records')
    session.run("""
        UNWIND $actions AS action
        MATCH (user:User {id: action.USERID})
        MATCH (target:Target {id: action.TARGETID})
        CREATE (user)-[:ACTION {id: action.ACTIONID, feature0: action.FEATURE0, feature1: action.FEATURE1,
        feature2: action.FEATURE2, feature4: action.FEATURE4, 
        label: action.LABEL, timestamp: action.TIMESTAMP}]->(target)
        """, actions=actions_dict)
