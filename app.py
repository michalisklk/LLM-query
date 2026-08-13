import os
import json
import time
from dotenv import load_dotenv
from google import genai
from google.genai import types
from pydantic import BaseModel, Field
import sqlite3

load_dotenv()

# 1. Structured output Schema για τον Δάσκαλο
class SQLResponse(BaseModel):
    sql_query: str = Field(description="The exact SQLite query to answer the user's question.")
    explanation: str = Field(description="A brief one-sentence explanation of what the query does.")


# 2. Το Schema της βάσης μας
DB_SCHEMA = """
Database Schema (SQLite):

Table: users
- user_id (INTEGER, Primary Key)
- name (TEXT)
- email (TEXT)
- signup_date (TEXT, Format: YYYY-MM-DD)
- country (TEXT)

Table: orders
- order_id (INTEGER, Primary Key)
- user_id (INTEGER, Foreign Key -> users.user_id)
- order_date (TEXT, Format: YYYY-MM-DD)
- total_amount (REAL)
- status (TEXT, Values: 'completed', 'pending', 'cancelled')

Table: order_items
- item_id (INTEGER, Primary Key)
- order_id (INTEGER, Foreign Key -> orders.order_id)
- product_name (TEXT)
- category (TEXT)
- price (REAL)
- quantity (INTEGER)
"""

SYSTEM_PROMPT = f"""
You are an expert SQL Generator and Data Analyst.
Given the DB Schema below:

{DB_SCHEMA}

Task:
Convert the user's natural language question into a valid SQLite query.
- Use only the tables and columns provided in the schema.
- Do NOT perform destructive queries (NO DROP, DELETE, INSERT, UPDATE). Only SELECT queries are allowed.
- Output strictly valid SQLite syntax.
"""

def execute_sql(query:str):
    connection=sqlite3.connect("ecommerce.db")
    cursor=connection.cursor()
    try:
        cursor.execute(query)
        rows=cursor.fetchall()
        columns = []
        if cursor.description is not None:
            for item in cursor.description:
                columns.append(item[0])
        connection.close()

        return rows,columns,None

    except Exception as e:
        connection.close()
        return None, None, str(e)

def run_query(sql_query:str):
    rows, columns, error = execute_sql(sql_query)

    if error:
        print(f"SQL Execution Error: {error}\n")
        return

    print("Query Results from DB:")
    if not rows:
        print("No data found for this query")
    else:
        print("   " + "  ".join(columns))

        for row in rows:
            print("   " + "  ".join(str(item) for item in row))

def call_LLM(client,user_quetion:str):
    response=client.models.generate_content(
        model='gemini-2.5-flash',
        contents=user_quetion,
        config=types.GenerateContentConfig(
            system_instruction=SYSTEM_PROMPT,
            response_mime_type="application/json",
            response_schema=SQLResponse,
            temperature=0.0
        )
    )
    ai_data=json.loads(response.text)
    sql_query = ai_data["sql_query"]
    explanation = ai_data["explanation"]
    print(f"AI Generated SQL : {sql_query}")
    print(f"Explanation      : {explanation}")

    run_query(sql_query)
def main():
    client = genai.Client(api_key=os.getenv("API_KEY"))
    
    print(" Welcome to Interactive Text-to-SQL Assistant!")
    print(" Type your question in natural language (or 'exit' to quit).")

    while True:
        Uinput = input("\nAsk a question about your DB > ").strip()
        
        if Uinput.lower() in ["exit", "quit", "q"]:
            print("\nGoodbye!")
            break
            
        if not Uinput:
            continue
            
        call_LLM(client, Uinput)

if __name__ == "__main__":
    main()