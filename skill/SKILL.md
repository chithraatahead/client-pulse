SKILL: Client Pulse Briefing

AHEAD Account Intelligence


What This Skill Does

When a sales rep names a specific client and wants to prepare for a call, this skill pulls live data from three MCP tools and generates a branded, one-page HTML briefing — designed to be read in under 30 seconds.

The output opens automatically in the rep's browser. No dashboards. No switching apps. Just ask and read.


Trigger Conditions

FIRE when the rep says things like:


"Give me a pulse on Acme Corporation"
"Brief me on BlueSky Financial"
"What do I need to know before my call with Greenfield Retail?"
"Prep me for Acme"
"Pull up the client briefing for BlueSky"
"Account intelligence for [client name]"


DO NOT fire for:


General questions with no client name — "how are all our accounts doing?"
Internal AHEAD questions — "how are we tracking against quota?"
Topic questions — "what's the status of our ServiceNow practice?"
Vague requests — "give me a summary of everything"


Rule of thumb: A specific client name + pre-call intent = fire the skill. Everything else = answer normally.


Tool Call Sequence

Call all three tools every time. Do not skip any.

Step 1 — get_client_profile(client_name)
Returns: name, industry, size, primary contacts, contract value.
If this returns {"error": "client_not_found"} — STOP immediately.
Do not call the other tools. Respond:


"Client not found: [name] does not exist in the system. Please check the spelling and try again. Available clients: Acme Corporation, BlueSky Financial, Greenfield Retail."



Step 2 — get_open_issues(client_name)
Returns: all open issues with severity, days open, owner.

Step 3 — get_engagement_history(client_name, last_n=3)
Returns: last 3 interactions with date, type, summary, sentiment.

Step 4 — Generate HTML briefing
Using all three results, fill the HTML template defined in the system prompt. Do NOT show HTML in chat.

Step 5 — save_briefing(html_content)
Pass the complete HTML. Saves to rep's Desktop and opens in browser automatically.


The 3 Signal Cards

The rep should understand the account situation from these three cards alone.

CardContentColor LogicLast SignalMost recent interaction sentiment + date + type↑ green if positive, ↓ red if negative, → gray if neutralOpen IssuesTotal count + HIGH severity count + worst issue nameRed if any critical/high, green if all clearOpen WithPull-quote from most recent positive interactionGold — this is the rep's conversation opener


Output Format


Single self-contained HTML file
AHEAD branded: dark navy header #1a2535, white body, gold accent #F5A623
Max width 900px, centered, card layout with shadow
Two-column body: issues + contacts left, engagement log right
Stat bar in header: Last Touch · Open Issues · Last Signal · Open With
JetBrains Mono for labels and metadata, Inter for body text
Issue ages > 10 days flagged with ▲ and orange color
Issues sorted: Critical → High → Medium → Low
Contacts shown with colored avatar initials



Tone Rules


Short. Every sentence earns its place.
Active voice. "Client escalated" not "An escalation was made."
Precise numbers. "$450K contract" not "a large contract."
No filler. Never write "It is worth noting that..."
The "Open With" quote should be something a rep can actually say out loud.



Error Handling

Client not found:

Client not found: "[name]" does not exist in the Client Pulse system.
Please check the spelling and try again.
Available clients: Acme Corporation, BlueSky Financial, Greenfield Retail.

No positive interactions for "Open With" card:

No recent wins on record. Lead with a check-in on open issues.

No open issues:
Show "All Clear" in green. This is good news — make it visible.


What Good Output Looks Like

A well-formed briefing for Acme Corporation:


Header: "Acme Corporation · Manufacturing · Enterprise · $450K ACV"
Health status: "Healthy" — all positive sentiment, low severity issues only
Last Signal card: ↑ Positive (Jun 20 QBR, client praised AHEAD responsiveness)
Open Issues card: 2 issues · 0 HIGH · all Low severity
Open With card: "Client confirmed expansion plans for Q3" (from Jun 20 QBR)
Issues table: ISS-101 (Low, 2d), ISS-102 (Low, 3d)
Engagement log: QBR positive → Call positive → Email positive
Contacts: John Smith (CTO), Sarah Lee (IT Director)


The rep reads this in 30 seconds and walks in confident.

What Bad Output Looks Like


Walls of text with no visual hierarchy
Markdown instead of HTML
Missing signal cards or engagement log
Hallucinated data when client is not found
"Open With" quote that no rep would actually say out loud
Issues not sorted by severity
HTML shown in chat instead of opening in browser
