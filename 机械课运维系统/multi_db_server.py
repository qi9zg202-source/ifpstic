from fastmcp import FastMCP
import json
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# ==============================================================================
# CONFIGURATION
# PLEASE UPDATE THESE VALUES OR USE ENVIRONMENT VARIABLES
# ==============================================================================

MYSQL_CONFIG = {
    "host": "localhost",
    "user": "root",
    "password": "password",
    "database": "my_fab_data",
    "port": 3306
}

ORACLE_CONFIG = {
    "user": "system",
    "password": "password",
    "dsn": "localhost:1521/XEPDB1" # Data Source Name
}

POSTGRES_CONFIG = {
    "host": "localhost",
    "user": "postgres",
    "password": "password",
    "dbname": "my_fab_data",
    "port": 5432
}

# Creates the MCP server
mcp = FastMCP("Universal Database Explorer")

# ==============================================================================
# MYSQL TOOL
# ==============================================================================
@mcp.tool()
def query_mysql(sql_query: str) -> str:
    """
    Execute a SQL query on the MySQL database.
    Use this for data related to Fab Tools and Equipment logs mainly stored in MySQL.
    """
    try:
        import mysql.connector
    except ImportError:
        return "Error: 'mysql-connector-python' is not installed. Please run `pip install mysql-connector-python`."

    if _is_destructive(sql_query):
        return "Error: Destructive queries are not allowed."

    conn = None
    try:
        conn = mysql.connector.connect(**MYSQL_CONFIG)
        cursor = conn.cursor(dictionary=True)
        cursor.execute(sql_query)
        
        if _is_select(sql_query):
            results = cursor.fetchall()
            return json.dumps(results, default=str, indent=2)
        else:
            conn.commit()
            return f"Query executed. Rows affected: {cursor.rowcount}"
            
    except Exception as e:
        return f"MySQL Error: {e}"
    finally:
        if conn and conn.is_connected():
            cursor.close()
            conn.close()

# ==============================================================================
# ORACLE TOOL
# ==============================================================================
@mcp.tool()
def query_oracle(sql_query: str) -> str:
    """
    Execute a SQL query on the Oracle database.
    Use this for legacy enterprise data or ERP system records.
    """
    try:
        import oracledb
    except ImportError:
        return "Error: 'oracledb' is not installed. Please run `pip install oracledb`."

    if _is_destructive(sql_query):
        return "Error: Destructive queries are not allowed."

    conn = None
    try:
        # Oracle thin mode (no instant client needed usually)
        conn = oracledb.connect(**ORACLE_CONFIG)
        cursor = conn.cursor()
        cursor.execute(sql_query)
        
        if _is_select(sql_query):
            # Oracle doesn't default to dict cursor easily, we map it manually
            columns = [col[0] for col in cursor.description]
            rows = cursor.fetchall()
            results = [dict(zip(columns, row)) for row in rows]
            return json.dumps(results, default=str, indent=2)
        else:
            conn.commit()
            return f"Query executed. Rows affected: {cursor.rowcount}"

    except Exception as e:
        return f"Oracle Error: {e}"
    finally:
        if conn:
            conn.close()

# ==============================================================================
# POSTGRESQL TOOL
# ==============================================================================
@mcp.tool()
def query_postgres(sql_query: str) -> str:
    """
    Execute a SQL query on the PostgreSQL database.
    Use this for advanced analytics data or specific application backends.
    """
    try:
        import psycopg2
        from psycopg2.extras import RealDictCursor
    except ImportError:
        return "Error: 'psycopg2-binary' is not installed. Please run `pip install psycopg2-binary`."

    if _is_destructive(sql_query):
        return "Error: Destructive queries are not allowed."

    conn = None
    try:
        conn = psycopg2.connect(**POSTGRES_CONFIG)
        cursor = conn.cursor(cursor_factory=RealDictCursor)
        cursor.execute(sql_query)
        
        if _is_select(sql_query):
            results = cursor.fetchall()
            return json.dumps(results, default=str, indent=2)
        else:
            conn.commit()
            return f"Query executed. Rows affected: {cursor.rowcount}"

    except Exception as e:
        return f"PostgreSQL Error: {e}"
    finally:
        if conn:
            conn.close()

# ==============================================================================
# HELPERS
# ==============================================================================
def _is_destructive(sql: str) -> bool:
    forbidden = ["DROP", "DELETE", "TRUNCATE", "ALTER", "GRANT", "REVOKE"]
    return any(k in sql.upper() for k in forbidden)

def _is_select(sql: str) -> bool:
    return sql.split()[0].upper() in ["SELECT", "SHOW", "DESCRIBE", "EXPLAIN", "WITH"]

if __name__ == "__main__":
    # Run via: fastmcp run multi_db_server.py --transport sse --port 8000
    mcp.run()
