import streamlit as st
import plotly.graph_objects as go
import pandas as pd

st.set_page_config(
    page_title="Sentimen Coretax | Dashboard Publik",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# ═══════════════════════════════════════════════════
# CSS — Modern, Clean, Fully Responsive
# ═══════════════════════════════════════════════════
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&family=JetBrains+Mono:wght@400;600&display=swap');

:root {
  --bg:       #060B18;
  --bg1:      #0D1526;
  --bg2:      #152035;
  --bg3:      #1C2B47;
  --gold:     #F0B429;
  --gold-dim: rgba(240,180,41,0.12);
  --teal:     #2DD4BF;
  --blue:     #3B82F6;
  --green:    #22C55E;
  --red:      #EF4444;
  --slate:    #64748B;
  --muted:    #94A3B8;
  --text:     #E2E8F0;
  --border:   rgba(255,255,255,0.06);
  --r:        14px;
}

*, *::before, *::after { box-sizing: border-box; }

html, body, .stApp, [data-testid="stAppViewContainer"] {
  background: var(--bg) !important;
  color: var(--text) !important;
  font-family: 'Inter', sans-serif !important;
}

#MainMenu, footer, header,
[data-testid="stToolbar"],
[data-testid="stDecoration"] { display: none !important; }

.block-container {
  padding: 0 !important;
  max-width: 100% !important;
}

/* ── HERO ── */
.hero {
  background: linear-gradient(160deg, #0D1526 0%, #0A1020 60%, #060B18 100%);
  padding: clamp(1.5rem, 5vw, 3rem) clamp(1rem, 4vw, 3rem) clamp(1.2rem, 4vw, 2rem);
  border-bottom: 1px solid var(--border);
  position: relative; overflow: hidden;
}
.hero::after {
  content: '';
  position: absolute; inset: 0;
  background:
    radial-gradient(ellipse 50% 60% at 80% 20%, rgba(240,180,41,.06) 0%, transparent 70%),
    radial-gradient(ellipse 40% 50% at 10% 80%, rgba(45,212,191,.04) 0%, transparent 70%);
  pointer-events: none;
}
.hero-badge {
  display: inline-flex; align-items: center; gap:.4rem;
  background: var(--gold-dim); border: 1px solid rgba(240,180,41,.25);
  color: var(--gold); padding: .25rem .75rem; border-radius: 99px;
  font-size: .7rem; font-weight: 600; letter-spacing:.08em;
  text-transform: uppercase; margin-bottom: .9rem;
}
.hero-title {
  font-size: clamp(1.6rem, 4vw, 2.8rem); font-weight: 800;
  line-height: 1.15; color: #fff; margin: 0 0 .6rem;
}
.hero-title em { color: var(--gold); font-style: normal; }
.hero-desc {
  font-size: clamp(.82rem, 2vw, .95rem); color: var(--muted);
  line-height: 1.7; max-width: 640px; margin: 0 0 1.2rem;
}
.hero-pills { display: flex; flex-wrap: wrap; gap: .5rem; }
.hero-pill {
  background: rgba(255,255,255,.04); border: 1px solid var(--border);
  color: var(--muted); padding: .2rem .7rem; border-radius: 99px; font-size: .72rem;
}
.hero-pill b { color: var(--teal); }

/* ── METRIC STRIP ── */
.metric-strip {
  display: grid; grid-template-columns: repeat(4, 1fr);
  gap: 1px; background: var(--border); border-bottom: 1px solid var(--border);
}
@media (max-width: 640px) { .metric-strip { grid-template-columns: repeat(2, 1fr); } }
.metric-tile {
  background: var(--bg1);
  padding: clamp(.9rem,3vw,1.4rem) clamp(.8rem,3vw,1.6rem);
  position: relative;
}
.metric-tile::before {
  content: ''; position: absolute; top: 0; left: 0; right: 0; height: 2px;
}
.mt-total::before { background: linear-gradient(90deg, var(--teal), var(--gold)); }
.mt-neg::before   { background: var(--red); }
.mt-pos::before   { background: var(--green); }
.mt-net::before   { background: var(--slate); }
.metric-label {
  font-size: .65rem; font-weight: 600; letter-spacing:.1em;
  text-transform: uppercase; color: var(--slate); margin-bottom: .35rem;
}
.metric-val {
  font-family: 'JetBrains Mono', monospace;
  font-size: clamp(1.5rem, 3.5vw, 2.2rem);
  font-weight: 600; color: #fff; line-height: 1; margin-bottom: .2rem;
}
.metric-sub { font-size: .72rem; color: var(--slate); }
.metric-ico { position: absolute; top: 1rem; right: 1rem; font-size: 1.2rem; opacity: .15; }

/* ── TABS ── */
.stTabs { padding: 0 clamp(1rem,4vw,3rem) !important; }
.stTabs [data-baseweb="tab-list"] {
  background: transparent !important; border-bottom: 1px solid var(--border) !important;
  gap: 0 !important; padding: 0 !important; flex-wrap: wrap !important;
}
.stTabs [data-baseweb="tab"] {
  background: transparent !important; color: var(--slate) !important;
  border-bottom: 2px solid transparent !important; border-radius: 0 !important;
  font-size: .82rem !important; font-weight: 500 !important;
  padding: .75rem 1.1rem !important; margin: 0 !important;
}
.stTabs [data-baseweb="tab"]:hover { color: var(--text) !important; }
.stTabs [aria-selected="true"] {
  color: var(--gold) !important; border-bottom-color: var(--gold) !important;
  background: transparent !important; font-weight: 600 !important;
}
.stTabs [data-baseweb="tab-panel"] { padding: clamp(1rem,3vw,2rem) 0 0 0 !important; }

/* ── CARDS ── */
.card {
  background: var(--bg1); border: 1px solid var(--border);
  border-radius: var(--r); padding: clamp(1rem,3vw,1.5rem); height: 100%;
}
.card-title { font-size: .82rem; font-weight: 600; color: var(--text); margin-bottom: .15rem; }
.card-sub { font-size: .7rem; color: var(--slate); margin-bottom: 1rem; }
.card-divider { width: 24px; height: 2px; background: var(--gold); border-radius: 1px; margin: .4rem 0 .9rem; }

/* ── STAT ROWS ── */
.stat-row {
  display: flex; justify-content: space-between; align-items: center;
  padding: .55rem 0; border-bottom: 1px solid var(--border); font-size: .8rem;
}
.stat-row:last-child { border-bottom: none; }
.stat-key { color: var(--muted); }
.stat-val { color: var(--text); font-weight: 500; font-family: 'JetBrains Mono', monospace; }
.stat-val.gold  { color: var(--gold); }
.stat-val.teal  { color: var(--teal); }
.stat-val.green { color: var(--green); }
.stat-val.red   { color: var(--red); }
.stat-val.blue  { color: var(--blue); }

/* ── TWEET CARDS ── */
.tweet {
  background: var(--bg2); border: 1px solid var(--border);
  border-left: 3px solid; border-radius: 10px;
  padding: .9rem 1rem; margin-bottom: .6rem;
}
.tweet.neg { border-left-color: var(--red); }
.tweet.pos { border-left-color: var(--green); }
.tweet.net { border-left-color: var(--slate); }
.tweet-orig { font-size: .8rem; color: var(--text); line-height: 1.6; margin-bottom: .35rem; }
.tweet-clean {
  font-size: .72rem; color: var(--muted); font-family: 'JetBrains Mono', monospace;
  background: var(--bg3); padding: .35rem .6rem; border-radius: 6px;
  margin-bottom: .35rem; line-height: 1.5;
}
.tweet-footer { display: flex; gap: .5rem; align-items: center; flex-wrap: wrap; }
.badge { padding: .15rem .55rem; border-radius: 99px; font-size: .62rem; font-weight: 700; letter-spacing:.05em; }
.badge.neg { background: rgba(239,68,68,.12); color: #FCA5A5; }
.badge.pos { background: rgba(34,197,94,.12);  color: #86EFAC; }
.badge.net { background: rgba(100,116,139,.12); color: #94A3B8; }

/* ── INSIGHT ── */
.insight {
  background: var(--bg2); border: 1px solid var(--border);
  border-radius: 10px; padding: 1rem 1.1rem;
}
.insight-val {
  font-family: 'JetBrains Mono', monospace;
  font-size: 1.8rem; font-weight: 600; color: var(--gold); line-height: 1.2;
}
.insight-label {
  font-size: .72rem; font-weight: 600; text-transform: uppercase;
  letter-spacing:.08em; color: var(--slate); margin-bottom: .25rem;
}
.insight-desc { font-size: .75rem; color: var(--muted); line-height: 1.55; margin-top: .3rem; }

/* ── FOLD GRID ── */
.fold-grid {
  display: grid; grid-template-columns: repeat(5,1fr); gap: .5rem; margin-top: .75rem;
}
@media (max-width: 640px) { .fold-grid { grid-template-columns: repeat(3,1fr); } }
.fold-pill {
  background: var(--bg3); border: 1px solid var(--border);
  border-radius: 8px; padding: .5rem .4rem; text-align: center;
}
.fold-name { font-size: .62rem; color: var(--slate); margin-bottom: .2rem; }
.fold-val { font-family: 'JetBrains Mono', monospace; font-size: .88rem; font-weight: 600; color: var(--teal); }

/* ── STEP ── */
.step { display: flex; gap: .65rem; align-items: flex-start; margin-bottom: .65rem; }
.step-dot {
  width: 22px; height: 22px; border-radius: 50%; flex-shrink: 0;
  display: flex; align-items: center; justify-content: center;
  font-size: .6rem; font-weight: 800; color: #060B18; margin-top: 1px;
}
.step-name { font-size: .8rem; font-weight: 600; color: var(--text); }
.step-desc { font-size: .68rem; color: var(--slate); margin-top: .1rem; }

/* ── PAGE WRAP ── */
.page-wrap { padding: 0 clamp(1rem,4vw,3rem); }

/* ── FOOTER ── */
.footer {
  border-top: 1px solid var(--border); margin-top: 2rem;
  padding: 1.2rem clamp(1rem,4vw,3rem);
  text-align: center; font-size: .7rem; color: var(--slate); line-height: 1.8;
}
.footer b { color: var(--gold); }

/* Streamlit overrides */
.stSelectbox > div > div { background: var(--bg2) !important; border-color: var(--border) !important; border-radius: 8px !important; }
label { color: var(--muted) !important; font-size: .8rem !important; }
::-webkit-scrollbar { width: 4px; height: 4px; }
::-webkit-scrollbar-track { background: var(--bg); }
::-webkit-scrollbar-thumb { background: var(--bg3); border-radius: 2px; }
</style>
""", unsafe_allow_html=True)


# ═══════════════════════════════════════════════════
# DATA AKTUAL — dari file Excel & gambar yang dikirim
# ═══════════════════════════════════════════════════
TOTAL = 2096
NEG   = 1611   # 76.9%
POS   = 359    # 17.1%
NET   = 126    # 6.0%

P_NEG = 0.768496
P_POS = 0.171241
P_NET = 0.060263
TRAIN = 1676
TEST  = 420

AKU  = 78.57
PRE  = 74.75
REC  = 78.57
F1   = 75.51

CV   = [78.33, 79.00, 77.33, 77.57, 79.47]
CV_M = 78.34
CV_S = 0.82

CM_LABELS = ['Positif', 'Netral', 'Negatif']
CM_VALUES = [
    [29,  0,  43],
    [ 2,  1,  22],
    [21,  2, 300],
]

TFIDF = {
    'pajak':0.041,'tahun':0.031,'aktivasi':0.031,'akun':0.028,
    'wajib':0.025,'wajib pajak':0.024,'nomor':0.023,'akun coretax':0.022,
    'kak':0.022,'surat':0.021,'pemberitahuan':0.020,'surat pemberitahuan':0.020,
    'pemberitahuan tahun':0.020,'lapor':0.020,'aktivasi akun':0.020,
    'aktivasi coretax':0.017,'pokok':0.017,'pokok wajib':0.017,
    'nomor pokok':0.017,'email':0.016,'kakak':0.015,
    'daftar':0.015,'data':0.015,'min':0.015,'jenderal':0.015,
}

TWEETS = [
    {"asli":"Apakah perlu menyatukan satu nomor wajib pajak bagi Suami-Istri ASN di Coretax? Jika perlu bagaimana caranya apabila akun coretax sudah dibuat?",
     "bersih":"satu nomor wajib pajak suami istri asn coretax instansi akun coretax","label":"Negatif"},
    {"asli":"Halo kak, jikalau karyawan ingin hanya registrasi coretax tapi kendala KK nya sudah hilang karena bercerai dan belum diurus di dukcapil, bagaimana cara daftarnya?",
     "bersih":"kak karyawan registrasi coretax kendala kk hilang cerai urus dukcapil daftar nomor kk","label":"Negatif"},
    {"asli":"Tujuan coretax untuk mempermudah tapi malah bikin emosi. Sudah coba berkali-kali tetap tidak bisa login.",
     "bersih":"tuju coretax mudah mudah emosi berkali login","label":"Negatif"},
    {"asli":"Coretax error terus, tidak bisa akses sejak pagi. Deadline lapor pajak sudah dekat tapi sistem malah down.",
     "bersih":"coretax error akses deadline lapor pajak dekat sistem down","label":"Negatif"},
    {"asli":"Alhamdulillah berhasil lapor SPT tahunan lewat coretax, lancar sekali! Terima kasih DJP sudah berinovasi.",
     "bersih":"alhamdulillah hasil lapor surat pemberitahuan tahun coretax lancar terima kasih djp inovasi","label":"Positif"},
    {"asli":"Ijin kak, buat yang mau tanya soal CoreTax ke aku boleh ya, aku bantu sebisaku untuk urusan perpajakan, gratis!",
     "bersih":"ijin kakak coretax bantu sebisaku handle klien urusan perpajakan gratis","label":"Positif"},
    {"asli":"Coretax sekarang sudah jauh lebih baik dan mudah digunakan. Tampilannya modern dan responsif.",
     "bersih":"coretax baik mudah tampilan modern responsif","label":"Positif"},
    {"asli":"Deadline lapor SPT tahunan orang pribadi melalui coretax adalah 31 Maret 2025. Segera lapor sebelum terlambat.",
     "bersih":"deadline lapor surat pemberitahuan tahun pribadi coretax maret lapor","label":"Netral"},
    {"asli":"Coretax adalah sistem administrasi perpajakan terbaru dari Direktorat Jenderal Pajak yang diluncurkan akhir 2024.",
     "bersih":"coretax sistem administrasi perpajakan baru direktorat jenderal pajak luncur akhir tahun","label":"Netral"},
    {"asli":"NIK Kakak telah terdaftar di Coretax, silakan pilih Aktivasi Akun Wajib Pajak pada laman awal Coretax agar dapat login.",
     "bersih":"nik kakak daftar coretax sila pilih aktivasi akun wajib pajak laman coretax login","label":"Netral"},
]

PT = dict(
    paper_bgcolor='rgba(0,0,0,0)',
    plot_bgcolor='rgba(0,0,0,0)',
    font=dict(family='Inter', color='#94A3B8', size=11),
    margin=dict(l=8, r=8, t=28, b=8),
)

css_map   = {'Positif':'pos','Negatif':'neg','Netral':'net'}
badge_map = {
    'Positif':'<span class="badge pos">😊 POSITIF</span>',
    'Negatif':'<span class="badge neg">😠 NEGATIF</span>',
    'Netral' :'<span class="badge net">😐 NETRAL</span>',
}


# ═══════════════════════════════════════════════════
# HERO
# ═══════════════════════════════════════════════════
st.markdown(f"""
<div class="hero">
  <div class="hero-badge">📊 Skripsi · STMIK Triguna Dharma · 2025</div>
  <h1 class="hero-title">Sentimen Masyarakat<br>terhadap <em>Coretax</em> di Platform X</h1>
  <p class="hero-desc">
    Analisis persepsi publik terhadap sistem perpajakan digital Coretax berdasarkan
    <strong style="color:#E2E8F0">{TOTAL:,} tweet</strong> menggunakan
    Categorical Naïve Bayes. Akurasi model <strong style="color:#F0B429">{AKU}%</strong>.
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


# ═══════════════════════════════════════════════════
# METRIC STRIP
# ═══════════════════════════════════════════════════
st.markdown(f"""
<div class="metric-strip">
  <div class="metric-tile mt-total">
    <div class="metric-ico">🐦</div>
    <div class="metric-label">Total Tweet</div>
    <div class="metric-val">{TOTAL:,}</div>
    <div class="metric-sub">Periode 44 hari</div>
  </div>
  <div class="metric-tile mt-neg">
    <div class="metric-ico">😠</div>
    <div class="metric-label">Negatif</div>
    <div class="metric-val">{NEG:,}</div>
    <div class="metric-sub">{NEG/TOTAL*100:.1f}% dari total</div>
  </div>
  <div class="metric-tile mt-pos">
    <div class="metric-ico">😊</div>
    <div class="metric-label">Positif</div>
    <div class="metric-val">{POS:,}</div>
    <div class="metric-sub">{POS/TOTAL*100:.1f}% dari total</div>
  </div>
  <div class="metric-tile mt-net">
    <div class="metric-ico">😐</div>
    <div class="metric-label">Netral</div>
    <div class="metric-val">{NET:,}</div>
    <div class="metric-sub">{NET/TOTAL*100:.1f}% dari total</div>
  </div>
</div>
""", unsafe_allow_html=True)


# ═══════════════════════════════════════════════════
# TABS
# ═══════════════════════════════════════════════════
tab1, tab2, tab3, tab4, tab5 = st.tabs([
    "📊  Distribusi",
    "📈  Evaluasi Model",
    "💬  Ulasan Publik",
    "🔄  Preprocessing",
    "📋  Ringkasan",
])


# ──────────────────────────────────────────────
# TAB 1
# ──────────────────────────────────────────────
with tab1:
    st.markdown('<div class="page-wrap">', unsafe_allow_html=True)

    c1, c2 = st.columns([1, 1.4], gap="large")

    with c1:
        st.markdown('<div class="card">', unsafe_allow_html=True)
        st.markdown('<div class="card-title">Proporsi Sentimen</div><div class="card-divider"></div>', unsafe_allow_html=True)
        st.markdown(f'<div class="card-sub">Total {TOTAL:,} tweet — Labeling InSet Lexicon</div>', unsafe_allow_html=True)
        fig = go.Figure(go.Pie(
            labels=['Negatif','Positif','Netral'], values=[NEG,POS,NET],
            hole=0.64,
            marker=dict(colors=['#EF4444','#22C55E','#475569'], line=dict(color='#060B18',width=3)),
            textinfo='percent', textfont=dict(size=12,family='JetBrains Mono',color='white'),
            insidetextorientation='horizontal',
            hovertemplate='<b>%{label}</b><br>%{value:,} tweet<br>%{percent:.1%}<extra></extra>',
            direction='clockwise', sort=False,
        ))
        fig.add_annotation(x=0.5,y=0.5,showarrow=False,
            text=f"<span style='font-size:24px;font-weight:700;color:#EF4444'>{NEG/TOTAL*100:.0f}%</span><br><span style='font-size:10px;color:#64748B'>Negatif</span>",
            font=dict(family='JetBrains Mono'))
        fig.update_layout(**PT, height=295, margin=dict(l=8,r=8,t=16,b=36),
            legend=dict(orientation='h',x=0.5,y=-0.12,xanchor='center',
                        font=dict(size=11),bgcolor='rgba(0,0,0,0)'))
        st.plotly_chart(fig, use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)

    with c2:
        st.markdown('<div class="card">', unsafe_allow_html=True)
        st.markdown('<div class="card-title">Jumlah Tweet per Kelas</div><div class="card-divider"></div>', unsafe_allow_html=True)
        st.markdown('<div class="card-sub">Perbandingan volume tiap kategori sentimen</div>', unsafe_allow_html=True)
        fig2 = go.Figure()
        for lbl,val,clr in [('Negatif',NEG,'#EF4444'),('Positif',POS,'#22C55E'),('Netral',NET,'#475569')]:
            fig2.add_trace(go.Bar(
                y=[lbl],x=[val],orientation='h',name=lbl,
                marker=dict(color=clr,line=dict(width=0)),
                text=f'  {val:,}  ({val/TOTAL*100:.1f}%)',
                textposition='inside',textfont=dict(size=12,color='white',family='JetBrains Mono'),
                hovertemplate=f'<b>{lbl}</b>: {val:,} tweet<extra></extra>',
            ))
        fig2.update_layout(**PT,height=210,showlegend=False,
            margin=dict(l=8,r=8,t=16,b=30),
            xaxis=dict(title='Jumlah Tweet',showgrid=True,gridcolor='rgba(255,255,255,.04)',tickfont=dict(size=10)),
            yaxis=dict(title='',tickfont=dict(size=12)),bargap=0.3)
        st.plotly_chart(fig2, use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)

    # TF-IDF
    st.markdown('<div class="card" style="margin-top:1rem">', unsafe_allow_html=True)
    st.markdown('<div class="card-title">Top 25 Fitur TF-IDF</div><div class="card-divider"></div>', unsafe_allow_html=True)
    st.markdown('<div class="card-sub">Kata/frasa dengan bobot rata-rata TF-IDF tertinggi — n-gram 1–2, min_df=2, max_features=5000</div>', unsafe_allow_html=True)
    tdf = pd.DataFrame(list(TFIDF.items()),columns=['f','b']).sort_values('b')
    blues = [f'rgba(59,130,246,{0.35+0.65*(i/len(tdf)):.2f})' for i in range(len(tdf))]
    fig3 = go.Figure(go.Bar(
        x=tdf['b'],y=tdf['f'],orientation='h',
        marker=dict(color=blues,line=dict(width=0)),
        hovertemplate='<b>%{y}</b><br>Bobot: %{x:.3f}<extra></extra>',
    ))
    fig3.update_layout(**PT,height=480,margin=dict(l=8,r=56,t=16,b=36),
        xaxis=dict(title='Rata-rata Skor TF-IDF',showgrid=True,gridcolor='rgba(255,255,255,.04)',tickfont=dict(size=10)),
        yaxis=dict(title='',tickfont=dict(size=10.5),automargin=True))
    st.plotly_chart(fig3, use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)

    st.markdown('<br>', unsafe_allow_html=True)
    ia,ib,ic = st.columns(3,gap="medium")
    with ia:
        st.markdown(f"""<div class="insight"><div class="insight-label">Dominasi Negatif</div>
          <div class="insight-val">{NEG/TOTAL*100:.1f}%</div>
          <div class="insight-desc">Keluhan utama: <em>error sistem</em>, <em>login gagal</em>, dan <em>lambat/down</em>.</div></div>""",unsafe_allow_html=True)
    with ib:
        st.markdown(f"""<div class="insight"><div class="insight-label">Sentimen Positif</div>
          <div class="insight-val">{POS/TOTAL*100:.1f}%</div>
          <div class="insight-desc">Pengguna puas memuji kemudahan lapor SPT dan inovasi DJP.</div></div>""",unsafe_allow_html=True)
    with ic:
        st.markdown(f"""<div class="insight"><div class="insight-label">Fitur TF-IDF #1</div>
          <div class="insight-val">pajak</div>
          <div class="insight-desc">Bobot tertinggi 0.041, diikuti <em>tahun</em> (0.031) dan <em>aktivasi</em> (0.031).</div></div>""",unsafe_allow_html=True)

    st.markdown('</div>', unsafe_allow_html=True)


# ──────────────────────────────────────────────
# TAB 2
# ──────────────────────────────────────────────
with tab2:
    st.markdown('<div class="page-wrap">', unsafe_allow_html=True)

    g1,g2,g3,g4 = st.columns(4,gap="medium")
    for col,name,val,clr in [(g1,"Akurasi",AKU,'#3B82F6'),(g2,"Presisi",PRE,'#22C55E'),(g3,"Recall",REC,'#F59E0B'),(g4,"F1-Score",F1,'#8B5CF6')]:
        with col:
            fig_g = go.Figure(go.Indicator(
                mode="gauge+number", value=val,
                number={'suffix':'%','font':{'size':22,'color':clr,'family':'JetBrains Mono'}},
                title={'text':name,'font':{'size':12,'color':'#94A3B8'}},
                gauge=dict(
                    axis=dict(range=[0,100],tickfont=dict(size=8,color='#475569'),tickcolor='#1C2B47',nticks=6),
                    bar=dict(color=clr,thickness=0.26),
                    bgcolor='#152035',bordercolor='#152035',borderwidth=0,
                    steps=[{'range':[0,70],'color':'rgba(255,255,255,0.02)'},
                           {'range':[70,100],'color':f'rgba({int(clr[1:3],16)},{int(clr[3:5],16)},{int(clr[5:7],16)},0.07)'}],
                    threshold=dict(line=dict(color='#F0B429',width=2.5),thickness=0.7,value=70),
                )
            ))
            fig_g.update_layout(**PT,height=185,margin=dict(l=4,r=4,t=20,b=4))
            col.plotly_chart(fig_g, use_container_width=True)

    st.markdown('<div style="text-align:center;font-size:.7rem;color:#475569;margin:-0.5rem 0 1.2rem">— Garis kuning = batas minimum 70% —</div>',unsafe_allow_html=True)

    ev1,ev2 = st.columns([1.1,1],gap="large")
    with ev1:
        st.markdown('<div class="card">', unsafe_allow_html=True)
        st.markdown('<div class="card-title">Perbandingan Metrik Evaluasi</div><div class="card-divider"></div>',unsafe_allow_html=True)
        st.markdown('<div class="card-sub">Akurasi, Presisi, Recall, F1-Score — 420 data testing</div>',unsafe_allow_html=True)
        fig_ev = go.Figure()
        for nm,vl,cl in [('Akurasi',AKU,'#3B82F6'),('Presisi',PRE,'#22C55E'),('Recall',REC,'#F59E0B'),('F1-Score',F1,'#8B5CF6')]:
            fig_ev.add_trace(go.Bar(x=[nm],y=[vl],name=nm,
                marker=dict(color=cl,line=dict(width=0)),
                text=f'{vl:.2f}%',textposition='outside',
                textfont=dict(size=11,color=cl,family='JetBrains Mono'),width=0.45))
        fig_ev.add_hline(y=70,line_dash='dot',line_color='#F0B429',line_width=1.5,
                         annotation_text='Min 70%',annotation_font=dict(size=9,color='#F0B429'))
        fig_ev.update_layout(**PT,height=280,showlegend=False,margin=dict(l=8,r=8,t=16,b=8),
            xaxis=dict(showgrid=False,tickfont=dict(size=11)),
            yaxis=dict(range=[0,93],showgrid=True,gridcolor='rgba(255,255,255,.04)',tickfont=dict(size=10)))
        st.plotly_chart(fig_ev, use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)

    with ev2:
        st.markdown('<div class="card">', unsafe_allow_html=True)
        st.markdown('<div class="card-title">Cross Validation — 5-Fold</div><div class="card-divider"></div>',unsafe_allow_html=True)
        st.markdown(f'<div class="card-sub">Rata-rata {CV_M:.2f}% ± {CV_S:.2f}% — model stabil & tidak overfitting</div>',unsafe_allow_html=True)
        fig_cv = go.Figure()
        fig_cv.add_trace(go.Bar(
            x=[f'Fold {i+1}' for i in range(5)],y=CV,
            marker=dict(color='#2DD4BF',line=dict(width=0)),
            text=[f'{v:.2f}%' for v in CV],textposition='outside',
            textfont=dict(size=10,color='#2DD4BF',family='JetBrains Mono'),width=0.5))
        fig_cv.add_hline(y=CV_M,line_dash='dash',line_color='#F0B429',line_width=1.5,
                         annotation_text=f'Rata-rata: {CV_M:.2f}%',annotation_font=dict(size=9,color='#F0B429'))
        fig_cv.update_layout(**PT,height=245,margin=dict(l=8,r=8,t=16,b=8),
            xaxis=dict(showgrid=False,tickfont=dict(size=10)),
            yaxis=dict(range=[76,81],showgrid=True,gridcolor='rgba(255,255,255,.04)',tickfont=dict(size=10),title='Akurasi (%)'))
        st.plotly_chart(fig_cv, use_container_width=True)
        folds_html=''.join([f'<div class="fold-pill"><div class="fold-name">Fold {i+1}</div><div class="fold-val">{v:.2f}%</div></div>' for i,v in enumerate(CV)])
        st.markdown(f'<div class="fold-grid">{folds_html}</div>',unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)

    # Confusion Matrix
    st.markdown('<div class="card" style="margin-top:1rem">', unsafe_allow_html=True)
    st.markdown('<div class="card-title">Confusion Matrix</div><div class="card-divider"></div>',unsafe_allow_html=True)
    st.markdown('<div class="card-sub">Matriks klasifikasi aktual vs prediksi pada 420 data testing</div>',unsafe_allow_html=True)

    cm1,cm2 = st.columns([1.5,1],gap="large")
    with cm1:
        fig_cm = go.Figure(go.Heatmap(
            z=CM_VALUES,
            x=['Pred: Positif','Pred: Netral','Pred: Negatif'],
            y=['Aktual: Positif','Aktual: Netral','Aktual: Negatif'],
            text=[[str(v) for v in row] for row in CM_VALUES],
            texttemplate='<b>%{text}</b>',
            textfont={'size':16,'color':'white','family':'JetBrains Mono'},
            colorscale=[[0,'#152035'],[0.15,'#1E3A5F'],[0.5,'#2563EB'],[1,'#1D4ED8']],
            showscale=False,
            hovertemplate='Aktual: %{y}<br>Prediksi: %{x}<br>Jumlah: %{z}<extra></extra>',
        ))
        fig_cm.update_layout(**PT,height=270,margin=dict(l=8,r=8,t=8,b=8),
            xaxis=dict(tickfont=dict(size=10),side='bottom'),
            yaxis=dict(tickfont=dict(size=10),autorange='reversed'))
        st.plotly_chart(fig_cm, use_container_width=True)

    with cm2:
        st.markdown('<br>',unsafe_allow_html=True)
        cm_stats = [
            ("✅ True Positif (TP)","29","green"),
            ("✅ True Netral (TP)","1",""),
            ("✅ True Negatif (TP)","300","red"),
            ("❌ Positif → Negatif","43","red"),
            ("❌ Netral → Negatif","22",""),
            ("❌ Negatif → Positif","21","green"),
            ("❌ Negatif → Netral","2",""),
        ]
        for lbl,val,cl in cm_stats:
            st.markdown(f"""<div class="stat-row">
              <span class="stat-key" style="font-size:.74rem">{lbl}</span>
              <span class="stat-val {cl}">{val}</span></div>""",unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

    # Prior P(Vj)
    st.markdown('<div class="card" style="margin-top:1rem">', unsafe_allow_html=True)
    st.markdown('<div class="card-title">Probabilitas Prior P(Vj)</div><div class="card-divider"></div>',unsafe_allow_html=True)
    st.markdown(f'<div class="card-sub">P(Vj) = |doc j| / |training| — dari {TRAIN:,} data training</div>',unsafe_allow_html=True)
    pa,pb,pc = st.columns(3,gap="medium")
    for col,label,jml,prob,clr in [(pa,"V1 = Negatif",1288,P_NEG,"#EF4444"),(pb,"V2 = Positif",287,P_POS,"#22C55E"),(pc,"V3 = Netral",101,P_NET,"#64748B")]:
        with col:
            col.markdown(f"""<div class="insight" style="border-left:3px solid {clr}">
              <div class="insight-label">{label}</div>
              <div class="insight-val" style="color:{clr};font-size:1.5rem">{prob:.6f}</div>
              <div class="insight-desc">{jml:,} / {TRAIN:,} tweet training</div></div>""",unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)


# ──────────────────────────────────────────────
# TAB 3
# ──────────────────────────────────────────────
with tab3:
    st.markdown('<div class="page-wrap">', unsafe_allow_html=True)
    st.markdown('<div class="card-title" style="font-size:1rem">Ulasan Masyarakat tentang Coretax</div><div class="card-divider"></div>',unsafe_allow_html=True)
    st.markdown('<div class="card-sub" style="margin-bottom:1rem">Sampel tweet dari Platform X yang telah dianalisis sentimen-nya menggunakan Categorical Naïve Bayes</div>',unsafe_allow_html=True)

    f1c,f2c = st.columns([1,2],gap="medium")
    with f1c:
        filter_lbl = st.selectbox("Filter Sentimen",["Semua","Negatif","Positif","Netral"])
    with f2c:
        show_pre = st.checkbox("Tampilkan hasil preprocessing",value=True)

    filtered = TWEETS if filter_lbl=="Semua" else [t for t in TWEETS if t['label']==filter_lbl]
    tc1,tc2 = st.columns(2,gap="medium")
    for i,tw in enumerate(filtered):
        cl = css_map[tw['label']]
        pre_html = f'<div class="tweet-clean">🔄 {tw["bersih"]}</div>' if show_pre else ''
        card = f'<div class="tweet {cl}"><div class="tweet-orig">{tw["asli"]}</div>{pre_html}<div class="tweet-footer">{badge_map[tw["label"]]}</div></div>'
        (tc1 if i%2==0 else tc2).markdown(card, unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)


# ──────────────────────────────────────────────
# TAB 4
# ──────────────────────────────────────────────
with tab4:
    st.markdown('<div class="page-wrap">', unsafe_allow_html=True)
    pp1,pp2 = st.columns([1,1.2],gap="large")

    with pp1:
        st.markdown('<div class="card">', unsafe_allow_html=True)
        st.markdown('<div class="card-title">Alur Preprocessing</div><div class="card-divider"></div>',unsafe_allow_html=True)
        st.markdown('<div class="card-sub">7 tahap sesuai flowchart skripsi</div>',unsafe_allow_html=True)
        steps = [
            ("#F0B429","Cleaning","Hapus URL, mention (@), hashtag (#), simbol, angka"),
            ("#2DD4BF","Case Folding","Konversi seluruh teks ke huruf kecil"),
            ("#22C55E","Normalisasi","Slang & singkatan → kata baku PUEBI"),
            ("#8B5CF6","Stopword Removal","Hapus kata tidak bermakna (Sastrawi + custom)"),
            ("#F59E0B","Tokenizing","Pecah teks menjadi token kata individual"),
            ("#EF4444","Stemming","Kata berimbuhan → kata dasar (Sastrawi ECS)"),
            ("#3B82F6","Labeling","Beri label otomatis dengan kamus InSet"),
        ]
        for i,(clr,name,desc) in enumerate(steps):
            st.markdown(f"""<div class="step">
              <div class="step-dot" style="background:{clr}">{i+1}</div>
              <div><div class="step-name">{name}</div><div class="step-desc">{desc}</div></div>
            </div>""",unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)

    with pp2:
        st.markdown('<div class="card">', unsafe_allow_html=True)
        st.markdown('<div class="card-title">Statistik Dataset</div><div class="card-divider"></div>',unsafe_allow_html=True)
        stats = [
            ("Total data","2,096 tweet",""),
            ("Data training (80%)","1,676 tweet","teal"),
            ("Data testing (20%)","420 tweet",""),
            ("Vocabulary unik","~2.500 kata",""),
            ("Fitur TF-IDF","5.000 fitur","gold"),
            ("N-gram range","1-gram & 2-gram",""),
            ("Kamus normalisasi","80+ entri slang",""),
            ("InSet Positif","~3.419 kata","green"),
            ("InSet Negatif","~6.609 kata","red"),
        ]
        for k,v,cl in stats:
            st.markdown(f'<div class="stat-row"><span class="stat-key">{k}</span><span class="stat-val {cl}">{v}</span></div>',unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)

        st.markdown('<div class="card" style="margin-top:1rem">', unsafe_allow_html=True)
        st.markdown('<div class="card-title">Contoh Preprocessing</div><div class="card-divider"></div>',unsafe_allow_html=True)
        ex = [
            ("@ezash Dari sebelum coretax jg masuk kalo si shopee dkk bikin bukti potong","coretax si shopee kawan kawan bikin bukti potong","Negatif"),
            ("Tujuan coretax untuk mempermudah mudah emosi https://t.co/xxx","tuju coretax mudah mudah emosi","Negatif"),
            ("Alhamdulillah berhasil lapor SPT tahunan lewat coretax, lancar!","alhamdulillah hasil lapor surat pemberitahuan tahun coretax lancar","Positif"),
        ]
        for orig,clean,lbl in ex:
            cl=css_map[lbl]
            st.markdown(f'<div class="tweet {cl}" style="margin-bottom:.5rem"><div class="tweet-orig" style="font-size:.75rem">{orig}</div><div class="tweet-clean">{clean}</div><div class="tweet-footer">{badge_map[lbl]}</div></div>',unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)

    st.markdown('</div>', unsafe_allow_html=True)


# ──────────────────────────────────────────────
# TAB 5
# ──────────────────────────────────────────────
with tab5:
    st.markdown('<div class="page-wrap">', unsafe_allow_html=True)
    rs1,rs2 = st.columns([1.1,1],gap="large")

    with rs1:
        st.markdown('<div class="card">', unsafe_allow_html=True)
        st.markdown('<div class="card-title">📌 Identitas Penelitian</div><div class="card-divider"></div>',unsafe_allow_html=True)
        info = [
            ("Judul","Analisis Sentimen Masyarakat Terhadap Aplikasi Coretax di Platform X",""),
            ("Peneliti","Aziz Fakhrizi","gold"),("NIM","2022020255",""),
            ("Institusi","STMIK Triguna Dharma, Medan",""),("Tahun","2025",""),
            ("Sumber Data","Platform X (Twitter)",""),("Jumlah Data",f"{TOTAL:,} tweet","teal"),
            ("Periode","15 Des 2024 – 27 Jan 2025",""),
            ("Algoritma","Categorical Naïve Bayes","teal"),
            ("Labeling","Lexicon InSet Bahasa Indonesia",""),
            ("Ekstraksi Fitur","TF-IDF (5.000 fitur, n-gram 1–2)",""),
            ("Smoothing","Laplace (alpha = 1.0)",""),
            ("Split Data","Training 80% : Testing 20%",""),
        ]
        for k,v,cl in info:
            st.markdown(f'<div class="stat-row"><span class="stat-key" style="width:42%;flex-shrink:0">{k}</span><span class="stat-val {cl}" style="text-align:right;font-family:inherit;font-size:.78rem">{v}</span></div>',unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)

    with rs2:
        st.markdown('<div class="card">', unsafe_allow_html=True)
        st.markdown('<div class="card-title">📊 Kinerja Model</div><div class="card-divider"></div>',unsafe_allow_html=True)
        for k,v,cl in [("Akurasi",f"{AKU:.2f}%","blue"),("Presisi",f"{PRE:.2f}%","green"),
                        ("Recall",f"{REC:.2f}%",""),("F1-Score",f"{F1:.2f}%",""),
                        ("CV 5-Fold Rata-rata",f"{CV_M:.2f}%","teal"),("CV Std Deviasi",f"±{CV_S:.2f}%","")]:
            st.markdown(f'<div class="stat-row"><span class="stat-key">{k}</span><span class="stat-val {cl}">{v}</span></div>',unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)

        st.markdown('<div class="card" style="margin-top:1rem">', unsafe_allow_html=True)
        st.markdown('<div class="card-title">💡 Temuan Utama</div><div class="card-divider"></div>',unsafe_allow_html=True)
        for ico,txt in [
            ("🔴",f"Sentimen negatif mendominasi ({NEG/TOTAL*100:.0f}%) — error sistem & login gagal."),
            ("🟢",f"Sentimen positif {POS/TOTAL*100:.0f}% — puas dengan kemudahan lapor SPT."),
            ("🔵",f"Akurasi {AKU:.2f}% melampaui batas minimum 70%."),
            ("⚡",f"Cross Validation stabil {CV_M:.2f}% ± {CV_S:.2f}% — tidak overfitting."),
            ("📌","Fitur pajak, tahun, aktivasi mendominasi TF-IDF dataset."),
        ]:
            st.markdown(f'<div style="display:flex;gap:.5rem;align-items:flex-start;margin-bottom:.55rem"><span style="font-size:.8rem;flex-shrink:0">{ico}</span><span style="font-size:.77rem;color:#94A3B8;line-height:1.5">{txt}</span></div>',unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)

    st.markdown('</div>', unsafe_allow_html=True)


# ═══════════════════════════════════════════════════
# FOOTER
# ═══════════════════════════════════════════════════
st.markdown(f"""
<div class="footer">
  <b>Dashboard Sentimen Coretax</b> — Skripsi STMIK Triguna Dharma Medan 2025<br>
  Peneliti: <b>Aziz Fakhrizi</b> (2022020255) · {TOTAL:,} tweet ·
  Categorical Naïve Bayes · InSet Lexicon<br>
  Akurasi: <b>{AKU}%</b> · CV 5-Fold: <b>{CV_M:.2f}% ± {CV_S:.2f}%</b> · 15 Des 2024 – 27 Jan 2025
</div>
""", unsafe_allow_html=True)
