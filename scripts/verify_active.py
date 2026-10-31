#!/usr/bin/env python3
"""
Automated 30-Day Activity Verifier & README Generator
for ridloabelian/awesome-one-person-company.

Zero external dependencies (uses Python stdlib + `gh` CLI or GITHUB_TOKEN).
"""

import datetime
import json
import os
import subprocess
import urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DATA_FILE = ROOT / "data" / "repos.json"
VERIFIED_FILE = ROOT / "data" / "verified_status.json"
README_EN = ROOT / "README.md"
README_ID = ROOT / "README.id.md"
GRAVEYARD_MD = ROOT / "GRAVEYARD.md"


def format_stars(count: int) -> str:
    if count >= 1000:
        val = count / 1000.0
        return f"{val:.1f}k" if val < 100 else f"{int(round(val))}k"
    return str(count)


def run_graphql(query: str) -> dict:
    token = os.environ.get("GITHUB_TOKEN")
    if token:
        req = urllib.request.Request(
            "https://api.github.com/graphql",
            data=json.dumps({"query": query}).encode("utf-8"),
            headers={
                "Authorization": f"Bearer {token}",
                "Content-Type": "application/json",
                "User-Agent": "awesome-one-person-company-verifier",
            },
            method="POST",
        )
        with urllib.request.urlopen(req, timeout=30) as resp:
            return json.loads(resp.read().decode("utf-8"))
    else:
        proc = subprocess.run(
            ["gh", "api", "graphql", "-f", f"query={query}"],
            capture_output=True,
            text=True,
            check=False,
        )
        if not proc.stdout:
            raise RuntimeError(f"GraphQL query failed: {proc.stderr}")
        return json.loads(proc.stdout)


def fetch_repo_metadata(repo_names: list[str]) -> dict[str, dict]:
    results = {}
    batch_size = 35
    for start in range(0, len(repo_names), batch_size):
        batch = repo_names[start : start + batch_size]
        parts = []
        alias_map = {}
        for idx, full_name in enumerate(batch):
            owner, name = full_name.split("/", 1)
            alias = f"r{idx}"
            alias_map[alias] = full_name
            parts.append(
                f'{alias}: repository(owner: "{owner}", name: "{name}") {{ '
                f"nameWithOwner url stargazerCount pushedAt isArchived "
                f"primaryLanguage {{ name }} licenseInfo {{ spdxId }} description }}"
            )
        query = "query { " + " ".join(parts) + " }"
        payload = run_graphql(query)
        data = payload.get("data") or {}
        for alias, orig_name in alias_map.items():
            node = data.get(alias)
            if node:
                results[orig_name] = node
    return results


def build_readme_en(
    categories_out: list[dict],
    graveyard: list[dict],
    verified_date: str,
    cutoff_date: str,
    total_active: int,
) -> str:
    lines = [
        '<div align="center">',
        "",
        "# 🚀 Awesome One-Person Company (Hulu–Hilir)",
        "",
        "**The Living, End-to-End Open-Source & Agentic AI Stack for Solopreneurs, Indie Hackers, and One-Person Companies.**",
        "",
        f"[![Active Repositories](https://img.shields.io/badge/Active_Repos_(%3C30d)-{total_active}_Verified-10b981?style=for-the-badge)](https://github.com/ridloabelian/awesome-one-person-company)",
        f"[![Last Audit](https://img.shields.io/badge/Last_Auto_Audit-{verified_date}-3b82f6?style=for-the-badge)](./data/verified_status.json)",
        "[![Agent Skill Ready](https://img.shields.io/badge/Agent_Skill-SKILL.md_Included-8b5cf6?style=for-the-badge)](./SKILL.md)",
        "[![License: MIT](https://img.shields.io/badge/License-MIT-f59e0b?style=for-the-badge)](./LICENSE)",
        "",
        "**[🌐 English](./README.md) | [🇮🇩 Bahasa Indonesia](./README.id.md) | [🪦 Stale Graveyard](./GRAVEYARD.md) | [🤖 Agent Skill (`SKILL.md`)](./SKILL.md) | [🐳 $5/mo VPS Stack](./stacks/lean-solopreneur-vps/)**",
        "",
        "</div>",
        "",
        "---",
        "",
        "## ⚡ Why This Repository Exists",
        "",
        "Most `awesome-indie` or `solopreneur` lists on GitHub suffer from three fatal flaws:",
        "1. **Full of Abandonware:** Half the repositories haven't seen a commit since 2024.",
        "2. **SaaS Subscription Traps:** They recommend $29–$199/mo SaaS tools that bleed solo founders dry before reaching Product-Market Fit.",
        "3. **Missing the 2026 Agentic Stack:** They ignore **AI Agent Harnesses**, **Token Cost-Cutters (60–95% savings)**, **Anti-AI-Slop Design Skills**, and **Programmatic Video Engines**.",
        "",
        "> [!IMPORTANT]",
        f"> **Strict 30-Day Maintenance Guarantee:** Every repository listed below is automatically audited via GitHub GraphQL API. Only repositories with active code pushes in the last **30 days** (since `{cutoff_date}`) survive on the main list. Stale projects are automatically moved to [GRAVEYARD.md](./GRAVEYARD.md).",
        "",
        "---",
        "",
        "## 🗺️ End-to-End One-Person Company Architecture (Hulu → Hilir)",
        "",
        "```mermaid",
        "flowchart TD",
        '    subgraph S1["1. Upstream: Market Intel & Stealth Scraping"]',
        '        A1["Agent-Reach / last30days-skill"] --> A2["Firecrawl / Scrapling / CloakBrowser"]',
        '        A2 --> A3["Google Maps Scraper / changedetection.io"]',
        "    end",
        "",
        '    subgraph S2["2. Virtual AI Workforce & Coding Harnesses"]',
        '        B1["gstack (Virtual CEO/PM/QA)"] --> B2["Orca / Paperclip (Fleet Manager)"]',
        '        B2 --> B3["Claude Code / OpenCode / OpenClaw / Hermes"]',
        "    end",
        "",
        '    subgraph S3["3. Product Build & Anti-AI-Slop UI"]',
        '        C1["Open-SaaS + PocketBase / Supabase"] --> C2["Shadcn + MagicUI + Open-Design"]',
        '        C2 --> C3["Anti-Slop Skills: taste-skill / impeccable / ui-ux-pro-max"]',
        "    end",
        "",
        '    subgraph S4["4. Zero-Cost AI Ops (60-95% Token Savings)"]',
        '        D1["OmniRoute / LiteLLM / 9router"] --> D2["Caveman / RTK / Headroom / Context-Mode"]',
        '        D2 --> D3["claude-mem / Mem0 (Persistent Memory)"]',
        "    end",
        "",
        '    subgraph S5["5. Content Factory & Programmatic Video"]',
        '        E1["HyperFrames / Remotion (Code-to-Video)"] --> E2["MoneyPrinterTurbo / OpenMontage / OpenShorts"]',
        '        E2 --> E3["Recordly / Cap + VoiceStudio (Local ElevenLabs)"]',
        "    end",
        "",
        '    subgraph S6["6. Go-To-Market, SEO/GEO & WhatsApp CRM"]',
        '        F1["Open-SEO + GEO-SEO + Humanizer"] --> F2["Postiz (Socials) + Listmonk (Email)"]',
        '        F2 --> F3["Twenty CRM + WAHA / DeskcommCRM (WhatsApp AI)"]',
        "    end",
        "",
        '    subgraph S7["7. Downstream: Self-Hosted PaaS, Security & Billing"]',
        '        G1["Coolify / Dokploy ($5 VPS) + n8n"] --> G2["Strix / Shannon (AI Pentester)"]',
        '        G2 --> G3["Polar.sh / PayListen + Umami / PostHog + Chatwoot"]',
        "    end",
        "",
        "    S1 --> S2 --> S3 --> S4 --> S5 --> S6 --> S7",
        "```",
        "",
        "---",
        "",
        "## 📑 Table of Contents",
        "",
    ]

    for cat in categories_out:
        anchor = (
            cat["title_en"]
            .lower()
            .replace(":", "")
            .replace("&", "")
            .replace("/", "")
            .replace("(", "")
            .replace(")", "")
            .replace(".", "")
            .replace(",", "")
            .replace("  ", " ")
            .strip()
            .replace(" ", "-")
        )
        lines.append(f"- [{cat['title_en']}](#{anchor}) ({len(cat['active'])} active repos)")

    lines.extend(
        [
            "- [💡 The Ultimate $5/mo Lean VPS Stack](#-the-ultimate-5mo-lean-vps-stack)",
            "- [🤖 Use as an AI Agent Skill](#-use-as-an-ai-agent-skill)",
            "- [🪦 Eliminated Stale Repositories (>30 Days Inactive)](#-eliminated-stale-repositories-30-days-inactive)",
            "",
            "---",
            "",
        ]
    )

    for cat in categories_out:
        lines.append(f"## {cat['title_en']}")
        lines.append("")
        lines.append(f"_{cat['desc_en']}_")
        lines.append("")
        lines.append("| Repository | Role | Stars | Last Push | Status | Why It's Essential for a 1-Person Company |")
        lines.append("| :--- | :--- | :---: | :---: | :---: | :--- |")
        for item in cat["active"]:
            r_name = item["nameWithOwner"]
            r_url = item["url"]
            stars = format_stars(item["stargazerCount"])
            pushed = item["pushedAt"][:10]
            lines.append(
                f"| **[{r_name}]({r_url})** | `{item['role_en']}` | ⭐ {stars} | `{pushed}` | 🟢 Active | {item['why_en']} |"
            )
        lines.append("")

    lines.extend(
        [
            "---",
            "",
            "## 💡 The Ultimate $5/mo Lean VPS Stack",
            "",
            "Don't fall into over-engineering paralysis. Run your entire One-Person Company on **1 Hetzner / DigitalOcean VPS ($5–$8/mo)** using this battle-tested combination (ready-to-deploy template in [`stacks/lean-solopreneur-vps/`](./stacks/lean-solopreneur-vps/)):",
            "",
            "1. **Control Plane & PaaS:** `coollabsio/coolify` or `Dokploy/dokploy` (manages SSL, previews, and 1-click containers)",
            "2. **Product Core:** `wasp-lang/open-saas` or `Next.js + shadcn/ui` + `supabase/supabase` / `InsForge/InsForge`",
            "3. **AI Workforce & Cost Guard:** `anthropics/claude-code` + `garrytan/gstack` + `JuliusBrussee/caveman` + `cheaper-inference/OmniRoute`",
            "4. **Anti-Slop Design Layer:** `Leonxlnx/taste-skill` + `pbakaus/impeccable` + `nextlevelbuilder/ui-ux-pro-max-skill`",
            "5. **Back-Office Automation:** `n8n-io/n8n` + `czlonkowski/n8n-mcp`",
            "6. **Growth & Distribution:** `gitroomhq/postiz-app` (socials) + `knadh/listmonk` (email via AWS SES) + `devlikeapro/waha` (WhatsApp)",
            "7. **Analytics, Monitoring & Billing:** `umami-software/umami` + `louislam/uptime-kuma` + `polarsource/polar`",
            "",
            "---",
            "",
            "## 🤖 Use as an AI Agent Skill",
            "",
            "This repository includes a standard [`SKILL.md`](./SKILL.md) so your AI coding agent (**Google Antigravity, Claude Code, Codex, Cursor, OpenClaw, or Hermes Agent**) can act as your **Solopreneur Stack Architect**.",
            "",
            "```bash",
            "# Clone directly into your agent skills directory",
            "git clone https://github.com/ridloabelian/awesome-one-person-company.git ~/.agents/skills/awesome-one-person-company",
            "```",
            "",
            "---",
            "",
            "## 🪦 Eliminated Stale Repositories (>30 Days Inactive)",
            "",
            f"To keep this list 100% high-signal, our automated verifier ([`scripts/verify_active.py`](./scripts/verify_active.py)) automatically removes any repository without a code push since `{cutoff_date}`:",
            "",
            "| Repository | Former Role | Stars | Last Push | Status |",
            "| :--- | :--- | :---: | :---: | :---: |",
        ]
    )

    for g in graveyard:
        st_en = "🔴 Archived on GitHub" if g.get("isArchived") else "🔴 Stale (>30d)"
        lines.append(
            f"| ~~[{g['nameWithOwner']}]({g['url']})~~ | {g['role_en']} | ⭐ {format_stars(g['stargazerCount'])} | `{g['pushedAt'][:10]}` | {st_en} |"
        )

    lines.extend(
        [
            "",
            "See [GRAVEYARD.md](./GRAVEYARD.md) for details and active replacements.",
            "",
            "---",
            "",
            "## 🤝 Contributing & Automated Verification",
            "",
            "To add a repository, edit [`data/repos.json`](./data/repos.json) and run:",
            "",
            "```bash",
            "python3 scripts/verify_active.py",
            "```",
            "",
            "Every pull request is automatically checked to ensure the repository is actively maintained within the last 30 days.",
            "",
            "## 📄 License",
            "",
            "MIT © [Ridlo Abelian](https://github.com/ridloabelian)",
            "",
        ]
    )
    return "\n".join(lines)


def build_readme_id(
    categories_out: list[dict],
    graveyard: list[dict],
    verified_date: str,
    cutoff_date: str,
    total_active: int,
) -> str:
    lines = [
        '<div align="center">',
        "",
        "# 🚀 Awesome One-Person Company (Hulu–Hilir) — Edisi Bahasa Indonesia",
        "",
        "**Kurasi Repositori GitHub Open-Source & Agentic AI Hulu-ke-Hilir untuk Solopreneur, Indie Hacker, dan One-Person Company.**",
        "",
        f"[![Active Repositories](https://img.shields.io/badge/Repo_Aktif_(%3C30_Hari)-{total_active}_Terverifikasi-10b981?style=for-the-badge)](https://github.com/ridloabelian/awesome-one-person-company)",
        f"[![Last Audit](https://img.shields.io/badge/Audit_Otomatis_Terakhir-{verified_date}-3b82f6?style=for-the-badge)](./data/verified_status.json)",
        "[![Agent Skill Ready](https://img.shields.io/badge/Agent_Skill-SKILL.md_Siap_Pakai-8b5cf6?style=for-the-badge)](./SKILL.md)",
        "[![License: MIT](https://img.shields.io/badge/Lisensi-MIT-f59e0b?style=for-the-badge)](./LICENSE)",
        "",
        "**[🌐 English](./README.md) | [🇮🇩 Bahasa Indonesia](./README.id.md) | [🪦 Kuburan Repo Stale](./GRAVEYARD.md) | [🤖 Agent Skill (`SKILL.md`)](./SKILL.md) | [🐳 Stack VPS $5/bln](./stacks/lean-solopreneur-vps/)**",
        "",
        "</div>",
        "",
        "---",
        "",
        "## ⚡ Kenapa Repositori Ini Dibuat?",
        "",
        "Mayoritas daftar `awesome-indie` atau `solopreneur` di GitHub memiliki 3 kelemahan fatal:",
        "1. **Penuh Bangkai Repo (*Abandonware*):** Banyak repo yang sudah tidak di-update sejak 2024–2025.",
        "2. **Jebakan Langganan SaaS Mahal:** Merekomendasikan layanan berbayar $29–$199/bulan yang menguras modal sebelum produk mencapai *Product-Market Fit*.",
        "3. **Ketinggalan Era Agentic AI 2026:** Tidak mencakup **Agent Harnesses**, **Kompresor Token (hemat 60–95%)**, **Skill Desain Anti-AI-Slop**, **Pabrik Video Otomatis**, maupun **Automasi WhatsApp & QRIS**.",
        "",
        "> [!IMPORTANT]",
        f"> **Jaminan Kurasi Ketat 30 Hari Terakhir:** Setiap repositori di daftar ini diaudit otomatis menggunakan GitHub GraphQL API. Hanya repo yang memiliki *commit/push* aktif dalam **30 hari terakhir** (sejak `{cutoff_date}`) yang bertahan di daftar utama. Repo yang tidak terawat otomatis dipindahkan ke [GRAVEYARD.md](./GRAVEYARD.md).",
        "",
        "---",
        "",
    ]

    for cat in categories_out:
        lines.append(f"## {cat['title_id']}")
        lines.append("")
        lines.append(f"_{cat['desc_id']}_")
        lines.append("")
        lines.append("| Repositori | Peran Bisnis | Stars | Push Terakhir | Status | Kenapa Wajib untuk One-Person Company |")
        lines.append("| :--- | :--- | :---: | :---: | :---: | :--- |")
        for item in cat["active"]:
            r_name = item["nameWithOwner"]
            r_url = item["url"]
            stars = format_stars(item["stargazerCount"])
            pushed = item["pushedAt"][:10]
            lines.append(
                f"| **[{r_name}]({r_url})** | `{item['role_id']}` | ⭐ {stars} | `{pushed}` | 🟢 Aktif | {item['why_id']} |"
            )
        lines.append("")

    lines.extend(
        [
            "---",
            "",
            "## 💡 Rekomendasi \"The $5/mo Lean VPS Stack\" (Siap Pakai)",
            "",
            "Jangan terjebak *over-engineering*. Jalankan seluruh operasional *One-Person Company* di **1 VPS Hetzner / DigitalOcean ($5–$8/bulan)** menggunakan kombinasi ini (file `docker-compose.yml` tersedia di [`stacks/lean-solopreneur-vps/`](./stacks/lean-solopreneur-vps/)):",
            "",
            "1. **Deployment & PaaS:** `coollabsio/coolify` atau `Dokploy/dokploy`",
            "2. **Pondasi Produk:** `wasp-lang/open-saas` + `supabase/supabase` / `InsForge/InsForge`",
            "3. **Tim AI & Penghemat Token:** `garrytan/gstack` + `JuliusBrussee/caveman` + `cheaper-inference/OmniRoute`",
            "4. **Penangkal Desain AI Generik:** `Leonxlnx/taste-skill` + `pbakaus/impeccable` + `nextlevelbuilder/ui-ux-pro-max-skill`",
            "5. **Otomasi Back-Office:** `n8n-io/n8n` + `czlonkowski/n8n-mcp`",
            "6. **Distribusi & CRM WhatsApp:** `gitroomhq/postiz-app` + `knadh/listmonk` + `devlikeapro/waha` / `melgarafael/DeskcommCRM`",
            "7. **Analitik, Monitoring & Pembayaran:** `umami-software/umami` + `louislam/uptime-kuma` + `polarsource/polar` (Global) / `fajarseptiansyah/PayListen` (QRIS Lokal)",
            "",
            "---",
            "",
            "## 🪦 Repo yang Dieliminasi (>30 Hari Tidak Dirawat)",
            "",
            "| Repositori | Peran Sebelumnya | Stars | Push Terakhir | Status |",
            "| :--- | :--- | :---: | :---: | :---: |",
        ]
    )

    for g in graveyard:
        st_id = "🔴 Diarsipkan di GitHub" if g.get("isArchived") else "🔴 Stale (>30h)"
        lines.append(
            f"| ~~[{g['nameWithOwner']}]({g['url']})~~ | {g['role_id']} | ⭐ {format_stars(g['stargazerCount'])} | `{g['pushedAt'][:10]}` | {st_id} |"
        )

    lines.extend(
        [
            "",
            "Lihat [GRAVEYARD.md](./GRAVEYARD.md) untuk daftar lengkap repo yang dieliminasi beserta penggantinya.",
            "",
            "## 📄 Lisensi",
            "",
            "MIT © [Ridlo Abelian](https://github.com/ridloabelian)",
            "",
        ]
    )
    return "\n".join(lines)


def build_graveyard_md(graveyard: list[dict], verified_date: str, cutoff_date: str) -> str:
    lines = [
        "# 🪦 Stale Repository Graveyard (>30 Days Inactive)",
        "",
        f"Last automated audit: **{verified_date}** (30-day activity cutoff: `{cutoff_date}`).",
        "",
        "Any repository in [`data/repos.json`](./data/repos.json) whose `pushedAt` timestamp is older than 30 days—or that has been archived by its maintainer—is automatically removed from the main playbook and logged here.",
        "",
        "| Repository | Category | Stars | Last Push | Reason |",
        "| :--- | :--- | :---: | :---: | :--- |",
    ]
    for g in graveyard:
        reason = "Archived" if g.get("isArchived") else f"No push since {g['pushedAt'][:10]} (>30 days)"
        lines.append(
            f"| **[{g['nameWithOwner']}]({g['url']})** | {g['category_en']} | ⭐ {format_stars(g['stargazerCount'])} | `{g['pushedAt'][:10]}` | 🔴 {reason} |"
        )
    lines.append("")
    return "\n".join(lines)


def main():
    config = json.loads(DATA_FILE.read_text(encoding="utf-8"))
    cutoff_days = config.get("cutoff_days", 30)

    all_repo_names = []
    for cat in config["categories"]:
        for r in cat["repos"]:
            all_repo_names.append(r["repo"])

    print(f"Auditing {len(all_repo_names)} repositories via GitHub GraphQL API...")
    metadata = fetch_repo_metadata(all_repo_names)

    # Determine reference 'now' from the newest pushedAt in metadata (or UTC now)
    max_pushed_str = max(
        (m["pushedAt"] for m in metadata.values() if m.get("pushedAt")),
        default=datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
    )
    ref_dt = datetime.datetime.strptime(max_pushed_str[:10], "%Y-%m-%d").date()
    cutoff_dt = ref_dt - datetime.timedelta(days=cutoff_days)
    verified_date = ref_dt.isoformat()
    cutoff_date = cutoff_dt.isoformat()

    categories_out = []
    graveyard = []
    total_active = 0

    for cat in config["categories"]:
        active_list = []
        for entry in cat["repos"]:
            meta = metadata.get(entry["repo"])
            if not meta:
                print(f"WARNING: Could not resolve {entry['repo']}")
                continue
            pushed_date = meta["pushedAt"][:10]
            merged = {
                **entry,
                **meta,
                "category_en": cat["title_en"],
            }
            if pushed_date >= cutoff_date and not meta.get("isArchived", False):
                active_list.append(merged)
                total_active += 1
            else:
                graveyard.append(merged)

        # Sort active repos in each category by stars descending for maximum clarity
        active_list.sort(key=lambda x: x["stargazerCount"], reverse=True)
        categories_out.append(
            {
                "id": cat["id"],
                "title_en": cat["title_en"],
                "title_id": cat["title_id"],
                "desc_en": cat["desc_en"],
                "desc_id": cat["desc_id"],
                "active": active_list,
            }
        )

    VERIFIED_FILE.write_text(
        json.dumps(
            {
                "verified_at": verified_date,
                "cutoff_date": cutoff_date,
                "total_audited": len(all_repo_names),
                "total_active": total_active,
                "total_eliminated": len(graveyard),
                "categories": categories_out,
                "graveyard": graveyard,
            },
            indent=2,
            ensure_ascii=False,
        ),
        encoding="utf-8",
    )

    README_EN.write_text(
        build_readme_en(categories_out, graveyard, verified_date, cutoff_date, total_active),
        encoding="utf-8",
    )
    README_ID.write_text(
        build_readme_id(categories_out, graveyard, verified_date, cutoff_date, total_active),
        encoding="utf-8",
    )
    GRAVEYARD_MD.write_text(
        build_graveyard_md(graveyard, verified_date, cutoff_date),
        encoding="utf-8",
    )

    print(f"Done! Active (<30d): {total_active} | Eliminated (>30d): {len(graveyard)}")
    for g in graveyard:
        print(f"  Eliminated: {g['nameWithOwner']} (last push: {g['pushedAt'][:10]})")


if __name__ == "__main__":
    main()
