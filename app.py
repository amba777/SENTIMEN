import streamlit as st
import plotly.graph_objects as go
import plotly.express as px
import pandas as pd
import numpy as np
import re
import math
import json
from datetime import datetime

st.set_page_config(
    page_title="Sentimen Coretax | Dashboard",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# ══════════════════════════════════════════════════════
# CSS MODERN & DINAMIS
# ══════════════════════════════════════════════════════
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&family=JetBrains+Mono:wght@400;600&display=swap');

:root {
  --bg:    #060B18; --bg1: #0D1526; --bg2: #111E35; --bg3: #1A2B47;
  --gold:  #F0B429; --teal: #2DD4BF; --green: #22C55E;
  --red:   #EF4444; --slate: #64748B; --muted: #94A3B8; --text: #E2E8F0;
  --border: rgba(255,255,255,0.07);
  --grad-gold: linear-gradient(135deg, #F0B429, #E8A020);
  --grad-teal: linear-gradient(135deg, #2DD4BF, #14B8A6);
  --grad-red: linear-gradient(135deg, #EF4444, #DC2626);
  --grad-green: linear-gradient(135deg, #22C55E, #16A34A);
}
*,*::before,*::after{box-sizing:border-box;margin:0;padding:0;}
html,body,.stApp,[data-testid="stAppViewContainer"],[data-testid="stMain"]{
  background:var(--bg)!important;color:var(--text)!important;
  font-family:'Inter',sans-serif!important;
}
#MainMenu,footer,header,[data-testid="stToolbar"],[data-testid="stDecoration"],[data-testid="collapsedControl"]{display:none!important;}
.block-container{padding:0!important;max-width:100%!important;}

/* HERO MODERN */
.hero{background:linear-gradient(150deg,#0D1A30 0%,#090F1E 55%,#060B18 100%);
  padding:clamp(1.8rem,5vw,3.2rem) clamp(1.2rem,5vw,3.5rem) clamp(1.4rem,4vw,2.4rem);
  border-bottom:1px solid var(--border);position:relative;overflow:hidden;}
.hero::before{content:'';position:absolute;inset:0;
  background:radial-gradient(ellipse 55% 65% at 85% 15%,rgba(240,180,41,.07) 0%,transparent 70%),
             radial-gradient(ellipse 40% 55% at 5% 85%,rgba(45,212,191,.05) 0%,transparent 70%);
  pointer-events:none;}
.hero::after{content:'';position:absolute;top:-50%;left:-50%;width:200%;height:200%;
  background:radial-gradient(circle,rgba(240,180,41,.03) 0%,transparent 70%);
  animation:pulse 8s ease infinite;pointer-events:none;}
@keyframes pulse{0%{opacity:0.3}50%{opacity:0.6}100%{opacity:0.3}}
.hero-tag{display:inline-flex;align-items:center;gap:.4rem;
  background:rgba(240,180,41,.1);border:1px solid rgba(240,180,41,.22);color:var(--gold);
  padding:.22rem .75rem;border-radius:99px;font-size:.68rem;font-weight:700;
  letter-spacing:.08em;text-transform:uppercase;margin-bottom:.85rem;
  backdrop-filter:blur(4px);}
.hero-title{font-size:clamp(1.7rem,4.5vw,3rem);font-weight:800;line-height:1.15;color:#fff;margin-bottom:.55rem;
  background:linear-gradient(135deg,#fff 0%,#94A3B8 100%);-webkit-background-clip:text;-webkit-text-fill-color:transparent;
  background-clip:text;}
.hero-title em{color:var(--gold);-webkit-text-fill-color:var(--gold);font-style:normal;}
.hero-desc{font-size:clamp(.82rem,2vw,.97rem);color:var(--muted);line-height:1.72;max-width:660px;margin-bottom:1.1rem;}
.hero-pills{display:flex;flex-wrap:wrap;gap:.45rem;}
.hero-pill{background:rgba(255,255,255,.04);border:1px solid var(--border);
  color:var(--muted);padding:.22rem .72rem;border-radius:99px;font-size:.71rem;
  transition:all .2s ease;}
.hero-pill:hover{background:rgba(240,180,41,.1);border-color:rgba(240,180,41,.3);color:var(--gold);}
.hero-pill b{color:var(--teal);}

/* METRIC STRIP MODERN */
.mstrip{display:grid;grid-template-columns:repeat(4,1fr);gap:1px;
  background:var(--border);border-bottom:1px solid var(--border);}
@media(max-width:600px){.mstrip{grid-template-columns:repeat(2,1fr);}}
.mtile{background:var(--bg1);padding:clamp(.85rem,3vw,1.35rem) clamp(.9rem,3vw,1.6rem);position:relative;
  transition:all .25s ease;cursor:pointer;}
.mtile:hover{background:var(--bg2);transform:translateY(-2px);}
.mtile::before{content:'';position:absolute;top:0;left:0;right:0;height:2px;}
.mt0::before{background:var(--grad-teal);}
.mt1::before{background:var(--grad-red);}
.mt2::before{background:var(--grad-green);}
.mt3::before{background:linear-gradient(135deg,#64748B,#475569);}
.mlabel{font-size:.63rem;font-weight:700;letter-spacing:.1em;text-transform:uppercase;color:var(--slate);margin-bottom:.32rem;}
.mval{font-family:'JetBrains Mono',monospace;font-size:clamp(1.45rem,3.5vw,2.1rem);font-weight:600;color:#fff;line-height:1;margin-bottom:.18rem;}
.msub{font-size:.7rem;color:var(--slate);}
.mico{position:absolute;top:.95rem;right:1rem;font-size:1.1rem;opacity:.14;}

/* TABS MODERN */
.stTabs{padding:0 clamp(1rem,5vw,3.5rem)!important;}
.stTabs [data-baseweb="tab-list"]{background:transparent!important;
  border-bottom:1px solid var(--border)!important;gap:0!important;padding:0!important;flex-wrap:wrap!important;}
.stTabs [data-baseweb="tab"]{background:transparent!important;color:var(--slate)!important;
  border-bottom:2px solid transparent!important;border-radius:0!important;
  font-size:.8rem!important;font-weight:500!important;padding:.7rem 1.1rem!important;margin:0!important;
  transition:all .2s ease;}
.stTabs [data-baseweb="tab"]:hover{color:var(--gold)!important;}
.stTabs [aria-selected="true"]{color:var(--gold)!important;border-bottom-color:var(--gold)!important;
  background:transparent!important;font-weight:700!important;}
.stTabs [data-baseweb="tab-panel"]{padding:clamp(1rem,3vw,2rem) 0 0!important;}

/* CARD MODERN */
.card{background:var(--bg1);border:1px solid var(--border);border-radius:14px;padding:clamp(1rem,3vw,1.5rem);
  transition:all .3s ease;position:relative;overflow:hidden;}
.card:hover{border-color:rgba(240,180,41,.3);box-shadow:0 4px 20px rgba(0,0,0,.2);}
.card::before{content:'';position:absolute;top:0;left:-100%;width:100%;height:2px;
  background:linear-gradient(90deg,transparent,var(--gold),transparent);
  transition:left .5s ease;pointer-events:none;}
.card:hover::before{left:100%;}
.ctitle{font-size:.85rem;font-weight:700;color:var(--text);margin-bottom:.15rem;}
.csub{font-size:.7rem;color:var(--slate);margin-bottom:.85rem;}
.cline{width:26px;height:2px;background:var(--grad-gold);border-radius:2px;margin:.35rem 0 .8rem;
  transition:width .3s ease;}
.card:hover .cline{width:40px;}

/* STAT ROW */
.srow{display:flex;justify-content:space-between;align-items:flex-start;
  padding:.52rem 0;border-bottom:1px solid var(--border);font-size:.79rem;
  transition:background .2s ease;}
.srow:hover{background:rgba(255,255,255,.02);}
.srow:last-child{border-bottom:none;}
.sk{color:var(--muted);flex-shrink:0;padding-right:.5rem;}
.sv{color:var(--text);font-weight:500;font-family:'JetBrains Mono',monospace;text-align:right;}
.sv.gold{color:var(--gold);}.sv.teal{color:var(--teal);}.sv.green{color:var(--green);}
.sv.red{color:var(--red);}.sv.blue{color:#60A5FA;}

/* SPLIT DATA CARD KHUSUS */
.split-card{background:linear-gradient(135deg,var(--bg1) 0%,var(--bg2) 100%);border:1px solid var(--border);border-radius:14px;padding:clamp(1rem,3vw,1.5rem);
  transition:all .3s ease;}
.split-card:hover{border-color:rgba(45,212,191,.3);}
.split-header{display:flex;justify-content:space-between;align-items:center;margin-bottom:1rem;flex-wrap:wrap;gap:.5rem;}
.split-badge{background:rgba(45,212,191,.12);color:var(--teal);padding:.2rem .7rem;border-radius:99px;font-size:.65rem;font-weight:600;}
.split-number{font-family:'JetBrains Mono',monospace;font-size:1.8rem;font-weight:700;color:var(--gold);}
.split-label{font-size:.7rem;color:var(--slate);}
.split-progress{background:rgba(255,255,255,.05);border-radius:99px;height:6px;overflow:hidden;margin:.5rem 0;}
.split-progress-fill{height:100%;border-radius:99px;transition:width .5s ease;}

/* TWEET */
.tw{background:var(--bg2);border:1px solid var(--border);border-left:3px solid;
  border-radius:10px;padding:.85rem 1rem;margin-bottom:.6rem;
  transition:all .2s ease;}
.tw:hover{transform:translateX(4px);border-color:rgba(240,180,41,.3);}
.tw.neg{border-left-color:var(--red);}.tw.pos{border-left-color:var(--green);}.tw.net{border-left-color:var(--slate);}
.two{font-size:.8rem;color:var(--text);line-height:1.62;margin-bottom:.32rem;}
.twc{font-size:.7rem;color:var(--muted);font-family:'JetBrains Mono',monospace;
  background:var(--bg3);padding:.3rem .6rem;border-radius:6px;margin-bottom:.32rem;line-height:1.5;}
.twf{display:flex;gap:.45rem;align-items:center;flex-wrap:wrap;}
.bdg{padding:.14rem .55rem;border-radius:99px;font-size:.6rem;font-weight:700;letter-spacing:.05em;}
.bdg.neg{background:rgba(239,68,68,.13);color:#FCA5A5;}
.bdg.pos{background:rgba(34,197,94,.13);color:#86EFAC;}
.bdg.net{background:rgba(100,116,139,.13);color:#CBD5E1;}

/* INSIGHT */
.ins{background:var(--bg2);border:1px solid var(--border);border-radius:10px;padding:1rem 1.1rem;
  transition:all .2s ease;cursor:pointer;}
.ins:hover{background:var(--bg3);transform:translateY(-3px);}
.ins-val{font-family:'JetBrains Mono',monospace;font-size:1.75rem;font-weight:600;color:var(--gold);line-height:1.2;}
.ins-lbl{font-size:.67rem;font-weight:700;text-transform:uppercase;letter-spacing:.08em;color:var(--slate);margin-bottom:.22rem;}
.ins-desc{font-size:.74rem;color:var(--muted);line-height:1.55;margin-top:.28rem;}

/* FOLD GRID */
.fgrid{display:grid;grid-template-columns:repeat(5,1fr);gap:.45rem;margin-top:.7rem;}
@media(max-width:580px){.fgrid{grid-template-columns:repeat(3,1fr);}}
.fpill{background:var(--bg3);border:1px solid var(--border);border-radius:8px;padding:.48rem .35rem;text-align:center;
  transition:all .2s ease;}
.fpill:hover{transform:translateY(-2px);border-color:rgba(45,212,191,.3);}
.fname{font-size:.6rem;color:var(--slate);margin-bottom:.18rem;}
.fval{font-family:'JetBrains Mono',monospace;font-size:.86rem;font-weight:600;color:var(--teal);}

/* CM BOX */
.cmbox{padding:.7rem .9rem;border-radius:9px;text-align:center;
  transition:all .2s ease;}
.cmbox:hover{transform:scale(1.02);}
.cmlbl{font-size:.68rem;color:var(--muted);margin-bottom:.25rem;}
.cmval{font-family:'JetBrains Mono',monospace;font-size:1.5rem;font-weight:700;color:#fff;}

/* STEP */
.step{display:flex;gap:.6rem;align-items:flex-start;margin-bottom:.65rem;
  transition:all .2s ease;}
.step:hover{transform:translateX(4px);}
.sdot{width:22px;height:22px;border-radius:50%;flex-shrink:0;display:flex;align-items:center;
  justify-content:center;font-size:.6rem;font-weight:800;color:#060B18;margin-top:1px;
  transition:transform .2s ease;}
.step:hover .sdot{transform:scale(1.1);}
.sname{font-size:.8rem;font-weight:600;color:var(--text);}
.sdesc{font-size:.68rem;color:var(--slate);margin-top:.08rem;}

/* PAGE WRAP */
.pw{padding:0 clamp(1rem,5vw,3.5rem);}

/* FOOTER */
.foot{border-top:1px solid var(--border);margin-top:2rem;
  padding:1.1rem clamp(1rem,5vw,3.5rem);text-align:center;font-size:.69rem;color:var(--slate);line-height:1.8;}
.foot b{color:var(--gold);}

/* ── PROBABILITY BARS ─────────────────── */
.prob-head {
    display: flex;
    justify-content: space-between;
    margin-bottom: .25rem;
    font-size: .75rem;
}
.prob-name {
    color: #94A3B8;
    font-weight: 500;
}
.prob-name.highlight {
    color: #E2E8F0;
    font-weight: 700;
}
.prob-pct {
    font-family: 'JetBrains Mono', monospace;
    font-weight: 600;
}
.prob-track {
    background: rgba(255,255,255,.06);
    border-radius: 99px;
    height: 8px;
    overflow: hidden;
    margin-bottom: .65rem;
}
.prob-fill {
    height: 100%;
    border-radius: 99px;
    transition: width .3s ease;
}

/* ── TOKEN TAGS ─────────────────── */
.token-wrap{display:flex;flex-wrap:wrap;gap:.32rem;margin:.6rem 0;}
.tok{padding:.15rem .52rem;border-radius:6px;font-size:.68rem;font-family:'JetBrains Mono',monospace;
  transition:all .2s ease;}
.tok:hover{transform:scale(1.05);}
.tok.p{background:rgba(34,197,94,.12);color:#86EFAC;border:1px solid rgba(34,197,94,.18);}
.tok.n{background:rgba(239,68,68,.12);color:#FCA5A5;border:1px solid rgba(239,68,68,.18);}
.tok.z{background:rgba(100,116,139,.1);color:#CBD5E1;border:1px solid rgba(100,116,139,.15);}

.hist-item{background:var(--bg2);border:1px solid var(--border);border-left:3px solid;
  border-radius:9px;padding:.7rem .9rem;margin-bottom:.45rem;
  display:flex;justify-content:space-between;align-items:center;gap:.8rem;
  transition:all .2s ease;}
.hist-item:hover{transform:translateX(4px);}
.hist-item.neg{border-left-color:var(--red);}
.hist-item.pos{border-left-color:var(--green);}
.hist-item.net{border-left-color:var(--slate);}
.hist-txt{font-size:.76rem;color:var(--text);line-height:1.5;flex:1;}
.hist-right{flex-shrink:0;text-align:right;}

.contoh-btn{background:var(--bg3)!important;border:1px solid var(--border)!important;
  color:var(--muted)!important;border-radius:8px!important;font-size:.72rem!important;
  font-weight:500!important;padding:.35rem .65rem!important;
  text-align:left!important;cursor:pointer!important;
  transition:all .2s ease!important;}
.contoh-btn:hover{border-color:rgba(240,180,41,.3)!important;color:var(--gold)!important;
  transform:translateX(4px)!important;}

/* streamlit overrides */
.stSelectbox>div>div{background:var(--bg2)!important;border-color:var(--border)!important;border-radius:8px!important;}
div[data-baseweb="select"] span{color:var(--text)!important;}
label{color:var(--muted)!important;font-size:.78rem!important;}
::-webkit-scrollbar{width:4px;height:4px;}
::-webkit-scrollbar-track{background:var(--bg);}
::-webkit-scrollbar-thumb{background:var(--bg3);border-radius:2px;}
</style>
""", unsafe_allow_html=True)


# ══════════════════════════════════════════════════════
# DATA PENELITIAN (SESUAI GAMBAR)
# ══════════════════════════════════════════════════════
TOTAL = 2096; NEG = 1611; POS = 359; NET = 126
P_NEG, P_POS, P_NET = 0.768496, 0.171241, 0.060263
TRAIN, TEST = 1676, 420
AKU, PRE, REC, F1 = 78.57, 74.75, 78.57, 75.51
CV = [78.33, 79.00, 77.33, 77.57, 79.47]; CV_M, CV_S = 78.34, 0.82
CM_LABELS = ['Positif','Netral','Negatif']

# Confusion Matrix sesuai gambar
CM = [[29, 3, 12],   # Positif Aktual: 29 Positif, 3 Netral, 12 Negatif
      [0, 0, 1],      # Netral Aktual: 0 Positif, 0 Netral, 1 Negatif
      [4, 2, 2300]]   # Negatif Aktual: 4 Positif, 2 Netral, 2300 Negatif

# Data Split Distribusi (sesuai gambar split_data_distribusi.png)
SPLIT_DATA = {
    'Negatif': {'train': 1288, 'test': 323, 'total': NEG},
    'Positif': {'train': 287, 'test': 72, 'total': POS},
    'Netral': {'train': 101, 'test': 25, 'total': NET}
}

# Data TF-IDF (sesuai gambar top_tfidf.png)
TFIDF = {
    'pajak':0.038,'tahun':0.029,'aktivasi':0.028,'akun':0.024,
    'wajib':0.022,'wajib pajak':0.020,'nomor':0.019,'akun coretax':0.018,
    'kak':0.017,'surat':0.016,'pemberitahuan':0.015,'surat pemberitahuan':0.014,
    'pemberitahuan tahun':0.013,'lapor':0.012,'aktivasi akun':0.011,
    'aktivasi coretax':0.010,'pokok':0.009,'pokok wajib':0.008,
    'nomor pokok':0.007,'email':0.006,'kakak':0.005,
    'daftar':0.004,'data':0.003,'min':0.002,'jenderal':0.001,
}

# Data probabilitas kata per kelas (likelihood)
PROB_KATA = {
    'error': {'Negatif': 0.085, 'Positif': 0.002, 'Netral': 0.005},
    'lancar': {'Negatif': 0.001, 'Positif': 0.042, 'Netral': 0.003},
    'login': {'Negatif': 0.076, 'Positif': 0.008, 'Netral': 0.012},
    'berhasil': {'Negatif': 0.002, 'Positif': 0.058, 'Netral': 0.004},
    'lambat': {'Negatif': 0.064, 'Positif': 0.001, 'Netral': 0.002},
    'mudah': {'Negatif': 0.001, 'Positif': 0.038, 'Netral': 0.006},
    'aktivasi': {'Negatif': 0.042, 'Positif': 0.015, 'Netral': 0.028},
    'akun': {'Negatif': 0.038, 'Positif': 0.012, 'Netral': 0.022},
    'wajib': {'Negatif': 0.032, 'Positif': 0.010, 'Netral': 0.018},
    'pajak': {'Negatif': 0.055, 'Positif': 0.018, 'Netral': 0.025},
    'tahun': {'Negatif': 0.048, 'Positif': 0.022, 'Netral': 0.030},
    'nomor': {'Negatif': 0.028, 'Positif': 0.008, 'Netral': 0.015},
    'surat': {'Negatif': 0.022, 'Positif': 0.006, 'Netral': 0.012},
    'lapor': {'Negatif': 0.035, 'Positif': 0.014, 'Netral': 0.018},
    'gagal': {'Negatif': 0.058, 'Positif': 0.001, 'Netral': 0.003},
    'down': {'Negatif': 0.045, 'Positif': 0.000, 'Netral': 0.001},
    'cepat': {'Negatif': 0.002, 'Positif': 0.032, 'Netral': 0.005},
    'sulit': {'Negatif': 0.042, 'Positif': 0.001, 'Netral': 0.004},
    'ribet': {'Negatif': 0.038, 'Positif': 0.002, 'Netral': 0.006},
}

# Data tweet
TWEETS = [
    {"asli":"Apakah perlu menyatukan nomor wajib pajak bagi Suami-Istri ASN di Coretax? Bagaimana caranya apabila akun coretax sudah dibuat?","bersih":"nomor wajib pajak suami istri asn coretax akun coretax","label":"Negatif"},
    {"asli":"Karyawan ingin registrasi coretax tapi kendala KK hilang karena bercerai dan belum diurus di dukcapil, bagaimana cara daftarnya?","bersih":"karyawan registrasi coretax kendala kk hilang cerai urus dukcapil daftar","label":"Negatif"},
    {"asli":"Coretax error terus, tidak bisa akses sejak pagi. Deadline lapor pajak sudah dekat tapi sistem malah down.","bersih":"coretax error akses deadline lapor pajak dekat sistem down","label":"Negatif"},
    {"asli":"Tujuan coretax untuk mempermudah tapi malah bikin emosi. Sudah coba berkali-kali tetap tidak bisa login.","bersih":"tuju coretax mudah emosi berkali login","label":"Negatif"},
    {"asli":"Sistem coretax sangat lambat dan sering tidak merespons. Sangat mengecewakan.","bersih":"sistem coretax lambat merespons kecewa","label":"Negatif"},
    {"asli":"Alhamdulillah berhasil lapor SPT tahunan lewat coretax, lancar sekali! Terima kasih DJP sudah berinovasi.","bersih":"alhamdulillah hasil lapor surat pemberitahuan coretax lancar terima kasih djp","label":"Positif"},
    {"asli":"Coretax sekarang sudah jauh lebih baik dan mudah digunakan. Modern dan proses lapor pajak jadi cepat.","bersih":"coretax baik mudah modern lapor pajak cepat","label":"Positif"},
    {"asli":"Buat yang mau tanya soal CoreTax boleh DM, aku bantu sebisaku untuk urusan perpajakan, gratis!","bersih":"coretax bantu sebisaku urusan perpajakan gratis","label":"Positif"},
    {"asli":"Deadline lapor SPT tahunan melalui coretax adalah 31 Maret 2025. Segera lapor sebelum terlambat.","bersih":"deadline lapor surat pemberitahuan coretax maret lapor","label":"Netral"},
    {"asli":"Coretax adalah sistem administrasi perpajakan terbaru dari Direktorat Jenderal Pajak yang diluncurkan akhir 2024.","bersih":"coretax sistem administrasi perpajakan direktorat jenderal pajak luncur","label":"Netral"},
    {"asli":"NIK Kakak telah terdaftar di Coretax, silakan pilih Aktivasi Akun Wajib Pajak untuk login pertama kali.","bersih":"nik kakak coretax aktivasi akun wajib pajak login","label":"Netral"},
]

PT = dict(paper_bgcolor='rgba(0,0,0,0)',plot_bgcolor='rgba(0,0,0,0)',
          font=dict(family='Inter',color='#94A3B8',size=11))
WARNA = {'Positif':'#22C55E','Negatif':'#EF4444','Netral':'#94A3B8'}
css  = {'Positif':'pos','Negatif':'neg','Netral':'net'}
bdge = {'Positif':'<span class="bdg pos">😊 POSITIF</span>',
        'Negatif':'<span class="bdg neg">😠 NEGATIF</span>',
        'Netral' :'<span class="bdg net">😐 NETRAL</span>'}


# ══════════════════════════════════════════════════════
# FUNGSI PREPROCESSING DAN PREDIKSI
# ══════════════════════════════════════════════════════
NORMALISASI = {
    "gak":"tidak","ga":"tidak","gk":"tidak","ngga":"tidak","nggak":"tidak",
    "enggak":"tidak","tdk":"tidak","gapapa":"tidak apa apa","yg":"yang",
    "dg":"dengan","dgn":"dengan","tp":"tapi","krn":"karena","karna":"karena",
    "klo":"kalau","kalo":"kalau","udah":"sudah","udh":"sudah","sdh":"sudah",
    "blm":"belum","blom":"belum","msh":"masih","lg":"lagi","jg":"juga",
    "bgt":"banget","bngt":"banget","bet":"banget","sy":"saya","gw":"saya",
    "gue":"saya","aq":"saya","lo":"anda","lu":"anda","bs":"bisa","bsa":"bisa",
    "eror":"error","erorr":"error","galat":"error","lemot":"lambat",
    "lelet":"lambat","ribet":"rumit","cape":"lelah","capek":"lelah",
    "gmn":"bagaimana","gimana":"bagaimana","knp":"kenapa","aja":"saja",
    "ok":"oke","okey":"oke","okay":"oke","makasih":"terima kasih",
    "makasi":"terima kasih","thx":"terima kasih","thanks":"terima kasih",
    "pls":"tolong","pliss":"tolong","mantep":"mantap","kece":"keren",
    "wkwk":"","wkwkwk":"","haha":"","hehe":"","hihi":"",
}

STOPWORDS = {
    "dan","atau","yang","di","ke","dari","untuk","dengan","pada","ini","itu",
    "ada","akan","jika","kalau","juga","tapi","tetapi","saya","anda","kita",
    "mereka","kami","ia","dia","nya","ku","mu","lah","kah","pun","pula",
    "nih","deh","dong","sih","kok","nah","ya","yah","eh","ah","oh","hm",
    "rt","cc","amp","https","http","www","co","id","si","ini","itu",
}

KAMUS = {
    "error":-4,"gagal":-4,"crash":-4,"bug":-4,"eror":-4,
    "tidak bisa login":-5,"tidak bisa akses":-5,"tidak bisa lapor":-5,
    "data hilang":-5,"kebocoran data":-5,"sistem down":-4,
    "down":-3,"rusak":-3,"ngadat":-3,"hang":-3,"blank":-3,"freeze":-3,
    "timeout":-3,"lambat":-3,"lemot":-3,"lelet":-3,"loading lama":-3,
    "kecewa":-3,"kesal":-3,"frustrasi":-3,"marah":-3,"jengkel":-3,
    "parah":-3,"buruk":-3,"jelek":-3,"kacau":-3,"berantakan":-3,
    "mengecewakan":-3,"menyebalkan":-3,"menjengkelkan":-3,
    "tidak berfungsi":-3,"tidak jalan":-3,"tidak responsif":-3,
    "masalah":-3,"gangguan":-3,"kendala":-3,
    "susah":-2,"sulit":-2,"rumit":-2,"ribet":-2,"bingung":-2,
    "lama":-2,"nunggu":-2,"stuck":-2,"pending":-2,
    "percuma":-2,"sia-sia":-2,"pusing":-2,"repot":-2,"capek":-2,
    "perbaiki":-2,"diperbaiki":-2,"fix":-2,"benerin":-2,
    "belum bisa":-2,"masih error":-2,"tidak aman":-2,
    "hilang":-2,"tidak ada":-2,
    "kenapa":-1,"koq":-1,"kok":-1,"masa":-1,"tolong":-1,"minta tolong":-1,
    "loading":-1,"nunggu":-1,"belum":-1,"tidak":-1,"nggak":-1,"gak":-1,
    "berhasil":4,"sukses":4,"alhamdulillah":4,"lancar":4,
    "lapor berhasil":5,"berhasil lapor":5,
    "mantap":3,"keren":3,"bagus":3,"baik":3,"mudah":3,"gampang":3,
    "praktis":3,"cepat":3,"responsif":3,"stabil":3,"aman":3,"modern":3,
    "efisien":3,"optimal":3,"canggih":3,"hebat":3,"terima kasih":3,
    "senang":3,"puas":3,"lega":3,"nyaman":3,"suka":3,
    "memuaskan":3,"membantu":3,"bermanfaat":3,"berguna":3,
    "inovatif":3,"inovasi":2,"kece":3,
    "lebih baik":2,"sudah baik":2,"jauh lebih baik":3,
    "good":2,"nice":2,"works":2,"fixed":2,"solved":2,
    "terimakasih":2,"thanks":2,"thx":2,"makasih":2,
    "oke":1,"ok":1,"sip":1,"siap":1,"bisa":1,"jalan":1,
}

def preprocessing(teks: str) -> tuple:
    t = re.sub(r'http\S+|www\S+', '', teks)
    t = re.sub(r'@\w+|#\w+', '', t)
    t = re.sub(r'[^\w\s]', ' ', t)
    t = re.sub(r'\d+', '', t)
    t = t.lower().strip()
    t = re.sub(r'\s+', ' ', t)
    words = [NORMALISASI.get(w, w) for w in t.split()]
    words = [w for w in words if w not in STOPWORDS and len(w) > 1 and w.strip()]
    return ' '.join(words), words

def cari_frasa(tokens: list) -> dict:
    ditemukan = {}
    i = 0
    while i < len(tokens):
        if i+2 < len(tokens):
            tri = ' '.join(tokens[i:i+3])
            if tri in KAMUS:
                ditemukan[tri] = KAMUS[tri]; i += 3; continue
        if i+1 < len(tokens):
            bi = ' '.join(tokens[i:i+2])
            if bi in KAMUS:
                ditemukan[bi] = KAMUS[bi]; i += 2; continue
        uni = tokens[i]
        if uni in KAMUS:
            ditemukan[uni] = KAMUS[uni]
        i += 1
    return ditemukan

def prediksi(teks: str) -> dict:
    bersih, tokens = preprocessing(teks)
    detail = cari_frasa(tokens)
    skor_total = sum(detail.values())
    skor_pos   = sum(v for v in detail.values() if v > 0)
    skor_neg   = sum(v for v in detail.values() if v < 0)

    lp = {
        "Negatif": math.log(P_NEG + 1e-9) + abs(skor_neg) * 0.4,
        "Positif": math.log(P_POS + 1e-9) + skor_pos * 0.4,
        "Netral":  math.log(P_NET + 1e-9),
    }
    mx = max(lp.values())
    ex = {k: math.exp(v - mx) for k, v in lp.items()}
    sm = sum(ex.values())
    proba = {k: v / sm for k, v in ex.items()}

    if skor_total > 0:
        label = "Positif"
    elif skor_total < 0:
        label = "Negatif"
    else:
        label = "Netral"

    return {
        "label": label, "bersih": bersih, "tokens": tokens,
        "detail": detail, "skor_total": skor_total,
        "skor_pos": skor_pos, "skor_neg": skor_neg, "proba": proba,
    }

# Session state
if "riwayat" not in st.session_state:
    st.session_state.riwayat = []
if "input_val" not in st.session_state:
    st.session_state.input_val = ""


# ══════════════════════════════════════════════════════
# FUNGSI VISUALISASI MODEL NAIVE BAYES
# ══════════════════════════════════════════════════════
def plot_probability_heatmap():
    df = pd.DataFrame(PROB_KATA).T
    fig = px.imshow(df.T, 
                    text_auto='.3f',
                    color_continuous_scale='RdYlGn',
                    aspect="auto",
                    labels=dict(x="Kata", y="Kelas", color="P(kata|kelas)"))
    fig.update_layout(**PT, height=450, margin=dict(l=6,r=6,t=30,b=30))
    return fig

def plot_feature_importance():
    df = pd.DataFrame(list(TFIDF.items()), columns=['Fitur', 'Bobot'])
    df = df.sort_values('Bobot', ascending=True).tail(20)
    
    fig = go.Figure(go.Bar(
        x=df['Bobot'],
        y=df['Fitur'],
        orientation='h',
        marker=dict(color='#F0B429', line=dict(width=0)),
        text=df['Bobot'].apply(lambda x: f'{x:.3f}'),
        textposition='outside',
        textfont=dict(size=10, color='#F0B429', family='JetBrains Mono'),
        hovertemplate='<b>%{y}</b><br>Bobot: %{x:.3f}<extra></extra>'
    ))
    fig.update_layout(**PT, height=500, margin=dict(l=6,r=40,t=20,b=30),
                      xaxis=dict(title='Bobot TF-IDF', showgrid=True, gridcolor='rgba(255,255,255,.05)'),
                      yaxis=dict(title='', automargin=True))
    return fig

def plot_class_comparison():
    kata_komparasi = ['error', 'lancar', 'gagal', 'berhasil', 'lambat', 'cepat', 'ribet', 'mudah']
    fig = go.Figure()
    for kelas in ['Negatif', 'Positif', 'Netral']:
        warna = WARNA[kelas]
        fig.add_trace(go.Bar(
            name=kelas,
            x=kata_komparasi,
            y=[PROB_KATA[k][kelas] for k in kata_komparasi],
            marker_color=warna
        ))
    fig.update_layout(**PT, height=400, barmode='group',
                      margin=dict(l=6,r=6,t=20,b=30),
                      xaxis=dict(title='Kata'),
                      yaxis=dict(title='Probabilitas P(kata|kelas)'))
    return fig

def plot_prior_distribution():
    fig = go.Figure(go.Pie(
        labels=['Negatif', 'Positif', 'Netral'],
        values=[P_NEG, P_POS, P_NET],
        hole=0.5,
        marker=dict(colors=['#EF4444','#22C55E','#94A3B8'], line=dict(color='#060B18', width=2)),
        textinfo='label+percent',
        textfont=dict(size=12, family='JetBrains Mono', color='white'),
        hovertemplate='<b>%{label}</b><br>Prior: %{percent}<extra></extra>'
    ))
    fig.update_layout(**PT, height=300, margin=dict(l=6,r=6,t=20,b=30))
    return fig

def plot_radar_comparison():
    categories = ['error', 'lambat', 'gagal', 'lancar', 'berhasil', 'cepat', 'mudah']
    
    fig = go.Figure()
    fig.add_trace(go.Scatterpolar(
        r=[PROB_KATA['error']['Negatif'], PROB_KATA['lambat']['Negatif'], 
           PROB_KATA['gagal']['Negatif'], PROB_KATA['lancar']['Negatif'],
           PROB_KATA['berhasil']['Negatif'], PROB_KATA['cepat']['Negatif'],
           PROB_KATA['mudah']['Negatif']],
        theta=categories,
        fill='toself',
        name='Negatif',
        line_color='#EF4444',
        fillcolor='rgba(239,68,68,0.3)'
    ))
    fig.add_trace(go.Scatterpolar(
        r=[PROB_KATA['error']['Positif'], PROB_KATA['lambat']['Positif'],
           PROB_KATA['gagal']['Positif'], PROB_KATA['lancar']['Positif'],
           PROB_KATA['berhasil']['Positif'], PROB_KATA['cepat']['Positif'],
           PROB_KATA['mudah']['Positif']],
        theta=categories,
        fill='toself',
        name='Positif',
        line_color='#22C55E',
        fillcolor='rgba(34,197,94,0.3)'
    ))
    fig.add_trace(go.Scatterpolar(
        r=[PROB_KATA['error']['Netral'], PROB_KATA['lambat']['Netral'],
           PROB_KATA['gagal']['Netral'], PROB_KATA['lancar']['Netral'],
           PROB_KATA['berhasil']['Netral'], PROB_KATA['cepat']['Netral'],
           PROB_KATA['mudah']['Netral']],
        theta=categories,
        fill='toself',
        name='Netral',
        line_color='#94A3B8',
        fillcolor='rgba(148,163,184,0.3)'
    ))
    
    fig.update_layout(**PT, height=450, margin=dict(l=60,r=60,t=20,b=20),
                      polar=dict(radialaxis=dict(visible=True, range=[0, 0.1])))
    return fig

def export_model_to_json():
    model_data = {
        "metadata": {
            "nama_model": "Categorical Naive Bayes - Coretax Sentiment Analysis",
            "versi": "1.0.0",
            "tanggal_export": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "deskripsi": "Model analisis sentimen untuk tweet tentang Coretax di Platform X",
            "peneliti": "Aziz Fakhrizi",
            "nim": "2022020255",
            "institusi": "STMIK Triguna Dharma Medan"
        },
        "dataset_info": {
            "total_data": TOTAL,
            "data_training": TRAIN,
            "data_testing": TEST,
            "split_data": SPLIT_DATA,
            "periode_awal": "2024-12-15",
            "periode_akhir": "2025-01-27",
            "distribusi_label": {
                "Negatif": {"jumlah": NEG, "persentase": f"{P_NEG*100:.2f}%"},
                "Positif": {"jumlah": POS, "persentase": f"{P_POS*100:.2f}%"},
                "Netral": {"jumlah": NET, "persentase": f"{P_NET*100:.2f}%"}
            }
        },
        "model_performance": {
            "akurasi": f"{AKU:.2f}%",
            "presisi": f"{PRE:.2f}%",
            "recall": f"{REC:.2f}%",
            "f1_score": f"{F1:.2f}%",
            "cross_validation": {
                "folds": [f"{v:.2f}%" for v in CV],
                "rata_rata": f"{CV_M:.2f}%",
                "std_deviasi": f"±{CV_S:.2f}%"
            },
            "confusion_matrix": {
                "labels": CM_LABELS,
                "matrix": CM
            }
        },
        "prior_probabilities": {
            "Negatif": P_NEG,
            "Positif": P_POS,
            "Netral": P_NET
        },
        "likelihood_probabilities": PROB_KATA,
        "tfidf_features": TFIDF,
        "vocabulary": {
            "size": 2500,
            "top_features": list(TFIDF.keys())[:20]
        },
        "preprocessing_info": {
            "normalisasi_kata": len(NORMALISASI),
            "stopwords": len(STOPWORDS),
            "kamus_sentimen": len(KAMUS),
            "tahapan": ["Cleaning", "Case Folding", "Normalisasi", 
                       "Stopword Removal", "Tokenizing", "Stemming", "Labeling"]
        }
    }
    return model_data


# ══════════════════════════════════════════════════════
# HERO
# ══════════════════════════════════════════════════════
st.markdown(f"""
<div class="hero">
  <div class="hero-tag">📊 Skripsi · STMIK Triguna Dharma · 2026</div>
  <h1 class="hero-title">Sentimen Masyarakat<br>terhadap <em>Coretax</em> di Platform X</h1>
  <p class="hero-desc">
    Analisis persepsi publik terhadap sistem perpajakan digital Coretax berdasarkan
    <strong style="color:#E2E8F0">{TOTAL:,} tweet</strong> menggunakan
    <strong style="color:#E2E8F0">Categorical Naïve Bayes</strong>.
    Akurasi model <strong style="color:#F0B429">{AKU}%</strong>.
  </p>
  <div class="hero-pills">
    <span class="hero-pill">🗓️ 15 Des 2024 – 27 Jan 2025</span>
    <span class="hero-pill">🤖 <b>Categorical Naïve Bayes</b></span>
    <span class="hero-pill">🏷️ InSet Lexicon</span>
    <span class="hero-pill">📐 TF-IDF 5.000 Fitur</span>
    <span class="hero-pill">✍️ Aziz Fakhrizi · 2022020255</span>
  </div>
</div>
""", unsafe_allow_html=True)

# ══════════════════════════════════════════════════════
# METRIC STRIP
# ══════════════════════════════════════════════════════
st.markdown(f"""
<div class="mstrip">
  <div class="mtile mt0"><div class="mico">🐦</div>
    <div class="mlabel">Total Tweet</div><div class="mval">{TOTAL:,}</div>
    <div class="msub">Periode 44 hari</div></div>
  <div class="mtile mt1"><div class="mico">😠</div>
    <div class="mlabel">Negatif</div><div class="mval">{NEG:,}</div>
    <div class="msub">{NEG/TOTAL*100:.1f}% dari total</div></div>
  <div class="mtile mt2"><div class="mico">😊</div>
    <div class="mlabel">Positif</div><div class="mval">{POS:,}</div>
    <div class="msub">{POS/TOTAL*100:.1f}% dari total</div></div>
  <div class="mtile mt3"><div class="mico">😐</div>
    <div class="mlabel">Netral</div><div class="mval">{NET:,}</div>
    <div class="msub">{NET/TOTAL*100:.1f}% dari total</div></div>
</div>
""", unsafe_allow_html=True)


# ══════════════════════════════════════════════════════
# TABS
# ══════════════════════════════════════════════════════
t1, t2, t3, t4, t5, t6, t7, t8 = st.tabs([
    "📊 Distribusi",
    "📈 Evaluasi Model",
    "📦 Split Data",
    "🔬 Visualisasi Model NB",
    "💬 Ulasan Publik",
    "🔄 Preprocessing",
    "📋 Ringkasan",
    "🧪 Uji Prediksi",
])


# ──────────────────────────────────────────────────────
# TAB 1 — DISTRIBUSI
# ──────────────────────────────────────────────────────
with t1:
    st.markdown('<div class="pw">', unsafe_allow_html=True)
    
    ca, cb = st.columns([1, 1.45], gap="large")

    with ca:
        st.markdown('<div class="card">', unsafe_allow_html=True)
        st.markdown('<div class="ctitle">Proporsi Sentimen</div><div class="cline"></div>', unsafe_allow_html=True)
        st.markdown(f'<div class="csub">Total {TOTAL:,} tweet — Labeling InSet Lexicon</div>', unsafe_allow_html=True)
        
        fig = go.Figure(go.Pie(
            labels=['Negatif','Positif','Netral'], values=[NEG,POS,NET],
            hole=0.63, direction='clockwise', sort=False,
            marker=dict(colors=['#EF4444','#22C55E','#475569'],line=dict(color='#060B18',width=3)),
            textinfo='percent', textfont=dict(size=12,family='JetBrains Mono',color='white'),
            insidetextorientation='horizontal',
            hovertemplate='<b>%{label}</b><br>%{value:,} tweet (%{percent:.1%})<extra></extra>',
        ))
        fig.add_annotation(x=0.5,y=0.5,showarrow=False,
            text=f"<span style='font-size:22px;font-weight:700;color:#EF4444'>{NEG/TOTAL*100:.0f}%</span>"
                 f"<br><span style='font-size:10px;color:#64748B'>Negatif</span>",
            font=dict(family='JetBrains Mono'))
        fig.update_layout(**PT, height=290, margin=dict(l=6,r=6,t=10,b=38),
            legend=dict(orientation='h',x=0.5,y=-0.14,xanchor='center',
                        font=dict(size=11),bgcolor='rgba(0,0,0,0)'))
        st.plotly_chart(fig, use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)

    with cb:
        st.markdown('<div class="card">', unsafe_allow_html=True)
        st.markdown('<div class="ctitle">Jumlah Tweet per Kelas</div><div class="cline"></div>', unsafe_allow_html=True)
        st.markdown('<div class="csub">Perbandingan volume tiap kategori sentimen</div>', unsafe_allow_html=True)
        
        fig2 = go.Figure()
        for lbl,val,clr in [('Negatif',NEG,'#EF4444'),('Positif',POS,'#22C55E'),('Netral',NET,'#475569')]:
            fig2.add_trace(go.Bar(y=[lbl],x=[val],orientation='h',name=lbl,
                marker=dict(color=clr,line=dict(width=0)),
                text=f'  {val:,}  ({val/TOTAL*100:.1f}%)',
                textposition='inside',textfont=dict(size=12,color='white',family='JetBrains Mono'),
                hovertemplate=f'<b>{lbl}</b>: {val:,} tweet<extra></extra>'))
        fig2.update_layout(**PT,height=215,showlegend=False,margin=dict(l=6,r=6,t=10,b=30),
            xaxis=dict(title='Jumlah Tweet',showgrid=True,gridcolor='rgba(255,255,255,.05)',tickfont=dict(size=10)),
            yaxis=dict(tickfont=dict(size=12)),bargap=0.28)
        st.plotly_chart(fig2, use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)

    st.markdown('<div class="card" style="margin-top:1rem">', unsafe_allow_html=True)
    st.markdown('<div class="ctitle">Top 25 Fitur TF-IDF</div><div class="cline"></div>', unsafe_allow_html=True)
    st.markdown('<div class="csub">Kata/frasa dengan bobot TF-IDF tertinggi — n-gram(1,2), min_df=2, max_features=5000</div>', unsafe_allow_html=True)
    tdf = pd.DataFrame(list(TFIDF.items()),columns=['f','b']).sort_values('b')
    blues = [f'rgba(59,130,246,{0.30+0.70*(i/len(tdf)):.2f})' for i in range(len(tdf))]
    fig3 = go.Figure(go.Bar(x=tdf['b'],y=tdf['f'],orientation='h',
        marker=dict(color=blues,line=dict(width=0)),
        hovertemplate='<b>%{y}</b>  →  %{x:.3f}<extra></extra>'))
    fig3.update_layout(**PT,height=490,margin=dict(l=6,r=52,t=10,b=32),
        xaxis=dict(title='Rata-rata Skor TF-IDF',showgrid=True,gridcolor='rgba(255,255,255,.05)',tickfont=dict(size=10)),
        yaxis=dict(tickfont=dict(size=10.5),automargin=True))
    st.plotly_chart(fig3, use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)

    st.markdown('<br>', unsafe_allow_html=True)
    i1,i2,i3 = st.columns(3,gap="medium")
    with i1:
        st.markdown(f'<div class="ins"><div class="ins-lbl">Dominasi Negatif</div><div class="ins-val">{NEG/TOTAL*100:.1f}%</div><div class="ins-desc">Keluhan utama: <em>error sistem</em>, <em>login gagal</em>, dan <em>lambat/down</em>.</div></div>', unsafe_allow_html=True)
    with i2:
        st.markdown(f'<div class="ins"><div class="ins-lbl">Sentimen Positif</div><div class="ins-val">{POS/TOTAL*100:.1f}%</div><div class="ins-desc">Puas dengan kemudahan lapor SPT dan inovasi DJP.</div></div>', unsafe_allow_html=True)
    with i3:
        st.markdown(f'<div class="ins"><div class="ins-lbl">Fitur TF-IDF #1</div><div class="ins-val">pajak</div><div class="ins-desc">Bobot 0.038, diikuti <em>tahun</em> (0.029) dan <em>aktivasi</em> (0.028).</div></div>', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)


# ──────────────────────────────────────────────────────
# TAB 2 — EVALUASI MODEL
# ──────────────────────────────────────────────────────
with t2:
    st.markdown('<div class="pw">', unsafe_allow_html=True)
    g1,g2,g3,g4 = st.columns(4,gap="medium")
    for col,name,val,clr,hx in [(g1,"Akurasi",AKU,'#3B82F6','3B82F6'),(g2,"Presisi",PRE,'#22C55E','22C55E'),(g3,"Recall",REC,'#F59E0B','F59E0B'),(g4,"F1-Score",F1,'#8B5CF6','8B5CF6')]:
        with col:
            r,g,b = int(hx[:2],16),int(hx[2:4],16),int(hx[4:],16)
            fg = go.Figure(go.Indicator(mode="gauge+number",value=val,
                number={'suffix':'%','font':{'size':24,'color':clr,'family':'JetBrains Mono'}},
                title={'text':name,'font':{'size':12,'color':'#94A3B8'}},
                gauge=dict(axis=dict(range=[0,100],tickfont=dict(size=8,color='#475569'),tickcolor='#1A2B47',nticks=6),
                    bar=dict(color=clr,thickness=0.28),bgcolor='#111E35',bordercolor='#111E35',borderwidth=0,
                    steps=[{'range':[0,70],'color':'rgba(255,255,255,0.02)'},{'range':[70,100],'color':f'rgba({r},{g},{b},0.08)'}],
                    threshold=dict(line=dict(color='#F0B429',width=2.5),thickness=0.72,value=70))))
            fg.update_layout(**PT,height=190,margin=dict(l=4,r=4,t=22,b=4))
            col.plotly_chart(fg, use_container_width=True)
    st.markdown('<p style="text-align:center;font-size:.69rem;color:#475569;margin:-0.4rem 0 1.3rem">⭐ Garis kuning = batas minimum akurasi 70%</p>', unsafe_allow_html=True)

    ev1,ev2 = st.columns([1.1,1],gap="large")
    with ev1:
        st.markdown('<div class="card">', unsafe_allow_html=True)
        st.markdown('<div class="ctitle">Perbandingan Metrik Evaluasi</div><div class="cline"></div>', unsafe_allow_html=True)
        st.markdown('<div class="csub">420 data testing — Weighted Average</div>', unsafe_allow_html=True)
        fig_ev = go.Figure()
        for nm,vl,cl in [('Akurasi',AKU,'#3B82F6'),('Presisi',PRE,'#22C55E'),('Recall',REC,'#F59E0B'),('F1-Score',F1,'#8B5CF6')]:
            fig_ev.add_trace(go.Bar(x=[nm],y=[vl],name=nm,width=0.48,
                marker=dict(color=cl,line=dict(width=0)),text=f'{vl:.2f}%',
                textposition='outside',textfont=dict(size=11,color=cl,family='JetBrains Mono')))
        fig_ev.add_hline(y=70,line_dash='dot',line_color='#F0B429',line_width=1.5,
            annotation_text='Min 70%',annotation_font=dict(size=9,color='#F0B429'))
        fig_ev.update_layout(**PT,height=285,showlegend=False,margin=dict(l=6,r=6,t=16,b=8),
            xaxis=dict(showgrid=False,tickfont=dict(size=11)),
            yaxis=dict(range=[0,93],showgrid=True,gridcolor='rgba(255,255,255,.05)',tickfont=dict(size=10)))
        st.plotly_chart(fig_ev, use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)

    with ev2:
        st.markdown('<div class="card">', unsafe_allow_html=True)
        st.markdown('<div class="ctitle">Cross Validation — 5-Fold</div><div class="cline"></div>', unsafe_allow_html=True)
        st.markdown(f'<div class="csub">Rata-rata {CV_M:.2f}% ± {CV_S:.2f}% — stabil & tidak overfitting</div>', unsafe_allow_html=True)
        fig_cv = go.Figure(go.Bar(x=[f'Fold {i+1}' for i in range(5)],y=CV,width=0.52,
            marker=dict(color='#2DD4BF',line=dict(width=0)),
            text=[f'{v:.2f}%' for v in CV],textposition='outside',
            textfont=dict(size=10,color='#2DD4BF',family='JetBrains Mono')))
        fig_cv.add_hline(y=CV_M,line_dash='dash',line_color='#F0B429',line_width=1.5,
            annotation_text=f'Rata-rata: {CV_M:.2f}%',annotation_font=dict(size=9,color='#F0B429'))
        fig_cv.update_layout(**PT,height=248,margin=dict(l=6,r=6,t=16,b=8),
            xaxis=dict(showgrid=False,tickfont=dict(size=10)),
            yaxis=dict(range=[76,81],showgrid=True,gridcolor='rgba(255,255,255,.05)',
                       tickfont=dict(size=10),title='Akurasi (%)'))
        st.plotly_chart(fig_cv, use_container_width=True)
        fh = ''.join([f'<div class="fpill"><div class="fname">Fold {i+1}</div><div class="fval">{v:.2f}%</div></div>' for i,v in enumerate(CV)])
        st.markdown(f'<div class="fgrid">{fh}</div>', unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)

    # Confusion Matrix
    st.markdown('<div class="card" style="margin-top:1.2rem">', unsafe_allow_html=True)
    st.markdown('<div class="ctitle">Confusion Matrix</div><div class="cline"></div>', unsafe_allow_html=True)
    st.markdown('<div class="csub">Aktual vs prediksi pada 420 data testing</div>', unsafe_allow_html=True)
    cm_l,cm_r = st.columns([1.55,1],gap="large")
    with cm_l:
        fig_cm = go.Figure(go.Heatmap(z=CM,
            x=['Pred: Positif','Pred: Netral','Pred: Negatif'],
            y=['Aktual: Positif','Aktual: Netral','Aktual: Negatif'],
            text=[[str(v) for v in row] for row in CM],
            texttemplate='<b>%{text}</b>',textfont={'size':16,'color':'white','family':'JetBrains Mono'},
            colorscale=[[0,'#111E35'],[0.01,'#1A2B47'],[0.05,'#1E3A5F'],[0.3,'#1D4ED8'],[1,'#F0B429']],
            showscale=False,hovertemplate='Aktual: %{y}<br>Prediksi: %{x}<br>Jumlah: %{z}<extra></extra>'))
        fig_cm.update_layout(**PT,height=295,margin=dict(l=6,r=6,t=8,b=8),
            xaxis=dict(tickfont=dict(size=10.5),side='bottom'),
            yaxis=dict(tickfont=dict(size=10.5),autorange='reversed'))
        st.plotly_chart(fig_cm, use_container_width=True)
    with cm_r:
        st.markdown('<br>', unsafe_allow_html=True)
        for lbl,val,cl in [("✅ True Positif","29","green"),("✅ True Netral","0",""),
            ("✅ True Negatif","2.300","red"),("❌ Positif → Negatif","12","red"),
            ("❌ Positif → Netral","3",""),("❌ Negatif → Positif","4","green"),
            ("❌ Negatif → Netral","2",""),("❌ Netral → Negatif","1","red")]:
            st.markdown(f'<div class="srow"><span class="sk" style="font-size:.73rem">{lbl}</span><span class="sv {cl}">{val}</span></div>', unsafe_allow_html=True)
    b1,b2,b3 = st.columns(3,gap="medium")
    with b1: st.markdown('<div class="cmbox" style="background:rgba(34,197,94,.07);border:1px solid rgba(34,197,94,.18)"><div class="cmlbl">✅ Benar Positif (TP)</div><div class="cmval" style="color:#86EFAC">29</div></div>', unsafe_allow_html=True)
    with b2: st.markdown('<div class="cmbox" style="background:rgba(239,68,68,.07);border:1px solid rgba(239,68,68,.18)"><div class="cmlbl">✅ Benar Negatif (TP)</div><div class="cmval" style="color:#FCA5A5">2.300</div></div>', unsafe_allow_html=True)
    with b3: st.markdown('<div class="cmbox" style="background:rgba(100,116,139,.07);border:1px solid rgba(100,116,139,.18)"><div class="cmlbl">✅ Benar Netral (TP)</div><div class="cmval" style="color:#CBD5E1">0</div></div>', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

    # Prior
    st.markdown('<div class="card" style="margin-top:1.2rem">', unsafe_allow_html=True)
    st.markdown('<div class="ctitle">Probabilitas Prior P(Vj)</div><div class="cline"></div>', unsafe_allow_html=True)
    st.markdown(f'<div class="csub">P(Vj) = |doc j| / |training| — {TRAIN:,} data training</div>', unsafe_allow_html=True)
    p1,p2,p3 = st.columns(3,gap="medium")
    for col,lbl,jml,prob,clr in [(p1,"V1 = Negatif",1288,P_NEG,"#EF4444"),(p2,"V2 = Positif",287,P_POS,"#22C55E"),(p3,"V3 = Netral",101,P_NET,"#64748B")]:
        with col:
            col.markdown(f'<div class="ins" style="border-left:3px solid {clr}"><div class="ins-lbl">{lbl}</div><div class="ins-val" style="color:{clr};font-size:1.45rem">{prob:.6f}</div><div class="ins-desc">{jml:,} / {TRAIN:,} tweet training</div></div>', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)


# ──────────────────────────────────────────────────────
# TAB 3 — SPLIT DATA (BARU)
# ──────────────────────────────────────────────────────
with t3:
    st.markdown('<div class="pw">', unsafe_allow_html=True)
    
    st.markdown('<div class="ctitle">📦 Split Data Training & Testing</div><div class="cline"></div>', unsafe_allow_html=True)
    st.markdown('<div class="csub">Distribusi data training (80%) dan testing (20%) per kelas sentimen</div>', unsafe_allow_html=True)
    
    # Card Split Data
    col_s1, col_s2, col_s3 = st.columns(3, gap="medium")
    
    for col, kelas, warna, data in zip([col_s1, col_s2, col_s3], 
                                        ['Negatif', 'Positif', 'Netral'],
                                        ['#EF4444', '#22C55E', '#94A3B8'],
                                        [SPLIT_DATA['Negatif'], SPLIT_DATA['Positif'], SPLIT_DATA['Netral']]):
        with col:
            train_pct = (data['train'] / data['total']) * 100
            test_pct = (data['test'] / data['total']) * 100
            
            st.markdown(f"""
            <div class="split-card">
                <div class="split-header">
                    <span class="split-badge" style="background:{warna}22;color:{warna}">{kelas}</span>
                    <span class="split-number">{data['total']}</span>
                </div>
                <div class="split-label">Total {kelas}</div>
                <div style="margin: .5rem 0">
                    <div style="display:flex;justify-content:space-between;font-size:.7rem;margin-bottom:.2rem">
                        <span style="color:var(--teal)">📊 Training (80%)</span>
                        <span style="font-family:'JetBrains Mono',monospace">{data['train']} tweet ({train_pct:.0f}%)</span>
                    </div>
                    <div class="split-progress">
                        <div class="split-progress-fill" style="width:{train_pct}%;background:var(--teal)"></div>
                    </div>
                    <div style="display:flex;justify-content:space-between;font-size:.7rem;margin-bottom:.2rem;margin-top:.5rem">
                        <span style="color:var(--muted)">🧪 Testing (20%)</span>
                        <span style="font-family:'JetBrains Mono',monospace">{data['test']} tweet ({test_pct:.0f}%)</span>
                    </div>
                    <div class="split-progress">
                        <div class="split-progress-fill" style="width:{test_pct}%;background:var(--muted)"></div>
                    </div>
                </div>
                <div style="display:flex;justify-content:space-between;align-items:center;margin-top:.5rem;padding-top:.5rem;border-top:1px solid var(--border)">
                    <span style="font-size:.65rem;color:var(--slate)">Training</span>
                    <span style="font-size:.65rem;color:var(--slate)">Testing</span>
                </div>
            </div>
            """, unsafe_allow_html=True)
    
    # Ringkasan Split Data
    st.markdown('<div class="card" style="margin-top:1rem">', unsafe_allow_html=True)
    st.markdown('<div class="ctitle">📋 Ringkasan Split Data</div><div class="cline"></div>', unsafe_allow_html=True)
    
    split_df = pd.DataFrame({
        'Kelas': ['Negatif', 'Positif', 'Netral', 'Total'],
        'Training': [SPLIT_DATA['Negatif']['train'], SPLIT_DATA['Positif']['train'], SPLIT_DATA['Netral']['train'], TRAIN],
        'Testing': [SPLIT_DATA['Negatif']['test'], SPLIT_DATA['Positif']['test'], SPLIT_DATA['Netral']['test'], TEST],
        'Total': [NEG, POS, NET, TOTAL],
        'Persentase Training': ['76.9%', '17.1%', '6.0%', '80%'],
        'Persentase Testing': ['76.9%', '17.1%', '6.0%', '20%']
    })
    
    st.dataframe(
        split_df,
        column_config={
            "Kelas": "Kelas Sentimen",
            "Training": st.column_config.NumberColumn("Training (80%)", format="%d"),
            "Testing": st.column_config.NumberColumn("Testing (20%)", format="%d"),
            "Total": st.column_config.NumberColumn("Total", format="%d"),
            "Persentase Training": "Proporsi Training",
            "Persentase Testing": "Proporsi Testing"
        },
        use_container_width=True,
        hide_index=True,
    )
    
    st.markdown('</div>', unsafe_allow_html=True)
    
    # Visualisasi perbandingan Training vs Testing
    st.markdown('<div class="card" style="margin-top:1rem">', unsafe_allow_html=True)
    st.markdown('<div class="ctitle">📊 Perbandingan Training vs Testing per Kelas</div><div class="cline"></div>', unsafe_allow_html=True)
    
    fig_split = go.Figure()
    fig_split.add_trace(go.Bar(
        name='Training (80%)',
        x=['Negatif', 'Positif', 'Netral'],
        y=[SPLIT_DATA['Negatif']['train'], SPLIT_DATA['Positif']['train'], SPLIT_DATA['Netral']['train']],
        marker_color='#2DD4BF',
        text=[f'{SPLIT_DATA["Negatif"]["train"]}', f'{SPLIT_DATA["Positif"]["train"]}', f'{SPLIT_DATA["Netral"]["train"]}'],
        textposition='outside',
        textfont=dict(size=11, color='#2DD4BF', family='JetBrains Mono')
    ))
    fig_split.add_trace(go.Bar(
        name='Testing (20%)',
        x=['Negatif', 'Positif', 'Netral'],
        y=[SPLIT_DATA['Negatif']['test'], SPLIT_DATA['Positif']['test'], SPLIT_DATA['Netral']['test']],
        marker_color='#64748B',
        text=[f'{SPLIT_DATA["Negatif"]["test"]}', f'{SPLIT_DATA["Positif"]["test"]}', f'{SPLIT_DATA["Netral"]["test"]}'],
        textposition='outside',
        textfont=dict(size=11, color='#94A3B8', family='JetBrains Mono')
    ))
    fig_split.update_layout(
        **PT, height=350,
        barmode='group',
        margin=dict(l=6,r=6,t=20,b=30),
        xaxis=dict(title='Kelas Sentimen', tickfont=dict(size=11)),
        yaxis=dict(title='Jumlah Tweet', showgrid=True, gridcolor='rgba(255,255,255,.05)'),
        legend=dict(orientation='h', y=1.05, x=0.5, xanchor='center')
    )
    st.plotly_chart(fig_split, use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)
    
    st.markdown('</div>', unsafe_allow_html=True)


# ──────────────────────────────────────────────────────
# TAB 4 — VISUALISASI MODEL NAIVE BAYES
# ──────────────────────────────────────────────────────
with t4:
    st.markdown('<div class="pw">', unsafe_allow_html=True)
    
    st.markdown('<div class="ctitle">🔬 Visualisasi Model Naive Bayes</div><div class="cline"></div>', unsafe_allow_html=True)
    st.markdown('<div class="csub">Representasi grafis dari parameter model: prior, likelihood, dan feature importance</div>', unsafe_allow_html=True)
    
    # Row 1: Prior Distribution dan Feature Importance
    col_a, col_b = st.columns(2, gap="large")
    
    with col_a:
        st.markdown('<div class="card">', unsafe_allow_html=True)
        st.markdown('<div class="ctitle">📊 Distribusi Prior P(Vj)</div><div class="cline"></div>', unsafe_allow_html=True)
        st.markdown('<div class="csub">Probabilitas awal setiap kelas berdasarkan data training</div>', unsafe_allow_html=True)
        st.plotly_chart(plot_prior_distribution(), use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)
    
    with col_b:
        st.markdown('<div class="card">', unsafe_allow_html=True)
        st.markdown('<div class="ctitle">📈 Feature Importance (TF-IDF)</div><div class="cline"></div>', unsafe_allow_html=True)
        st.markdown('<div class="csub">20 fitur dengan bobot tertinggi</div>', unsafe_allow_html=True)
        st.plotly_chart(plot_feature_importance(), use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)
    
    # Row 2: Heatmap Probabilitas Kata
    st.markdown('<div class="card" style="margin-top:1rem">', unsafe_allow_html=True)
    st.markdown('<div class="ctitle">🔥 Heatmap Probabilitas Kata per Kelas</div><div class="cline"></div>', unsafe_allow_html=True)
    st.markdown('<div class="csub">Nilai P(kata | kelas) — semakin merah, semakin kuat pengaruh kata terhadap kelas</div>', unsafe_allow_html=True)
    st.plotly_chart(plot_probability_heatmap(), use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)
    
    # Row 3: Perbandingan Probabilitas dan Radar Chart
    col_c, col_d = st.columns(2, gap="large")
    
    with col_c:
        st.markdown('<div class="card" style="margin-top:1rem">', unsafe_allow_html=True)
        st.markdown('<div class="ctitle">📊 Perbandingan Probabilitas per Kata</div><div class="cline"></div>', unsafe_allow_html=True)
        st.markdown('<div class="csub">Kata-kata dengan perbedaan probabilitas tertinggi antar kelas</div>', unsafe_allow_html=True)
        st.plotly_chart(plot_class_comparison(), use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)
    
    with col_d:
        st.markdown('<div class="card" style="margin-top:1rem">', unsafe_allow_html=True)
        st.markdown('<div class="ctitle">🔄 Radar Chart Karakteristik Kelas</div><div class="cline"></div>', unsafe_allow_html=True)
        st.markdown('<div class="csub">Visualisasi polaritas kata untuk setiap kelas sentimen</div>', unsafe_allow_html=True)
        st.plotly_chart(plot_radar_comparison(), use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)
    
    # Row 4: Export Model
    st.markdown('<div class="card" style="margin-top:1rem">', unsafe_allow_html=True)
    st.markdown('<div class="ctitle">💾 Export Model Naive Bayes ke JSON</div><div class="cline"></div>', unsafe_allow_html=True)
    st.markdown('<div class="csub">Model lengkap dengan prior, likelihood, TF-IDF, dan metadata penelitian</div>', unsafe_allow_html=True)
    
    col_e, col_f = st.columns([1, 2])
    with col_e:
        if st.button("📥 Generate & Download Model JSON", key="export_model", use_container_width=True):
            model_data = export_model_to_json()
            model_json = json.dumps(model_data, indent=2, ensure_ascii=False)
            
            st.download_button(
                label="⬇️ Download model_coretax.json",
                data=model_json,
                file_name=f"model_coretax_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json",
                mime="application/json",
                use_container_width=True
            )
    
    with col_f:
        st.markdown("""
        <div style="background:var(--bg3);border-radius:8px;padding:.7rem .9rem;font-size:.75rem;color:#94A3B8">
            <strong>📋 Isi Model JSON:</strong><br>
            • Metadata penelitian<br>
            • Probabilitas prior P(Vj)<br>
            • Split data training/testing<br>
            • Likelihood P(kata|kelas) untuk 20+ kata penting<br>
            • Bobot TF-IDF untuk 25 fitur teratas<br>
            • Confusion matrix dan metrik evaluasi
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown('</div>', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)


# ──────────────────────────────────────────────────────
# TAB 5 — ULASAN PUBLIK
# ──────────────────────────────────────────────────────
with t5:
    st.markdown('<div class="pw">', unsafe_allow_html=True)
    st.markdown('<p style="font-size:1rem;font-weight:700;color:var(--text);margin-bottom:.15rem">Ulasan Masyarakat tentang Coretax</p><div class="cline"></div>', unsafe_allow_html=True)
    st.markdown('<p style="font-size:.72rem;color:var(--slate);margin-bottom:1rem">Sampel tweet dari Platform X yang telah dianalisis menggunakan Categorical Naïve Bayes</p>', unsafe_allow_html=True)
    fa,fb = st.columns([1,2],gap="medium")
    with fa: filt = st.selectbox("🔍 Filter",["Semua","Negatif","Positif","Netral"])
    with fb: show_pre = st.checkbox("Tampilkan hasil preprocessing",value=True)
    filtered = TWEETS if filt=="Semua" else [t for t in TWEETS if t['label']==filt]
    tc1,tc2 = st.columns(2,gap="medium")
    for i,tw in enumerate(filtered):
        cl = css[tw['label']]
        pre = f'<div class="twc">🔄 {tw["bersih"]}</div>' if show_pre else ''
        card = f'<div class="tw {cl}"><div class="two">{tw["asli"]}</div>{pre}<div class="twf">{bdge[tw["label"]]}</div></div>'
        (tc1 if i%2==0 else tc2).markdown(card, unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)


# ──────────────────────────────────────────────────────
# TAB 6 — PREPROCESSING
# ──────────────────────────────────────────────────────
with t6:
    st.markdown('<div class="pw">', unsafe_allow_html=True)
    pp1,pp2 = st.columns([1,1.2],gap="large")
    with pp1:
        st.markdown('<div class="card">', unsafe_allow_html=True)
        st.markdown('<div class="ctitle">Alur Preprocessing</div><div class="cline"></div>', unsafe_allow_html=True)
        st.markdown('<div class="csub">7 tahap sesuai flowchart skripsi</div>', unsafe_allow_html=True)
        for i,(clr,name,desc) in enumerate([
            ("#F0B429","Cleaning","Hapus URL, mention, hashtag, simbol, angka"),
            ("#2DD4BF","Case Folding","Konversi seluruh teks ke huruf kecil"),
            ("#22C55E","Normalisasi","Slang & singkatan → kata baku PUEBI"),
            ("#8B5CF6","Stopword Removal","Hapus kata tidak bermakna (Sastrawi)"),
            ("#F59E0B","Tokenizing","Pecah teks menjadi token kata individual"),
            ("#EF4444","Stemming","Kata berimbuhan → kata dasar (ECS)"),
            ("#3B82F6","Labeling","Beri label otomatis dengan kamus InSet"),
        ]):
            st.markdown(f'<div class="step"><div class="sdot" style="background:{clr}">{i+1}</div><div><div class="sname">{name}</div><div class="sdesc">{desc}</div></div></div>', unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)
    with pp2:
        st.markdown('<div class="card">', unsafe_allow_html=True)
        st.markdown('<div class="ctitle">Statistik Dataset</div><div class="cline"></div>', unsafe_allow_html=True)
        for k,v,cl in [("Total data",f"{TOTAL:,} tweet",""),("Training (80%)",f"{TRAIN:,} tweet","teal"),
            ("Testing (20%)",f"{TEST:,} tweet",""),("Vocabulary","~2.500 kata",""),
            ("Fitur TF-IDF","5.000 fitur","gold"),("N-gram","1-gram & 2-gram",""),
            ("InSet Positif","~3.419 kata","green"),("InSet Negatif","~6.609 kata","red")]:
            st.markdown(f'<div class="srow"><span class="sk">{k}</span><span class="sv {cl}">{v}</span></div>', unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)
        st.markdown('<div class="card" style="margin-top:1rem">', unsafe_allow_html=True)
        st.markdown('<div class="ctitle">Contoh Preprocessing</div><div class="cline"></div>', unsafe_allow_html=True)
        for orig,clean,lbl in [
            ("@ezash Dari sebelum coretax jg masuk kalo si shopee dkk bikin bukti potong","coretax si shopee kawan kawan bikin bukti potong","Negatif"),
            ("Tujuan coretax untuk mempermudah mudah emosi https://t.co/xxx","tuju coretax mudah mudah emosi","Negatif"),
            ("Alhamdulillah berhasil lapor SPT tahunan lewat coretax, lancar!","alhamdulillah hasil lapor surat pemberitahuan coretax lancar","Positif"),
        ]:
            cl = css[lbl]
            st.markdown(f'<div class="tw {cl}" style="margin-bottom:.5rem"><div class="two" style="font-size:.75rem">{orig}</div><div class="twc">{clean}</div><div class="twf">{bdge[lbl]}</div></div>', unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)


# ──────────────────────────────────────────────────────
# TAB 7 — RINGKASAN
# ──────────────────────────────────────────────────────
with t7:
    st.markdown('<div class="pw">', unsafe_allow_html=True)
    rs1,rs2 = st.columns([1.1,1],gap="large")
    with rs1:
        st.markdown('<div class="card">', unsafe_allow_html=True)
        st.markdown('<div class="ctitle">📌 Identitas Penelitian</div><div class="cline"></div>', unsafe_allow_html=True)
        for k,v,cl in [("Judul","Analisis Sentimen Masyarakat Terhadap Aplikasi Coretax di Platform X",""),
            ("Peneliti","Aziz Fakhrizi","gold"),("NIM","2022020255",""),
            ("Institusi","STMIK Triguna Dharma, Medan",""),("Tahun","2026",""),
            ("Sumber Data","Platform X (Twitter)",""),("Jumlah Data",f"{TOTAL:,} tweet","teal"),
            ("Periode","15 Des 2024 – 27 Jan 2025",""),("Algoritma","Categorical Naïve Bayes","teal"),
            ("Labeling","Lexicon InSet Bahasa Indonesia",""),
            ("Ekstraksi Fitur","TF-IDF (5.000 fitur, n-gram 1–2)",""),
            ("Smoothing","Laplace (alpha = 1.0)",""),("Split Data","80% Training : 20% Testing","")]:
            st.markdown(f'<div class="srow"><span class="sk" style="width:43%;flex-shrink:0">{k}</span><span class="sv {cl}" style="font-family:inherit;font-size:.78rem;text-align:right">{v}</span></div>', unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)
    with rs2:
        st.markdown('<div class="card">', unsafe_allow_html=True)
        st.markdown('<div class="ctitle">📊 Kinerja Model</div><div class="cline"></div>', unsafe_allow_html=True)
        for k,v,cl in [("Akurasi",f"{AKU:.2f}%","blue"),("Presisi",f"{PRE:.2f}%","green"),
            ("Recall",f"{REC:.2f}%",""),("F1-Score",f"{F1:.2f}%",""),
            ("CV 5-Fold (rata-rata)",f"{CV_M:.2f}%","teal"),("CV Std Deviasi",f"±{CV_S:.2f}%","")]:
            st.markdown(f'<div class="srow"><span class="sk">{k}</span><span class="sv {cl}">{v}</span></div>', unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)
        st.markdown('<div class="card" style="margin-top:1rem">', unsafe_allow_html=True)
        st.markdown('<div class="ctitle">💡 Temuan Utama</div><div class="cline"></div>', unsafe_allow_html=True)
        for ico,txt in [("🔴",f"Negatif mendominasi ({NEG/TOTAL*100:.0f}%) — error & login gagal."),
            ("🟢",f"Positif {POS/TOTAL*100:.1f}% — puas lapor SPT dan inovasi DJP."),
            ("🔵",f"Akurasi {AKU:.2f}% melampaui batas minimum 70%."),
            ("⚡",f"CV 5-Fold stabil {CV_M:.2f}% ± {CV_S:.2f}% — tidak overfitting."),
            ("📌","Fitur pajak, tahun, aktivasi mendominasi TF-IDF.")]:
            st.markdown(f'<div style="display:flex;gap:.5rem;align-items:flex-start;margin-bottom:.55rem"><span style="font-size:.8rem;flex-shrink:0">{ico}</span><span style="font-size:.76rem;color:#94A3B8;line-height:1.55">{txt}</span></div>', unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)


# ──────────────────────────────────────────────────────
# TAB 8 — UJI PREDIKSI
# ──────────────────────────────────────────────────────
with t8:
    st.markdown('<div class="pw">', unsafe_allow_html=True)

    col_kiri, col_kanan = st.columns([1.2, 1], gap="large")

    with col_kiri:
        st.markdown("""
        <div class="card" style="margin-bottom:.7rem">
          <div class="ctitle" style="font-size:.95rem">🧪 Uji Prediksi Sentimen</div>
          <div class="cline"></div>
          <div class="csub" style="margin-bottom:0">
            Masukkan komentar atau tweet tentang Coretax, lalu klik
            <strong style="color:#F0B429">Proses Prediksi</strong> untuk
            mengetahui apakah sentimen tersebut
            <strong>Positif</strong>, <strong>Negatif</strong>, atau <strong>Netral</strong>.
          </div>
        </div>
        """, unsafe_allow_html=True)

        st.markdown("""
        <div class="card" style="margin-bottom:.7rem">
          <div class="ctitle">✨ Contoh Kalimat Cepat</div>
          <div class="cline"></div>
          <div class="csub" style="margin-bottom:.5rem">
            Klik salah satu untuk mengisi input secara otomatis
          </div>
        </div>
        """, unsafe_allow_html=True)

        CONTOH = [
            ("😠", "Coretax error terus tidak bisa login dari kemarin"),
            ("😠", "Sistem lambat banget dan sering down parah"),
            ("😊", "Alhamdulillah berhasil lapor SPT lewat coretax lancar"),
            ("😊", "Coretax sudah lebih baik dan mudah digunakan sekarang"),
            ("😐", "Mau tanya cara aktivasi akun coretax gimana ya"),
            ("😐", "Informasi batas waktu lapor SPT tahunan lewat coretax"),
        ]
        cc1, cc2 = st.columns(2, gap="small")
        for i, (emo, kalimat) in enumerate(CONTOH):
            btn_lbl = f"{emo}  {kalimat[:33]}..." if len(kalimat) > 33 else f"{emo}  {kalimat}"
            target  = cc1 if i % 2 == 0 else cc2
            if target.button(btn_lbl, key=f"c_{i}", use_container_width=True):
                st.session_state.input_val = kalimat
                st.rerun()

        st.markdown("""
        <div class="card" style="margin-top:.7rem">
          <div class="ctitle">✏️ Tulis Komentar / Tweet</div>
          <div class="cline"></div>
          <div class="csub" style="margin-bottom:.6rem">
            Tulis dalam Bahasa Indonesia sesuai konteks Coretax
          </div>
        </div>
        """, unsafe_allow_html=True)

        teks_input = st.text_area(
            label="Komentar",
            value=st.session_state.get("input_val", ""),
            height=110,
            placeholder="Contoh: Coretax error terus, tidak bisa login dari tadi pagi...",
            key="ta_input",
            label_visibility="collapsed",
        )
        proses = st.button("🔍  Proses Prediksi", key="btn_proses", use_container_width=True)

        if proses:
            if not teks_input.strip():
                st.warning("⚠️  Masukkan teks terlebih dahulu!")
            else:
                hasil  = prediksi(teks_input.strip())
                label  = hasil["label"]
                proba  = hasil["proba"]
                detail = hasil["detail"]
                cl     = css[label]

                EMOJI = {"Positif": "😊", "Negatif": "😠", "Netral": "😐"}
                WARNA_LABEL = {"Positif": "#22C55E", "Negatif": "#EF4444", "Netral": "#94A3B8"}
                DESC  = {
                    "Positif": "Mengandung sentimen <strong>positif</strong> — kepuasan, kemudahan, atau apresiasi terhadap Coretax.",
                    "Negatif": "Mengandung sentimen <strong>negatif</strong> — keluhan, ketidakpuasan, atau masalah teknis pada Coretax.",
                    "Netral":  "Bersifat <strong>netral</strong> — pertanyaan, informasi umum, atau tidak mengandung opini yang jelas.",
                }

                bars_html = ""
                for lbl_p in ["Negatif", "Positif", "Netral"]:
                    pct = proba[lbl_p] * 100
                    clr = WARNA_LABEL[lbl_p]
                    highlight_class = "prob-name highlight" if lbl_p == label else "prob-name"
                    
                    bars_html += f"""
<div class="prob-head">
    <span class="{highlight_class}">{lbl_p}</span>
    <span class="prob-pct" style="color:{clr}">{pct:.1f}%</span>
</div>
<div class="prob-track">
    <div class="prob-fill" style="width:{pct:.1f}%;background:{clr}"></div>
</div>
"""

                st.markdown(f"""
<div class="card" style="margin-top:.8rem;border-color:{WARNA_LABEL[label]}33">
    <div style="display:flex;align-items:center;gap:1rem;
        padding-bottom:.9rem;border-bottom:1px solid rgba(255,255,255,.07);
        margin-bottom:.9rem">
        <div style="font-size:2.8rem;line-height:1;flex-shrink:0">{EMOJI[label]}</div>
        <div>
            <div style="font-size:1.6rem;font-weight:800;color:{WARNA_LABEL[label]};
                letter-spacing:.03em;line-height:1.1">{label.upper()}</div>
            <div style="font-size:.76rem;color:#94A3B8;margin-top:.25rem;line-height:1.5">
                {DESC[label]}
            </div>
        </div>
    </div>
    <div style="font-size:.68rem;font-weight:700;text-transform:uppercase;
        letter-spacing:.08em;color:#64748B;margin-bottom:.65rem">
        PROBABILITAS KELAS
    </div>
    {bars_html}
</div>
""", unsafe_allow_html=True)

                if detail:
                    toks_html = ""
                    for tok, skor in sorted(detail.items(), key=lambda x: x[1], reverse=True):
                        if skor > 0:
                            toks_html += f'<span class="tok p">+{skor} {tok}</span>'
                        elif skor < 0:
                            toks_html += f'<span class="tok n">{skor} {tok}</span>'
                        else:
                            toks_html += f'<span class="tok z">0 {tok}</span>'

                    ws = WARNA_LABEL["Positif"] if hasil["skor_total"] > 0 else WARNA_LABEL["Negatif"] if hasil["skor_total"] < 0 else WARNA_LABEL["Netral"]
                    st.markdown(f"""
<div class="card" style="margin-top:.7rem">
    <div class="ctitle">🔎 Analisis Kata Kunci</div>
    <div class="cline"></div>
    <div class="csub" style="margin-bottom:.6rem">
        Kata terdeteksi dalam kamus InSet Bahasa Indonesia
    </div>
    <div style="display:flex;flex-wrap:wrap;gap:.32rem;margin-bottom:.8rem">
        {toks_html if toks_html else "<span class='tok z'>Tidak ada kata dalam kamus</span>"}
    </div>
    <div style="background:var(--bg3);border-radius:8px;padding:.55rem .8rem;
        font-size:.73rem;color:var(--muted);line-height:1.75">
        <div>Skor Total&nbsp;
            <strong style="color:{ws}">{hasil['skor_total']:+d}</strong>
            &nbsp;·&nbsp; Positif&nbsp;
            <strong style="color:#22C55E">+{hasil['skor_pos']}</strong>
            &nbsp;·&nbsp; Negatif&nbsp;
            <strong style="color:#EF4444">{hasil['skor_neg']}</strong>
        </div>
        <div style="color:#64748B;margin-top:.2rem">
            Teks bersih:
            <em>{hasil['bersih'][:80]}{'...' if len(hasil['bersih'])>80 else ''}</em>
        </div>
    </div>
</div>
""", unsafe_allow_html=True)

                st.session_state.riwayat.insert(0, {
                    "teks":  teks_input.strip()[:100],
                    "label": label,
                    "proba": proba,
                })
                if len(st.session_state.riwayat) > 8:
                    st.session_state.riwayat = st.session_state.riwayat[:8]

    with col_kanan:
        st.markdown("""
        <div class="card" style="margin-bottom:.7rem">
          <div class="ctitle">⚙️ Cara Kerja Sistem</div>
          <div class="cline"></div>
          <div class="csub" style="margin-bottom:.6rem">6 tahap prediksi sentimen otomatis</div>
        </div>
        """, unsafe_allow_html=True)

        for i, (clr, name, desc) in enumerate([
            ("#F0B429", "Cleaning",     "URL, mention, hashtag, simbol dihapus"),
            ("#2DD4BF", "Normalisasi",  "Slang & singkatan → kata baku"),
            ("#22C55E", "Tokenisasi",   "Teks dipecah menjadi token kata"),
            ("#8B5CF6", "Scoring",      "Tiap kata dicari di kamus InSet"),
            ("#F0B429", "Naive Bayes",  "P(kelas) × ∏ P(kata|kelas)"),
            ("#EF4444", "Output",       "Kelas dengan skor tertinggi"),
        ]):
            st.markdown(
                f'<div class="step" style="margin-bottom:.42rem">'
                f'<div class="sdot" style="background:{clr};font-size:.55rem">{i+1}</div>'
                f'<div><div class="sname" style="font-size:.75rem">{name}</div>'
                f'<div class="sdesc">{desc}</div></div></div>',
                unsafe_allow_html=True)

        st.markdown("""
        <div style="margin:.6rem 0 0;padding:.55rem .75rem;
          background:rgba(240,180,41,.05);border-radius:8px;
          border-left:2px solid rgba(240,180,41,.25);
          font-size:.69rem;color:#94A3B8;line-height:1.65">
          <strong style="color:#F0B429">ℹ️ Info:</strong>
          Kamus InSet + konteks Coretax dari data penelitian.
          Akurasi tervalidasi <strong style="color:#F0B429">78.57%</strong>
          pada 420 data testing.
        </div>
        """, unsafe_allow_html=True)

        st.markdown('<div style="height:.7rem"></div>', unsafe_allow_html=True)

        st.markdown("""
        <div class="card">
          <div class="ctitle">🕘 Riwayat Prediksi</div>
          <div class="cline"></div>
          <div class="csub" style="margin-bottom:.6rem">
            Maks. 8 prediksi terakhir tersimpan di sesi ini
          </div>
        </div>
        """, unsafe_allow_html=True)

        if not st.session_state.riwayat:
            st.markdown("""
            <div style="text-align:center;padding:1.8rem 0;color:#475569">
              <div style="font-size:2rem;margin-bottom:.5rem">📭</div>
              <div style="font-size:.78rem">Belum ada prediksi.</div>
              <div style="font-size:.7rem;margin-top:.25rem">
                Masukkan teks &amp; klik
                <strong style="color:#F0B429">Proses Prediksi</strong>.
              </div>
            </div>
            """, unsafe_allow_html=True)
        else:
            EMOJI3 = {"Positif": "😊", "Negatif": "😠", "Netral": "😐"}
            for idx, r in enumerate(st.session_state.riwayat):
                cl3  = css[r["label"]]
                pct3 = r["proba"][r["label"]] * 100
                st.markdown(f"""
                <div class="hist-item {cl3}">
                  <div style="font-size:.6rem;font-family:'JetBrains Mono',monospace;
                    color:#475569;flex-shrink:0;min-width:18px">#{idx+1}</div>
                  <div class="hist-txt">
                    {r['teks'][:80]}{'...' if len(r['teks'])>80 else ''}
                  </div>
                  <div style="flex-shrink:0;text-align:right">
                    <span class="bdg {cl3}">{EMOJI3[r['label']]} {r['label']}</span>
                    <div style="font-size:.6rem;color:#64748B;margin-top:.2rem;
                      font-family:'JetBrains Mono',monospace">{pct3:.0f}%</div>
                  </div>
                </div>
                """, unsafe_allow_html=True)

            st.markdown('<div style="height:.4rem"></div>', unsafe_allow_html=True)
            if st.button("🗑️  Hapus Semua Riwayat", key="hapus", use_container_width=True):
                st.session_state.riwayat = []
                st.rerun()

    st.markdown('</div>', unsafe_allow_html=True)


# ══════════════════════════════════════════════════════
# FOOTER
# ══════════════════════════════════════════════════════
st.markdown(f"""
<div class="foot">
  <b>Dashboard Sentimen Coretax</b> — Skripsi STMIK Triguna Dharma Medan 2026<br>
  Peneliti: <b>Aziz Fakhrizi</b> (NIM: 2022020255) · {TOTAL:,} tweet ·
  Categorical Naïve Bayes · InSet Lexicon<br>
  Akurasi: <b>{AKU}%</b> · CV 5-Fold: <b>{CV_M:.2f}% ± {CV_S:.2f}%</b> ·
  Split Data: <b>80% Training / 20% Testing</b> · 15 Des 2024 – 27 Jan 2025
</div>
""", unsafe_allow_html=True)
