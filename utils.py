from data.sql_connection import MySQLConnector
from local_llm.main import llm_mistral
import json
import re

def connectSQL():
    """_summary_
        function to get the mysqlconnector class from the folder 
        use its connecting method and get the data
        
        __return__:
            this function returns the db connection 
    """
    db = MySQLConnector()
    return db

def getData(ticket_id):
    """_summary_
    this function gets the db from connectSQL and use sql to query the data,
    after getting the data this function return the data in JSON format
    this json format data will be used to ask question from the chatbot
    
    __return__
    """
    sql_connection = connectSQL()
    sql_connection.connect()

    result = sql_connection.fetch_query_as_json(f"""
        SELECT * 
        FROM ticket as t 
        LEFT JOIN `change` as c ON c.id = t.id
        LEFT JOIN ticket_incident as ti ON t.id = ti.id
        LEFT JOIN ticket_problem as tp ON t.id = tp.id
        LEFT JOIN ticket_request as tr ON t.id = tr.id 
        LEFT JOIN work_order_request_management as worm ON t.id = worm.id 
        LEFT JOIN project as p ON t.id = p.id
        WHERE t.id = {ticket_id}
        LIMIT 1
    """)
    
    sql_connection.close()
    return result

def getModel():
    """_summary_
    this function helps to get the model from '/local_llm' folder 
    and main.py inside it a function to get the model ( mistral)
    
    __return__ : this function return a mistral llm model locally downloaded in our repo
                path : ('/models')
    """
    llm = llm_mistral()
    return llm



# def getPrompt(user_query: str, ticket_id: int):
#     try:
#         row_data = getData(ticket_id)
#         if not row_data:
#             return f"No data found for ID {ticket_id}"
        
#         # Optional: filter out only important fields
#         limited_row = {
#             k: v for k, v in row_data[0].items() 
#             if isinstance(v, (int, float, str)) and len(str(v)) < 500
#         }

#         context_str = json.dumps(limited_row, indent=2, ensure_ascii=False)
        
#     except Exception as e:
#         context_str = "Error loading data."
#         print(f"❌ Failed to convert DB data to JSON: {e}")

#     return f"""
#             You are an intelligent, multilingual assistant trained to answer user queries based on structured ticket data.
#             Respond in the same language as the user (Hindi, English, Hinglish, etc.).
#             📊 Data Context for ID: {ticket_id}
#             {context_str}
#             🧠 User Query:
#             {user_query}
#             Instructions:
#             Use the data above to answer the query professionally. If the information is missing, say: "This is out of my scope."
#         """


def getPrompt(user_query: str, ticket_id: int):
    try:
        row_data = getData(ticket_id)
        if not row_data:
            return f"⚠️ No data found in the database for Ticket ID: {ticket_id}."

        raw = row_data[0]

        # ✨ Include all fields, but truncate values > 300 chars
        formatted_fields = []
        for key, value in raw.items():
            if not isinstance(value, (str, int, float)):
                continue
            value_str = str(value).strip()

            # Remove HTML tags from description fields
            if key.lower() in ["description", "solution"] or key.lower().endswith("comment"):
                value_str = re.sub(r'<.*?>', '', value_str)

            if len(value_str) > 300:
                value_str = value_str[:300] + "... (truncated)"

            field_name = key.replace("_", " ").capitalize()
            formatted_fields.append(f"{field_name}: {value_str}")

        context_str = "\n".join(formatted_fields)

    except Exception as e:
        context_str = "❌ Error loading ticket data."
        print(f"❌ JSON formatting error: {e}")

    return f"""
        You are a professional AI assistant trained to analyze structured ticket data and respond intelligently.

        🧾 Ticket Data for ID {ticket_id}:
        {context_str}

        🗣️ User Query:
        {user_query}

        🎯 Instructions:
        - Respond in the **same language or tone** as the user (English, Hindi, Hinglish).
        - Maintain a friendly and professional tone.
        - If the query is unrelated to the ticket data or the required information is missing, politely reply:
        "Yeh query ticket data se match nahi karti hai." or "This is out of my scope."
        - Be clear, helpful, and avoid guessing when data is missing.
    """
