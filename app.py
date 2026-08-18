import streamlit as st
import requests

st.set_page_config(page_title="Agregador de Mídias", layout="wide")
st.title("🎥 Agregador de Mídias Gratuitas")

# Menu Lateral para as chaves
st.sidebar.header("Configurações de API")
pexels_key = st.sidebar.text_input("Pexels API Key", type="password")
pixabay_key = st.sidebar.text_input("Pixabay API Key", type="password")

query = st.text_input("Digite a palavra-chave em inglês (ex: car, nature, dog):", "")
media_type = st.radio("Tipo de Mídia:", ["Fotos", "Vídeos"], horizontal=True)

# Busca Pexels
def search_pexels(query, api_key, media_type):
    headers = {"Authorization": api_key}
    if media_type == "Fotos":
        url = f"https://api.pexels.com/v1/search?query={query}&per_page=6"
        res = requests.get(url, headers=headers)
        if res.status_code == 200:
            return [{'url': item['src']['medium'], 'download': item['src']['original']} for item in res.json().get('photos', [])]
    else:
        url = f"https://api.pexels.com/videos/search?query={query}&per_page=6"
        res = requests.get(url, headers=headers)
        if res.status_code == 200:
            return [{'url': item['video_files'][0]['link'], 'download': item['video_files'][0]['link']} for item in res.json().get('videos', [])]
    return []

# Busca Pixabay
def search_pixabay(query, api_key, media_type):
    if media_type == "Fotos":
        url = f"https://pixabay.com/api/?key={api_key}&q={query}&per_page=6&image_type=photo"
        res = requests.get(url)
        if res.status_code == 200:
            return [{'url': item['webformatURL'], 'download': item['largeImageURL']} for item in res.json().get('hits', [])]
    else:
        url = f"https://pixabay.com/api/videos/?key={api_key}&q={query}&per_page=6"
        res = requests.get(url)
        if res.status_code == 200:
            return [{'url': item['videos']['medium']['url'], 'download': item['videos']['medium']['url']} for item in res.json().get('hits', [])]
    return []

# Execução da busca
if st.button("Buscar"):
    if not query:
        st.warning("Digite um termo para busca.")
    elif not pexels_key and not pixabay_key:
        st.error("Insira ao menos uma chave de API no menu lateral.")
    else:
        col1, col2 = st.columns(2)

        # Pexels
        with col1:
            st.subheader("Pexels")
            if pexels_key:
                results_pexels = search_pexels(query, pexels_key, media_type)
                for item in results_pexels:
                    if media_type == "Fotos":
                        st.image(item['url'], use_container_width=True)
                    else:
                        st.video(item['url'])
                    st.link_button("⬇️ Baixar Mídia", item['download'])

        # Pixabay
        with col2:
            st.subheader("Pixabay")
            if pixabay_key:
                results_pixabay = search_pixabay(query, pixabay_key, media_type)
                for item in results_pixabay:
                    if media_type == "Fotos":
                        st.image(item['url'], use_container_width=True)
                    else:
                        st.video(item['url'])
                    st.link_button("⬇️ Baixar Mídia", item['download'])