import json
import webbrowser
import tempfile
import os

from mcp.server.fastmcp import FastMCP


mcp = FastMCP("client-pulse")

# Load mock data
DATA_FILE = os.path.join(os.path.dirname(__file__), "data.json")

def load_data():
    with open(DATA_FILE, "r") as f:
        return json.load(f)

def find_client(name: str):
    data = load_data()
    for client in data["clients"]:
        if client["name"].lower() == name.lower():
            return client
    return None

@mcp.tool()
def get_client_profile(client_name: str) -> dict:
    """Get basic profile information for a client including industry, size, contacts and contract value"""
    client = find_client(client_name)
    if not client:
        return {"error": "client_not_found", "message": f"No client found with name '{client_name}'"}
    return {
        "id": client["id"],
        "name": client["name"],
        "industry": client["industry"],
        "size": client["size"],
        "primary_contacts": client["primary_contacts"],
        "contract_value": client["contract_value"]
    }

@mcp.tool()
def get_open_issues(client_name: str) -> dict:
    """Get all open support and service issues for a client"""
    client = find_client(client_name)
    if not client:
        return {"error": "client_not_found", "message": f"No client found with name '{client_name}'"}
    return {
        "client": client["name"],
        "open_issues": client["issues"],
        "total_count": len(client["issues"])
    }

@mcp.tool()
def get_engagement_history(client_name: str, last_n: int = 3) -> dict:
    """Get the last N interactions with a client including calls, emails and QBRs"""
    client = find_client(client_name)
    if not client:
        return {"error": "client_not_found", "message": f"No client found with name '{client_name}'"}
    history = client["engagement_history"][:last_n]
    return {
        "client": client["name"],
        "interactions": history,
        "returned": len(history)
    }
@mcp.tool()
def save_briefing(html_content: str) -> dict:
    """Save an HTML briefing to a file and open it in the browser"""
    desktop = os.path.expanduser("~/Desktop")
    filepath = os.path.join(desktop, "client-pulse-briefing.html")
    
    with open(filepath, "w") as f:
        f.write(html_content)
    
    webbrowser.open(f"file://{filepath}")
    
    return {
        "status": "success",
        "message": f"Briefing saved and opened in browser",
        "filepath": filepath
    }

if __name__ == "__main__":
    mcp.run()