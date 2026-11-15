pt1 = """import json, os, urllib.parse
from datetime import datetime
import pandas as pd
import requests
import streamlit as st

st.set_page_config(page_title="Kanira Advisor | Institutional Wealth & Derivatives Portal", page_icon="🏛️", layout="wide")

BRAND_NAME = "Kanira Advisor"
PARTNER_TAG = "Authorized Business Partner — Mirae Asset Sharekhan • Mumbai & Mira-Bhayandar"
PORTAL_URL = "https://streamlit.app"
WHATSAPP_NO = "919820000000"  # Replace with your 12-digit WhatsApp number
GSHEET_WEBHOOK = "PASTE_YOUR_GOOGLE_WEB_APP_URL_HERE"
USER_DB_FILE = "kanira_users.json"

st.markdown('''<style>
.hero-box {
    background: linear-gradient(135deg, #0b1f3a 0%, #163a6b 60%, #f37021 140%);
    padding: 2.2rem 2.5rem; border-radius: 14px; color: #ffffff;
    box-shadow: 0 10px 28px rgba(11, 31, 58, 0.22); margin-bottom: 1.5rem;
}
.hero-badge {
    display: inline-block; background: rgba(255,255,255,0.16); border: 1px solid rgba(255,255,255,0.28);
    padding: 4px 14px; border-radius: 20px; font-size: 0.82rem; font-weight: 600; letter-spacing: 0.5px; margin-bottom: 0.6rem;
}
.hero-title { font-size: 2.15rem; font-weight: 800; margin: 0.2rem 0; line-height: 1.2; }
.hero-sub { font-size: 1.02rem; opacity: 0.92; margin-top: 0.4rem; }
.feat-card {
    background: #ffffff; border: 1px solid #e2e8f0; border-top: 4px solid #f37021;
    border-radius: 10px; padding: 1.1rem 1.2rem; box-shadow: 0 4px 12px rgba(0,0,0,0.04); height: 100%;
}
.feat-card h4 { color: #0b1f3a; margin: 0 0 0.4rem 0; font-size: 1.05rem; }
.feat-card p { color: #475569; font-size: 0.88rem; margin: 0; line-height: 1.45; }
div[data-testid="stMetric"] {
    background: #f8fafc; border: 1px solid #e2e8f0; border-left: 4px solid #0b1f3a;
    padding: 12px 16px; border-radius: 8px;
}
</style>''', unsafe_allow_html=True)

DEFAULT_USERS = {
    "admin": {"pass": "kanira2026", "role": "Advisor Admin", "name": "Kanira Advisory Desk", "phone": WHATSAPP_NO, "active": True},
    "client": {"pass": "hni2026", "role": "HNI Wealth Client", "name": "Privileged HNI Client", "phone": "", "active": True}
}

def load_users():
    users = dict(DEFAULT_USERS)
    if GSHEET_WEBHOOK.startswith("https://"):
        try:
            rows = requests.get(f"{GSHEET_WEBHOOK}?sheet=Users", timeout=8).json()
            for r in rows[1:]:
                if len(r) >= 4 and str(r).strip():
                    u = str(r).strip().lower()
                    users[u] = {"pass": str(r), "role": str(r), "name": str(r), "phone": str(r) if len(r) > 4 else "", "active": str(r).upper() != "FALSE" if len(r) > 5 else True}
            return users
        except Exception:
            pass
    if os.path.exists(USER_DB_FILE):
        try:
            with open(USER_DB_FILE, "r", encoding="utf-8") as f:
                users.update(json.load(f))
        except Exception:
            pass
    return users

def save_new_user(uname, uinfo):
    if GSHEET_WEBHOOK.startswith("https://"):
        try:
            requests.post(GSHEET_WEBHOOK, json={"sheet": "Users", "action": "append", "row": [uname, uinfo["pass"], uinfo["role"], uinfo["name"], uinfo["phone"], "TRUE"]}, timeout=8)
        except Exception:
            pass
    cur = load_users()
    cur[uname] = uinfo
    with open(USER_DB_FILE, "w", encoding="utf-8") as f:
        json.dump(cur, f, indent=2)

def save_lead(name, phone, interest):
    ts = datetime.now().strftime("%Y-%m-%d %H:%M")
    if GSHEET_WEBHOOK.startswith("https://"):
        try:
            requests.post(GSHEET_WEBHOOK, json={"sheet": "Leads", "action": "append", "row": [ts, name, phone, interest]}, timeout=8)
        except Exception:
            pass
    pd.DataFrame([{"Timestamp": ts, "Name": name, "Phone": phone, "Interest": interest}]).to_csv("kanira_portal_leads.csv", mode="a", header=not os.path.exists("kanira_portal_leads.csv"), index=False)
"""
