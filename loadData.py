import pandas as pd
from neo4j import GraphDatabase

# Replace 'file.tsv' with the paths to your TSV files
actions = pd.read_csv('mooc_actions.tsv', delimiter='\t', names=['ACTIONID', 'USERID', 'TARGETID', 'TIMESTAMP'],
                      skiprows=1)
action_features = pd.read_csv('mooc_action_features.tsv', delimiter='\t',
                              names=['ACTIONID', 'FEATURE0', 'FEATURE1', 'FEATURE2', 'FEATURE3'], skiprows=1)
action_labels = pd.read_csv('mooc_action_labels.tsv', delimiter='\t', names=['ACTIONID', 'LABEL'], skiprows=1)

# Merge the dataframes on ACTIONID
actions = actions.merge(action_features, on='ACTIONID').merge(action_labels, on='ACTIONID')

uri = "bolt://localhost:7687"  # replace with your Neo4j URI
username = input("Enter your Neo4j username: ")
password = input("Enter your Neo4j password: ")

driver = GraphDatabase.driver(uri, auth=(username, password))

with driver.session() as session:
    # Create user nodes
    for user_id in actions['USERID'].unique():
        session.run("CREATE (:User {id: $id})", id=user_id)

    # Create target nodes
    for target_id in actions['TARGETID'].unique():
        session.run("CREATE (:Target {id: $id})", id=target_id)

    # Create action relationships
    for index, row in actions.iterrows():
        session.run("""
            MATCH (user:User {id: $user_id})
            MATCH (target:Target {id: $target_id})
            CREATE (user)-[:ACTION {id: $action_id, feature0: $feature0, feature1: $feature1,
            feature2: $feature2, feature3: $feature3, label: $label}]->(target)
            """, user_id=row['USERID'], target_id=row['TARGETID'], action_id=row['ACTIONID'], feature0=row['FEATURE0'],
                    feature1=row['FEATURE1'], feature2=row['FEATURE2'], feature3=row['FEATURE3'], label=row['LABEL'])

    driver.close()
