#!/usr/bin/env python3
"""
AdGuard DNS Whitelist Generator
Automatically updates home.txt, enterprise.txt, and hybrid.txt
"""

import re
import requests
from pathlib import Path

# --- Configuration ---
OUTPUT_DIR = Path("dns-rules")
OUTPUT_DIR.mkdir(exist_ok=True)

HEADERS = {"User-Agent": "Mozilla/5.0 (compatible; AdGuard-Updater/1.0)"}

# --- Trusted Sources ---
SOURCES = {
    "home_streaming_gaming": [
        "https://raw.githubusercontent.com/AdguardTeam/AdguardFilters/master/GeneralExtensionsFilter/filters.txt",
        "https://raw.githubusercontent.com/AdguardTeam/AdguardFilters/master/SpywareFilter/filters.txt",
        "https://raw.githubusercontent.com/oisd/oisd-domains/master/domains_strict.txt",
    ],
    "enterprise_productivity": [
        "https://learn.microsoft.com/en-us/microsoft-365/enterprise/urls-and-ip-address-ranges?view=o365-worldwide",
        "https://open.dingtalk.com/document/org/open-api-domain-list",
        "https://www.feishu.cn/hc/zh-cn/articles/360041195034",
    ]
}

# --- Manual Curated Domains ---
MANUAL_HOME = {
    "*.youtube.com",
    "*.ytimg.com",
    "*.googlevideo.com",
    "*.ggpht.com",
    "*.netflix.com",
    "*.nflximg.com",
    "*.nflxvideo.net",
    "*.disneyplus.com",
    "*.steampowered.com",
    "*.steamstatic.com",
    "*.xboxlive.com",
    "*.playstation.com",
    "*.nintendo.com",
    "*.mi.com",
    "*.xiaomi.com",
    "*.apple.com",
    "*.icloud.com",
    "*.tuya.com",
    "*.smartlife.cloud",
}

MANUAL_ENTERPRISE = {
    "*.office.com",
    "*.office.net",
    "*.microsoftonline.com",
    "*.sharepoint.com",
    "*.onedrive.com",
    "*.outlook.com",
    "*.teams.microsoft.com",
    "*.skype.com",
    "*.live.com",
    "*.dingtalk.com",
    "*.alibaba.com",
    "*.feishu.cn",
    "*.larksuite.com",
    "*.zoom.us",
    "*.zoom.com",
    "*.webex.com",
    "*.cisco.com",
    "*.google.com",
    "*.gstatic.com",
    "*.googleapis.com",
    "*.slack.com",
    "*.dropbox.com",
}

def fetch_content(url: str) -> str:
    try:
        resp = requests.get(url, headers=HEADERS, timeout=15)
        resp.raise_for_status()
        return resp.text
    except Exception as e:
        print(f"⚠️ Failed to fetch {url}: {e}")
        return ""

def extract_domains_from_adguard(text: str) -> set:
    domains = set()
    matches = re.findall(r'\|\|([a-zA-Z0-9.-]+)\^', text)
    domains.update(f"*.{d}" for d in matches if d and not d.startswith('www.'))
    return domains

def extract_domains_from_oisd(text: str) -> set:
    domains = set()
    for line in text.splitlines():
        line = line.strip()
        if line and not line.startswith('#'):
            domain = line.split()[0] if ' ' in line else line
            if '.' in domain and not domain.startswith('www.'):
                domains.add(f"*.{domain}")
    return domains

def extract_domains_from_html(text: str) -> set:
    domains = set()
    patterns = [
        r'(?:microsoft|office|sharepoint|outlook|teams)[a-zA-Z0-9.-]*\.[a-zA-Z]+',
        r'(?:dingtalk|feishu|larksuite|zoom|webex)[a-zA-Z0-9.-]*\.[a-zA-Z]+'
    ]
    for pattern in patterns:
        matches = re.findall(pattern, text, re.IGNORECASE)
        domains.update(f"*.{m}" for m in matches)
    return domains

def clean_domain(d: str) -> str:
    d = d.strip().lower()
    if not d.startswith('*.'):
        d = f"*.{d}"
    return d

def save_rules(domains: set, filepath: Path):
    cleaned = sorted(set(clean_domain(d) for d in domains if d.strip()))
    filepath.write_text('\n'.join(cleaned) + '\n', encoding='utf-8')
    print(f"✅ Saved {len(cleaned)} domains to {filepath}")

def main():
    print("🔍 Starting DNS whitelist update...")

    home_domains = set(MANUAL_HOME)
    enterprise_domains = set(MANUAL_ENTERPRISE)

    # Fetch from AdGuard & OISD
    for url in SOURCES["home_streaming_gaming"]:
        content = fetch_content(url)
        if "oisd" in url:
            home_domains.update(extract_domains_from_oisd(content))
        else:
            home_domains.update(extract_domains_from_adguard(content))

    # Fetch from Microsoft Docs
    m365_content = fetch_content(SOURCES["enterprise_productivity"][0])
    m365_domains = re.findall(
        r'([a-zA-Z0-9.-]*\.(microsoft|office|sharepoint|outlook|teams)\.[a-zA-Z]+)',
        m365_content, re.IGNORECASE)
    enterprise_domains.update(f"*.{match[0]}" for match in m365_domains)

    # Fetch from DingTalk/Feishu
    for url in SOURCES["enterprise_productivity"][1:3]:
        content = fetch_content(url)
        enterprise_domains.update(re.findall(r'"?domain"?\s*[:=]\s*"([a-zA-Z0-9.-]+)"', content))

    # Save Files
    save_rules(home_domains, OUTPUT_DIR / "home.txt")
    save_rules(enterprise_domains, OUTPUT_DIR / "enterprise.txt")
    save_rules(home_domains | enterprise_domains, OUTPUT_DIR / "hybrid.txt")

    print("🎉 Whitelist update completed!")

if __name__ == "__main__":
    main()
