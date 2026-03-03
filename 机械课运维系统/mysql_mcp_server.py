from fastmcp import FastMCP
import mysql.connector
import json

# Create an MCP server
mcp = FastMCP("MySQL Explorer")

# ==============================================================================
# CONFIGURATION
# PLEASE UPDATE THESE VALUES OR USE ENVIRONMENT VARIABLES
# ==============================================================================
DB_CONFIG = {
    "host": "localhost",
    "user": "your_username",      # CHANGE ME
    "password": "your_password",  # CHANGE ME
    "database": "your_database",  # CHANGE ME
    "port": 3306
}

@mcp.tool()
def query_database(sql_query: str) -> str:
    """
    Execute a custom SQL query on the MySQL database and return the results.
    Useful for retrieving specific data, analyzing tables, or checking records.
    
    Args:
        sql_query: The SQL query to execute (e.g., "SELECT * FROM users LIMIT 5")
    """
    # Security Precaution: In a real agentic scenario, you might want to restrict this
    # to read-only operations.
    forbidden_keywords = ["DROP", "DELETE", "TRUNCATE", "ALTER"]
    if any(keyword in sql_query.upper() for keyword in forbidden_keywords):
        return f"Error: Destructive queries containing {forbidden_keywords} are not allowed in this demo."

    conn = None
    try:
        conn = mysql.connector.connect(**DB_CONFIG)
        cursor = conn.cursor(dictionary=True) # Return results as dictionaries
        
        cursor.execute(sql_query)
        
        # If it's a SELECT query, fetch results
        if sql_query.strip().upper().startswith("SELECT") or sql_query.strip().upper().startswith("SHOW"):
            results = cursor.fetchall()
            return json.dumps(results, default=str, indent=2)
        else:
            conn.commit()
            return f"Query executed successfully. Rows affected: {cursor.rowcount}"

    except mysql.connector.Error as err:
        return f"MySQL Error: {err}"
    except Exception as e:
        return f"General Error: {e}"
    finally:
        if conn and conn.is_connected():
            cursor.close()
            conn.close()

if __name__ == "__main__":
    # fastmcp handles the serving (default port is usually dynamically assigned or stdio)
    # To run specifically for Dify (via SSE), we usually use:
    # mcp.run(transport="sse") 
    # But usually 'fastmcp run mysql_mcp_server.py' from CLI is preferred.
    mcp.run()
