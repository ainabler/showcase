import streamlit as st
from groq import Groq


st.set_page_config(page_title="Simple LLM", page_icon=":rocket:",layout="wide")

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

    model1= st.selectbox("Model 1",[
                            "llama-3.1-8b-instant",
                            "llama-3.2-11b-vision-preview",
                            "llama-3.2-1b-preview",
                            "llama-3.2-3b-preview",
                            "llama-3.2-90b-vision-preview",
                            "llama-3.3-70b-specdec",
                            "llama-3.3-70b-versatile",
                            "llama-guard-3-8b",
                            "llama3-70b-8192",
                            "llama3-8b-8192",
                            ])
    model2= st.selectbox("Model 2",[
                            "llama-3.1-8b-instant",
                            "llama-3.2-11b-vision-preview",
                            "llama-3.2-1b-preview",
                            "llama-3.2-3b-preview",
                            "llama-3.2-90b-vision-preview",
                            "llama-3.3-70b-specdec",
                            "llama-3.3-70b-versatile",
                            "llama-guard-3-8b",
                            "llama3-70b-8192",
                            "llama3-8b-8192",
                            ])

def llm(tanya,model):
    from groq import Groq  # Pastikan impor dilakukan di bagian atas file

   
    client = Groq(api_key=st.session_state.groq_api)
    completion = client.chat.completions.create(
        model=model,
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

if st.button("Get response"):
    hasil1 = llm(tanya,model1)
    hasil2 = llm(tanya,model2)

    col1, col2 = st.columns(2)
    with col1:
        st.subheader(f"Model: {model1}")
        st.write(hasil1)
    with col2:   
        st.subheader(f"Model: {model2}")
        st.write(hasil2)
    
