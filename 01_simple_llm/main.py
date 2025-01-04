import streamlit as st
from groq import Groq


st.set_page_config(page_title="Simple LLM", page_icon=":rocket:")

if "groq_api" not in st.session_state:
    st.session_state.groq_api = ""

with st.sidebar:
    st.subheader("Simple LLM")
    st.write("Masukan API key yang bisa didapat dari https://groq.dev")
    groq_api = st.text_input("Groq API: ")
    simpan_api = st.button("Simpan API")

    if simpan_api:
        st.session_state.groq_api = groq_api
        st.write("API telah disimpan")

    model = st.selectbox("Pilih Model bahasa Anda",["llama-3.3-70b-versatile","llama-3.1-8b-instant"])

def llm(tanya):
    from groq import Groq  # Pastikan impor dilakukan di bagian atas file

    client = Groq(api_key=st.session_state.groq_api)
    completion = client.chat.completions.create(
        model="llama-3.1-8b-instant",
        messages=[
            {
                "role": "user",
                "content": tanya,
            },
        ],
        temperature=1,
        max_tokens=1024,
        top_p=1,
        stream=True,
        stop=None,
    )

    # Mengumpulkan hasil dari setiap chunk
    response = ""
    for chunk in completion:
        content = chunk.choices[0].delta.content or ""
        response += content

    return response


tanya = st.text_area("Apa yang ingin Anda tanyakan?")

if st.button("Kirim"):
    hasil = llm(tanya)
    st.write(hasil)
