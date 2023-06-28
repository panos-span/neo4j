import time
from neo4j import GraphDatabase
import random

uri = "bolt://localhost:7687"  # replace with your Neo4j URI
username = input("Enter your Neo4j username: ")
password = input("Enter your Neo4j password: ")

driver = GraphDatabase.driver(uri, auth=(username, password))

queries = ["""
            MATCH (u:User) RETURN COUNT(u) AS UserCount
            """,
           """
           MATCH (t:Target) RETURN COUNT(t) AS TargetCount""",
           """
           MATCH ()-[a:ACTION]->() RETURN COUNT(a) AS ActionCount
           """,
           """
           MATCH (u:User {id: $user_id})-[a:ACTION]->(t:Target) RETURN a.id AS ActionID, t.id AS TargetID
           """,
           """
           MATCH (u:User)-[a:ACTION]->() RETURN u.id AS UserID, COUNT(a) AS ActionCount
           """,
           """
           MATCH (u:User)-[a:ACTION]->(t:Target) RETURN t.id AS TargetID, COUNT(DISTINCT u) AS UserCount
           """,
           """
           MATCH (u:User)-[a:ACTION]->() RETURN (COUNT(a)/COUNT(DISTINCT u)) AS AverageActionsPerUser
           """,
           """
           MATCH (u:User)-[a:ACTION]->(t:Target) WHERE a.feature2 > 0 RETURN u.id AS UserID, t.id AS TargetID
           """,
           """
           MATCH ()-[a:ACTION {label: 1}]->(t:Target) RETURN t.id AS TargetID, COUNT(a) AS ActionCount
           """

           ]


USER_COUNT = 7047
user_id = random.randint(1, USER_COUNT)
with driver.session() as session:
    for count, query in enumerate(queries):
        start_time = time.time()
        print("--------------------------------------------------")
        print(f"Running query: {query}")
        if count == 3:
            # Generate a random user ID for query 4
            print(f"User ID: {user_id}")
            session.run(query, user_id=user_id)
        else:
            session.run(query)
        elapsed_time = time.time() - start_time
        print(f"The query {query} took {elapsed_time} seconds to run.")
