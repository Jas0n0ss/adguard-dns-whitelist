# 🛡️ AdGuard DNS Whitelist Rules

> DNS whitelist rules for **Home**, **Enterprise**, and **Hybrid** environments, **automatically updated daily** to fix false positives in AdGuard Home.

[![License: MIT](https://p.ipic.vip/m7b6qe.jpg)](LICENSE)
[![CI/CD Status](https://github.com/jas0n0ss/adguard-dns-whitelist/actions/workflows/update-rules.yml/badge.svg)](https://github.com/jas0n0ss/adguard-dns-whitelist/actions)
[![Last Updated](https://p.ipic.vip/exwdtx.jpg)](https://github.com/jas0n0ss/adguard-dns-whitelist/actions)

This project provides **curated DNS whitelist rules** for AdGuard Home, automatically updated every day to ensure compatibility with streaming, office tools, gaming, and smart devices.

---

## 📚 Rule Files

| File                                                   | Use Case             | Update Mode                           |
| ------------------------------------------------------ | -------------------- | ------------------------------------- |
| [`dns-rules/home.txt`](dns-rules/home.txt)             | Home Network         | Streaming, gaming, IoT                |
| [`dns-rules/enterprise.txt`](dns-rules/enterprise.txt) | Enterprise           | Microsoft 365, DingTalk, Feishu, Zoom |
| [`dns-rules/hybrid.txt`](dns-rules/hybrid.txt)         | Hybrid (Recommended) | Merged from home + enterprise         |

> 💡 **Recommended**: Use `hybrid.txt` for most users.

---

## 🚀 How to Use

### Method 1: Manual Import

1. Go to AdGuard Home (`http://<your-ip>:3000`)
2. Navigate to **Filtering → Whitelist**
3. Paste domains from the `.txt` file
4. Click **Apply**

### Method 2: CLI Download

```bash
##
curl -s https://raw.githubusercontent.com/jas0n0ss/adguard-dns-whitelist/main/dns-rules/hybrid.txt \
     -o /etc/adguard/whitelist.txt
##
sudo systemctl restart AdGuardHome
```
