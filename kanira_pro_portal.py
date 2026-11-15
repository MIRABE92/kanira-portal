import json, os, urllib.parse
from datetime import datetime
import pandas as pd
import requests
import streamlit as st

st.set_page_config(page_title="Kanira Advisor | Institutional Wealth & Derivatives Portal", page_icon="🏛️", layout="wide")

BRAND_NAME = "Kanira Advisor"
PARTNER_TAG = "Authorized Business Partner — Mirae Asset Sharekhan • Mumbai & Mira-Bhayandar"
WHATSAPP_NO = "919702767077"
GSHEET_WEBHOOK = "https://script.google.com/macros/s/AKfycbwJQqdo0iVqeKRdGnAkyfK4j0P63N8dPgUXuTowqsZMhxiJk1Dy8nwl23e_ngctunU/exec"
PORTAL_URL = "https://streamlit.app"
USER_DB_FILE = "kanira_users.json"

st.markdown('''<style>
.stApp { background-color: #f4f7fb; }
.hero-banner {
    background: linear-gradient(135deg, #091a32 0%, #13386c 65%, #f37021 145%);
    padding: 2.2rem 2.5rem; border-radius: 16px; color: #ffffff;
    box-shadow: 0 12px 30px rgba(9, 26, 50, 0.22); margin-bottom: 1.4rem;
}
.hero-pill {
    display: inline-block; background: rgba(255,255,255,0.15); border: 1px solid rgba(255,255,255,0.3);
    padding: 4px 14px; border-radius: 20px; font-size: 0.8rem; font-weight: 600; letter-spacing: 0.6px; margin-bottom: 0.6rem;
}
.hero-h1 { font-size: 2.2rem; font-weight: 800; margin: 0.2rem 0; line-height: 1.2; }
.hero-p { font-size: 1.02rem; opacity: 0.92; margin: 0.4rem 0 0 0; }
.glass-card {
    background: #ffffff; border: 1px solid #e2e8f0; border-top: 4px solid #f37021;
    border-radius: 12px; padding: 1.2rem; box-shadow: 0 4px 14px rgba(15, 23, 42, 0.05); height: 100%;
}
.glass-card h4 { color: #091a32; margin: 0 0 0.45rem 0; font-size: 1.05rem; font-weight: 700; }
.glass-card p { color: #475569; font-size: 0.88rem; margin: 0; line-height: 1.45; }
div[data-testid="stForm"] {
    background: #ffffff; border: 1px solid #cbd5e1; border-radius: 14px;
    padding: 1.4rem; box-shadow: 0 6px 20px rgba(15, 23, 42, 0.06);
}
</style>''', unsafe_allow_html=True)

def make_wa_link(phone, message):
    clean_phone = "".join(ch for ch in str(phone) if ch.isdigit())
    encoded_msg = urllib.parse.quote(message)
    if clean_phone:
        return "https://whatsapp.com" + clean_phone + "&text=" + encoded_msg
    return "https://whatsapp.com" + encoded_msg

DEFAULT_USERS = {
    "admin": {"pass": "kanira2026", "role": "Advisor Admin", "name": "Kanira Advisory Desk", "phone": WHATSAPP_NO, "active": True},
    "client": {"pass": "hni2026", "role": "HNI Wealth Client", "name": "Privileged HNI Client", "phone": "", "active": True}
}

def load_users():
    users = dict(DEFAULT_USERS)
    if GSHEET_WEBHOOK.startswith("https://"):
        try:
            rows = requests.get(GSHEET_WEBHOOK + "?sheet=Users", timeout=6).json()
            for r in rows[1:]:
                if len(r) >= 4 and str(r).strip():
                    u = str(r).strip().lower()
                    users[u] = {"pass": str(r), "role": str(r), "name": str(r), "phone": str(r) if len(r) > 4 else "", "active": True}
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

def save_user(uname, uinfo):
    if GSHEET_WEBHOOK.startswith("https://"):
        try:
            requests.post(GSHEET_WEBHOOK, json={"sheet": "Users", "action": "append", "row": [uname, uinfo["pass"], uinfo["role"], uinfo["name"], uinfo["phone"], "TRUE"]}, timeout=6)
        except Exception:
            pass
    cur = load_users()
    cur[uname] = uinfo
    with open(USER_DB_FILE, "w", encoding="utf-8") as f:
        json.dump(cur, f, indent=2)

def save_lead(name, phone, service):
    ts = datetime.now().strftime("%Y-%m-%d %H:%M")
    if GSHEET_WEBHOOK.startswith("https://"):
        try:
            requests.post(GSHEET_WEBHOOK, json={"sheet": "Leads", "action": "append", "row": [ts, name, phone, service]}, timeout=6)
        except Exception:
            pass
    pd.DataFrame([{"Timestamp": ts, "Name": name, "Phone": phone, "Interest": service}]).to_csv("kanira_leads.csv", mode="a", header=not os.path.exists("kanira_leads.csv"), index=False)

users_db = load_users()
if "auth_user" not in st.session_state:
    st.session_state.auth_user = None

if not st.session_state.auth_user:
    st.markdown(f'''<div class="hero-banner">
        <div class="hero-pill">SEBI-REGISTERED SUB-BROKER PARTNER • INSTITUTIONAL ANALYTICS SUITE</div>
        <div class="hero-h1">🏛️ {BRAND_NAME} — Wealth, Equity & Derivatives Portal</div>
        <div class="hero-p">{PARTNER_TAG}</div>
    </div>''', unsafe_allow_html=True)

    b1, b2, b3, b4 = st.columns(4)
    b1.markdown('<div class="glass-card"><h4>📈 2-Month F&O & Greeks</h4><p>Live NSE futures fair value, calendar spreads, all 5 Option Greeks & custom-days 52W P&L.</p></div>', unsafe_allow_html=True)
    b2.markdown('<div class="glass-card"><h4>🇮🇳 NSE Positional & Valuation</h4><p>Editable P/E & PEG fair price, 200/63/14 MAs, multi-timeframe RSI & FII/DII ownership value.</p></div>', unsafe_allow_html=True)
    b3.markdown('<div class="glass-card"><h4>📊 HNI Portfolio & Stress-Test</h4><p>0-100 Portfolio Health Rating, crash simulations, XIRR & capital-gains tax harvesting.</p></div>', unsafe_allow_html=True)
    b4.markdown('<div class="glass-card"><h4>🛡️ Covered Call & Collar Desk</h4><p>Generate monthly option yield on Demat holdings or lock in zero-cost downside floors.</p></div>', unsafe_allow_html=True)

    st.write("")
    st.link_button("💬 Chat Directly With Kanira Advisory Desk on WhatsApp", make_wa_link(WHATSAPP_NO, "Hello Kanira Advisor, I would like to know more about your Wealth & F&O Portal."))
    st.write("")

    col1, col2 = st.columns([1, 1.25], gap="large")
    with col1:
        with st.form("login_box"):
            st.subheader("🔐 Client & Advisor Sign In")
            u = st.text_input("Username", placeholder="Enter your assigned username").strip().lower()
            p = st.text_input("Password", type="password", placeholder="Enter your password")
            if st.form_submit_button("🚀 Unlock Institutional Terminal", use_container_width=True, type="primary"):
                if u in users_db and users_db[u]["pass"] == p:
                    st.session_state.auth_user = {**users_db[u], "username": u}
                    st.rerun()
                else:
                    st.error("Invalid username or password. Request access on the right.")
            st.caption("Demo Access: `client` / `hni2026` (HNI Tier) • `admin` / `kanira2026` (Advisor)")

    with col2:
        with st.form("lead_box"):
            st.subheader("📞 Request Client Login or Free Portfolio Review")
            l_name = st.text_input("Your Full Name", placeholder="e.g. Rajesh Mehta")
            l_phone = st.text_input("Your Mobile Number (+91)", placeholder="e.g. 9702767077")
            l_srv = st.selectbox("Select Service / Access Tier", ["HNI Wealth Client Login", "F&O Trader Terminal Login", "Free Portfolio Health Rating", "Free Sharekhan Demat Account"])
            submitted = st.form_submit_button("Submit Request & Get WhatsApp Link", use_container_width=True)
        if submitted:
            if l_name and l_phone:
                save_lead(l_name, l_phone, l_srv)
                msg = f"Hello {BRAND_NAME}, I am {l_name} ({l_phone}). Please activate my access for {l_srv}."
                st.success("✅ Request saved! Click the button below to confirm on WhatsApp:")
                st.link_button("📲 Send Confirmation on WhatsApp", make_wa_link(WHATSAPP_NO, msg), type="primary")
            else:
                st.warning("Please fill in both Name and Mobile Number.")
    st.stop()

user = st.session_state.auth_user
with st.sidebar:
    st.markdown(f"### 🏛️ {BRAND_NAME}")
    st.success(f"👤 **{user['name']}**  \nTier: `{user['role']}`")
    if user["role"] == "Advisor Admin":
        with st.expander("👥 Create & Share Client Logins"):
            with st.form("new_client_form"):
                c_name = st.text_input("Client Name")
                c_phone = st.text_input("Client WhatsApp (e.g. 919820012345)")
                c_user = st.text_input("Assign Username").strip().lower()
                c_pass = st.text_input("Assign Password", value="kanira@123")
                c_role = st.selectbox("Role", ["HNI Wealth Client", "F&O Trader", "Advisor Admin"])
                if st.form_submit_button("💾 Save Client Login"):
                    if c_name and c_user and c_pass:
                        save_user(c_user, {"pass": c_pass, "role": c_role, "name": c_name, "phone": c_phone.strip(), "active": True})
                        st.success(f"Saved {c_name}!")
                        st.rerun()
            for uname, uinfo in users_db.items():
                invite = f"Hello {uinfo['name']}, your {BRAND_NAME} Portal login is ready!\nLink: {PORTAL_URL}\nUser: {uname}\nPass: {uinfo['pass']}"
                st.link_button(f"📲 Share Login: {uinfo['name']} ({uname})", make_wa_link(uinfo.get("phone", ""), invite))

    if st.button("🚪 Logout", use_container_width=True):
        st.session_state.auth_user = None
        st.rerun()
    st.divider()

TOOLS = [
    ("nse_positional_pro.py", "🇮🇳 NSE Positional & P/E-PEG Terminal", "Analytics", ["Advisor Admin", "F&O Trader"]),
    ("option_dashboard.py", "📈 2-Month Futures & Option Greeks", "Derivatives", ["Advisor Admin", "F&O Trader", "HNI Wealth Client"]),
    ("hedging_desk.py", "🛡️ HNI Covered Call & Collar Hedging", "Derivatives", ["Advisor Admin", "F&O Trader", "HNI Wealth Client"]),
    ("portfolio_builder.py", "📊 Portfolio Rating & Wealth Builder", "Wealth & HNI", ["Advisor Admin", "HNI Wealth Client"]),
    ("hni_wealth_suite.py", "🏛️ HNI Crash Stress-Test & XIRR", "Wealth & HNI", ["Advisor Admin", "HNI Wealth Client"]),
    ("fast_finance.py", "⚡ Financial Statement & Ratio Engine", "Research", ["Advisor Admin"])
]

nav = {sec: [] for _, _, sec, _ in TOOLS}
for fname, title, sec, roles in TOOLS:
    if user["role"] in roles and os.path.exists(fname):
        nav[sec].append(st.Page(fname, title=title))
nav = {k: v for k, v in nav.items() if v}

if nav:
    st.navigation(nav).run()
else:
    st.info("Portal unlocked! Ensure your tool files (option_dashboard.py, nse_positional_pro.py, etc.) are uploaded in the same repository.")
