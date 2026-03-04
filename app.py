import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from datetime import datetime
import random

# ─────────────────────────────────────────────
# KONFIGURASI HALAMAN
# ─────────────────────────────────────────────
st.set_page_config(
    page_title="CoretaxSentimen | Dashboard Analisis Publik",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# ─────────────────────────────────────────────
# CSS KUSTOM — Desain Elegan Dark Navy + Gold (RESPONSIVE)
# ─────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@300;400;500;600;700;800&family=Space+Mono:wght@400;700&display=swap');

:root {
    --navy:    #0A0F1E;
    --navy2:   #111827;
    --navy3:   #1C2740;
    --gold:    #F5C842;
    --gold2:   #E8A820;
    --teal:    #22D3EE;
    --green:   #10B981;
    --red:     #F43F5E;
    --gray:    #94A3B8;
    --white:   #F1F5F9;
    --card:    rgba(28, 39, 64, 0.85);
    --border:  rgba(245, 200, 66, 0.18);
}

* { font-family: 'Plus Jakarta Sans', sans-serif !important; }

html, body, .stApp {
    background: var(--navy) !important;
    color: var(--white) !important;
}

/* Sembunyikan elemen bawaan Streamlit */
#MainMenu, footer, header { visibility: hidden; }
.block-container { padding: 0.5rem 1rem 1rem 1rem !important; max-width: 1400px !important; }

/* Responsive padding */
@media (max-width: 768px) {
    .block-container { padding: 0.25rem 0.5rem 0.5rem 0.5rem !important; }
}

/* ── HERO BANNER (Responsive) ── */
.hero-wrap {
    background: linear-gradient(135deg, #0A0F1E 0%, #111827 50%, #0F172A 100%);
    border-bottom: 1px solid var(--border);
    padding: 1.5rem 1rem 1rem;
    margin: -0.5rem -1rem 1rem -1rem;
    position: relative;
    overflow: hidden;
    border-radius: 0 0 20px 20px;
}
@media (max-width: 768px) {
    .hero-wrap { padding: 1rem 0.75rem 0.75rem; margin: -0.25rem -0.5rem 0.5rem -0.5rem; }
}
.hero-wrap::before {
    content: '';
    position: absolute; top: -60px; right: -60px;
    width: 300px; height: 300px;
    background: radial-gradient(circle, rgba(245,200,66,0.08) 0%, transparent 70%);
    border-radius: 50%;
}
.hero-wrap::after {
    content: '';
    position: absolute; bottom: -40px; left: 20%;
    width: 200px; height: 200px;
    background: radial-gradient(circle, rgba(34,211,238,0.06) 0%, transparent 70%);
    border-radius: 50%;
}
.hero-badge {
    display: inline-block;
    background: rgba(245,200,66,0.12);
    border: 1px solid rgba(245,200,66,0.3);
    color: var(--gold);
    padding: 0.2rem 0.7rem;
    border-radius: 20px;
    font-size: 0.65rem;
    font-weight: 700;
    letter-spacing: 1px;
    text-transform: uppercase;
    margin-bottom: 0.5rem;
}
.hero-title {
    font-size: 2rem;
    font-weight: 800;
    color: var(--white);
    line-height: 1.15;
    margin: 0 0 0.3rem 0;
}
@media (max-width: 768px) {
    .hero-title { font-size: 1.5rem; }
}
.hero-title span { color: var(--gold); }
.hero-sub {
    font-size: 0.85rem;
    color: var(--gray);
    max-width: 600px;
    margin: 0 0 0.8rem 0;
    line-height: 1.6;
}
@media (max-width: 768px) {
    .hero-sub { font-size: 0.75rem; }
}
.hero-meta {
    display: flex; gap: 1rem; flex-wrap: wrap;
}
.hero-meta-item {
    display: flex; align-items: center; gap: 0.3rem;
    font-size: 0.7rem; color: var(--gray);
}
.hero-meta-item strong { color: var(--teal); }

/* ── METRIC CARDS (Responsive Grid) ── */
.metric-grid {
    display: grid;
    grid-template-columns: repeat(4, 1fr);
    gap: 0.8rem;
    margin-bottom: 1.2rem;
}
@media (max-width: 768px) {
    .metric-grid { grid-template-columns: repeat(2, 1fr); gap: 0.5rem; }
}
.metric-card {
    background: var(--card);
    border: 1px solid var(--border);
    border-radius: 12px;
    padding: 1rem 1rem;
    position: relative;
    overflow: hidden;
    backdrop-filter: blur(10px);
    transition: transform 0.2s;
}
.metric-card:hover { transform: translateY(-2px); }
.metric-card::before {
    content: '';
    position: absolute; top: 0; left: 0; right: 0;
    height: 3px;
}
.mc-total::before  { background: linear-gradient(90deg, var(--teal), var(--gold)); }
.mc-pos::before    { background: linear-gradient(90deg, #10B981, #34D399); }
.mc-neg::before    { background: linear-gradient(90deg, #F43F5E, #FB7185); }
.mc-net::before    { background: linear-gradient(90deg, #94A3B8, #CBD5E1); }
.metric-label {
    font-size: 0.65rem; font-weight: 700; letter-spacing: 1px;
    text-transform: uppercase; color: var(--gray); margin-bottom: 0.4rem;
}
.metric-value {
    font-family: 'Space Mono', monospace !important;
    font-size: 1.8rem; font-weight: 700;
    color: var(--white); line-height: 1;
    margin-bottom: 0.2rem;
}
@media (max-width: 768px) {
    .metric-value { font-size: 1.4rem; }
}
.metric-pct {
    font-size: 0.7rem; color: var(--gray);
}
.metric-icon {
    position: absolute; top: 1rem; right: 1rem;
    font-size: 1.4rem; opacity: 0.25;
}

/* ── SECTION TITLE ── */
.section-title {
    font-size: 1rem; font-weight: 700;
    color: var(--white); margin-bottom: 0.2rem;
}
.section-sub {
    font-size: 0.72rem; color: var(--gray); margin-bottom: 0.8rem;
}
.section-divider {
    width: 30px; height: 3px;
    background: var(--gold);
    border-radius: 2px; margin-bottom: 0.8rem;
}

/* ── CHART CARDS ── */
.chart-card {
    background: var(--card);
    border: 1px solid var(--border);
    border-radius: 14px;
    padding: 1.2rem;
    margin-bottom: 1.2rem;
    backdrop-filter: blur(10px);
}
@media (max-width: 768px) {
    .chart-card { padding: 0.8rem; margin-bottom: 0.8rem; }
}

/* ── TWEET CARDS ── */
.tweet-card {
    background: rgba(17, 24, 39, 0.8);
    border-left: 3px solid;
    border-radius: 8px;
    padding: 0.8rem 1rem;
    margin-bottom: 0.6rem;
    transition: transform 0.15s;
}
.tweet-card:hover { transform: translateX(4px); }
.tweet-card.pos { border-left-color: var(--green); }
.tweet-card.neg { border-left-color: var(--red); }
.tweet-card.net { border-left-color: var(--gray); }
.tweet-text {
    font-size: 0.8rem; color: var(--white); line-height: 1.5; margin-bottom: 0.3rem;
}
.tweet-meta {
    font-size: 0.65rem; color: var(--gray);
    display: flex; gap: 0.8rem; flex-wrap: wrap;
}
.badge-pos { background: rgba(16,185,129,0.15); color: #34D399; padding: 2px 6px; border-radius: 8px; font-size: 0.6rem; font-weight: 700; }
.badge-neg { background: rgba(244,63,94,0.15);  color: #FB7185; padding: 2px 6px; border-radius: 8px; font-size: 0.6rem; font-weight: 700; }
.badge-net { background: rgba(148,163,184,0.15);color: #CBD5E1; padding: 2px 6px; border-radius: 8px; font-size: 0.6rem; font-weight: 700; }

/* ── INSIGHT CARDS ── */
.insight-box {
    background: linear-gradient(135deg, rgba(245,200,66,0.06), rgba(245,200,66,0.02));
    border: 1px solid rgba(245,200,66,0.2);
    border-radius: 10px;
    padding: 1rem;
    margin-bottom: 0.8rem;
}
.insight-num {
    font-family: 'Space Mono', monospace !important;
    font-size: 1.6rem; font-weight: 700; color: var(--gold);
}
.insight-desc { font-size: 0.75rem; color: var(--gray); line-height: 1.5; }

/* ── FOOTER ── */
.footer-wrap {
    border-top: 1px solid var(--border);
    padding: 1rem 0 0;
    margin-top: 1.5rem;
    text-align: center;
    color: var(--gray);
    font-size: 0.7rem;
}
.footer-wrap strong { color: var(--gold); }

/* ── SCROLLBAR ── */
::-webkit-scrollbar { width: 4px; height: 4px; }
::-webkit-scrollbar-track { background: var(--navy); }
::-webkit-scrollbar-thumb { background: var(--navy3); border-radius: 3px; }

/* Override Streamlit tab style (Responsive) */
.stTabs [data-baseweb="tab-list"] {
    background: var(--navy3) !important;
    border-radius: 8px; padding: 3px; gap: 3px;
    border: 1px solid var(--border);
    flex-wrap: wrap !important;
}
.stTabs [data-baseweb="tab"] {
    background: transparent !important;
    color: var(--gray) !important;
    border-radius: 6px;
    font-size: 0.75rem; font-weight: 600;
    padding: 0.4rem 0.8rem;
    white-space: nowrap;
}
@media (max-width: 768px) {
    .stTabs [data-baseweb="tab"] { font-size: 0.65rem; padding: 0.3rem 0.5rem; }
}
.stTabs [aria-selected="true"] {
    background: var(--gold) !important;
    color: var(--navy) !important;
}
.stTabs [data-baseweb="tab-panel"] { padding-top: 1rem; }
</style>
""", unsafe_allow_html=True)


# ─────────────────────────────────────────────
# DATA PENELITIAN (Data Aktual dari Skripsi)
# ─────────────────────────────────────────────

# Data dari distribusi_label (1).png
TOTAL = 2096  # 2096 tweet sesuai data
JML_NEG = 1611  # 76.9%
JML_POS = 359   # 17.1%
JML_NET = 126   # 6.0%

PCT_NEG = (JML_NEG / TOTAL) * 100
PCT_POS = (JML_POS / TOTAL) * 100
PCT_NET = (JML_NET / TOTAL) * 100

# Data dari evaluasi_model (1).png
AKURASI = 78.57
PRESISI = 74.75
RECALL = 78.57
F1_SCORE = 75.51

# Data dari cross_validation (2).png
CV_FOLDS = [78.33, 79.00, 77.33, 77.57, 79.47]
CV_MEAN = 78.34
CV_STD = 0.82

# Data dari confusion_matrix (2).png - SESUAI DENGAN GAMBAR YANG DIKIRIM
# Format: Baris = Aktual, Kolom = Prediksi
CM_LABELS = ['Positif', 'Netral', 'Negatif']
CM_VALUES = [
    [29, 3, 12],   # Positif Aktual: 29 Positif, 3 Netral, 12 Negatif
    [0, 0, 1],      # Netral Aktual: 0 Positif, 0 Netral, 1 Negatif
    [4, 2, 2300]    # Negatif Aktual: 4 Positif, 2 Netral, 2300 Negatif
]

# Data TF-IDF top features (dari top_tfidf.png)
TFIDF_FEATURES = {
    'tahun': 0.038, 'aktivasi': 0.028, 'akun': 0.024, 'wajib': 0.022,
    'wajib pajak': 0.020, 'nomor': 0.019, 'akun coretax': 0.018,
    'kak': 0.017, 'surat': 0.016, 'pemberitahuan': 0.015,
    'surat pemberitahuan': 0.014, 'pemberitahuan tahun': 0.013,
    'lapor': 0.012, 'aktivasi akun': 0.011, 'aktivasi coretax': 0.010,
    'pokok': 0.009, 'pokok wajib': 0.008, 'nomor pokok': 0.007,
    'email': 0.006, 'kakak': 0.005, 'daftar': 0.004,
    'data': 0.003, 'min': 0.002, 'jenderal': 0.001
}

# Data preprocessing dari Excel
@st.cache_data
def load_preprocessing_data():
    """Load data preprocessing dari file Excel yang sudah diekstrak"""
    preprocessing_samples = [
        {"teks_asli": "@ezash Dari sebelum coretax jg masuk kalo si shopee dkk bikin bukti potong", 
         "hasil_preprocessing": "coretax si shopee kawan kawan bikin bukti potong", "label": "Negatif"},
        {"teks_asli": "nah iya nih moots yg belum lapor spt tahunan orang pribadi wajib lapor di coretax yaaa", 
         "hasil_preprocessing": "moots lapor surat pemberitahuan tahun tahun pribadi wajib lapor coretax yaaa", "label": "Negatif"},
        {"teks_asli": "Tujuan coretax untuk mempermudah mudah emosi https://t.co/RGdvXTkQ1R", 
         "hasil_preprocessing": "tuju coretax mudah mudah emosi", "label": "Negatif"},
        {"teks_asli": "@heniloanr Ijin Kakk buat yg mau tanya2 soal CoreTax ke aku bolehh yaa reply disini atau di dm aku bantu sebisaku. Aku sering handle klien untuk urusan perpajakan free yaa!", 
         "hasil_preprocessing": "ijin kakk coretax bolehh yaa reply bantu sebisaku handle klien urusan perpajakan free yaa", "label": "Positif"},
        {"teks_asli": "Halo teman-teman! Setelah kode otorisasi diperoleh tahap selanjutnya adalah melakukan validasi kode otorisasi di Coretax agar akun dapat digunakan secara optimal dalam layanan perpajakan digital.", 
         "hasil_preprocessing": "teman teman kode otorisasi oleh tahap validasi kode otorisasi coretax akun optimal layan paja digital", "label": "Negatif"}
    ]
    return preprocessing_samples

# Data tweet untuk ulasan publik
@st.cache_data
def load_tweet_samples():
    """Load sample tweets untuk ditampilkan di dashboard"""
    tweet_samples = [
        {"tweet": "Coretax error terus, tidak bisa login dari kemarin. Deadline pajak makin dekat!", 
         "label": "Negatif", "preprocessing": "coretax error login deadline pajak dekat"},
        {"tweet": "Alhamdulillah berhasil lapor SPT lewat coretax, lancar sekali! Terima kasih DJP.", 
         "label": "Positif", "preprocessing": "alhamdulillah hasil lapor spt coretax lancar terima kasih djp"},
        {"tweet": "Coretax adalah sistem perpajakan terbaru dari DJP yang diluncurkan akhir 2024.", 
         "label": "Netral", "preprocessing": "coretax sistem perpajakan baru djp luncur akhir"},
        {"tweet": "Sistem coretax sangat lambat dan sering down. Sangat mengecewakan!", 
         "label": "Negatif", "preprocessing": "sistem coretax lambat down mengecewakan"},
        {"tweet": "Coretax sekarang sudah jauh lebih baik dan mudah digunakan. Mantap!", 
         "label": "Positif", "preprocessing": "coretax baik mudah mantap"},
        {"tweet": "Deadline lapor SPT tahunan melalui coretax adalah 31 Maret 2025.", 
         "label": "Netral", "preprocessing": "deadline lapor spt tahunan coretax maret"},
    ]
    return tweet_samples

df_preprocessing = load_preprocessing_data()
df_tweets = load_tweet_samples()

# Warna konsisten
WARNA = {'Positif':'#10B981','Negatif':'#F43F5E','Netral':'#94A3B8'}

# PLOTLY THEME - TANPA MARGIN (agar bisa diatur per chart)
PLOTLY_THEME = dict(
    paper_bgcolor='rgba(0,0,0,0)',
    plot_bgcolor='rgba(0,0,0,0)',
    font=dict(family='Plus Jakarta Sans', color='#94A3B8', size=11),
)


# ─────────────────────────────────────────────
# HERO BANNER
# ─────────────────────────────────────────────
st.markdown(f"""
<div class="hero-wrap">
  <div class="hero-badge">📊 Penelitian Skripsi · STMIK Triguna Dharma 2025</div>
  <h1 class="hero-title">Analisis Sentimen Masyarakat<br><span>Coretax</span> di Platform X</h1>
  <p class="hero-sub">
    Visualisasi persepsi masyarakat terhadap aplikasi perpajakan Coretax berdasarkan
    analisis <strong style="color:#F5C842">{TOTAL:,} tweet</strong> menggunakan
    algoritma <strong>Categorical Naïve Bayes</strong>.
  </p>
  <div class="hero-meta">
    <div class="hero-meta-item">🗓️ Periode: <strong>15 Des 2024 – 27 Jan 2025</strong></div>
    <div class="hero-meta-item">🤖 Metode: <strong>Categorical Naïve Bayes</strong></div>
    <div class="hero-meta-item">📚 Sumber: <strong>Platform X</strong></div>
    <div class="hero-meta-item">✍️ <strong>Aziz Fakhrizi</strong> (2022020255)</div>
  </div>
</div>
""", unsafe_allow_html=True)


# ─────────────────────────────────────────────
# METRIC CARDS (Data Aktual)
# ─────────────────────────────────────────────
st.markdown(f"""
<div class="metric-grid">
  <div class="metric-card mc-total">
    <div class="metric-icon">🐦</div>
    <div class="metric-label">Total Tweet</div>
    <div class="metric-value">{TOTAL:,}</div>
    <div class="metric-pct">Data periode 44 hari</div>
  </div>
  <div class="metric-card mc-neg">
    <div class="metric-icon">😠</div>
    <div class="metric-label">Sentimen Negatif</div>
    <div class="metric-value">{JML_NEG:,}</div>
    <div class="metric-pct">{PCT_NEG:.1f}% dari total</div>
  </div>
  <div class="metric-card mc-pos">
    <div class="metric-icon">😊</div>
    <div class="metric-label">Sentimen Positif</div>
    <div class="metric-value">{JML_POS:,}</div>
    <div class="metric-pct">{PCT_POS:.1f}% dari total</div>
  </div>
  <div class="metric-card mc-net">
    <div class="metric-icon">😐</div>
    <div class="metric-label">Sentimen Netral</div>
    <div class="metric-value">{JML_NET:,}</div>
    <div class="metric-pct">{PCT_NET:.1f}% dari total</div>
  </div>
</div>
""", unsafe_allow_html=True)


# ─────────────────────────────────────────────
# TABS NAVIGASI
# ─────────────────────────────────────────────
tab1, tab2, tab3, tab4, tab5 = st.tabs([
    "📊 Distribusi",
    "📈 Evaluasi Model",
    "🔄 Preprocessing",
    "💬 Ulasan",
    "📋 Ringkasan",
])


# ══════════════════════════════════════════════
# TAB 1 — DISTRIBUSI SENTIMEN
# ══════════════════════════════════════════════
with tab1:
    col1, col2 = st.columns([1, 1.2], gap="small")

    with col1:
        st.markdown('<div class="chart-card">', unsafe_allow_html=True)
        st.markdown('<div class="section-title">Proporsi Sentimen</div>', unsafe_allow_html=True)
        st.markdown('<div class="section-divider"></div>', unsafe_allow_html=True)
        st.markdown(f'<div class="section-sub">Total {TOTAL:,} tweet</div>', unsafe_allow_html=True)

        fig_pie = go.Figure(go.Pie(
            labels=['Negatif','Positif','Netral'],
            values=[JML_NEG, JML_POS, JML_NET],
            hole=0.6,
            marker=dict(
                colors=['#F43F5E','#10B981','#64748B'],
                line=dict(color='#0A0F1E', width=2)
            ),
            textinfo='percent',
            textfont=dict(size=12, family='Space Mono'),
            hovertemplate='<b>%{label}</b><br>%{value:,} tweet<br>%{percent}<extra></extra>',
        ))
        fig_pie.add_annotation(
            text=f"<b style='font-size:20px'>{PCT_NEG:.0f}%</b><br><span style='font-size:10px;color:#94A3B8'>Negatif</span>",
            x=0.5, y=0.5, showarrow=False,
            font=dict(size=12, color='#F1F5F9')
        )
        fig_pie.update_layout(
            **PLOTLY_THEME, 
            height=280,
            margin=dict(l=5, r=5, t=20, b=30),
            legend=dict(orientation='h', y=-0.15, x=0.5, xanchor='center',
                        font=dict(size=10, color='#94A3B8')),
            showlegend=True
        )
        st.plotly_chart(fig_pie, use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)

    with col2:
        st.markdown('<div class="chart-card">', unsafe_allow_html=True)
        st.markdown('<div class="section-title">Top Fitur TF-IDF</div>', unsafe_allow_html=True)
        st.markdown('<div class="section-divider"></div>', unsafe_allow_html=True)
        st.markdown('<div class="section-sub">15 fitur dengan bobot tertinggi</div>', unsafe_allow_html=True)

        # Bar chart untuk TF-IDF features
        features_df = pd.DataFrame(list(TFIDF_FEATURES.items()), columns=['Fitur', 'Bobot'])
        features_df = features_df.sort_values('Bobot', ascending=True).tail(15)
        
        fig_tfidf = go.Figure(go.Bar(
            x=features_df['Bobot'],
            y=features_df['Fitur'],
            orientation='h',
            marker=dict(color='#F5C842', line=dict(width=0)),
            text=features_df['Bobot'].apply(lambda x: f'{x:.3f}'),
            textposition='outside',
            textfont=dict(size=9, color='#F5C842', family='Space Mono'),
            hovertemplate='<b>%{y}</b><br>Bobot: %{x:.3f}<extra></extra>'
        ))
        fig_tfidf.update_layout(
            **PLOTLY_THEME, 
            height=280,
            margin=dict(l=5, r=5, t=20, b=30),
            xaxis=dict(title='Bobot TF-IDF', showgrid=True, gridcolor='rgba(148,163,184,0.08)', tickfont=dict(size=8)),
            yaxis=dict(title='', automargin=True, tickfont=dict(size=9)),
            hovermode='y',
        )
        st.plotly_chart(fig_tfidf, use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)

    # ── Perbandingan Volume per Kelas ──
    st.markdown('<div class="chart-card">', unsafe_allow_html=True)
    st.markdown('<div class="section-title">Perbandingan Volume per Kelas</div>', unsafe_allow_html=True)
    st.markdown('<div class="section-divider"></div>', unsafe_allow_html=True)

    fig_hbar = go.Figure()
    labels_list = ['Negatif','Positif','Netral']
    values_list = [JML_NEG, JML_POS, JML_NET]
    colors_list = ['#F43F5E','#10B981','#64748B']
    
    for lbl, val, clr in zip(labels_list, values_list, colors_list):
        fig_hbar.add_trace(go.Bar(
            x=[val], y=[lbl], orientation='h',
            marker=dict(color=clr, line=dict(width=0)),
            text=f'{val:,} ({val/TOTAL*100:.1f}%)',
            textposition='inside', textfont=dict(size=11, color='white', family='Space Mono'),
            name=lbl,
            hovertemplate=f'<b>{lbl}</b>: {val:,} tweet<extra></extra>'
        ))
    fig_hbar.update_layout(
        **PLOTLY_THEME, 
        height=200,
        margin=dict(l=5, r=5, t=20, b=30),
        showlegend=False,
        xaxis=dict(title='Jumlah Tweet', showgrid=True, gridcolor='rgba(148,163,184,0.08)'),
        yaxis=dict(title=''),
        bargap=0.3,
    )
    st.plotly_chart(fig_hbar, use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)


# ══════════════════════════════════════════════
# TAB 2 — EVALUASI MODEL (DIPERBAIKI - TANPA DUPLIKASI MARGIN)
# ══════════════════════════════════════════════
with tab2:
    st.markdown('<div class="section-title">📈 Hasil Evaluasi Model</div>', unsafe_allow_html=True)
    st.markdown('<div class="section-divider"></div>', unsafe_allow_html=True)
    
    # ── METRIK GAUGE (diperbaiki - margin hanya diatur sekali) ──
    col_g1, col_g2, col_g3, col_g4 = st.columns(4, gap="small")
    
    with col_g1:
        fig_g1 = go.Figure(go.Indicator(
            mode="gauge+number",
            value=AKURASI,
            title={'text': "Akurasi", 'font': {'size': 12, 'color': '#F1F5F9'}},
            number={'suffix': '%', 'font': {'size': 20, 'color': '#3B82F6', 'family': 'Space Mono'}},
            gauge={
                'axis': {'range': [0,100], 'tickfont': {'size': 8, 'color': '#94A3B8'}},
                'bar': {'color': '#3B82F6', 'thickness': 0.3},
                'bgcolor': '#1C2740',
                'bordercolor': '#1C2740',
                'steps': [
                    {'range': [0,70], 'color': 'rgba(148,163,184,0.1)'},
                    {'range': [70,100], 'color': 'rgba(59,130,246,0.1)'}
                ],
                'threshold': {'line': {'color': '#F5C842','width': 2}, 'thickness': 0.6, 'value': 70}
            }
        ))
        fig_g1.update_layout(
            **PLOTLY_THEME, 
            height=200,
            margin=dict(l=5, r=5, t=20, b=5)  # margin hanya diatur di sini
        )
        st.plotly_chart(fig_g1, use_container_width=True)
    
    with col_g2:
        fig_g2 = go.Figure(go.Indicator(
            mode="gauge+number",
            value=PRESISI,
            title={'text': "Presisi", 'font': {'size': 12, 'color': '#F1F5F9'}},
            number={'suffix': '%', 'font': {'size': 20, 'color': '#10B981', 'family': 'Space Mono'}},
            gauge={
                'axis': {'range': [0,100], 'tickfont': {'size': 8, 'color': '#94A3B8'}},
                'bar': {'color': '#10B981', 'thickness': 0.3},
                'bgcolor': '#1C2740',
                'bordercolor': '#1C2740',
                'steps': [
                    {'range': [0,70], 'color': 'rgba(148,163,184,0.1)'},
                    {'range': [70,100], 'color': 'rgba(16,185,129,0.1)'}
                ],
                'threshold': {'line': {'color': '#F5C842','width': 2}, 'thickness': 0.6, 'value': 70}
            }
        ))
        fig_g2.update_layout(
            **PLOTLY_THEME, 
            height=200,
            margin=dict(l=5, r=5, t=20, b=5)
        )
        st.plotly_chart(fig_g2, use_container_width=True)
    
    with col_g3:
        fig_g3 = go.Figure(go.Indicator(
            mode="gauge+number",
            value=RECALL,
            title={'text': "Recall", 'font': {'size': 12, 'color': '#F1F5F9'}},
            number={'suffix': '%', 'font': {'size': 20, 'color': '#F59E0B', 'family': 'Space Mono'}},
            gauge={
                'axis': {'range': [0,100], 'tickfont': {'size': 8, 'color': '#94A3B8'}},
                'bar': {'color': '#F59E0B', 'thickness': 0.3},
                'bgcolor': '#1C2740',
                'bordercolor': '#1C2740',
                'steps': [
                    {'range': [0,70], 'color': 'rgba(148,163,184,0.1)'},
                    {'range': [70,100], 'color': 'rgba(245,158,11,0.1)'}
                ],
                'threshold': {'line': {'color': '#F5C842','width': 2}, 'thickness': 0.6, 'value': 70}
            }
        ))
        fig_g3.update_layout(
            **PLOTLY_THEME, 
            height=200,
            margin=dict(l=5, r=5, t=20, b=5)
        )
        st.plotly_chart(fig_g3, use_container_width=True)
    
    with col_g4:
        fig_g4 = go.Figure(go.Indicator(
            mode="gauge+number",
            value=F1_SCORE,
            title={'text': "F1-Score", 'font': {'size': 12, 'color': '#F1F5F9'}},
            number={'suffix': '%', 'font': {'size': 20, 'color': '#8B5CF6', 'family': 'Space Mono'}},
            gauge={
                'axis': {'range': [0,100], 'tickfont': {'size': 8, 'color': '#94A3B8'}},
                'bar': {'color': '#8B5CF6', 'thickness': 0.3},
                'bgcolor': '#1C2740',
                'bordercolor': '#1C2740',
                'steps': [
                    {'range': [0,70], 'color': 'rgba(148,163,184,0.1)'},
                    {'range': [70,100], 'color': 'rgba(139,92,246,0.1)'}
                ],
                'threshold': {'line': {'color': '#F5C842','width': 2}, 'thickness': 0.6, 'value': 70}
            }
        ))
        fig_g4.update_layout(
            **PLOTLY_THEME, 
            height=200,
            margin=dict(l=5, r=5, t=20, b=5)
        )
        st.plotly_chart(fig_g4, use_container_width=True)
    
    st.markdown("""
    <div style="font-size:0.7rem;color:#64748B;text-align:center;margin-top:-0.5rem;margin-bottom:1rem">
    ⭐ Garis kuning = batas minimum akurasi 70%
    </div>""", unsafe_allow_html=True)
    
    # ── CROSS VALIDATION ──
    col_cv1, col_cv2 = st.columns([1.2, 1], gap="small")
    
    with col_cv1:
        st.markdown('<div class="chart-card">', unsafe_allow_html=True)
        st.markdown('<div class="section-title">Cross Validation (5-Fold)</div>', unsafe_allow_html=True)
        st.markdown('<div class="section-divider"></div>', unsafe_allow_html=True)
        st.markdown(f'<div class="section-sub">Rata-rata: {CV_MEAN:.2f}% ± {CV_STD:.2f}%</div>', unsafe_allow_html=True)

        # Bar chart untuk cross validation
        fold_names = [f'Fold {i+1}' for i in range(5)]
        colors = ['#22D3EE', '#22D3EE', '#22D3EE', '#22D3EE', '#22D3EE']
        
        fig_cv = go.Figure()
        fig_cv.add_trace(go.Bar(
            x=fold_names,
            y=CV_FOLDS,
            marker=dict(color=colors, line=dict(width=0)),
            text=[f'{val:.2f}%' for val in CV_FOLDS],
            textposition='outside',
            textfont=dict(size=10, color='#22D3EE', family='Space Mono'),
            hovertemplate='<b>%{x}</b><br>Akurasi: %{y:.2f}%<extra></extra>'
        ))
        fig_cv.add_hline(y=CV_MEAN, line_dash='dash', line_color='#F5C842', line_width=2,
                         annotation_text=f'Rata-rata: {CV_MEAN:.2f}%',
                         annotation_font=dict(size=9, color='#F5C842'))
        fig_cv.update_layout(
            **PLOTLY_THEME, 
            height=250,
            margin=dict(l=5, r=5, t=20, b=30),
            xaxis=dict(title='', showgrid=False, tickfont=dict(size=9)),
            yaxis=dict(title='Akurasi (%)', range=[76, 81], 
                       showgrid=True, gridcolor='rgba(148,163,184,0.08)',
                       tickfont=dict(size=9)),
            hovermode='x',
        )
        st.plotly_chart(fig_cv, use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)
    
    with col_cv2:
        st.markdown('<div class="chart-card">', unsafe_allow_html=True)
        st.markdown('<div class="section-title">Statistik Validasi</div>', unsafe_allow_html=True)
        st.markdown('<div class="section-divider"></div>', unsafe_allow_html=True)
        
        cv_df = pd.DataFrame({
            'Fold': fold_names,
            'Akurasi (%)': CV_FOLDS
        })
        
        # Tampilkan tabel
        st.dataframe(
            cv_df,
            column_config={
                "Fold": "Fold",
                "Akurasi (%)": st.column_config.NumberColumn(
                    "Akurasi (%)",
                    format="%.2f%%",
                )
            },
            use_container_width=True,
            hide_index=True,
        )
        
        st.markdown(f"""
        <div style="margin-top:1rem;padding:0.5rem;background:rgba(34,211,238,0.05);border-radius:8px;border-left:2px solid #22D3EE">
          <span style="color:#22D3EE;font-weight:700">Rata-rata: {CV_MEAN:.2f}%</span><br>
          <span style="color:#94A3B8;font-size:0.75rem">Standar Deviasi: ±{CV_STD:.2f}%</span>
        </div>
        """, unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)

    # ── CONFUSION MATRIX (SESUAI DENGAN GAMBAR) ──
    st.markdown('<div class="chart-card">', unsafe_allow_html=True)
    st.markdown('<div class="section-title">🔢 Confusion Matrix</div>', unsafe_allow_html=True)
    st.markdown('<div class="section-divider"></div>', unsafe_allow_html=True)
    st.markdown('<div class="section-sub">Matriks klasifikasi (Aktual vs Prediksi) - Data Testing</div>', unsafe_allow_html=True)

    # Heatmap confusion matrix dengan nilai sesuai gambar
    fig_cm = go.Figure(data=go.Heatmap(
        z=CM_VALUES,
        x=CM_LABELS,
        y=CM_LABELS,
        text=CM_VALUES,
        texttemplate='<b>%{text}</b>',
        textfont={'size': 14, 'color': '#F1F5F9', 'family': 'Space Mono'},
        colorscale=[[0, '#1C2740'], [0.3, '#2D3A5E'], [0.6, '#3B4A7A'], [1, '#F5C842']],
        showscale=False,
        hovertemplate='Aktual: %{y}<br>Prediksi: %{x}<br>Jumlah: %{z}<extra></extra>'
    ))
    
    # Tambahkan anotasi untuk total per baris
    annotations = []
    for i, label in enumerate(CM_LABELS):
        total = sum(CM_VALUES[i])
        annotations.append(dict(
            x=1.15, y=i,
            text=f'Total: {total}',
            showarrow=False,
            font=dict(size=10, color='#94A3B8'),
            xref='paper',
            yref='y'
        ))
    
    fig_cm.update_layout(
        **PLOTLY_THEME, 
        height=300,
        margin=dict(l=5, r=60, t=20, b=30),
        xaxis=dict(title='Kelas Prediksi', side='bottom', tickfont=dict(size=11)),
        yaxis=dict(title='Kelas Aktual', autorange='reversed', tickfont=dict(size=11)),
        annotations=annotations
    )
    st.plotly_chart(fig_cm, use_container_width=True)
    
    # Informasi tambahan confusion matrix
    col_cm1, col_cm2, col_cm3 = st.columns(3)
    with col_cm1:
        st.markdown("""
        <div style="background:rgba(16,185,129,0.05);padding:0.5rem;border-radius:8px;text-align:center">
          <span style="color:#10B981;font-size:0.7rem">✅ Benar Positif</span><br>
          <span style="color:white;font-size:1.2rem;font-family:'Space Mono'">29</span>
        </div>
        """, unsafe_allow_html=True)
    with col_cm2:
        st.markdown("""
        <div style="background:rgba(244,63,94,0.05);padding:0.5rem;border-radius:8px;text-align:center">
          <span style="color:#F43F5E;font-size:0.7rem">✅ Benar Negatif</span><br>
          <span style="color:white;font-size:1.2rem;font-family:'Space Mono'">2300</span>
        </div>
        """, unsafe_allow_html=True)
    with col_cm3:
        st.markdown("""
        <div style="background:rgba(148,163,184,0.05);padding:0.5rem;border-radius:8px;text-align:center">
          <span style="color:#94A3B8;font-size:0.7rem">✅ Benar Netral</span><br>
          <span style="color:white;font-size:1.2rem;font-family:'Space Mono'">0</span>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown('</div>', unsafe_allow_html=True)


# ══════════════════════════════════════════════
# TAB 3 — PREPROCESSING
# ══════════════════════════════════════════════
with tab3:
    st.markdown('<div class="section-title">🔄 Tahapan Preprocessing</div>', unsafe_allow_html=True)
    st.markdown('<div class="section-divider"></div>', unsafe_allow_html=True)
    
    col1, col2 = st.columns([1, 1], gap="small")
    
    with col1:
        st.markdown('<div class="chart-card">', unsafe_allow_html=True)
        st.markdown('<div class="section-title">📝 Alur Preprocessing</div>', unsafe_allow_html=True)
        st.markdown('<div class="section-divider"></div>', unsafe_allow_html=True)
        
        tahapan = [
            ("1","Cleaning","Hapus URL, mention, hashtag, simbol","#F5C842"),
            ("2","Case Folding","Konversi teks ke huruf kecil","#22D3EE"),
            ("3","Normalisasi","Slang → kata baku (PUEBI)","#10B981"),
            ("4","Stopword Removal","Hapus kata tidak bermakna","#8B5CF6"),
            ("5","Tokenizing","Pecah teks menjadi token kata","#F59E0B"),
            ("6","Stemming","Kata berimbuhan → kata dasar","#F43F5E"),
            ("7","Labeling","Lexicon InSet + kamus Coretax","#3B82F6"),
        ]
        
        for num, name, desc, clr in tahapan:
            st.markdown(f"""
            <div style="display:flex;align-items:flex-start;gap:0.5rem;margin-bottom:0.5rem">
              <div style="background:{clr};color:#0A0F1E;width:20px;height:20px;
                border-radius:50%;display:flex;align-items:center;justify-content:center;
                font-size:0.6rem;font-weight:800;flex-shrink:0;margin-top:2px">{num}</div>
              <div>
                <div style="font-size:0.75rem;font-weight:700;color:#F1F5F9">{name}</div>
                <div style="font-size:0.65rem;color:#64748B">{desc}</div>
              </div>
            </div>""", unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)

    with col2:
        st.markdown('<div class="chart-card">', unsafe_allow_html=True)
        st.markdown('<div class="section-title">📊 Statistik Preprocessing</div>', unsafe_allow_html=True)
        st.markdown('<div class="section-divider"></div>', unsafe_allow_html=True)
        
        st.markdown(f"""
        <table style="width:100%;border-collapse:collapse;font-size:0.8rem;color:#94A3B8;">
          <tr><td style="padding:6px 0;border-bottom:1px solid rgba(245,200,66,0.08);">Total Data Awal</td>
              <td style="padding:6px 0;border-bottom:1px solid rgba(245,200,66,0.08);color:#F1F5F9;text-align:right">{TOTAL:,} tweet</td></tr>
          <tr><td style="padding:6px 0;border-bottom:1px solid rgba(245,200,66,0.08);">Kata Unik (Vocabulary)</td>
              <td style="padding:6px 0;border-bottom:1px solid rgba(245,200,66,0.08);color:#F1F5F9;text-align:right">~2.500 kata</td></tr>
          <tr><td style="padding:6px 0;border-bottom:1px solid rgba(245,200,66,0.08);">Jumlah Fitur (TF-IDF)</td>
              <td style="padding:6px 0;border-bottom:1px solid rgba(245,200,66,0.08);color:#F1F5F9;text-align:right">5.000 fitur</td></tr>
          <tr><td style="padding:6px 0;border-bottom:1px solid rgba(245,200,66,0.08);">N-gram Range</td>
              <td style="padding:6px 0;border-bottom:1px solid rgba(245,200,66,0.08);color:#F1F5F9;text-align:right">1-gram, 2-gram</td></tr>
          <tr><td style="padding:6px 0;">Probabilitas Prior</td>
              <td style="padding:6px 0;color:#F1F5F9;text-align:right">Neg: 76.8%, Pos: 17.1%, Net: 6.0%</td></tr>
        </table>
        """, unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)

    # ── Contoh Hasil Preprocessing ──
    st.markdown('<div class="chart-card">', unsafe_allow_html=True)
    st.markdown('<div class="section-title">📋 Contoh Hasil Preprocessing</div>', unsafe_allow_html=True)
    st.markdown('<div class="section-divider"></div>', unsafe_allow_html=True)

    # Tampilkan tabel preprocessing
    pre_df = pd.DataFrame(df_preprocessing)
    st.dataframe(
        pre_df,
        column_config={
            "teks_asli": "Teks Asli",
            "hasil_preprocessing": "Hasil Preprocessing",
            "label": st.column_config.TextColumn("Label", width="small"),
        },
        use_container_width=True,
        hide_index=True,
    )
    st.markdown('</div>', unsafe_allow_html=True)


# ══════════════════════════════════════════════
# TAB 4 — ULASAN PUBLIK
# ══════════════════════════════════════════════
with tab4:
    st.markdown('<div class="section-title">💬 Ulasan Masyarakat</div>', unsafe_allow_html=True)
    st.markdown('<div class="section-divider"></div>', unsafe_allow_html=True)

    # Filter
    fcol1, fcol2 = st.columns([1, 2], gap="small")
    with fcol1:
        filter_label = st.selectbox(
            "Filter Sentimen",
            ["Semua", "Negatif", "Positif", "Netral"],
            key="filter_label_tab4"
        )
    
    with fcol2:
        show_option = st.radio(
            "Tampilkan:",
            ["Teks Asli", "Hasil Preprocessing", "Keduanya"],
            horizontal=True,
            key="show_option"
        )

    # Filter dataframe
    df_tweets_filtered = df_tweets if filter_label == "Semua" else [t for t in df_tweets if t['label'] == filter_label]
    
    if len(df_tweets_filtered) == 0:
        st.info(f"Tidak ada tweet dengan sentimen {filter_label}")
    else:
        # Tampilkan dalam grid 2 kolom
        col_tw1, col_tw2 = st.columns(2, gap="small")
        
        badge_map = {
            'Positif': '<span class="badge-pos">😊 POSITIF</span>',
            'Negatif': '<span class="badge-neg">😠 NEGATIF</span>',
            'Netral' : '<span class="badge-net">😐 NETRAL</span>',
        }
        css_map = {'Positif':'pos','Negatif':'neg','Netral':'net'}

        for i, tweet in enumerate(df_tweets_filtered):
            badge = badge_map[tweet['label']]
            css_cl = css_map[tweet['label']]
            
            if show_option == "Teks Asli":
                display_text = tweet['tweet']
            elif show_option == "Hasil Preprocessing":
                display_text = tweet['preprocessing']
            else:  # Keduanya
                display_text = f"📝 {tweet['tweet']}\n\n🔄 {tweet['preprocessing']}"
            
            card = f"""
            <div class="tweet-card {css_cl}">
              <div class="tweet-text">{display_text}</div>
              <div class="tweet-meta">
                {badge}
              </div>
            </div>"""
            
            if i % 2 == 0:
                col_tw1.markdown(card, unsafe_allow_html=True)
            else:
                col_tw2.markdown(card, unsafe_allow_html=True)


# ══════════════════════════════════════════════
# TAB 5 — RINGKASAN RISET
# ══════════════════════════════════════════════
with tab5:
    rc1, rc2 = st.columns([1.2, 1], gap="small")

    with rc1:
        st.markdown('<div class="chart-card">', unsafe_allow_html=True)
        st.markdown('<div class="section-title">📌 Tentang Penelitian</div>', unsafe_allow_html=True)
        st.markdown('<div class="section-divider"></div>', unsafe_allow_html=True)
        st.markdown(f"""
        <table style="width:100%;border-collapse:collapse;font-size:0.8rem;color:#94A3B8;">
          <tr><td style="padding:6px 0;border-bottom:1px solid rgba(245,200,66,0.08);width:35%">Judul</td>
              <td style="padding:6px 0;border-bottom:1px solid rgba(245,200,66,0.08);color:#F1F5F9">
              Analisis Sentimen Masyarakat Terhadap Aplikasi Coretax di Platform X</td></tr>
          <tr><td style="padding:6px 0;border-bottom:1px solid rgba(245,200,66,0.08)">Peneliti</td>
              <td style="padding:6px 0;border-bottom:1px solid rgba(245,200,66,0.08);color:#F5C842">Aziz Fakhrizi</td></tr>
          <tr><td style="padding:6px 0;border-bottom:1px solid rgba(245,200,66,0.08)">NIM</td>
              <td style="padding:6px 0;border-bottom:1px solid rgba(245,200,66,0.08);color:#F1F5F9">2022020255</td></tr>
          <tr><td style="padding:6px 0;border-bottom:1px solid rgba(245,200,66,0.08)">Institusi</td>
              <td style="padding:6px 0;border-bottom:1px solid rgba(245,200,66,0.08);color:#F1F5F9">STMIK Triguna Dharma, Medan</td></tr>
          <tr><td style="padding:6px 0;border-bottom:1px solid rgba(245,200,66,0.08)">Metode</td>
              <td style="padding:6px 0;border-bottom:1px solid rgba(245,200,66,0.08);color:#22D3EE">Categorical Naïve Bayes</td></tr>
          <tr><td style="padding:6px 0;border-bottom:1px solid rgba(245,200,66,0.08)">Labeling</td>
              <td style="padding:6px 0;border-bottom:1px solid rgba(245,200,66,0.08);color:#F1F5F9">Lexicon InSet</td></tr>
          <tr><td style="padding:6px 0;border-bottom:1px solid rgba(245,200,66,0.08)">Ekstraksi Fitur</td>
              <td style="padding:6px 0;border-bottom:1px solid rgba(245,200,66,0.08);color:#F1F5F9">TF-IDF (5.000 fitur)</td></tr>
          <tr><td style="padding:6px 0">Periode Data</td>
              <td style="padding:6px 0;color:#F1F5F9">15 Des 2024 – 27 Jan 2025</td></tr>
        </table>
        """, unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)

    with rc2:
        st.markdown('<div class="chart-card">', unsafe_allow_html=True)
        st.markdown('<div class="section-title">📊 Ringkasan Kinerja</div>', unsafe_allow_html=True)
        st.markdown('<div class="section-divider"></div>', unsafe_allow_html=True)
        
        # Metric cards kecil
        st.markdown(f"""
        <div style="display:grid;grid-template-columns:1fr 1fr;gap:0.5rem;margin-bottom:0.5rem">
          <div style="background:rgba(59,130,246,0.1);border-radius:8px;padding:0.5rem;text-align:center">
            <span style="color:#94A3B8;font-size:0.65rem">AKURASI</span><br>
            <span style="color:#3B82F6;font-size:1.4rem;font-family:'Space Mono'">{AKURASI}%</span>
          </div>
          <div style="background:rgba(16,185,129,0.1);border-radius:8px;padding:0.5rem;text-align:center">
            <span style="color:#94A3B8;font-size:0.65rem">PRESISI</span><br>
            <span style="color:#10B981;font-size:1.4rem;font-family:'Space Mono'">{PRESISI}%</span>
          </div>
          <div style="background:rgba(245,158,11,0.1);border-radius:8px;padding:0.5rem;text-align:center">
            <span style="color:#94A3B8;font-size:0.65rem">RECALL</span><br>
            <span style="color:#F59E0B;font-size:1.4rem;font-family:'Space Mono'">{RECALL}%</span>
          </div>
          <div style="background:rgba(139,92,246,0.1);border-radius:8px;padding:0.5rem;text-align:center">
            <span style="color:#94A3B8;font-size:0.65rem">F1-SCORE</span><br>
            <span style="color:#8B5CF6;font-size:1.4rem;font-family:'Space Mono'">{F1_SCORE}%</span>
          </div>
        </div>
        
        <div style="background:rgba(34,211,238,0.05);border-radius:8px;padding:0.5rem;margin-top:0.5rem">
          <span style="color:#22D3EE;font-size:0.7rem;font-weight:700">CROSS VALIDATION (5-FOLD)</span><br>
          <span style="color:#F1F5F9;font-size:1rem;font-family:'Space Mono'">{CV_MEAN:.2f}% ± {CV_STD:.2f}%</span>
        </div>
        """, unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)

    # Kesimpulan
    st.markdown('<div class="chart-card">', unsafe_allow_html=True)
    st.markdown('<div class="section-title">💡 Temuan Utama</div>', unsafe_allow_html=True)
    st.markdown('<div class="section-divider"></div>', unsafe_allow_html=True)
    
    ic1, ic2, ic3 = st.columns(3, gap="small")
    with ic1:
        st.markdown(f"""
        <div class="insight-box">
          <div class="insight-num">{PCT_NEG:.1f}%</div>
          <div class="insight-desc">
            Tweet <strong style="color:#F43F5E">negatif</strong> mendominasi 
            (keluhan error sistem, login gagal, lambat)
          </div>
        </div>""", unsafe_allow_html=True)
    with ic2:
        st.markdown(f"""
        <div class="insight-box">
          <div class="insight-num">{AKURASI}%</div>
          <div class="insight-desc">
            Akurasi model <strong style="color:#3B82F6">Categorical Naïve Bayes</strong> 
            pada data testing
          </div>
        </div>""", unsafe_allow_html=True)
    with ic3:
        st.markdown(f"""
        <div class="insight-box">
          <div class="insight-num">2,300</div>
          <div class="insight-desc">
            <strong style="color:#10B981">True Negatif</strong> tertinggi dalam 
            confusion matrix
          </div>
        </div>""", unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)


# ─────────────────────────────────────────────
# FOOTER
# ─────────────────────────────────────────────
st.markdown(f"""
<div class="footer-wrap">
  <strong>CoretaxSentimen Dashboard · Skripsi STMIK Triguna Dharma Medan 2025</strong><br>
  Peneliti: <strong>Aziz Fakhrizi</strong> (NIM: 2022020255) · 
  Data: Platform X · {TOTAL:,} tweet · Metode: Categorical Naïve Bayes + InSet Lexicon<br>
  Periode: 15 Des 2024 – 27 Jan 2025 · Akurasi: {AKURASI}% ± {CV_STD}% (5-Fold CV)<br><br>
  <span style="color:#334155">Dashboard ini bersifat publik dan responsif di semua perangkat</span>
</div>
""", unsafe_allow_html=True)