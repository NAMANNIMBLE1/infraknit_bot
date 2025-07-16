import pymysql
import json
import os

class MySQLConnector:
    def __init__(self, host=None, user=None, password=None, database=None):  # ✅ Fixed this line
        self.conn = None
        self.cursor = None
        self.config = {
            "host": host or "",
            "user": user or "",
            "password": password or "",
            "database": database or ""
        }

    def connect(self):
        try:
            self.conn = pymysql.connect(**self.config, connect_timeout=5)
            self.cursor = self.conn.cursor()
            print("✅ DB connection successful.")
        except Exception as e:
            print("❌ DB connection failed:", e)

    def fetch_query(self, query, params=None):
        if not self.cursor:
            print("❌ No active DB connection.")
            return None
        try:
            self.cursor.execute(query, params or ())
            return self.cursor.fetchall()
        except Exception as e:
            print("❌ Query execution failed:", e)
            return None

    def fetch_query_as_json(self, query, params=None):
        if not self.cursor:
            print("❌ No active DB connection.")
            return None
        try:
            self.cursor.execute(query, params or ())
            columns = [desc[0] for desc in self.cursor.description]
            rows = self.cursor.fetchall()
            
            # Ensure unique column names
            seen_columns = {}
            unique_columns = []
            for col in columns:
                if col in seen_columns:
                    seen_columns[col] += 1
                    unique_columns.append(f"{col}_{seen_columns[col]}")
                else:
                    seen_columns[col] = 1
                    unique_columns.append(col)
            
            return [dict(zip(unique_columns, row)) for row in rows]
        except Exception as e:
            print("❌ Query execution failed:", e)
            return None

    def close(self):
        if self.cursor:
            self.cursor.close()
        if self.conn:
            self.conn.close()
            print("✅ DB connection closed.")

# -------------------------------------
# Usage
# -------------------------------------
# if __name__ == "__main__":
#     db = MySQLConnector()
#     db.connect()

#     result = db.fetch_query_as_json("""
#         SELECT * 
#         FROM ticket as t 
#         LEFT JOIN `change` as c ON c.id = t.id
#         LEFT JOIN ticket_incident as ti ON t.id = ti.id
#         LEFT JOIN ticket_problem as tp ON t.id = tp.id
#         LEFT JOIN ticket_request as tr ON t.id = tr.id 
#         LEFT JOIN work_order_request_management as worm ON t.id = worm.id 
#         LEFT JOIN project as p ON t.id = p.id
#     """)

#     if result:
#         output_dir = "data"
#         os.makedirs(output_dir, exist_ok=True)
#         output_file = os.path.join(output_dir, "query_results.json")

#         with open(output_file, 'w', encoding='utf-8') as f:
#             json.dump(result, f, indent=2, default=str, ensure_ascii=False)

#         print(f"✅ Results saved to {output_file}")
#         print(f"📊 Total records: {len(result)}")
#         print(f"📋 Columns per record: {len(result[0]) if result else 0}")
#     else:
#         print("❌ No result or query failed.")

#     db.close()
