from flask import Flask, render_template, request
import sqlite3, re, requests, os

app = Flask(__name__)
DB_FILE = "database.db"

def init_db():
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS scans (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        url TEXT,
        risk_score INTEGER,
        threats TEXT
    )''')
    conn.commit()
    conn.close()

def scan_url(url):
    threats = []
    risky_keywords = ['login', 'secure', 'verify', 'free', 'bonus', 'bitcoin', 'auth', 'password',
        # Financial / Scam
        'banking', 'account', 'credit', 'loan', 'pay', 'money', 'transfer', 'win', 'prize',
        # Phishing / Fake
        'update', 'confirm', 'support', 'customer', 'service', 'official', 'signin',
        # Malware / Exploits
        'download', 'exe', 'install', 'setup', 'update-now', 'hack', 'exploit', 'crack', 'keygen',
        # Dark Web / Deep Web URLs
        'onion', 'tor', 'darkweb', 'deepweb', 'hidden', 'blackmarket', 'drug', 'weapon', 'silkroad',
        'marketplace', 'hitman', 'counterfeit', 'illegal', 'scam', 'fraud', 'porn', 'xxx', 'sex',
        # Cryptocurrency / Laundering
        'crypto', 'ethereum', 'btc', 'wallet', 'exchange', 'mining', 'cashout', 'launder']
    score = 0

    if not re.match(r'^https?://', url):
        threats.append("Invalid URL format (missing http:// or https://)")
        score += 50

    for keyword in risky_keywords:
        if keyword in url.lower():
            threats.append(f"Suspicious keyword: {keyword}")
            score += 10

    try:
        resp = requests.head(url, timeout=3)
        if 'Server' not in resp.headers:
            threats.append("Missing Server header in response")
            score += 5
    except Exception as e:
        threats.append("URL unreachable or timed out, assuming high risk. Do not visit!")
        score += 40

    if score > 100:
        score = 100
    return score, ', '.join(threats) if threats else 'No threats detected'

@app.route('/', methods=['GET', 'POST'])
def index():
    result = None
    if request.method == 'POST':
        url = request.form.get('url', '').strip()
        score, threats = scan_url(url)
        conn = sqlite3.connect(DB_FILE)
        c = conn.cursor()
        c.execute('INSERT INTO scans (url, risk_score, threats) VALUES (?, ?, ?)', (url, score, threats))
        conn.commit()
        conn.close()
        result = {'url': url, 'score': score, 'threats': threats}
    return render_template('index.html', result=result)

@app.route('/history')
def history():
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()
    c.execute('SELECT url, risk_score, threats FROM scans ORDER BY id DESC LIMIT 50')
    rows = c.fetchall()
    conn.close()
    return {'history': [{'url': r[0], 'score': r[1], 'threats': r[2]} for r in rows]}

if __name__ == '__main__':
    init_db()
    app.run(debug=True, host='127.0.0.1', port=5000)
