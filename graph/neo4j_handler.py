# graph/neo4j_handler.py
from py2neo import Graph

class Neo4jHandler:
    def __init__(self, uri="bolt://localhost:7687", user="neo4j", password="test"):
        self.graph = Graph(uri, auth=(user, password))
        print("[INFO] Connected to Neo4j.")

    def add_question_answer(self, question, answer):
        self.graph.run("""
            MERGE (q:Question {text: $q_text})
            MERGE (a:Answer {text: $a_text})
            MERGE (q)-[:HAS_ANSWER]->(a)
        """, q_text=question, a_text=answer)

    def close(self):
        # Not strictly required with py2neo but good for symmetry
        print("[INFO] Connection closed (if applicable).")
