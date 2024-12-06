import streamlit as st
import hashlib
import base64
import os
from dotenv import load_dotenv

load_dotenv()

# Configuração da página
st.set_page_config(page_title="Text Encrypter", page_icon="🔒", layout="centered")

# Estilo CSS personalizado
st.markdown(
    """
    <style>
    .main {
        padding: 2rem;
    }
    .stTitle {
        color: #2E4053;
        font-size: 42px;
        text-align: center;
    }
    .stButton>button {
        background-color: #2E4053;
        color: white;
        width: 100%;
    }
    </style>
""",
    unsafe_allow_html=True,
)

# Dicionário de substituição (mantido o mesmo)
checar_alfa = {
    "a": "ᴀ",
    "b": "ʙ",
    "c": "ᴄ",
    "d": "ᴅ",
    "e": "ᴇ",
    "f": "ꜰ",
    "g": "ɢ",
    "h": "ʜ",
    "i": "ɪ",
    "j": "ᴊ",
    "k": "ᴋ",
    "l": "ʟ",
    "m": "ᴍ",
    "n": "ɴ",
    "o": "ᴏ",
    "p": "ᴩ",
    "q": "ԛ",
    "r": "ʀ",
    "s": "🇸",
    "t": "ᴛ",
    "u": "ᴜ",
    "v": "ᴠ",
    "w": "ᴡ",
    "x": "🇽",
    "y": "🇾",
    "z": "ᴢ",
}

# Interface do aplicativo
st.title("✨ Text Encrypter ✨")

# Adiciona uma breve descrição
st.markdown("### Transforme seu texto em caracteres especiais")

# Container principal
with st.container():
    # Entrada de texto com placeholder
    texto_input = st.text_area(
        "Digite seu texto aqui:",
        placeholder="Digite algo para encriptar...",
        height=100,
    ).lower()

    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        if st.button("🔒 Encriptar"):
            if texto_input:
                # Transformando o texto
                texto_transformado = texto_input
                for letra, caractere in checar_alfa.items():
                    texto_transformado = texto_transformado.replace(letra, caractere)

                # Exibindo resultado em um box
                st.success("Texto encriptado com sucesso!")
                st.code(texto_transformado, language=None)

                # Botão para copiar
                st.markdown(
                    f"""
                    <div style="text-align: center">
                        <small>Clique no código acima para copiar</small>
                    </div>
                """,
                    unsafe_allow_html=True,
                )
            else:
                st.warning("Por favor, digite algum texto para encriptar!")

# Rodapé
st.markdown("""---""")

def hash_encrypt(text, key=os.getenv("SHACODE_256_KEY")):
    """Encrypts text using SHA-256 hash algorithm with a key"""
    # Combine the text with the key
    text_with_key = text + key
    return hashlib.sha256(text_with_key.encode()).hexdigest()

def decrypt_hash(encrypted_text, original_text, key=""):
    """Verify if the encrypted text matches with original text + key"""
    return hash_encrypt(original_text, key) == encrypted_text

def caesar_cipher(text, shift=3):
    """Encrypts text using Caesar cipher with specified shift"""
    result = ""
    for char in text:
        if char.isalpha():
            ascii_offset = ord('a') if char.islower() else ord('A')
            result += chr((ord(char) - ascii_offset + shift) % 26 + ascii_offset)
        else:
            result += char
    return result

def base64_encode(text):
    """Encrypts text using base64 encoding"""
    return base64.b64encode(text.encode()).decode()

def reverse_text(text):
    """Reverses the input text"""
    return text[::-1]

# Adicionando todas as opções de criptografia
st.markdown("### Métodos de Criptografia")
tab1, tab2, tab3, tab4 = st.tabs(["SHA-256", "Caesar Cipher", "Base64", "Texto Reverso"])

with tab1:
    texto_input_sha_256 = st.text_input("Digite seu texto para encriptar com SHA-256:")
    if st.button("🔑 Encriptar com Hash"):
        if texto_input_sha_256:
            hash_result = hash_encrypt(texto_input_sha_256)
            st.success("Texto encriptado com hash SHA-256!")
            st.code(hash_result, language=None)
            st.markdown(
                """
                <div style="text-align: center">
                    <small>Clique no código acima para copiar</small>
                </div>
                """,
                unsafe_allow_html=True,
            )
        else:
            st.warning("Por favor, digite algum texto para encriptar!")

with tab2:
    texto_caesar = st.text_input("Digite texto para cifra de Caesar:")
    shift = st.slider("Selecione o deslocamento", 1, 25, 3)
    if st.button("🔄 Aplicar Cifra de Caesar"):
        if texto_caesar:
            caesar_result = caesar_cipher(texto_caesar, shift)
            st.success("Texto cifrado!")
            st.code(caesar_result, language=None)

with tab3:
    texto_base64 = st.text_input("Digite texto para codificação Base64:")
    if st.button("📝 Codificar em Base64"):
        if texto_base64:
            base64_result = base64_encode(texto_base64)
            st.success("Texto codificado!")
            st.code(base64_result, language=None)

with tab4:
    texto_reverso = st.text_input("Digite texto para inverter:")
    if st.button("⏪ Inverter Texto"):
        if texto_reverso:
            reverse_result = reverse_text(texto_reverso)
            st.success("Texto invertido!")
            st.code(reverse_result, language=None)
