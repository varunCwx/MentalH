import pandas as pd
from neo4j import GraphDatabase

# ---- CONFIG ----
excel_file = "aapka file path"  # Replace with your actual Excel file
neo4j_uri = "bolt://localhost:7687"
neo4j_user = "neoappuser"
neo4j_password = "kuch bhi lagalo"  # Set this

# ---- Load Excel ----
df = pd.read_excel(excel_file)

# Basic cleanup

df.dropna(subset=["questionText", "answerText"], inplace=True)

# ---- Neo4j Driver Setup ----
driver = GraphDatabase.driver(neo4j_uri, auth=(neo4j_user, neo4j_password))

# ---- Ingest Data ----
def create_graph(tx, question, answer):
    tx.run("""
        MERGE (q:Question {text: $question})
        MERGE (a:Answer {text: $answer})
        MERGE (q)-[:HAS_ANSWER]->(a)
    """, question=question, answer=answer)

with driver.session() as session:
    for _, row in df.iterrows():
        session.write_transaction(create_graph, row["questionText"], row["answerText"])

driver.close()
print("✅ Data pushed to GraphDB.")


