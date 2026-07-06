Eval Report — Client Pulse Briefing


Overview

Three scenarios were tested against the Client Pulse skill running on Claude Desktop with a local MCP server backed by mock JSON data. Each scenario tests a distinct behavior: valid data retrieval, graceful error handling, and trigger boundary enforcement.


Scenario 1 — Valid Client, All Data Present

Prompt:

Give me a pulse on Acme Corporation

Expected: All three tools called, HTML briefing generated, browser opens automatically.

What I Observed (First Run):
Tools connected but returned empty responses. Root cause: data.json had a stray json prefix on the first line (json{ instead of {), causing Python's JSON parser to fail silently.

What I Fixed:
Removed the json prefix from line 1 of data.json. Restarted Claude Desktop.

Result After Fix: ✅ Pass

All 4 tools called in sequence — get_client_profile, get_open_issues, get_engagement_history, save_briefing. HTML briefing generated correctly and opened in browser automatically. Rep-facing message in chat said "Your briefing is ready — check your browser." Clean, no raw HTML visible in chat.

Assessment:
Full pipeline worked end to end. The fixed HTML template with {{PLACEHOLDERS}} produced consistent, readable output. The save_briefing tool eliminated the need for any manual steps from the rep.


Scenario 2 — Unknown Client Name

Prompt:

Give me a pulse on Microsoft

Expected: Clean error message. No hallucination. No briefing generated.

What I Observed (First Run):
Claude got stuck and returned no response. Error handling rule was too vague — "say so clearly" was not explicit enough for Claude to know what to do.

What I Fixed:
Updated Rule 3 in the system prompt from:

If the client does not exist, say so clearly. Do not guess or continue.

To:

If get_client_profile returns an error — STOP immediately. Do not call 
any other tools. Do not generate HTML. Respond only with: "Client not 
found: [name]. Please check the spelling and try again."

Result After Fix: ✅ Pass

Claude called get_client_profile, received the structured error, stopped immediately, and returned a clean error message. No other tools were called. No data was fabricated.

Known Limitation:
Current implementation uses exact string matching. "Acme Corp" would fail even though "Acme Corporation" exists. A production version would use fuzzy matching or a Salesforce search endpoint.


Scenario 3 — Ambiguous Prompt (Skill Should NOT Fire)

Prompt:

How are all our accounts doing?

Expected: Skill does not activate. Claude answers normally without calling any tools.

What I Observed: ✅ Pass (first run)

No tools were called. Claude responded conversationally without triggering the briefing pipeline. The trigger boundary held correctly — no specific client name meant no skill activation.

Assessment:
Trigger conditions worked as designed. The rule "only trigger when a rep names a specific client" was specific enough to prevent false activations on general account questions.

## Performance Observations

**Precision:** Data accuracy verified against data.json for Acme Corporation.
All fields matched exactly — ACV, industry, issue count, sentiment, 
contacts, and engagement history. No hallucinated data observed.

**Time to output:** Approximately 12-15 seconds from prompt to 
browser open. This includes 3 tool calls + HTML generation + 
save_briefing. Acceptable for a pre-call briefing use case.


Prompt Iterations Made

#What ChangedWhy1Added save_briefing toolRaw HTML was appearing in chat instead of rendering2Added "Do NOT show HTML in chat" to Rule 4Claude was showing code alongside opening browser3Strengthened error handling rule with explicit STOP instructionClaude got stuck on unknown client instead of returning clean error4Fixed json{ prefix in data.jsonTools were returning empty responses due to malformed JSON5Fixed {{EMPLOYEE_COUNT}} mapping from employee_count to size fieldTemplate was rendering blank for employee count6Fixed {{ACV}} mapping from acv to contract_valueTemplate was rendering blank for contract value7Changed "Open With" to "Recent Win" in stat barMore intuitive label for the rep


Overall Results

ScenarioResultNotesValid client✅ PassFull pipeline worked after fixing malformed JSONUnknown client✅ PassClean error after strengthening Rule 3Ambiguous prompt✅ PassSkill did not fire on first run


What I'd Fix With More Time

1. Fuzzy client name matching
"Acme Corp" currently fails. A production version would use fuzzy matching so reps don't need to type the exact client name.

2. Ambiguous trigger response
When the skill doesn't fire, Claude should guide the rep: "Try: Give me a pulse on [client name]" rather than a generic response.

3. MuleSoft integration
Replace data.json with live Salesforce data via AHEAD's existing MuleSoft API layer. Tool interfaces stay identical — only the data source changes.

4. Feedback loop
Add thumbs up/down to the briefing HTML. Track which sections reps use. Iterate the prompt and template based on real usage.


Eval conducted on Claude Desktop using local MCP server with mock JSON data store.
Three clients tested: Acme Corporation, BlueSky Financial, Greenfield Retail.
All scenarios passed after prompt and data iterations documented above.
