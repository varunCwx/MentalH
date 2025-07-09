# ingest/excel_ingest.py
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

import pandas as pd
from graph.neo4j_handler import Neo4jHandler

def ingest_excel_to_neo4j(filepath):
    print("[INFO] Loading Excel data...")
    df = pd.read_excel(filepath)

    df.columns = [col.strip().lower() for col in df.columns]
    if 'questiontext' not in df or 'answertext' not in df:
        raise ValueError("Excel must have 'questionText' and 'answerText' columns")

    print(f"[INFO] Loaded {len(df)} rows from Excel.")

    handler = Neo4jHandler()

    for _, row in df.iterrows():
        question = str(row['questiontext']).strip()
        answer = str(row['answertext']).strip()
        if question and answer:
            handler.add_question_answer(question, answer)

    handler.close()
    print("✅ Ingestion complete.")

if __name__ == "__main__":
    ingest_excel_to_neo4j("/Users/varuncwx/Desktop/hackathon/data/qa.xlsx")
