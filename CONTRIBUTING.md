# Contributing to Awesome One-Person Company

Thank you for helping keep **Awesome One-Person Company (Hulu–Hilir)** the highest-signal, zero-abandonware playbook for solo founders!

## Strict Inclusion Rules

1. **Must Pass the 30-Day Activity Check:**
   Every repository added MUST have an active code commit (`pushedAt`) within the last **30 days** and must NOT be archived (`isArchived: false`).
2. **Must Provide Direct Solopreneur Leverage:**
   The repository must help a 1-person company execute faster, cut SaaS/LLM costs, automate operations, or acquire/retain customers.
3. **Edit `data/repos.json` Only:**
   Do not edit `README.md`, `README.id.md`, or `GRAVEYARD.md` directly. Instead:
   - Add your entry (with both English `*_en` and Indonesian `*_id` descriptions) to [`data/repos.json`](./data/repos.json).
   - Run `python3 scripts/verify_active.py` to verify the repository via GitHub GraphQL API and regenerate the markdown files.
