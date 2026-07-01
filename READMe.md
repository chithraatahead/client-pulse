### Client Pulse — AHEAD Account Brief

A Claude-powered one page briefing for AHEAD account teams. Ask Claude about any client by name and get a structured, branded HTML briefing in seconds — open issues, engagement history, key contacts, and the three things you need to know about your Account.

A sales rep types:

Give me a pulse on 'Acme Corporation'

Claude calls three MCP tools, pulls client data, generates a branded HTML briefing, and opens it in the browser automatically. The rep reads it in under 30 seconds. 


### Project Structure

client-pulse/
├── mcp-server/
│   ├── server.py        # MCP server — 4 tools
│   └── data.json        # Mock client data — 3 clients
├── skill/
│   ├── SKILL.md         # Skill documentation + system prompt
│   └── example-output/  # Sample briefings
├── evals/
│   └── eval-report.md   # 3 test scenarios with results
└── README.md            # This file


### Setup Instructions

Prerequisites


Python 3.11 or higher
Claude Desktop installed
pip or pip3


Step 1 — Clone the repo

bashgit clone https://github.com/YOUR_USERNAME/client-pulse.git
cd client-pulse

Step 2 — Install dependencies

bashpip3 install mcp

Step 3 — Connect to Claude Desktop

Find your Claude Desktop config file:

bashopen ~/Library/Application\ Support/Claude/

Open config.json and add the mcpServers section:

json{
  "mcpServers": {
    "client-pulse": {
      "command": "/Library/Frameworks/Python.framework/Versions/3.13/bin/python3",
      "args": [
        "/path/to/client-pulse/mcp-server/server.py"
      ]
    }
  }
}

Replace /path/to/client-pulse with the actual path on your machine.

Step 4 — Restart Claude Desktop

Quit and reopen Claude Desktop. You should see the client-pulse integration connected.

Step 5 — Set up the Project

In Claude Desktop:

Create a New Project called "Client Pulse"
Paste the system prompt from skill/SKILL.md into Project Instructions
Start a new chat and type: Give me a pulse on Acme Corporation


The briefing will open in your browser automatically.


### The Four Tools

ToolWhat It Doesget_client_profileReturns client name, industry, size, contacts, contract valueget_open_issuesReturns all open issues with severity, days open, ownerget_engagement_historyReturns last N interactions with date, type, summary, sentimentsave_briefingSaves the generated HTML to Desktop and opens it in the browser


### Mock Clients

Three clients are included in data.json:

Each client has a different profile, issue severity mix, and sentiment history — designed to produce meaningfully different briefings.


### Design Rationale

### Why 3 separate tools instead of 1?

Each tool returns a different type of data at a different granularity. Splitting them means Claude can call only what it needs — and future tools (like get_renewal_date or get_competitor_intel) can be added without changing existing ones. It also makes error handling cleaner: if issues fail to load, the profile still renders.

### Why JSON instead of SQLite?

The brief asked for mock data. JSON is readable, editable, and requires zero setup. For production this would be a Salesforce API call or the where the Call,QBR and Email related sentiment data reside — the tool structure stays same, only the data layer changes.

### Why 3 signal cards?

Designed around one question: what does a rep actually need in the 30 seconds before a call? The emotional temperature (last sentiment), what's pressing most and important to customer right now (open issues), and recent win along with the supporting detail.

Why a branded HTML output?

Plain text briefings get ignored. A briefing that looks like an internal AHEAD product gets used. Which is also tending with Account team currently.  The HTML is self-contained — it can be saved, shared,hosted on Roost or screenshotted. 

### Fixed HTML template?

Giving Claude a complete template with {{PLACEHOLDERS}} produces consistent output every time with precision. Without a template, Claude improvises the layout on each run — output looks different, sections move around, reps can't build a mental model of where to look. Consistency is a feature.

### Claude desktop vs claude.ai
This implementation uses Claude Desktop to connect to the local MCP server. Claude.ai in the browser does not currently support custom local MCP servers. In production, the MCP server would be hosted in the cloud, enabling use from Claude.ai or any web interface with zero local setup.


### Future Improvements

1. Connect to real Salesforce data and real sentiment data for QBR, Email and Calls
The JSON mock is a stand-in. In production, get_client_profile would call the Salesforce REST API or MCP. The tool interface is identical — only the data source changes.

2. Add fuzzy name matching
Right now "Acme Corp" fails because the tool does exact string matching against "Acme Corporation." A production version would use fuzzy matching or a search endpoint so reps don't need to type the exact client name.

3. Human Intelligence-in-the-loop review step
Before the final briefing renders, the rep should see a draft and be able to adjust focus — example "I already know about the issues, skip that section." This not only gives opportunity to improve the Briefing overtime but also avoids over-reliance on AI judgment for high-stakes conversations.

4. Deploy to cloud
The MCP server runs locally right now. For enterprise rollout it would deploy to a cloud endpoint, the system prompt would live in a central Claude Enterprise workspace, and every AHEAD Account team would get access with zero local setup — just open a browser.

5. Feedback loop
Add a thumbs up/down to the briefing HTML. Track which sections reps actually use. Survey win rates on calls where reps used the briefing vs. didn't. Use that data to iterate the prompt and the template.
         
The pattern built here — MCP tools + Claude skill + structured HTML output — is fully reusable. The same architecture could power pre-QBR deep dives, renewal alerts, new rep onboarding briefs, and executive dashboards. The MCP server is the reusable layer. Each skill is just a different way of asking it questions.

Built as part of the AHEAD FDE Technical Assessment — AI Engineering
