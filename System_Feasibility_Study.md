# System Feasibility Study
## Discord-Based Companion Service Booking Bot

**Document type:** System Feasibility Study  
**Scope:** Concept, features, and feasibility of a Discord bot for welcome onboarding, service ordering, private tickets, and staff matching  
**Note:** This document describes the system in general terms and does not reference any specific commercial brand.

---

## 1. Introduction

### 1.1 Purpose
This study evaluates whether a Discord bot is a feasible way to automate customer onboarding, service requests, ticket handling, and staff assignment for a companion / gaming-support community.

### 1.2 Problem Statement
Manual handling of welcomes, orders, and staff matching in Discord is slow and inconsistent. Customers may struggle to find who is available; staff may miss requests; order details can be incomplete or scattered across DMs.

### 1.3 Proposed Solution
A Discord bot that:
- Welcomes new members automatically
- Provides interactive panels for information and ordering
- Guides customers through a structured order form
- Creates private ticket channels
- Notifies eligible staff and supports volunteer-based matching
- Grants chosen staff access to the ticket for fulfillment and payment follow-up

### 1.4 Objectives
- Reduce manual admin work for welcomes and order intake
- Standardize the information collected for each request
- Improve visibility of online / eligible staff
- Keep order discussions private and organized in tickets
- Support multi-staff orders when a customer needs more than one companion

---

## 2. System Overview

### 2.1 System Concept
The bot acts as a **front desk and order desk** inside Discord:
1. Greets new members
2. Lets admins post persistent interaction panels
3. Walks customers through service choices
4. Opens a private ticket
5. Helps match customers with available staff

### 2.2 Users

| Role | How they use the system |
|------|-------------------------|
| New member | Receives a welcome message with service overview and links |
| Customer | Submits an order via buttons, selects preferences, confirms details, chooses staff |
| Staff / companion | Views matching requests, volunteers, enters availability time |
| Moderator / admin | Posts panels, monitors tickets, closes tickets, confirms settled orders |
| Bot | Automates messages, forms, channel creation, permissions, and matching UI |

### 2.3 High-Level Flow
```
Member joins → Welcome message
Admin posts panels → Welcome panel / Order panel
Customer clicks “Submit request”
  → Choose service type
  → (If needed) Choose device
  → Choose game / duration / gender preference
  → Fill form (rank or game name, notes, start time, staff count)
  → Private ticket created
Customer confirms details → Eligible staff notified
Staff volunteer → Customer selects staff → Staff get ticket access
Ticket closed when done → Channel deleted after a short delay
```

---

## 3. Features

### 3.1 Automatic Welcome
- Triggered when a member joins the server
- Posts a branded-style welcome embed (colors, avatar thumbnail, service summary)
- Includes guidance and channel links for help or self-service ordering

### 3.2 Welcome Panel (Admin Command)
- Admin posts a persistent panel with buttons
- **Get started:** Short private guidance message
- **Who’s online?:** Lists non-offline staff with status indicators
- Each listed staff member can have a **Request** button that DMs them on the customer’s behalf

### 3.3 Service Request Panel (Admin Command)
- Admin posts a persistent “submit order” panel
- Customers start the order flow without messaging staff first

### 3.4 Guided Order Flow
Interactive steps (buttons and dropdowns):
1. **Service type** — e.g. play-together vs chat-only
2. **Device** — e.g. PC or mobile (skipped for chat-only)
3. **Preferences** — game (when applicable), session length, preferred staff gender
4. **Modal form** — rank or specific game name (when needed), notes, start time, number of staff required

Validation includes:
- Required selections before continuing
- Time format checking (e.g. `20:30`, `8:30pm`, or “now”)
- Staff count within an allowed range
- Prevention of duplicate open tickets for the same user

### 3.5 Private Ticket Creation
- Creates a private text channel under a configured category
- Permissions limited to the customer, moderators, and the bot
- Posts a summary of the order for confirmation
- Includes links (e.g. pricing) and actions to confirm or close

### 3.6 Staff Matching
- After confirmation, eligible staff (by role tags such as game / gender) are notified in a staff channel
- Staff can volunteer and enter their available start time
- Volunteers can withdraw by pressing again
- When enough volunteers exist, the customer selects the required number
- Selected staff receive channel permissions and a handoff message (including payment guidance)

### 3.7 Ticket Lifecycle
- Owner or moderator can close a ticket
- Closing updates the staff-side message (if present) and deletes the channel after a short countdown
- Optional settlement confirmation can record a ticket number for records (when a database is connected)

### 3.8 Persistent Interactions
- Key panels use persistent button IDs so they keep working after bot restarts
- Bot registers these views on startup

---

## 4. Technical Feasibility

### 4.1 Technology Stack
| Component | Approach | Feasibility |
|-----------|----------|-------------|
| Platform | Discord (existing community hub) | High — users already present |
| Runtime | Python | High — common, readable, well supported |
| Library | discord.py (commands + UI views/modals) | High — mature for bots and components |
| Structure | Cogs + modular views | High — easier maintenance and extension |
| Config | Environment variables for secrets; constants for IDs | High |
| Optional DB | Pool-backed inserts for settled tickets | Medium — needed only if settlement tracking is required |

### 4.2 Technical Requirements
- Discord application + bot token
- Privileged intents as needed: members, presences, message content
- Correct role, category, and channel IDs configured
- Hosting that can run a long-lived process (local PC, VPS, or cloud)
- Optional: database if order settlement IDs must persist

### 4.3 Architecture Fit
The design maps cleanly to Discord’s interaction model:
- **Commands** for admin setup
- **Buttons / selects / modals** for customer input
- **Channels + permission overwrites** for private tickets
- **Role-based filtering** for who should see which orders

### 4.4 Technical Risks and Mitigations
| Risk | Impact | Mitigation |
|------|--------|------------|
| Discord API rate limits | Delayed messages | Batch carefully; keep embeds concise |
| Presence intent not enabled | “Who’s online?” inaccurate | Enable intent in Developer Portal + code |
| CDN image URLs expire | Broken panel images | Use stable image hosting |
| Bot restart drops non-persistent views | Buttons stop working | Use persistent `custom_id`s and re-register views |
| Missing database for settlement | Settlement feature fails | Make DB optional or add connection at deploy |
| Secrets in git history | Token leak | `.gitignore`, rotate tokens, never commit `.env` |

**Verdict — Technical feasibility: Feasible.**

---

## 5. Operational Feasibility

### 5.1 Day-to-Day Operation
- Admins post panels once (or when redesigning)
- Customers self-serve most of the order intake
- Staff respond in a dedicated channel using volunteer buttons
- Moderators intervene mainly for exceptions, pricing confirmation, and ticket closure

### 5.2 Staff Readiness
Staff need short training on:
- Reading role-tagged requests
- Volunteering / withdrawing
- Entering availability time correctly
- Waiting for customer selection before joining

### 5.3 Operational Benefits
- Less copy-paste of order details in DMs
- Clearer audit trail inside ticket channels
- Faster matching when multiple staff are online
- Consistent welcome experience for every join

### 5.4 Operational Constraints
- Requires accurate Discord role setup (game roles, gender roles, mod role)
- Staff must keep DMs open if DM-request feature is used
- Presence-based “online” lists depend on Discord presence data
- Someone must host and monitor the bot process

**Verdict — Operational feasibility: Feasible**, assuming roles and hosting are maintained.

---

## 6. Economic Feasibility

### 6.1 Cost Categories
| Item | Typical cost profile |
|------|----------------------|
| Discord | Free for bot usage within normal limits |
| Development | Mostly one-time (already implemented concept) |
| Hosting | Low monthly cost for a small always-on process; free if run locally with downtime risk |
| Domain / image hosting | Optional, low |
| Database | Optional; free tier or small managed instance |
| Maintenance | Occasional updates when Discord API or server IDs change |

### 6.2 Expected Benefits
- Fewer staff hours spent collecting order details
- Faster response to customers
- Fewer lost or incomplete requests
- Better customer experience → higher conversion / retention potential

### 6.3 Cost–Benefit View
For a community already using Discord, incremental cost is low relative to manual coordination effort. The main investment is initial setup (IDs, roles, hosting) and light ongoing maintenance.

**Verdict — Economic feasibility: Feasible / low cost.**

---

## 7. Schedule Feasibility

| Phase | Activities | Relative effort |
|-------|------------|-----------------|
| Setup | Bot token, intents, invite permissions, role/channel IDs | Short |
| Deploy | Install dependencies, configure `.env`, run process | Short |
| Panel publish | Admins run setup commands in target channels | Short |
| Pilot | Test welcome, order, ticket, volunteer, choose, close | Short–medium |
| Harden | Hosting, logging, optional DB, token hygiene | Medium |
| Iterate | New games, copy changes, analytics | Ongoing |

A first working deployment can be achieved quickly because the core interaction patterns are already defined. Extra time is mainly for environment setup and staff training—not for inventing the product concept.

**Verdict — Schedule feasibility: Feasible.**

---

## 8. Legal, Security, and Risk Feasibility

### 8.1 Security
- Bot token must remain private
- Ticket channels restrict visibility via permission overwrites
- Only ticket owners and moderators should close tickets
- Staff volunteering is restricted by required roles

### 8.2 Privacy
- Order notes and ranks may contain personal preferences; keep tickets private
- Avoid logging sensitive content to public channels
- Follow Discord Terms of Service and community privacy expectations

### 8.3 Platform Dependency
- System depends entirely on Discord availability and API rules
- Feature breakage is possible if Discord changes Components / Intents
- Acceptable risk if Discord is already the community’s primary platform

### 8.4 Overall Risk Level
**Medium-low** for a small-to-medium community; manageable with token hygiene, role discipline, and basic hosting monitoring.

**Verdict — Legal / security feasibility: Acceptable with standard safeguards.**

---

## 9. Alternatives Considered

| Alternative | Pros | Cons |
|-------------|------|------|
| Manual DMs / forms | Simple | Unscalable, inconsistent |
| External website form | Rich UI, easy analytics | Extra hosting; users leave Discord |
| Google Form + sheet | Cheap intake | Weak real-time staff matching inside Discord |
| Third-party ticket bots | Fast setup | Less custom matching / multi-select logic |

The custom Discord bot is the best fit when the community already lives in Discord and needs **interactive matching**, not just form collection.

---

## 10. Conclusion and Recommendation

### 10.1 Summary of Findings
| Feasibility area | Result |
|------------------|--------|
| Technical | Feasible |
| Operational | Feasible |
| Economic | Feasible (low ongoing cost) |
| Schedule | Feasible |
| Legal / security | Acceptable with controls |

### 10.2 Recommendation
**Proceed with implementation / deployment** of the Discord companion booking bot.

It is a practical automation layer for:
- Welcoming members
- Structured service ordering
- Private ticket handling
- Role-aware staff volunteering and customer selection

### 10.3 Suggested Next Steps
1. Confirm Discord intents, roles, categories, and channel IDs
2. Deploy the bot on a reliable host
3. Publish welcome and order panels
4. Run a pilot with staff on a few real requests
5. Optionally add database-backed settlement tracking and monitoring alerts

---

## Appendix A — Feature Checklist

- [x] Auto welcome on member join  
- [x] Admin welcome panel with get-started + online staff  
- [x] DM request to selected staff  
- [x] Admin service-request panel  
- [x] Multi-step order UI (service → device → preferences → modal)  
- [x] Duplicate-ticket prevention  
- [x] Private ticket channel creation  
- [x] Confirm details → staff notification  
- [x] Staff volunteer + availability time  
- [x] Customer multi-select of staff  
- [x] Permission grant to chosen staff  
- [x] Ticket close + delayed channel delete  
- [x] Persistent panel buttons after restart  

## Appendix B — Glossary

| Term | Meaning |
|------|---------|
| Cog | A modular feature package loaded by the bot |
| View | A set of Discord UI components (buttons / selects) |
| Modal | A pop-up form for short text input |
| Ticket | Private channel for one customer request |
| Persistent view | Buttons that keep working after bot restart via fixed IDs |
| Volunteer | Staff member who offers to take a request |

---

*End of System Feasibility Study*
