import streamlit as st
import numpy as np
import joblib
from datetime import datetime

# Konfigurasi halaman
st.set_page_config(
    page_title="Prediksi PCOS",
    page_icon="🌸",
    layout="wide",
    initial_sidebar_state="expanded"
)

# CSS untuk styling dengan tema 
def get_css():
    # Deteksi tema dari Streamlit 
    return f"""
    <style>
        /* Main background and theme */
        .main {{
            padding: 2rem;
        }}
        
        /* Header styling dengan gradien pink-purple feminim */
        .header-container {{
            background: linear-gradient(135deg, #ff9a9e 0%, #fecfef 50%, #fecfef 100%);
            padding: 2.5rem;
            border-radius: 20px;
            margin-bottom: 2rem;
            color: #4a154b;
            text-align: center;
            box-shadow: 0 15px 35px rgba(255, 154, 158, 0.3);
            border: 1px solid rgba(255, 182, 193, 0.3);
        }}
        
        .header-title {{
            font-size: 2.8rem;
            font-weight: 700;
            margin-bottom: 0.5rem;
            text-shadow: 0 2px 4px rgba(255, 255, 255, 0.3);
        }}
        
        .header-subtitle {{
            font-size: 1.3rem;
            opacity: 0.9;
            margin-bottom: 0;
            font-weight: 500;
        }}
        
        /* Card styling dengan warna soft pink */
        .info-card {{
            background: linear-gradient(145deg, #fdf2f8 0%, #fce7f3 100%);
            padding: 2rem;
            border-radius: 18px;
            box-shadow: 0 8px 25px rgba(219, 39, 119, 0.1);
            border: 1px solid rgba(251, 207, 232, 0.5);
            margin-bottom: 1.5rem;
        }}
        
        .info-card h3 {{
            color: #be185d;
            margin-bottom: 1rem;
            font-weight: 600;
        }}
        
        .info-card p, .info-card li {{
            color: #831843;
            line-height: 1.6;
        }}
        
        /* Metric card dengan gradien pink cantik */
        .metric-card {{
            background: linear-gradient(135deg, #f8a2c2 0%, #cd919e 100%);
            color: white;
            padding: 2rem;
            border-radius: 18px;
            text-align: center;
            margin: 1rem 0;
            box-shadow: 0 10px 30px rgba(248, 162, 194, 0.4);
            border: 1px solid rgba(255, 255, 255, 0.2);
        }}
        
        .metric-card h4 {{
            margin-bottom: 0.5rem;
            font-weight: 500;
            opacity: 0.9;
        }}
        
        .metric-card h2 {{
            margin: 0.5rem 0;
            font-weight: 700;
            font-size: 2.2rem;
        }}
        
        /* Section headers dengan accent pink */
        .section-header {{
            color: #be185d;
            font-size: 1.4rem;
            font-weight: 600;
            margin: 2rem 0 1.5rem 0;
            padding-bottom: 0.7rem;
            border-bottom: 3px solid #f472b6;
            position: relative;
        }}
        
        .section-header::after {{
            content: '';
            position: absolute;
            bottom: -3px;
            left: 0;
            width: 60px;
            height: 3px;
            background: linear-gradient(90deg, #ec4899, #be185d);
            border-radius: 2px;
        }}
        
        /* Result styling dengan warna feminim */
        .result-positive {{
            background: linear-gradient(135deg, #f87171 0%, #ef4444 100%);
            color: white;
            padding: 2.5rem;
            border-radius: 20px;
            text-align: center;
            font-size: 1.2rem;
            font-weight: 600;
            box-shadow: 0 15px 35px rgba(248, 113, 113, 0.3);
            margin: 2rem 0;
            border: 1px solid rgba(255, 255, 255, 0.2);
        }}
        
        .result-negative {{
            background: linear-gradient(135deg, #10b981 0%, #059669 100%);
            color: white;
            padding: 2.5rem;
            border-radius: 20px;
            text-align: center;
            font-size: 1.2rem;
            font-weight: 600;
            box-shadow: 0 15px 35px rgba(16, 185, 129, 0.3);
            margin: 2rem 0;
            border: 1px solid rgba(255, 255, 255, 0.2);
        }}
        
        /* Button styling dengan pink gradient */
        .stButton > button {{
            background: linear-gradient(135deg, #ec4899 0%, #be185d 100%);
            color: white;
            border: none;
            padding: 1rem 2.5rem;
            border-radius: 25px;
            font-weight: 600;
            font-size: 1.1rem;
            transition: all 0.3s ease;
            box-shadow: 0 8px 25px rgba(236, 72, 153, 0.3);
            width: 100%;
        }}
        
        .stButton > button:hover {{
            transform: translateY(-3px);
            box-shadow: 0 12px 35px rgba(236, 72, 153, 0.4);
            background: linear-gradient(135deg, #be185d 0%, #9d174d 100%);
        }}
        
        /* Hide streamlit elements */
        #MainMenu {{visibility: hidden;}}
        footer {{visibility: hidden;}}
        
        /* Custom input styling dengan pink accents */
        .stSelectbox label, .stNumberInput label {{
            font-weight: 600;
            color: #be185d;
        }}
        
        .stSelectbox > div > div > select {{
            border: 2px solid #f8a2c2;
            border-radius: 10px;
        }}
        
        .stSelectbox > div > div > select:focus {{
            border-color: #ec4899;
            box-shadow: 0 0 0 2px rgba(236, 72, 153, 0.2);
        }}
        
        .stNumberInput > div > div > input {{
            border: 2px solid #f8a2c2;
            border-radius: 10px;
        }}
        
        .stNumberInput > div > div > input:focus {{
            border-color: #ec4899;
            box-shadow: 0 0 0 2px rgba(236, 72, 153, 0.2);
        }}
        
        /* Radio button styling */
        .stRadio > label {{
            color: #be185d;
            font-weight: 600;
        }}
        
        /* Sidebar styling */
        .css-1d391kg {{
            background: linear-gradient(180deg, #fdf2f8 0%, #fce7f3 100%);
        }}
        
        /* Footer styling */
        .footer-style {{
            background: linear-gradient(135deg, #fce7f3 0%, #fbcfe8 100%);
            color: #831843;
            padding: 1.5rem;
            border-radius: 15px;
            text-align: center;
            margin-top: 2rem;
            border: 1px solid rgba(251, 207, 232, 0.5);
        }}
        
        /* Responsive design */
        @media (max-width: 768px) {{
            .header-title {{
                font-size: 2rem;
            }}
            
            .header-subtitle {{
                font-size: 1rem;
            }}
            
            .info-card, .metric-card {{
                padding: 1.5rem;
            }}
        }}
    </style>
    """

# Apply CSS
st.markdown(get_css(), unsafe_allow_html=True)

# Memuat model dengan penanganan error
@st.cache_resource
def load_model():
    try:
        return joblib.load("model_pcos.pkl")
    except FileNotFoundError:
        st.error("⚠️ File model 'model_pcos.pkl' tidak ditemukan. Pastikan file berada di direktori yang benar.")
        return None

model = load_model()

# Header
st.markdown("""
<div class="header-container">
    <div class="header-title">🌸 Prediksi Risiko PCOS</div>
    <div class="header-subtitle">Penilaian Risiko PCOS untuk Kesehatan Wanita</div>
</div>
""", unsafe_allow_html=True)

# Konten utama
col1, col2 = st.columns([2, 1])

with col1:
    # Bagian informasi
    st.markdown("""
    <div class="info-card">
        <h3>💖 Tentang Prediksi PCOS</h3>
        <p>Sistem prediksi ini dirancang khusus untuk wanita, untuk menilai risiko Anda terkena Polycystic Ovary Syndrome (PCOS). PCOS adalah kondisi hormonal yang umum terjadi pada wanita usia reproduksi. Silakan isi informasi di bawah ini dengan akurat untuk prediksi yang paling dapat diandalkan.</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Bagian input
    st.markdown('<div class="section-header">👩‍⚕️ Informasi Pribadi</div>', unsafe_allow_html=True)
    
    col_age, col_weight = st.columns(2)
    with col_age:
        age = st.number_input("Usia (tahun)", min_value=10, max_value=60, step=1, value=25)
    with col_weight:
        weight = st.number_input("Berat Badan (kg)", min_value=30.0, max_value=150.0, step=0.1, value=60.0)
    
    col_height, col_bmi = st.columns(2)
    with col_height:
        height = st.number_input("Tinggi Badan (cm)", min_value=120.0, max_value=200.0, step=0.1, value=160.0)
    with col_bmi:
        bmi = st.number_input("Indeks Massa Tubuh (BMI)", min_value=10.0, max_value=60.0, step=0.1, value=23.4)
    
    st.markdown('<div class="section-header">🌺 Kesehatan Menstruasi</div>', unsafe_allow_html=True)
    
    col_cycle, col_length = st.columns(2)
    with col_cycle:
        cycle = st.selectbox("Siklus Menstruasi", ["Teratur", "Tidak Teratur"], index=0)
    with col_length:
        cycle_length = st.number_input("Panjang Siklus (hari)", min_value=0, max_value=50, step=1, value=28)
    
    st.markdown('<div class="section-header">📏 Ukuran Tubuh</div>', unsafe_allow_html=True)
    
    col_hip, col_waist = st.columns(2)
    with col_hip:
        hip = st.number_input("Lingkar Pinggul (inci)", min_value=20.0, max_value=60.0, step=0.1, value=36.0)
    with col_waist:
        waist = st.number_input("Lingkar Pinggang (inci)", min_value=20.0, max_value=60.0, step=0.1, value=28.0)
    
    waist_hip_ratio = st.number_input("Rasio Pinggang-Pinggul", min_value=0.5, max_value=1.5, step=0.01, value=0.78)
    
    st.markdown('<div class="section-header">✨ Evaluasi Gejala PCOS</div>', unsafe_allow_html=True)
    
    col_sym1, col_sym2 = st.columns(2)
    with col_sym1:
        weight_gain = st.selectbox("Apakah mengalami kenaikan berat badan?", ["Tidak", "Ya"], index=0)
        hair_growth = st.selectbox("Apakah mengalami pertumbuhan rambut berlebih (hirsutisme)?", ["Tidak", "Ya"], index=0)
        skin_darkening = st.selectbox("Apakah mengalami penggelapan kulit (acanthosis nigricans)?", ["Tidak", "Ya"], index=0)
    
    with col_sym2:
        hair_loss = st.selectbox("Apakah mengalami kerontokan rambut?", ["Tidak", "Ya"], index=0)
        pimples = st.selectbox("Apakah mengalami masalah jerawat?", ["Tidak", "Ya"], index=0)

with col2:
    st.markdown("""
    <div class="info-card">
        <h3>📝 Tanda-Tanda Umum PCOS</h3>
        <ul>
            <li><strong>Haid tidak teratur:</strong> PCOS menyebabkan ovulasi terganggu yang berakibat pada siklus menstruasi yang tidak menentu.</li>
            <li><strong>Hirsutisme:</strong> Pertumbuhan rambut berlebih akibat peningkatan hormon androgen. Rambut bisa tumbuh di wajah, dada, punggung, perut, dan paha.</li>
            <li><strong>Jerawat & wajah berminyak:</strong> Produksi sebum berlebih akibat hormon androgen menyebabkan jerawat di wajah, punggung, dan tubuh.</li>
            <li><strong>Obesitas:</strong> Penumpukan lemak, khususnya di area perut, umum terjadi pada penderita PCOS.</li>
            <li><strong>Penggelapan kulit:</strong> Acanthosis Nigricans, yaitu kulit menggelap di area lipatan seperti leher, ketiak, atau selangkangan.</li>
        </ul>
        <p><em>Jika Anda mengalami beberapa gejala di atas, sistem ini dapat membantu memberikan penilaian awal terhadap risiko PCOS.</em></p>
    </div>
    """, unsafe_allow_html=True)

# Bagian prediksi
st.markdown('<div class="section-header">🔮 Analisis Risiko PCOS</div>', unsafe_allow_html=True)

# Fungsi helper
def ya_tidak_to_num(val): 
    return 1 if val == "Ya" else 0

def cycle_to_num(val): 
    return 1 if val == "Tidak Teratur" else 0

# Menyiapkan data input
input_data = [
    age,
    weight,
    height,
    bmi,
    cycle_to_num(cycle),
    cycle_length,
    hip,
    waist,
    ya_tidak_to_num(weight_gain),
    ya_tidak_to_num(hair_growth),
    ya_tidak_to_num(skin_darkening),
    ya_tidak_to_num(hair_loss),
    ya_tidak_to_num(pimples),
    waist_hip_ratio
]

# Tombol prediksi dan hasil
col_predict, col_info = st.columns([1, 1])

with col_predict:
    if st.button("💖 Analisis Risiko PCOS Saya", key="predict_button"):
        if model is not None:
            try:
                data_np = np.array([input_data])
                prediction = model.predict(data_np)[0]
                
                if prediction == 1:
                    st.markdown("""
                    <div class="result-positive">
                        <h3>⚠️ Anda memiliki risiko PCOS</h3>
                        <p>Kami sangat merekomendasikan untuk segera berkonsultasi dengan dokter spesialis kandungan atau endokrinologi untuk pemeriksaan lebih lanjut dan penanganan yang tepat.</p>
                        <p><strong>Ingat: Deteksi dini adalah kunci untuk penanganan yang efektif! 💪</strong></p>
                    </div>
                    """, unsafe_allow_html=True)
                else:
                    st.markdown("""
                    <div class="result-negative">
                        <h3>✨ Anda tidak memiliki risiko PCOS</h3>
                        <p>Ini adalah kabar baik! Terus jaga gaya hidup sehat dengan pola makan bergizi, olahraga teratur, dan kelola stres dengan baik.</p>
                        <p><strong>Tetap lakukan pemeriksaan kesehatan rutin! 🌸</strong></p>
                    </div>
                    """, unsafe_allow_html=True)
                    
            except Exception as e:
                st.error(f"Terjadi kesalahan saat melakukan analisis: {str(e)}")
        else:
            st.error("Model tidak berhasil dimuat. Tidak dapat melakukan prediksi.")

with col_info:
    st.markdown("""
    <div class="info-card">
        <h4>📋 Catatan Penting untuk Kesehatan Anda</h4>
        <ul>
            <li><strong>Bukan diagnosis medis:</strong> Ini adalah alat skrining awal</li>
            <li><strong>Konsultasi dokter:</strong> Selalu diskusikan dengan profesional kesehatan</li>
            <li><strong>Akurasi data:</strong> Hasil bergantung pada informasi yang Anda berikan</li>
            <li><strong>Pemeriksaan rutin:</strong> Lakukan check-up kesehatan berkala</li>
            <li><strong>Gaya hidup sehat:</strong> Kunci utama pencegahan dan pengelolaan PCOS</li>
        </ul>
    </div>
    """, unsafe_allow_html=True)

# Footer
st.markdown("---")
st.markdown(f"""
<div class="footer-style">
    <p><strong>🌸 Prediksi Risiko PCOS untuk Wanita</strong></p>
    <p>Didukung oleh teknologi Machine Learning | Selalu konsultasi dengan profesional kesehatan</p>
    <p><em>Kesehatan Anda adalah prioritas utama. Jaga diri Anda dengan baik! 💖</em></p>
    <p>Terakhir diperbarui: {datetime.now().strftime("%B %Y")}</p>
</div>
""", unsafe_allow_html=True)