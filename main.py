import requests
import streamlit as st

API_BASE_URL = st.secrets['API_BASE_URL']

PAGES = ("Accueil", "Pingouin", "Chat / Chien")


st.set_page_config(page_title="Zoologist", page_icon="🐾", layout="wide")


def change_page(page: str) -> None:
    st.session_state.page = page


def display_result(prediction: str, confidence: float | None = None) -> None:
    st.success(f"Prédiction : **{prediction}**")
    if confidence is not None:
        confidence = max(0.0, min(float(confidence), 1.0))
        st.metric("Pourcentage de correspondance", f"{confidence * 100:.1f} %")
        st.progress(confidence)


def display_api_error(error: Exception) -> None:
    if isinstance(error, requests.Timeout):
        st.error("L'API met trop de temps à répondre. Réessaie dans quelques instants.")
    elif isinstance(error, requests.ConnectionError):
        st.error("Impossible de joindre l'API Zoologist.")
    elif isinstance(error, requests.HTTPError):
        response = error.response
        detail = response.text if response is not None else str(error)
        st.error(f"L'API a renvoyé une erreur : {detail}")
    else:
        st.error(f"Une erreur est survenue : {error}")


def home_page() -> None:
    st.title("🐾 Zoologist")
    st.subheader("Que souhaites-tu identifier ?")
    st.write(
        "Choisis un outil de prédiction. Les calculs sont effectués "
        "par l'API Zoologist déployée dans le cloud."
    )

    left, right = st.columns(2, gap="large")
    with left:
        with st.container(border=True):
            st.header("🐧 Pingouin")
            st.write("Renseigne ses mesures physiques et son île pour prédire son espèce.")
            st.button(
                "Identifier un pingouin",
                type="primary",
                use_container_width=True,
                on_click=change_page,
                args=("Pingouin",),
            )

    with right:
        with st.container(border=True):
            st.header("🐱 🐶 Chat ou chien")
            st.write("Importe une photo pour savoir si elle représente un chat ou un chien.")
            st.button(
                "Analyser une photo",
                type="primary",
                use_container_width=True,
                on_click=change_page,
                args=("Chat / Chien",),
            )


def penguin_page() -> None:
    st.title("🐧 Identifier l'espèce d'un pingouin")
    st.caption("Complète les caractéristiques, puis lance la prédiction.")

    with st.form("penguin_form"):
        left, right = st.columns(2)
        with left:
            island = st.selectbox("Île", ["Biscoe", "Dream", "Torgersen"])
            bill_length_mm = st.slider("Longueur du bec (mm)", 20.0, 70.0, 45.0, 0.1)
            bill_depth_mm = st.slider("Profondeur du bec (mm)", 10.0, 30.0, 17.0, 0.1)
        with right:
            flipper_length_mm = st.slider(
                "Longueur des nageoires (mm)", 150.0, 250.0, 200.0, 1.0
            )
            body_mass_g = st.slider(
                "Masse corporelle (g)", 2000.0, 7000.0, 4000.0, 50.0
            )
            sex = st.selectbox("Sexe", ["Male", "Female"])

        submitted = st.form_submit_button(
            "Prédire l'espèce", type="primary", use_container_width=True
        )

    if submitted:
        params = {
            "island": island,
            "bill_length_mm": bill_length_mm,
            "bill_depth_mm": bill_depth_mm,
            "flipper_length_mm": flipper_length_mm,
            "body_mass_g": body_mass_g,
            "sex": sex,
        }
        try:
            with st.spinner("Analyse des caractéristiques..."):
                response = requests.get(
                    f"{API_BASE_URL}/predict_tf", params=params, timeout=60
                )
                response.raise_for_status()
                result = response.json()
            display_result(result["prediction"], result.get("confidence"))
        except (requests.RequestException, ValueError, KeyError) as error:
            display_api_error(error)


def cat_dog_page() -> None:
    st.title("🐱 🐶 Reconnaître un chat ou un chien")
    st.caption("Importe une image JPG, JPEG ou PNG.")

    uploaded_image = st.file_uploader(
        "Choisir une photo", type=["jpg", "jpeg", "png"], accept_multiple_files=False
    )
    if uploaded_image is None:
        st.info("Ajoute une photo pour activer l'analyse.")
        return

    st.image(uploaded_image, caption="Image à analyser", width=420)
    if st.button("Analyser la photo", type="primary", use_container_width=True):
        files = {
            "img": (
                uploaded_image.name,
                uploaded_image.getvalue(),
                uploaded_image.type or "application/octet-stream",
            )
        }
        try:
            with st.spinner("Analyse de l'image..."):
                response = requests.post(
                    f"{API_BASE_URL}/predict_image", files=files, timeout=90
                )
                response.raise_for_status()
                result = response.json()
            labels = {"cat": "Chat", "dog": "Chien"}
            prediction = labels.get(result["prediction"], result["prediction"])
            display_result(prediction, result.get("confidence"))
        except (requests.RequestException, ValueError, KeyError) as error:
            display_api_error(error)


if "page" not in st.session_state:
    st.session_state.page = "Accueil"

with st.sidebar:
    st.title("Navigation")
    for page_name, icon in zip(PAGES, ("🏠", "🐧", "🐱 / 🐶")):
        st.button(
            f"{icon} {page_name}",
            use_container_width=True,
            type="primary" if st.session_state.page == page_name else "secondary",
            on_click=change_page,
            args=(page_name,),
            key=f"nav_{page_name}",
        )
    st.divider()
    st.caption("API Zoologist • Google Cloud Run")

if st.session_state.page == "Pingouin":
    penguin_page()
elif st.session_state.page == "Chat / Chien":
    cat_dog_page()
else:
    home_page()
