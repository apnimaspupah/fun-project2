import streamlit as st
import requests 
import json

st.title("🤖 Chatbot Seperti ChatGPT")

def get_ai_rensponse(user_input, chat_history):

    try:
        api_key = "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"
    except KeyError:
        st.error("API key tidak ditemukan. Pastikan Anda telah mengatur API key di secrets.")
        return "Error: API key tidak ditemukan."

    message = chat_history + [{"role": "user", "content": user_input}] 

    try: 
        response = requests.post(
            "https://api.openai.com/v1/chat/completions",
            headers={
                "Content-Type": "application/json",
                "Authorization": f"Bearer {api_key}"
            },
            data=json.dumps({
                "model": "mistralai/mistral-7b-instruct:free",
                "messages": message,
            })
        )

        response.raise_for_status() 
        ai_messages = response.json()["choices"][0]["message"]["content"]

        return ai_messages
    
    except requests.exceptions.RequestException as e:
        st.error(f"Terjadi kesalahan saat menghubungi API: {e}")
        
    
    except Exception as e:
        st.error(f"Terjadi kesalahan: {e}")
       
    return None



## UI Part

if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state["messages"]:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

## Handling User Input

if prompt := st.chat_input("Ketik pesan Anda di sini..."):
    #nambahin pesan user ke chat history
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # Mendapatkan respons dari AI
    with st.chat_message("assistant"):
        with st.spinner("berfikir..."):

            ai_response = get_ai_rensponse(prompt, st.session_state.messages) 
            if ai_response:
                st.markdown(ai_response)
                # Menambahkan respons AI ke chat history

                st.session_state.messages.append({"role": "assistant", "content": ai_response})
            else:
                st.error("Tidak ada respons dari AI. Silakan coba lagi.")
