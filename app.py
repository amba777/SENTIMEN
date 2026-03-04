import streamlit as st
import plotly.graph_objects as go
import pandas as pd

st.set_page_config(
    page_title="Sentimen Coretax | Dashboard",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="collapsed",
)

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&family=JetBrains+Mono:wght@400;600&display=swap');

:root {
  --bg:     #060B18;
  --bg1:    #0D1526;
  --bg2:    #111E35;
  --bg3:    #1A2B47;
  --gold:   #F0B429;
  --teal:   #2DD4BF;
  --green:  #22C55E;
  --red:    #EF4444;
  --slate:  #64748B;
  --muted:  #94A3B8;
  --text:   #E2E8F0;
  --border: rgba(255,255,255,0.07);
}

*, *::before, *::after { box-sizing: border-box; margin: 0; padding: 0; }

html, body, .stApp,
[data-testid="stAppViewContainer"],
[data-testid="stMain"] {
  background: var(--bg) !important;
  color: var(--text) !important;
  font-family: 'Inter', sans-serif !important;
}

#MainMenu, footer, header,
[data-testid="stToolbar"],
[data-testid="stDecoration"],
[data-testid="collapsedControl"] { display: none !important; }

.block-container { padding: 0 !important; max-width: 100% !important; }

/* ── HERO ────────────────────────── */
.hero {
  background: linear-gradient(150deg,#0D1A30 0%,#090F1E 55%,#060B18 100%);
  padding: clamp(1.8rem,5vw,3.2rem) clamp(1.2rem,5vw,3.5rem) clamp(1.4rem,4vw,2.4rem);
  border-bottom: 1px solid var(--border);
  position: relative; overflow: hidden;
}
.hero::before {
  content:'';position:absolute;inset:0;
  background:
    radial-gradient(ellipse 55% 65% at 85% 15%, rgba(240,180,41,.07) 0%,transparent 70%),
    radial-gradient(ellipse 40% 55% at 5%  85%, rgba(45,212,191,.05) 0%,transparent 70%);
  pointer-events:none;
}
.hero-tag {
  display:inline-flex;align-items:center;gap:.4rem;
  background:rgba(240,180,41,.1);border:1px solid rgba(240,180,41,.22);
  color:var(--gold);padding:.22rem .75rem;border-radius:99px;
  font-size:.68rem;font-weight:700;letter-spacing:.08em;
  text-transform:uppercase;margin-bottom:.85rem;
}
.hero-title {
  font-size:clamp(1.7rem,4.5vw,3rem);font-weight:800;
  line-height:1.15;color:#fff;margin-bottom:.55rem;
}
.hero-title em{color:var(--gold);font-style:normal;}
.hero-desc {
  font-size:clamp(.82rem,2vw,.97rem);color:var(--muted);
  line-height:1.72;max-width:660px;margin-bottom:1.1rem;
}
.hero-pills{display:flex;flex-wrap:wrap;gap:.45rem;}
.hero-pill{
  background:rgba(255,255,255,.04);border:1px solid var(--border);
  color:var(--muted);padding:.22rem .72rem;border-radius:99px;font-size:.71rem;
}
.hero-pill b{color:var(--teal);}

/* ── METRIC STRIP ────────────────── */
.mstrip{
  display:grid;grid-template-columns:repeat(4,1fr);
  gap:1px;background:var(--border);border-bottom:1px solid var(--border);
}
@media(max-width:600px){.mstrip{grid-template-columns:repeat(2,1fr);}}
.mtile{
  background:var(--bg1);
  padding:clamp(.85rem,3vw,1.35rem) clamp(.9rem,3vw,1.6rem);
  position:relative;
}
.mtile::before{content:'';position:absolute;top:0;left:0;right:0;height:2px;}
.mt0::before{background:linear-gradient(90deg,var(--teal),var(--gold));}
.mt1::before{background:var(--red);}
.mt2::before{background:var(--green);}
.mt3::before{background:var(--slate);}
.mlabel{font-size:.63rem;font-weight:700;letter-spacing:.1em;text-transform:uppercase;color:var(--slate);margin-bottom:.32rem;}
.mval{font-family:'JetBrains Mono',monospace;font-size:clamp(1.45rem,3.5vw,2.1rem);font-weight:600;color:#fff;line-height:1;margin-bottom:.18rem;}
.msub{font-size:.7rem;color:var(--slate);}
.mico{position:absolute;top:.95rem;right:1rem;font-size:1.1rem;opacity:.14;}

/* ── PAGE ────────────────────────── */
.pw{padding:0 clamp(1rem,5vw,3.5rem);}

/* ── TABS ────────────────────────── */
.stTabs{padding:0 clamp(1rem,5vw,3.5rem) !important;}
.stTabs [data-baseweb="tab-list"]{
  background:transparent !important;
  border-bottom:1px solid var(--border) !important;
  gap:0 !important;padding:0 !important;flex-wrap:wrap !important;
}
.stTabs [data-baseweb="tab"]{
  background:transparent !important;color:var(--slate) !important;
  border-bottom:2px solid transparent !important;border-radius:0 !important;
  font-size:.8rem !important;font-weight:500 !important;
  padding:.7rem 1.1rem !important;margin:0 !important;
}
.stTabs [data-baseweb="tab"]:hover{color:var(--text) !important;}
.stTabs [aria-selected="true"]{
  color:var(--gold) !important;border-bottom-color:var(--gold) !important;
  background:transparent !important;font-weight:700 !important;
}
.stTabs [data-baseweb="tab-panel"]{padding:clamp(1rem,3vw,2rem) 0 0 !important;}

/* ── CARD ────────────────────────── */
.card{background:var(--bg1);border:1px solid var(--border);border-radius:14px;padding:clamp(1rem,3vw,1.5rem);}
.ctitle{font-size:.85rem;font-weight:700;color:var(--text);margin-bottom:.15rem;}
.csub{font-size:.7rem;color:var(--slate);margin-bottom:.85rem;}
.cline{width:26px;height:2px;background:var(--gold);border-radius:1px;margin:.35rem 0 .8rem;}

/* ── STAT ROW ────────────────────── */
.srow{display:flex;justify-content:space-between;align-items:flex-start;padding:.52rem 0;border-bottom:1px solid var(--border);font-size:.79rem;}
.srow:last-child{border-bottom:none;}
.sk{color:var(--muted);flex-shrink:0;padding-right:.5rem;}
.sv{color:var(--text);font-weight:500;font-family:'JetBrains Mono',monospace;text-align:right;}
.sv.gold{color:var(--gold);}.sv.teal{color:var(--teal);}.sv.green{color:var(--green);}.sv.red{color:var(--red);}.sv.blue{color:#60A5FA;}

/* ── TWEET ───────────────────────── */
.tw{background:var(--bg2);border:1px solid var(--border);border-left:3px solid;border-radius:10px;padding:.85rem 1rem;margin-bottom:.6rem;}
.tw.neg{border-left-color:var(--red);}
.tw.pos{border-left-color:var(--green);}
.tw.net{border-left-color:var(--slate);}
.two{font-size:.8rem;color:var(--text);line-height:1.62;margin-bottom:.32rem;}
.twc{font-size:.7rem;color:var(--muted);font-family:'JetBrains Mono',monospace;background:var(--bg3);padding:.3rem .6rem;border-radius:6px;margin-bottom:.32rem;line-height:1.5;}
.twf{display:flex;gap:.45rem;align-items:center;flex-wrap:wrap;}
.bdg{padding:.14rem .55rem;border-radius:99px;font-size:.6rem;font-weight:700;letter-spacing:.05em;}
.bdg.neg{background:rgba(239,68,68,.13);color:#FCA5A5;}
.bdg.pos{background:rgba(34,197,94,.13);color:#86EFAC;}
.bdg.net{background:rgba(100,116,139,.13);color:#CBD5E1;}

/* ── INSIGHT ─────────────────────── */
.ins{background:var(--bg2);border:1px solid var(--border);border-radius:10px;padding:1rem 1.1rem;}
.ins-val{font-family:'JetBrains Mono',monospace;font-size:1.75rem;font-weight:600;color:var(--gold);line-height:1.2;}
.ins-lbl{font-size:.67rem;font-weight:700;text-transform:uppercase;letter-spacing:.08em;color:var(--slate);margin-bottom:.22rem;}
.ins-desc{font-size:.74rem;color:var(--muted);line-height:1.55;margin-top:.28rem;}

/* ── FOLD GRID ───────────────────── */
.fgrid{display:grid;grid-template-columns:repeat(5,1fr);gap:.45rem;margin-top:.7rem;}
@media(max-width:580px){.fgrid{grid-template-columns:repeat(3,1fr);}}
.fpill{background:var(--bg3);border:1px solid var(--border);border-radius:8px;padding:.48rem .35rem;text-align:center;}
.fname{font-size:.6rem;color:var(--slate);margin-bottom:.18rem;}
.fval{font-family:'JetBrains Mono',monospace;font-size:.86rem;font-weight:600;color:var(--teal);}

/* ── CM BOX ──────────────────────── */
.cmbox{padding:.7rem .9rem;border-radius:9px;text-align:center;}
.cmlbl{font-size:.68rem;color:var(--muted);margin-bottom:.25rem;}
.cmval{font-family:'JetBrains Mono',monospace;font-size:1.5rem;font-weight:700;color:#fff;}

/* ── STEP ────────────────────────── */
.step{display:flex;gap:.6rem;align-items:flex-start;margin-bottom:.65rem;}
.sdot{width:22px;height:22px;border-radius:50%;flex-shrink:0;display:flex;align-items:center;justify-content:center;font-size:.6rem;font-weight:800;color:#060B18;margin-top:1px;}
.sname{font-size:.8rem;font-weight:600;color:var(--text);}
.sdesc{font-size:.68rem;color:var(--slate);margin-top:.08rem;}

/* ── FOOTER ──────────────────────── */
.foot{border-top:1px solid var(--border);margin-top:2rem;padding:1.1rem clamp(1rem,5vw,3.5rem);text-align:center;font-size:.69rem;color:var(--slate);line-height:1.8;}
.foot b{color:var(--gold);}

/* streamlit widgets */
.stSelectbox>div>div{background:var(--bg2) !important;border-color:var(--border) !important;border-radius:8px !important;color:var(--text) !important;}
div[data-baseweb="select"] span{color:var(--text) !important;}
label{color:var(--muted) !important;font-size:.78rem !important;}
.stCheckbox label{color:var(--muted) !important;}
::-webkit-scrollbar{width:4px;height:4px;}
::-webkit-scrollbar-track{background:var(--bg);}
::-webkit-scrollbar-thumb{background:var(--bg3);border-radius:2px;}
</style>
""", unsafe_allow_html=True)


# ═══════════════════════════════════════════
# DATA AKTUAL  ← dari file Excel + gambar
# ═══════════════════════════════════════════
TOTAL = 2096
NEG   = 1611   # 76.9 %
POS   = 359    # 17.1 %
NET   = 126    # 6.0  %

P_NEG, P_POS, P_NET = 0.768496, 0.171241, 0.060263
TRAIN, TEST = 1676, 420

AKU, PRE, REC, F1 = 78.57, 74.75, 78.57, 75.51
CV    = [78.33, 79.00, 77.33, 77.57, 79.47]
CV_M, CV_S = 78.34, 0.82

# ── Confusion Matrix BENAR (dari confusion_matrix.png yang Anda kirim) ──
# Baris = Aktual, Kolom = Prediksi  [Positif, Netral, Negatif]
CM_LABELS = ['Positif', 'Netral', 'Negatif']
CM = [
    [29,  3,  12],   # Aktual Positif  → Pred Pos=29, Pred Net=3, Pred Neg=12
    [ 0,  0,   1],   # Aktual Netral   → Pred Pos=0,  Pred Net=0, Pred Neg=1
    [ 4,  2, 2300],  # Aktual Negatif  → Pred Pos=4,  Pred Net=2, Pred Neg=2300
]

TFIDF = {
    'pajak':0.041,'tahun':0.031,'aktivasi':0.031,'akun':0.028,
    'wajib':0.025,'wajib pajak':0.024,'nomor':0.023,
    'akun coretax':0.022,'kak':0.022,'surat':0.021,
    'pemberitahuan':0.020,'surat pemberitahuan':0.020,
    'pemberitahuan tahun':0.020,'lapor':0.020,'aktivasi akun':0.020,
    'aktivasi coretax':0.017,'pokok':0.017,'pokok wajib':0.017,
    'nomor pokok':0.017,'email':0.016,'kakak':0.015,
    'daftar':0.015,'data':0.015,'min':0.015,'jenderal':0.015,
}

TWEETS = [
    {"asli": "Apakah perlu menyatukan satu nomor wajib pajak bagi Suami-Istri ASN di Coretax? Jika perlu bagaimana caranya apabila akun coretax sudah dibuat?",
     "bersih": "satu nomor wajib pajak suami istri asn coretax instansi akun coretax", "label": "Negatif"},
    {"asli": "Halo kak, karyawan ingin registrasi coretax tapi kendala KK sudah hilang karena bercerai dan belum diurus di dukcapil, bagaimana cara daftarnya?",
     "bersih": "kak karyawan registrasi coretax kendala kk hilang cerai urus dukcapil daftar nomor kk", "label": "Negatif"},
    {"asli": "Coretax error terus, tidak bisa akses sejak pagi. Deadline lapor pajak sudah dekat tapi sistem malah down terus.",
     "bersih": "coretax error akses deadline lapor pajak dekat sistem down", "label": "Negatif"},
    {"asli": "Tujuan coretax untuk mempermudah tapi malah bikin emosi. Sudah coba berkali-kali tetap tidak bisa login.",
     "bersih": "tuju coretax mudah mudah emosi berkali login", "label": "Negatif"},
    {"asli": "Sistem coretax sangat lambat dan sering tidak merespons. Sangat mengecewakan untuk urusan perpajakan.",
     "bersih": "sistem coretax lambat merespons kecewa pajak", "label": "Negatif"},
    {"asli": "Alhamdulillah berhasil lapor SPT tahunan lewat coretax, lancar sekali! Terima kasih DJP sudah berinovasi.",
     "bersih": "alhamdulillah hasil lapor surat pemberitahuan tahun coretax lancar terima kasih djp inovasi", "label": "Positif"},
    {"asli": "Coretax sekarang sudah jauh lebih baik dan mudah digunakan. Tampilannya modern dan proses lapor pajak jadi cepat.",
     "bersih": "coretax baik mudah tampilan modern lapor pajak cepat", "label": "Positif"},
    {"asli": "Buat yang mau tanya soal CoreTax boleh DM aku, aku bantu sebisaku untuk urusan perpajakan, gratis!",
     "bersih": "coretax bantu sebisaku urusan perpajakan gratis", "label": "Positif"},
    {"asli": "Deadline lapor SPT tahunan orang pribadi melalui coretax adalah 31 Maret 2025. Segera lapor sebelum terlambat.",
     "bersih": "deadline lapor surat pemberitahuan tahun pribadi coretax maret lapor", "label": "Netral"},
    {"asli": "Coretax adalah sistem administrasi perpajakan terbaru dari Direktorat Jenderal Pajak yang diluncurkan akhir 2024.",
     "bersih": "coretax sistem administrasi perpajakan baru direktorat jenderal pajak luncur akhir tahun", "label": "Netral"},
    {"asli": "NIK Kakak telah terdaftar di Coretax, silakan pilih Aktivasi Akun Wajib Pajak pada laman awal Coretax untuk login pertama kali.",
     "bersih": "nik kakak daftar coretax sila pilih aktivasi akun wajib pajak laman coretax login", "label": "Netral"},
]

PT = dict(paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)',
          font=dict(family='Inter', color='#94A3B8', size=11))
css  = {'Positif':'pos','Negatif':'neg','Netral':'net'}
bdge = {'Positif':'<span class="bdg pos">😊 POSITIF</span>',
        'Negatif':'<span class="bdg neg">😠 NEGATIF</span>',
        'Netral' :'<span class="bdg net">😐 NETRAL</span>'}


# ═══════════════════════════════════════════
# HERO
# ═══════════════════════════════════════════
st.markdown(f"""
<div class="hero">
  <div class="hero-tag">📊 Skripsi · STMIK Triguna Dharma · 2026</div>
  <h1 class="hero-title">Sentimen Masyarakat<br>terhadap <em>Coretax</em> di Platform X</h1>
  <p class="hero-desc">
    Analisis persepsi publik terhadap sistem perpajakan digital Coretax
    berdasarkan <strong style="color:#E2E8F0">{TOTAL:,} tweet</strong>
    menggunakan algoritma <strong style="color:#E2E8F0">Categorical Naïve Bayes</strong>.
    Akurasi model mencapai <strong style="color:#F0B429">{AKU}%</strong>.
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

# ═══════════════════════════════════════════
# METRIC STRIP
# ═══════════════════════════════════════════
st.markdown(f"""
<div class="mstrip">
  <div class="mtile mt0"><div class="mico">🐦</div>
    <div class="mlabel">Total Tweet</div>
    <div class="mval">{TOTAL:,}</div>
    <div class="msub">Periode 44 hari</div></div>
  <div class="mtile mt1"><div class="mico">😠</div>
    <div class="mlabel">Negatif</div>
    <div class="mval">{NEG:,}</div>
    <div class="msub">{NEG/TOTAL*100:.1f}% dari total</div></div>
  <div class="mtile mt2"><div class="mico">😊</div>
    <div class="mlabel">Positif</div>
    <div class="mval">{POS:,}</div>
    <div class="msub">{POS/TOTAL*100:.1f}% dari total</div></div>
  <div class="mtile mt3"><div class="mico">😐</div>
    <div class="mlabel">Netral</div>
    <div class="mval">{NET:,}</div>
    <div class="msub">{NET/TOTAL*100:.1f}% dari total</div></div>
</div>
""", unsafe_allow_html=True)

# ═══════════════════════════════════════════
# TABS
# ═══════════════════════════════════════════
t1,t2,t3,t4,t5 = st.tabs([
    "📊  Distribusi",
    "📈  Evaluasi Model",
    "💬  Ulasan Publik",
    "🔄  Preprocessing",
    "📋  Ringkasan",
])


# ─────────────────────────────────────────
# TAB 1 — DISTRIBUSI
# ─────────────────────────────────────────
with t1:
    st.markdown('<div class="pw">', unsafe_allow_html=True)

    ca, cb = st.columns([1, 1.45], gap="large")

    with ca:
        st.markdown('<div class="card">', unsafe_allow_html=True)
        st.markdown('<div class="ctitle">Proporsi Sentimen</div><div class="cline"></div>', unsafe_allow_html=True)
        st.markdown(f'<div class="csub">Total {TOTAL:,} tweet — Labeling InSet Lexicon</div>', unsafe_allow_html=True)
        fig_pie = go.Figure(go.Pie(
            labels=['Negatif','Positif','Netral'], values=[NEG,POS,NET],
            hole=0.63, direction='clockwise', sort=False,
            marker=dict(colors=['#EF4444','#22C55E','#475569'],
                        line=dict(color='#060B18',width=3)),
            textinfo='percent',
            textfont=dict(size=12,family='JetBrains Mono',color='white'),
            insidetextorientation='horizontal',
            hovertemplate='<b>%{label}</b><br>%{value:,} tweet (%{percent:.1%})<extra></extra>',
        ))
        fig_pie.add_annotation(x=0.5,y=0.5,showarrow=False,
            text=f"<span style='font-size:22px;font-weight:700;color:#EF4444'>{NEG/TOTAL*100:.0f}%</span>"
                 f"<br><span style='font-size:10px;color:#64748B'>Negatif</span>",
            font=dict(family='JetBrains Mono'))
        fig_pie.update_layout(**PT, height=290,
            margin=dict(l=6,r=6,t=10,b=38),
            legend=dict(orientation='h',x=0.5,y=-0.14,xanchor='center',
                        font=dict(size=11),bgcolor='rgba(0,0,0,0)'))
        st.plotly_chart(fig_pie, use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)

    with cb:
        st.markdown('<div class="card">', unsafe_allow_html=True)
        st.markdown('<div class="ctitle">Jumlah Tweet per Kelas</div><div class="cline"></div>', unsafe_allow_html=True)
        st.markdown('<div class="csub">Perbandingan volume tiap kategori sentimen</div>', unsafe_allow_html=True)
        fig_bar = go.Figure()
        for lbl,val,clr in [('Negatif',NEG,'#EF4444'),('Positif',POS,'#22C55E'),('Netral',NET,'#475569')]:
            fig_bar.add_trace(go.Bar(
                y=[lbl], x=[val], orientation='h', name=lbl,
                marker=dict(color=clr, line=dict(width=0)),
                text=f'  {val:,}  ({val/TOTAL*100:.1f}%)',
                textposition='inside',
                textfont=dict(size=12,color='white',family='JetBrains Mono'),
                hovertemplate=f'<b>{lbl}</b>: {val:,} tweet<extra></extra>',
            ))
        fig_bar.update_layout(**PT, height=215, showlegend=False,
            margin=dict(l=6,r=6,t=10,b=30),
            xaxis=dict(title='Jumlah Tweet', showgrid=True,
                       gridcolor='rgba(255,255,255,.05)', tickfont=dict(size=10)),
            yaxis=dict(tickfont=dict(size=12)), bargap=0.28)
        st.plotly_chart(fig_bar, use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)

    # TF-IDF
    st.markdown('<div class="card" style="margin-top:1rem">', unsafe_allow_html=True)
    st.markdown('<div class="ctitle">Top 25 Fitur TF-IDF</div><div class="cline"></div>', unsafe_allow_html=True)
    st.markdown('<div class="csub">Kata/frasa dengan bobot rata-rata TF-IDF tertinggi — n-gram (1,2), min_df=2, max_features=5000</div>', unsafe_allow_html=True)
    tdf = pd.DataFrame(list(TFIDF.items()), columns=['f','b']).sort_values('b')
    blues = [f'rgba(59,130,246,{0.30+0.70*(i/len(tdf)):.2f})' for i in range(len(tdf))]
    fig_tf = go.Figure(go.Bar(
        x=tdf['b'], y=tdf['f'], orientation='h',
        marker=dict(color=blues, line=dict(width=0)),
        hovertemplate='<b>%{y}</b>  →  %{x:.3f}<extra></extra>',
    ))
    fig_tf.update_layout(**PT, height=490,
        margin=dict(l=6,r=52,t=10,b=32),
        xaxis=dict(title='Rata-rata Skor TF-IDF', showgrid=True,
                   gridcolor='rgba(255,255,255,.05)', tickfont=dict(size=10)),
        yaxis=dict(tickfont=dict(size=10.5), automargin=True))
    st.plotly_chart(fig_tf, use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)

    st.markdown('<br>', unsafe_allow_html=True)
    i1,i2,i3 = st.columns(3, gap="medium")
    with i1:
        st.markdown(f"""<div class="ins">
          <div class="ins-lbl">Dominasi Negatif</div>
          <div class="ins-val">{NEG/TOTAL*100:.1f}%</div>
          <div class="ins-desc">Keluhan utama: <em>error sistem</em>, <em>login gagal</em>, dan <em>lambat/down</em>.</div>
        </div>""", unsafe_allow_html=True)
    with i2:
        st.markdown(f"""<div class="ins">
          <div class="ins-lbl">Sentimen Positif</div>
          <div class="ins-val">{POS/TOTAL*100:.1f}%</div>
          <div class="ins-desc">Puas dengan kemudahan lapor SPT dan inovasi DJP dalam sistem pajak digital.</div>
        </div>""", unsafe_allow_html=True)
    with i3:
        st.markdown(f"""<div class="ins">
          <div class="ins-lbl">Fitur TF-IDF #1</div>
          <div class="ins-val">pajak</div>
          <div class="ins-desc">Bobot tertinggi 0.041, diikuti <em>tahun</em> (0.031) dan <em>aktivasi</em> (0.031).</div>
        </div>""", unsafe_allow_html=True)

    st.markdown('</div>', unsafe_allow_html=True)  # pw


# ─────────────────────────────────────────
# TAB 2 — EVALUASI MODEL
# ─────────────────────────────────────────
with t2:
    st.markdown('<div class="pw">', unsafe_allow_html=True)

    # 4 gauge
    g1,g2,g3,g4 = st.columns(4, gap="medium")
    for col,name,val,clr,hx in [
        (g1,"Akurasi",  AKU,'#3B82F6','3B82F6'),
        (g2,"Presisi",  PRE,'#22C55E','22C55E'),
        (g3,"Recall",   REC,'#F59E0B','F59E0B'),
        (g4,"F1-Score", F1, '#8B5CF6','8B5CF6'),
    ]:
        with col:
            r,g,b = int(hx[:2],16),int(hx[2:4],16),int(hx[4:],16)
            fg = go.Figure(go.Indicator(
                mode="gauge+number", value=val,
                number={'suffix':'%','font':{'size':24,'color':clr,'family':'JetBrains Mono'}},
                title={'text':name,'font':{'size':12,'color':'#94A3B8'}},
                gauge=dict(
                    axis=dict(range=[0,100], tickfont=dict(size=8,color='#475569'),
                              tickcolor='#1A2B47', nticks=6),
                    bar=dict(color=clr, thickness=0.28),
                    bgcolor='#111E35', bordercolor='#111E35', borderwidth=0,
                    steps=[
                        {'range':[0,70],  'color':'rgba(255,255,255,0.02)'},
                        {'range':[70,100],'color':f'rgba({r},{g},{b},0.08)'},
                    ],
                    threshold=dict(line=dict(color='#F0B429',width=2.5),
                                   thickness=0.72, value=70),
                )
            ))
            fg.update_layout(**PT, height=190, margin=dict(l=4,r=4,t=22,b=4))
            col.plotly_chart(fg, use_container_width=True)

    st.markdown('<p style="text-align:center;font-size:.69rem;color:#475569;margin:-0.4rem 0 1.3rem">⭐ Garis kuning = batas minimum akurasi 70%</p>', unsafe_allow_html=True)

    ev1, ev2 = st.columns([1.1,1], gap="large")

    with ev1:
        st.markdown('<div class="card">', unsafe_allow_html=True)
        st.markdown('<div class="ctitle">Perbandingan Metrik Evaluasi</div><div class="cline"></div>', unsafe_allow_html=True)
        st.markdown('<div class="csub">Akurasi, Presisi, Recall, F1-Score — 420 data testing</div>', unsafe_allow_html=True)
        fig_ev = go.Figure()
        for nm,vl,cl in [('Akurasi',AKU,'#3B82F6'),('Presisi',PRE,'#22C55E'),
                          ('Recall',REC,'#F59E0B'),('F1-Score',F1,'#8B5CF6')]:
            fig_ev.add_trace(go.Bar(
                x=[nm], y=[vl], name=nm, width=0.48,
                marker=dict(color=cl, line=dict(width=0)),
                text=f'{vl:.2f}%', textposition='outside',
                textfont=dict(size=11,color=cl,family='JetBrains Mono'),
            ))
        fig_ev.add_hline(y=70, line_dash='dot', line_color='#F0B429', line_width=1.5,
                         annotation_text='Min 70%',
                         annotation_font=dict(size=9,color='#F0B429'))
        fig_ev.update_layout(**PT, height=285, showlegend=False,
            margin=dict(l=6,r=6,t=16,b=8),
            xaxis=dict(showgrid=False, tickfont=dict(size=11)),
            yaxis=dict(range=[0,93], showgrid=True,
                       gridcolor='rgba(255,255,255,.05)', tickfont=dict(size=10)))
        st.plotly_chart(fig_ev, use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)

    with ev2:
        st.markdown('<div class="card">', unsafe_allow_html=True)
        st.markdown('<div class="ctitle">Cross Validation — 5-Fold</div><div class="cline"></div>', unsafe_allow_html=True)
        st.markdown(f'<div class="csub">Rata-rata {CV_M:.2f}% ± {CV_S:.2f}% — model stabil & tidak overfitting</div>', unsafe_allow_html=True)
        fig_cv = go.Figure(go.Bar(
            x=[f'Fold {i+1}' for i in range(5)], y=CV, width=0.52,
            marker=dict(color='#2DD4BF', line=dict(width=0)),
            text=[f'{v:.2f}%' for v in CV], textposition='outside',
            textfont=dict(size=10,color='#2DD4BF',family='JetBrains Mono'),
        ))
        fig_cv.add_hline(y=CV_M, line_dash='dash', line_color='#F0B429', line_width=1.5,
                         annotation_text=f'Rata-rata: {CV_M:.2f}%',
                         annotation_font=dict(size=9,color='#F0B429'))
        fig_cv.update_layout(**PT, height=248,
            margin=dict(l=6,r=6,t=16,b=8),
            xaxis=dict(showgrid=False, tickfont=dict(size=10)),
            yaxis=dict(range=[76,81], showgrid=True,
                       gridcolor='rgba(255,255,255,.05)',
                       tickfont=dict(size=10), title='Akurasi (%)'))
        st.plotly_chart(fig_cv, use_container_width=True)
        folds_html = ''.join([
            f'<div class="fpill"><div class="fname">Fold {i+1}</div>'
            f'<div class="fval">{v:.2f}%</div></div>'
            for i,v in enumerate(CV)
        ])
        st.markdown(f'<div class="fgrid">{folds_html}</div>', unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)

    # ── CONFUSION MATRIX ──────────────────────────────
    st.markdown('<div class="card" style="margin-top:1.2rem">', unsafe_allow_html=True)
    st.markdown('<div class="ctitle">Confusion Matrix</div><div class="cline"></div>', unsafe_allow_html=True)
    st.markdown('<div class="csub">Matriks klasifikasi aktual vs prediksi pada 420 data testing — Categorical Naïve Bayes</div>', unsafe_allow_html=True)

    cm_left, cm_right = st.columns([1.55, 1], gap="large")

    with cm_left:
        # warna: diagonal = kuning keemasan, lainnya biru gelap
        z_color = []
        for i in range(3):
            row = []
            for j in range(3):
                row.append(CM[i][j])
            z_color.append(row)

        fig_cm = go.Figure(go.Heatmap(
            z=z_color,
            x=['Pred: Positif','Pred: Netral','Pred: Negatif'],
            y=['Aktual: Positif','Aktual: Netral','Aktual: Negatif'],
            text=[[str(v) for v in row] for row in CM],
            texttemplate='<b>%{text}</b>',
            textfont={'size':16,'color':'white','family':'JetBrains Mono'},
            colorscale=[
                [0,    '#111E35'],
                [0.01, '#1A2B47'],
                [0.05, '#1E3A5F'],
                [0.3,  '#1D4ED8'],
                [1,    '#F0B429'],   # diagonal tinggi = gold
            ],
            showscale=False,
            hovertemplate='Aktual: %{y}<br>Prediksi: %{x}<br>Jumlah: %{z}<extra></extra>',
        ))
        fig_cm.update_layout(**PT, height=295,
            margin=dict(l=6,r=6,t=8,b=8),
            xaxis=dict(tickfont=dict(size=10.5), side='bottom'),
            yaxis=dict(tickfont=dict(size=10.5), autorange='reversed'))
        st.plotly_chart(fig_cm, use_container_width=True)

    with cm_right:
        st.markdown('<br>', unsafe_allow_html=True)
        # TP (diagonal)
        tp_pos = CM[0][0]   # 29
        tp_net = CM[1][1]   # 0
        tp_neg = CM[2][2]   # 2300
        # error
        fp_p_ke_neg = CM[0][2]  # Positif → Negatif = 12
        fp_p_ke_net = CM[0][1]  # Positif → Netral  = 3
        fp_neg_ke_pos= CM[2][0]  # Negatif → Positif = 4
        fp_neg_ke_net= CM[2][1]  # Negatif → Netral  = 2
        fp_net_ke_neg= CM[1][2]  # Netral  → Negatif = 1

        rows = [
            ("✅ True Positif",    str(tp_pos),  "green"),
            ("✅ True Netral",     str(tp_net),  ""),
            ("✅ True Negatif",    str(tp_neg),  "red"),
            ("❌ Positif → Negatif", str(fp_p_ke_neg),"red"),
            ("❌ Positif → Netral",  str(fp_p_ke_net),""),
            ("❌ Negatif → Positif", str(fp_neg_ke_pos),"green"),
            ("❌ Negatif → Netral",  str(fp_neg_ke_net),""),
            ("❌ Netral  → Negatif", str(fp_net_ke_neg),"red"),
        ]
        for lbl,val,cl in rows:
            st.markdown(
                f'<div class="srow"><span class="sk" style="font-size:.73rem">{lbl}</span>'
                f'<span class="sv {cl}">{val}</span></div>',
                unsafe_allow_html=True)

    # 3 kotak TP besar di bawah CM
    st.markdown('<br>', unsafe_allow_html=True)
    b1,b2,b3 = st.columns(3, gap="medium")
    with b1:
        st.markdown(f"""<div class="cmbox" style="background:rgba(34,197,94,.07);border:1px solid rgba(34,197,94,.18)">
          <div class="cmlbl">✅ Benar Positif (TP)</div>
          <div class="cmval" style="color:#86EFAC">29</div></div>""", unsafe_allow_html=True)
    with b2:
        st.markdown(f"""<div class="cmbox" style="background:rgba(239,68,68,.07);border:1px solid rgba(239,68,68,.18)">
          <div class="cmlbl">✅ Benar Negatif (TP)</div>
          <div class="cmval" style="color:#FCA5A5">2,300</div></div>""", unsafe_allow_html=True)
    with b3:
        st.markdown(f"""<div class="cmbox" style="background:rgba(100,116,139,.07);border:1px solid rgba(100,116,139,.18)">
          <div class="cmlbl">✅ Benar Netral (TP)</div>
          <div class="cmval" style="color:#CBD5E1">0</div></div>""", unsafe_allow_html=True)

    st.markdown('</div>', unsafe_allow_html=True)  # card

    # Prior P(Vj)
    st.markdown('<div class="card" style="margin-top:1.2rem">', unsafe_allow_html=True)
    st.markdown('<div class="ctitle">Probabilitas Prior P(Vj)</div><div class="cline"></div>', unsafe_allow_html=True)
    st.markdown(f'<div class="csub">P(Vj) = |doc j| / |training| — dari {TRAIN:,} data training</div>', unsafe_allow_html=True)
    p1,p2,p3 = st.columns(3, gap="medium")
    for col,lbl,jml,prob,clr in [
        (p1,"V1 = Negatif",1288,P_NEG,"#EF4444"),
        (p2,"V2 = Positif",287, P_POS,"#22C55E"),
        (p3,"V3 = Netral", 101, P_NET,"#64748B"),
    ]:
        with col:
            col.markdown(f"""<div class="ins" style="border-left:3px solid {clr}">
              <div class="ins-lbl">{lbl}</div>
              <div class="ins-val" style="color:{clr};font-size:1.45rem">{prob:.6f}</div>
              <div class="ins-desc">{jml:,} / {TRAIN:,} tweet training</div>
            </div>""", unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)  # pw


# ─────────────────────────────────────────
# TAB 3 — ULASAN PUBLIK
# ─────────────────────────────────────────
with t3:
    st.markdown('<div class="pw">', unsafe_allow_html=True)
    st.markdown('<p style="font-size:1rem;font-weight:700;color:var(--text);margin-bottom:.15rem">Ulasan Masyarakat tentang Coretax</p>', unsafe_allow_html=True)
    st.markdown('<div class="cline"></div>', unsafe_allow_html=True)
    st.markdown('<p style="font-size:.72rem;color:var(--slate);margin-bottom:1rem">Sampel tweet dari Platform X yang telah dianalisis menggunakan Categorical Naïve Bayes</p>', unsafe_allow_html=True)

    fa, fb = st.columns([1,2], gap="medium")
    with fa:
        filt = st.selectbox("🔍 Filter Sentimen", ["Semua","Negatif","Positif","Netral"])
    with fb:
        show_pre = st.checkbox("Tampilkan hasil preprocessing", value=True)

    filtered = TWEETS if filt=="Semua" else [t for t in TWEETS if t['label']==filt]

    if not filtered:
        st.info(f"Tidak ada tweet dengan label {filt}")
    else:
        tc1, tc2 = st.columns(2, gap="medium")
        for i, tw in enumerate(filtered):
            cl   = css[tw['label']]
            pre  = f'<div class="twc">🔄 {tw["bersih"]}</div>' if show_pre else ''
            card = (f'<div class="tw {cl}">'
                    f'<div class="two">{tw["asli"]}</div>'
                    f'{pre}'
                    f'<div class="twf">{bdge[tw["label"]]}</div>'
                    f'</div>')
            (tc1 if i%2==0 else tc2).markdown(card, unsafe_allow_html=True)

    st.markdown('</div>', unsafe_allow_html=True)


# ─────────────────────────────────────────
# TAB 4 — PREPROCESSING
# ─────────────────────────────────────────
with t4:
    st.markdown('<div class="pw">', unsafe_allow_html=True)
    pp1, pp2 = st.columns([1,1.2], gap="large")

    with pp1:
        st.markdown('<div class="card">', unsafe_allow_html=True)
        st.markdown('<div class="ctitle">Alur Preprocessing</div><div class="cline"></div>', unsafe_allow_html=True)
        st.markdown('<div class="csub">7 tahap sesuai flowchart skripsi</div>', unsafe_allow_html=True)
        steps = [
            ("#F0B429","Cleaning",         "Hapus URL, mention (@), hashtag (#), simbol, angka"),
            ("#2DD4BF","Case Folding",      "Konversi seluruh teks ke huruf kecil"),
            ("#22C55E","Normalisasi",        "Slang & singkatan → kata baku PUEBI (80+ entri)"),
            ("#8B5CF6","Stopword Removal",  "Hapus kata tidak bermakna (Sastrawi + custom)"),
            ("#F59E0B","Tokenizing",         "Pecah teks menjadi token kata individual"),
            ("#EF4444","Stemming",           "Kata berimbuhan → kata dasar (Sastrawi ECS)"),
            ("#3B82F6","Labeling",           "Beri label otomatis dengan kamus InSet"),
        ]
        for i,(clr,name,desc) in enumerate(steps):
            st.markdown(f"""<div class="step">
              <div class="sdot" style="background:{clr}">{i+1}</div>
              <div><div class="sname">{name}</div><div class="sdesc">{desc}</div></div>
            </div>""", unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)

    with pp2:
        st.markdown('<div class="card">', unsafe_allow_html=True)
        st.markdown('<div class="ctitle">Statistik Dataset</div><div class="cline"></div>', unsafe_allow_html=True)
        for k,v,cl in [
            ("Total data",         f"{TOTAL:,} tweet", ""),
            ("Data training (80%)",f"{TRAIN:,} tweet", "teal"),
            ("Data testing  (20%)",f"{TEST:,} tweet",  ""),
            ("Vocabulary unik",    "~2.500 kata",       ""),
            ("Fitur TF-IDF",       "5.000 fitur",       "gold"),
            ("N-gram range",       "1-gram & 2-gram",   ""),
            ("Kamus normalisasi",  "80+ entri slang",   ""),
            ("InSet Positif",      "~3.419 kata",       "green"),
            ("InSet Negatif",      "~6.609 kata",       "red"),
        ]:
            st.markdown(f'<div class="srow"><span class="sk">{k}</span><span class="sv {cl}">{v}</span></div>',
                        unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)

        st.markdown('<div class="card" style="margin-top:1rem">', unsafe_allow_html=True)
        st.markdown('<div class="ctitle">Contoh Preprocessing</div><div class="cline"></div>', unsafe_allow_html=True)
        ex = [
            ("@ezash Dari sebelum coretax jg masuk kalo si shopee dkk bikin bukti potong",
             "coretax si shopee kawan kawan bikin bukti potong","Negatif"),
            ("Tujuan coretax untuk mempermudah mudah emosi https://t.co/xxx",
             "tuju coretax mudah mudah emosi","Negatif"),
            ("Alhamdulillah berhasil lapor SPT tahunan lewat coretax, lancar!",
             "alhamdulillah hasil lapor surat pemberitahuan tahun coretax lancar","Positif"),
        ]
        for orig,clean,lbl in ex:
            cl = css[lbl]
            st.markdown(
                f'<div class="tw {cl}" style="margin-bottom:.5rem">'
                f'<div class="two" style="font-size:.75rem">{orig}</div>'
                f'<div class="twc">{clean}</div>'
                f'<div class="twf">{bdge[lbl]}</div></div>',
                unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)

    st.markdown('</div>', unsafe_allow_html=True)


# ─────────────────────────────────────────
# TAB 5 — RINGKASAN
# ─────────────────────────────────────────
with t5:
    st.markdown('<div class="pw">', unsafe_allow_html=True)
    rs1, rs2 = st.columns([1.1,1], gap="large")

    with rs1:
        st.markdown('<div class="card">', unsafe_allow_html=True)
        st.markdown('<div class="ctitle">📌 Identitas Penelitian</div><div class="cline"></div>', unsafe_allow_html=True)
        for k,v,cl in [
            ("Judul","Analisis Sentimen Masyarakat Terhadap Aplikasi Coretax di Platform X",""),
            ("Peneliti","Aziz Fakhrizi","gold"),
            ("NIM","2022020255",""),
            ("Institusi","STMIK Triguna Dharma, Medan",""),
            ("Tahun","2026",""),
            ("Sumber Data","Platform X (Twitter)",""),
            ("Jumlah Data",f"{TOTAL:,} tweet","teal"),
            ("Periode","15 Des 2024 – 27 Jan 2025",""),
            ("Algoritma","Categorical Naïve Bayes","teal"),
            ("Labeling","Lexicon InSet Bahasa Indonesia",""),
            ("Ekstraksi Fitur","TF-IDF (5.000 fitur, n-gram 1–2)",""),
            ("Smoothing","Laplace (alpha = 1.0)",""),
            ("Split Data","Training 80% : Testing 20%",""),
        ]:
            st.markdown(
                f'<div class="srow">'
                f'<span class="sk" style="width:43%;flex-shrink:0">{k}</span>'
                f'<span class="sv {cl}" style="font-family:inherit;font-size:.78rem;text-align:right">{v}</span>'
                f'</div>', unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)

    with rs2:
        st.markdown('<div class="card">', unsafe_allow_html=True)
        st.markdown('<div class="ctitle">📊 Kinerja Model</div><div class="cline"></div>', unsafe_allow_html=True)
        for k,v,cl in [
            ("Akurasi",            f"{AKU:.2f}%","blue"),
            ("Presisi (Weighted)", f"{PRE:.2f}%","green"),
            ("Recall (Weighted)",  f"{REC:.2f}%",""),
            ("F1-Score (Weighted)",f"{F1:.2f}%",""),
            ("CV 5-Fold (rata-rata)",f"{CV_M:.2f}%","teal"),
            ("CV Std Deviasi",     f"±{CV_S:.2f}%",""),
        ]:
            st.markdown(f'<div class="srow"><span class="sk">{k}</span><span class="sv {cl}">{v}</span></div>',
                        unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)

        st.markdown('<div class="card" style="margin-top:1rem">', unsafe_allow_html=True)
        st.markdown('<div class="ctitle">💡 Temuan Utama</div><div class="cline"></div>', unsafe_allow_html=True)
        for ico,txt in [
            ("🔴",f"Sentimen negatif mendominasi ({NEG/TOTAL*100:.0f}%) — keluhan error & login gagal."),
            ("🟢",f"Sentimen positif {POS/TOTAL*100:.1f}% — puas lapor SPT dan inovasi DJP."),
            ("🔵",f"Akurasi {AKU:.2f}% melampaui batas minimum 70%."),
            ("⚡",f"CV 5-Fold stabil {CV_M:.2f}% ± {CV_S:.2f}% — tidak overfitting."),
            ("📌","Fitur pajak, tahun, aktivasi mendominasi TF-IDF dataset."),
        ]:
            st.markdown(
                f'<div style="display:flex;gap:.5rem;align-items:flex-start;margin-bottom:.55rem">'
                f'<span style="font-size:.8rem;flex-shrink:0">{ico}</span>'
                f'<span style="font-size:.76rem;color:#94A3B8;line-height:1.55">{txt}</span>'
                f'</div>', unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)

    st.markdown('</div>', unsafe_allow_html=True)


# ═══════════════════════════════════════════
# FOOTER
# ═══════════════════════════════════════════
st.markdown(f"""
<div class="foot">
  <b>Dashboard Sentimen Coretax</b> — Skripsi STMIK Triguna Dharma Medan 2026<br>
  Peneliti: <b>Aziz Fakhrizi</b> (2022020255) · {TOTAL:,} tweet ·
  Categorical Naïve Bayes · InSet Lexicon<br>
  Akurasi: <b>{AKU}%</b> · CV 5-Fold: <b>{CV_M:.2f}% ± {CV_S:.2f}%</b> ·
  15 Des 2024 – 27 Jan 2025
</div>
""", unsafe_allow_html=True)
