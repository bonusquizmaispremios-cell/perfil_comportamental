import streamlit as st
from groq import Groq
from datetime import datetime
import json

st.set_page_config(page_title="Perfil Comportamental IA", page_icon="🧠", layout="wide")

st.markdown("""
    <style>

    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap');
    .stApp { background-color:#F5F3FF; font-family:'Inter',sans-serif; }
    [data-testid="stSidebar"] { display:none; }
    .stTextInput>div>div>input, .stTextArea>div>textarea,
    .stSelectbox>div>div>div, .stNumberInput>div>div>input {
        background-color:#FFFFFF !important; color:#1A1A2E !important;
        border:1px solid #CED4DA !important; font-family:'Inter',sans-serif !important;
    }
    .stButton>button {
        width:100%; border-radius:10px; height:3.2em;
        background:linear-gradient(135deg,#6D28D9,#5B21B6) !important; color:white !important;
        font-weight:600; border:none; box-shadow:2px 2px 8px rgba(0,0,0,0.1);
        font-family:'Inter',sans-serif !important; transition:all 0.2s ease;
    }
    .stButton>button:hover { background:linear-gradient(135deg,#5B21B6,#6D28D9) !important; transform:translateY(-1px); }
    .stApp .stButton>button, .stApp .stButton>button p,
    .stApp .stButton>button span, .stApp .stButton>button div { color:white !important; }
    .stApp h1, .stApp h2, .stApp h3 { color:#3B0764 !important; font-family:'Inter',sans-serif !important; font-weight:700 !important; }
    .card { background:linear-gradient(135deg,#F5F3FF,#EDE9FE); padding:20px; border-radius:14px; border:1px solid #C4B5FD; margin-bottom:14px; white-space:normal; word-wrap:break-word; }
    .stApp .card, .stApp .card p, .stApp .card span, .stApp .card div, .stApp .card strong { color:#3B0764 !important; }
    .card-blue { background:linear-gradient(135deg,#EFF6FF,#DBEAFE); padding:20px; border-radius:14px; border:1px solid #93C5FD; margin-bottom:14px; }
    .stApp .card-blue, .stApp .card-blue p, .stApp .card-blue div { color:#1E3A8A !important; }
    .card-red { background:linear-gradient(135deg,#FFF5F5,#FEE2E2); padding:20px; border-radius:14px; border:1px solid #FECACA; margin-bottom:14px; }
    .stApp .card-red, .stApp .card-red p, .stApp .card-red div { color:#7F1D1D !important; }
    .card-green { background:linear-gradient(135deg,#F0FDF4,#DCFCE7); padding:20px; border-radius:14px; border:1px solid #86EFAC; margin-bottom:14px; }
    .stApp .card-green, .stApp .card-green p, .stApp .card-green div { color:#14532D !important; }
    .card-yellow { background:linear-gradient(135deg,#FFFBEB,#FEF3C7); padding:18px; border-radius:12px; border:1px solid #FCD34D; margin-bottom:12px; }
    .stApp .card-yellow, .stApp .card-yellow p, .stApp .card-yellow div { color:#78350F !important; }
    .badge { background:#6D28D9; color:white !important; padding:4px 12px; border-radius:20px; font-size:0.78em; font-weight:600; display:inline-block; margin:2px; }
    .badge-verde { background:#059669; color:white !important; padding:4px 12px; border-radius:20px; font-size:0.78em; font-weight:600; display:inline-block; margin:2px; }
    .badge-amarelo { background:#B45309; color:white !important; padding:4px 12px; border-radius:20px; font-size:0.78em; font-weight:600; display:inline-block; margin:2px; }
    .badge-roxo { background:#6D28D9; color:white !important; padding:4px 12px; border-radius:20px; font-size:0.78em; font-weight:600; display:inline-block; margin:2px; }
    .divider { border:none; height:1px; background:linear-gradient(to right,transparent,#C4B5FD,transparent); margin:18px 0; }
    .hist-item { background:#FFFFFF; border-radius:10px; padding:12px 16px; margin-bottom:8px; border-left:4px solid #C4B5FD; }
    .stApp .hist-item, .stApp .hist-item p, .stApp .hist-item span, .stApp .hist-item div { color:#3B0764 !important; }
    .stat-box { background:#FFFFFF; border-radius:12px; padding:16px; text-align:center; border:1px solid #C4B5FD; }
    .stApp .stat-box div, .stApp .stat-box span { color:#3B0764 !important; }
    .chat-user { background:#FFFFFF; border:1px solid #C4B5FD; border-radius:12px 12px 4px 12px; padding:12px 16px; margin:8px 0; }
    .stApp .chat-user, .stApp .chat-user p, .stApp .chat-user div { color:#3B0764 !important; }
    .chat-persona { background:#EDE9FE; border:1px solid #C4B5FD; border-radius:4px 12px 12px 12px; padding:12px 16px; margin:8px 0; }
    .stApp .chat-persona, .stApp .chat-persona p, .stApp .chat-persona div { color:#3B0764 !important; }

    </style>
""", unsafe_allow_html=True)

SYSTEM_PROMPT = "Você é um especialista em psicologia comportamental e desenvolvimento humano. Analisa perfis DISC, Enneagrama e Myers-Briggs de forma precisa e prática. Sempre usa linguagem acessível, exemplos concretos e foco em aplicação prática. Português do Brasil."

@st.cache_resource
def get_cache_perfil_comp():
    return {"perfis": {}}

_cache = get_cache_perfil_comp()

CHAVES_SALVAR = ["usuario","historico_perfil_comportamental"]

def gerar_json():
    return json.dumps({k: st.session_state.get(k) for k in CHAVES_SALVAR}, ensure_ascii=False, indent=2, default=str)

def carregar_json_sessao(dados):
    for k,v in dados.items():
        if k in CHAVES_SALVAR:
            st.session_state[k] = v

def salvar_perfil_cache(usuario):
    _cache["perfis"][usuario] = {k: st.session_state.get(k) for k in CHAVES_SALVAR}

def perfis_salvos():
    return [p for p in _cache["perfis"].keys() if len(p.strip()) >= 2]

def carregar_perfil_cache(usuario):
    return _cache["perfis"].get(usuario)

defaults = {
    "etapa": "Login", "usuario": "", "api_key": "",
    "historico_perfil_comportamental": [],
}
for k,v in defaults.items():
    if k not in st.session_state:
        st.session_state[k] = v

# ── LOGIN ──
if st.session_state.etapa == "Login":
    st.markdown("# 🧠 Perfil Comportamental IA")
    st.markdown("<div class=\'card\'><b>🔒 ACESSO RESTRITO A CLIENTES DO QUIZ COM PRÊMIOS</b><br>🔗 quizcompremios.com.br</div>", unsafe_allow_html=True)
    st.info("💻 **Dica:** Pela complexidade dos agentes, no computador a experiência é mais agradável.")
    with st.container():
        nome  = st.text_input("Seu Nome:", key="nome_login")
        chave = st.text_input("🔑 Sua Chave API da Groq:", type="password", key="chave_login")
        arq_j = st.file_uploader("📂 Carregar dados salvos (.json):", type=["json"], key="upload_login")
        dados_login = json.load(arq_j) if arq_j else None
        if st.button("✨ ENTRAR", key="btn_entrar_login"):
            if len(nome.strip()) < 2:
                st.warning("Digite um nome com pelo menos 2 caracteres.")
            elif chave.strip():
                st.session_state.usuario = nome.strip()
                st.session_state.api_key = chave
                if dados_login: carregar_json_sessao(dados_login)
                st.session_state.etapa = "App"
                st.rerun()
            else:
                st.warning("Preencha nome e chave API.")

elif st.session_state.etapa == "App":
    historico = st.session_state.get("historico_perfil_comportamental", [])
    salvar_perfil_cache(st.session_state.usuario)

    _tab_home_pc, _tab_disc, _tab_ennea, _tab_mbti, _tab_carreiras, _tab_comunicar, _tab_relatorio, _tab_pontos, _tab_pontos_cegos, _tab_diario_pc, _tab_biblioteca_pc = st.tabs(['🏠 Home', '🎯 Meu Perfil DISC', '🔮 Enneagrama', '🧩 Myers-Briggs', '💼 Carreiras Ideais', '🤝 Como Me Comunicar', '📊 Relatório Completo', '🏆 Pontos Fortes', '⚠️ Pontos Cegos', '📓 Diário', '📚 Biblioteca'])

    with _tab_home_pc:
        st.title(f"🧠 Olá, {st.session_state.usuario}!")
        st.markdown(f"*Descubra quem você realmente é — e como usar isso a seu favor.*")
        st.markdown("<hr class='divider'>", unsafe_allow_html=True)
        st.markdown(f"### Bem-vindo ao **Perfil Comportamental IA**")
        st.markdown(f"<div class='card'>Use as abas acima para navegar entre as funcionalidades. Cada aba oferece uma ferramenta diferente com IA.</div>", unsafe_allow_html=True)
        col1, col2, col3 = st.columns(3)
        with col1: st.markdown(f"<div class='stat-box'><div style='font-size:1.8em;'>🏠</div><div style='font-size:0.8em;'>Perfil Comportamental IA</div></div>", unsafe_allow_html=True)
        with col2: st.markdown(f"<div class='stat-box'><div style='font-size:1.8em;'>🤖</div><div style='font-size:0.8em;'>Powered by IA</div></div>", unsafe_allow_html=True)
        with col3: st.markdown(f"<div class='stat-box'><div style='font-size:1.8em;'>💾</div><div style='font-size:0.8em;'>Salve seus dados</div></div>", unsafe_allow_html=True)
        st.markdown("<hr class='divider'>", unsafe_allow_html=True)
        col_sv, _ = st.columns([1,3])
        with col_sv:
            st.download_button("💾 Salvar dados (.json)", data=json.dumps({k:st.session_state.get(k) for k in CHAVES_SALVAR}, ensure_ascii=False, indent=2, default=str), file_name=f"perfil_comportamental_{st.session_state.usuario}.json", mime="application/json", key="dl_perfil_1")

    with _tab_disc:
        st.header("🎯 Meu Perfil DISC", key="dl_perfil_2")
        prompt_disc = st.text_area("Descreva sua situação ou dúvida:", height=120, key="prompt_disc", placeholder="Digite aqui...")
        if st.button("🤖 GERAR COM IA", key="btn_disc", use_container_width=True):
            if prompt_disc.strip():
                with st.spinner("A IA está analisando..."):
                    try:
                        client = Groq(api_key=st.session_state.api_key)
                        msgs = [{"role":"system","content":SYSTEM_PROMPT},{"role":"user","content":prompt_disc}]
                        resp = client.chat.completions.create(messages=msgs, model="openai/gpt-oss-120b", max_tokens=2048)
                        resultado_disc = resp.choices[0].message.content
                        st.session_state["res_disc"] = resultado_disc
                        historico.append({"data":datetime.now().strftime("%d/%m %H:%M"),"aba":"Meu Perfil DISC","resumo":prompt_disc[:60],"conteudo":resultado_disc})
                        st.session_state.historico_perfil_comportamental = historico
                    except Exception as e:
                        st.error(f"Erro na API: {e}")
            else:
                st.warning("Digite sua situação antes de gerar.")
        if st.session_state.get("res_disc"):
            st.markdown(f"<div class='card'>{st.session_state['res_disc']}</div>", unsafe_allow_html=True)
            st.download_button("📋 Baixar resultado", data=st.session_state["res_disc"], file_name="disc_resultado.txt", mime="text/plain", key="dl_disc")

    with _tab_ennea:
        st.header("🔮 Enneagrama")
        prompt_ennea = st.text_area("Descreva sua situação ou dúvida:", height=120, key="prompt_ennea", placeholder="Digite aqui...")
        if st.button("🤖 GERAR COM IA", key="btn_ennea", use_container_width=True):
            if prompt_ennea.strip():
                with st.spinner("A IA está analisando..."):
                    try:
                        client = Groq(api_key=st.session_state.api_key)
                        msgs = [{"role":"system","content":SYSTEM_PROMPT},{"role":"user","content":prompt_ennea}]
                        resp = client.chat.completions.create(messages=msgs, model="openai/gpt-oss-120b", max_tokens=2048)
                        resultado_ennea = resp.choices[0].message.content
                        st.session_state["res_ennea"] = resultado_ennea
                        historico.append({"data":datetime.now().strftime("%d/%m %H:%M"),"aba":"Enneagrama","resumo":prompt_ennea[:60],"conteudo":resultado_ennea})
                        st.session_state.historico_perfil_comportamental = historico
                    except Exception as e:
                        st.error(f"Erro na API: {e}")
            else:
                st.warning("Digite sua situação antes de gerar.")
        if st.session_state.get("res_ennea"):
            st.markdown(f"<div class='card'>{st.session_state['res_ennea']}</div>", unsafe_allow_html=True)
            st.download_button("📋 Baixar resultado", data=st.session_state["res_ennea"], file_name="ennea_resultado.txt", mime="text/plain", key="dl_ennea")

    with _tab_mbti:
        st.header("🧩 Myers-Briggs")
        prompt_mbti = st.text_area("Descreva sua situação ou dúvida:", height=120, key="prompt_mbti", placeholder="Digite aqui...")
        if st.button("🤖 GERAR COM IA", key="btn_mbti", use_container_width=True):
            if prompt_mbti.strip():
                with st.spinner("A IA está analisando..."):
                    try:
                        client = Groq(api_key=st.session_state.api_key)
                        msgs = [{"role":"system","content":SYSTEM_PROMPT},{"role":"user","content":prompt_mbti}]
                        resp = client.chat.completions.create(messages=msgs, model="openai/gpt-oss-120b", max_tokens=2048)
                        resultado_mbti = resp.choices[0].message.content
                        st.session_state["res_mbti"] = resultado_mbti
                        historico.append({"data":datetime.now().strftime("%d/%m %H:%M"),"aba":"Myers-Briggs","resumo":prompt_mbti[:60],"conteudo":resultado_mbti})
                        st.session_state.historico_perfil_comportamental = historico
                    except Exception as e:
                        st.error(f"Erro na API: {e}")
            else:
                st.warning("Digite sua situação antes de gerar.")
        if st.session_state.get("res_mbti"):
            st.markdown(f"<div class='card'>{st.session_state['res_mbti']}</div>", unsafe_allow_html=True)
            st.download_button("📋 Baixar resultado", data=st.session_state["res_mbti"], file_name="mbti_resultado.txt", mime="text/plain", key="dl_mbti")

    with _tab_carreiras:
        st.header("💼 Carreiras Ideais")
        prompt_carreiras = st.text_area("Descreva sua situação ou dúvida:", height=120, key="prompt_carreiras", placeholder="Digite aqui...")
        if st.button("🤖 GERAR COM IA", key="btn_carreiras", use_container_width=True):
            if prompt_carreiras.strip():
                with st.spinner("A IA está analisando..."):
                    try:
                        client = Groq(api_key=st.session_state.api_key)
                        msgs = [{"role":"system","content":SYSTEM_PROMPT},{"role":"user","content":prompt_carreiras}]
                        resp = client.chat.completions.create(messages=msgs, model="openai/gpt-oss-120b", max_tokens=2048)
                        resultado_carreiras = resp.choices[0].message.content
                        st.session_state["res_carreiras"] = resultado_carreiras
                        historico.append({"data":datetime.now().strftime("%d/%m %H:%M"),"aba":"Carreiras Ideais","resumo":prompt_carreiras[:60],"conteudo":resultado_carreiras})
                        st.session_state.historico_perfil_comportamental = historico
                    except Exception as e:
                        st.error(f"Erro na API: {e}")
            else:
                st.warning("Digite sua situação antes de gerar.")
        if st.session_state.get("res_carreiras"):
            st.markdown(f"<div class='card'>{st.session_state['res_carreiras']}</div>", unsafe_allow_html=True)
            st.download_button("📋 Baixar resultado", data=st.session_state["res_carreiras"], file_name="carreiras_resultado.txt", mime="text/plain", key="dl_carreiras")

    with _tab_comunicar:
        st.header("🤝 Como Me Comunicar")
        prompt_comunicar = st.text_area("Descreva sua situação ou dúvida:", height=120, key="prompt_comunicar", placeholder="Digite aqui...")
        if st.button("🤖 GERAR COM IA", key="btn_comunicar", use_container_width=True):
            if prompt_comunicar.strip():
                with st.spinner("A IA está analisando..."):
                    try:
                        client = Groq(api_key=st.session_state.api_key)
                        msgs = [{"role":"system","content":SYSTEM_PROMPT},{"role":"user","content":prompt_comunicar}]
                        resp = client.chat.completions.create(messages=msgs, model="openai/gpt-oss-120b", max_tokens=2048)
                        resultado_comunicar = resp.choices[0].message.content
                        st.session_state["res_comunicar"] = resultado_comunicar
                        historico.append({"data":datetime.now().strftime("%d/%m %H:%M"),"aba":"Como Me Comunicar","resumo":prompt_comunicar[:60],"conteudo":resultado_comunicar})
                        st.session_state.historico_perfil_comportamental = historico
                    except Exception as e:
                        st.error(f"Erro na API: {e}")
            else:
                st.warning("Digite sua situação antes de gerar.")
        if st.session_state.get("res_comunicar"):
            st.markdown(f"<div class='card'>{st.session_state['res_comunicar']}</div>", unsafe_allow_html=True)
            st.download_button("📋 Baixar resultado", data=st.session_state["res_comunicar"], file_name="comunicar_resultado.txt", mime="text/plain", key="dl_comunicar")

    with _tab_relatorio:
        st.header("📊 Relatório Completo")
        prompt_relatorio = st.text_area("Descreva sua situação ou dúvida:", height=120, key="prompt_relatorio", placeholder="Digite aqui...")
        if st.button("🤖 GERAR COM IA", key="btn_relatorio", use_container_width=True):
            if prompt_relatorio.strip():
                with st.spinner("A IA está analisando..."):
                    try:
                        client = Groq(api_key=st.session_state.api_key)
                        msgs = [{"role":"system","content":SYSTEM_PROMPT},{"role":"user","content":prompt_relatorio}]
                        resp = client.chat.completions.create(messages=msgs, model="openai/gpt-oss-120b", max_tokens=2048)
                        resultado_relatorio = resp.choices[0].message.content
                        st.session_state["res_relatorio"] = resultado_relatorio
                        historico.append({"data":datetime.now().strftime("%d/%m %H:%M"),"aba":"Relatório Completo","resumo":prompt_relatorio[:60],"conteudo":resultado_relatorio})
                        st.session_state.historico_perfil_comportamental = historico
                    except Exception as e:
                        st.error(f"Erro na API: {e}")
            else:
                st.warning("Digite sua situação antes de gerar.")
        if st.session_state.get("res_relatorio"):
            st.markdown(f"<div class='card'>{st.session_state['res_relatorio']}</div>", unsafe_allow_html=True)
            st.download_button("📋 Baixar resultado", data=st.session_state["res_relatorio"], file_name="relatorio_resultado.txt", mime="text/plain", key="dl_relatorio")

    with _tab_pontos:
        st.header("🏆 Pontos Fortes")
        prompt_pontos = st.text_area("Descreva sua situação ou dúvida:", height=120, key="prompt_pontos", placeholder="Digite aqui...")
        if st.button("🤖 GERAR COM IA", key="btn_pontos", use_container_width=True):
            if prompt_pontos.strip():
                with st.spinner("A IA está analisando..."):
                    try:
                        client = Groq(api_key=st.session_state.api_key)
                        msgs = [{"role":"system","content":SYSTEM_PROMPT},{"role":"user","content":prompt_pontos}]
                        resp = client.chat.completions.create(messages=msgs, model="openai/gpt-oss-120b", max_tokens=2048)
                        resultado_pontos = resp.choices[0].message.content
                        st.session_state["res_pontos"] = resultado_pontos
                        historico.append({"data":datetime.now().strftime("%d/%m %H:%M"),"aba":"Pontos Fortes","resumo":prompt_pontos[:60],"conteudo":resultado_pontos})
                        st.session_state.historico_perfil_comportamental = historico
                    except Exception as e:
                        st.error(f"Erro na API: {e}")
            else:
                st.warning("Digite sua situação antes de gerar.")
        if st.session_state.get("res_pontos"):
            st.markdown(f"<div class='card'>{st.session_state['res_pontos']}</div>", unsafe_allow_html=True)
            st.download_button("📋 Baixar resultado", data=st.session_state["res_pontos"], file_name="pontos_resultado.txt", mime="text/plain", key="dl_pontos")

    with _tab_pontos_cegos:
        st.header("⚠️ Pontos Cegos")
        prompt_pontos_cegos = st.text_area("Descreva sua situação ou dúvida:", height=120, key="prompt_pontos_cegos", placeholder="Digite aqui...")
        if st.button("🤖 GERAR COM IA", key="btn_pontos_cegos", use_container_width=True):
            if prompt_pontos_cegos.strip():
                with st.spinner("A IA está analisando..."):
                    try:
                        client = Groq(api_key=st.session_state.api_key)
                        msgs = [{"role":"system","content":SYSTEM_PROMPT},{"role":"user","content":prompt_pontos_cegos}]
                        resp = client.chat.completions.create(messages=msgs, model="openai/gpt-oss-120b", max_tokens=2048)
                        resultado_pontos_cegos = resp.choices[0].message.content
                        st.session_state["res_pontos_cegos"] = resultado_pontos_cegos
                        historico.append({"data":datetime.now().strftime("%d/%m %H:%M"),"aba":"Pontos Cegos","resumo":prompt_pontos_cegos[:60],"conteudo":resultado_pontos_cegos})
                        st.session_state.historico_perfil_comportamental = historico
                    except Exception as e:
                        st.error(f"Erro na API: {e}")
            else:
                st.warning("Digite sua situação antes de gerar.")
        if st.session_state.get("res_pontos_cegos"):
            st.markdown(f"<div class='card'>{st.session_state['res_pontos_cegos']}</div>", unsafe_allow_html=True)
            st.download_button("📋 Baixar resultado", data=st.session_state["res_pontos_cegos"], file_name="pontos_cegos_resultado.txt", mime="text/plain", key="dl_pontos_cegos")

    with _tab_diario_pc:
        st.header("📓 Diário")
        prompt_diario_pc = st.text_area("Descreva sua situação ou dúvida:", height=120, key="prompt_diario_pc", placeholder="Digite aqui...")
        if st.button("🤖 GERAR COM IA", key="btn_diario_pc", use_container_width=True):
            if prompt_diario_pc.strip():
                with st.spinner("A IA está analisando..."):
                    try:
                        client = Groq(api_key=st.session_state.api_key)
                        msgs = [{"role":"system","content":SYSTEM_PROMPT},{"role":"user","content":prompt_diario_pc}]
                        resp = client.chat.completions.create(messages=msgs, model="openai/gpt-oss-120b", max_tokens=2048)
                        resultado_diario_pc = resp.choices[0].message.content
                        st.session_state["res_diario_pc"] = resultado_diario_pc
                        historico.append({"data":datetime.now().strftime("%d/%m %H:%M"),"aba":"Diário","resumo":prompt_diario_pc[:60],"conteudo":resultado_diario_pc})
                        st.session_state.historico_perfil_comportamental = historico
                    except Exception as e:
                        st.error(f"Erro na API: {e}")
            else:
                st.warning("Digite sua situação antes de gerar.")
        if st.session_state.get("res_diario_pc"):
            st.markdown(f"<div class='card'>{st.session_state['res_diario_pc']}</div>", unsafe_allow_html=True)
            st.download_button("📋 Baixar resultado", data=st.session_state["res_diario_pc"], file_name="diario_pc_resultado.txt", mime="text/plain", key="dl_diario_pc")

    with _tab_biblioteca_pc:
        st.header("📚 Biblioteca")
        prompt_biblioteca_pc = st.text_area("Descreva sua situação ou dúvida:", height=120, key="prompt_biblioteca_pc", placeholder="Digite aqui...")
        if st.button("🤖 GERAR COM IA", key="btn_biblioteca_pc", use_container_width=True):
            if prompt_biblioteca_pc.strip():
                with st.spinner("A IA está analisando..."):
                    try:
                        client = Groq(api_key=st.session_state.api_key)
                        msgs = [{"role":"system","content":SYSTEM_PROMPT},{"role":"user","content":prompt_biblioteca_pc}]
                        resp = client.chat.completions.create(messages=msgs, model="openai/gpt-oss-120b", max_tokens=2048)
                        resultado_biblioteca_pc = resp.choices[0].message.content
                        st.session_state["res_biblioteca_pc"] = resultado_biblioteca_pc
                        historico.append({"data":datetime.now().strftime("%d/%m %H:%M"),"aba":"Biblioteca","resumo":prompt_biblioteca_pc[:60],"conteudo":resultado_biblioteca_pc})
                        st.session_state.historico_perfil_comportamental = historico
                    except Exception as e:
                        st.error(f"Erro na API: {e}")
            else:
                st.warning("Digite sua situação antes de gerar.")
        if st.session_state.get("res_biblioteca_pc"):
            st.markdown(f"<div class='card'>{st.session_state['res_biblioteca_pc']}</div>", unsafe_allow_html=True)
            st.download_button("📋 Baixar resultado", data=st.session_state["res_biblioteca_pc"], file_name="biblioteca_pc_resultado.txt", mime="text/plain", key="dl_biblioteca_pc")


# --- RODAPÉ ---
st.markdown("<hr class='divider'>", unsafe_allow_html=True)
st.markdown(f"<div style='text-align:center;font-size:0.75em;color:#94A3B8;'>© 2026 Perfil Comportamental IA · Quiz Com Prêmios</div>", unsafe_allow_html=True)
