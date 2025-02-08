import streamlit as st
import pandas as pd
import re
import logging
import matplotlib.pyplot as plt
import os

from LLMapp import generate_recommendations, detect_anomalies, call_llm_for_viz


API_KEY = "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"

if not API_KEY:
    raise ValueError("Clé API manquante. Veuillez la définir dans le fichier .env")

# Configuration du journal de logs
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)

def main():
    st.set_page_config(page_title="📊 Dataviz Dynamique", layout="wide")
    st.sidebar.title("🌟 Exploration des Données")

    with st.sidebar.expander("🔍 Options d'Exploration", expanded=True):
        st.markdown("""
        ### Naviguez entre les sections :
        - **Accueil** : Introduction et aperçu de l'application.
        - **Tests de Qualité des Données** : Analyse approfondie des données.
        - **Analyses IA Avancées** : Analyse des données et visualisations personnalisées.
        """, unsafe_allow_html=True)

    pages = {
        "🏠 Accueil": "home",
        "🧪 Tests de Qualité des Données": "data_quality_tests",
        "🤖 Analyses IA Avancées": "ai_analytics"
    }

    selected_page = st.sidebar.radio("### Choisissez une section :", list(pages.keys()), label_visibility="collapsed")

    if selected_page == "🏠 Accueil":
        st.markdown("""
        <style>
        h1 {
            font-size: 3em;
            text-align: center;
            color: #2C3E50;
        }
        p {
            font-size: 1.2em;
            line-height: 1.8;
            text-align: justify;
        }
        ul {
            font-size: 1.2em;
            line-height: 1.8;
        }
        </style>
        <h1>Bienvenue dans l'Assistant Data Insights</h1>
        <p>Cette application innovante vous offre une expérience unique pour explorer et analyser vos données grâce à des outils avancés d'intelligence artificielle et de visualisation. Voici ce que vous pouvez accomplir :</p>
        <ul>
        <li>🛠️ <strong>Créer des visualisations interactives</strong> adaptées à vos besoins.</li>
        <li>🔗 <strong>Découvrir des relations et corrélations</strong> cachées dans vos jeux de données.</li>
        <li>🚀 <strong>Exploiter des recommandations intelligentes</strong> générées par l'IA pour optimiser vos décisions.</li>
        </ul>
        <p>Naviguez facilement entre les différentes sections via le menu latéral pour tirer le meilleur parti de vos données.</p>
        <div style="text-align: center; margin-top: 20px;">
            <img src="https://img.freepik.com/vecteurs-libre/gros-employe-isole-travaillant-dans-illustration-plate-bureau-lieu-travail_1150-41780.jpg" alt="Illustration des capacités de l'application" style="border-radius: 15px;">
        </div>
        """, unsafe_allow_html=True)
    
    elif selected_page == "🧪 Tests de Qualité des Données":
        st.markdown("<h1 style='text-align: center; color: #2C3E50;'>Tests de Qualité des Données</h1>", unsafe_allow_html=True)
        st.info("Vous allez être redirigé vers l'interface des tests de qualité des données.")
        if st.button("🚀 Ouvrir les Tests de Qualité des Données"):
            with st.spinner("Chargement de l'interface des tests..."):
                os.system("streamlit run tests.py")  # Commande pour lancer tests.py

    elif selected_page == "🤖 Analyses IA Avancées":
        st.markdown("<h1 style='text-align: center; color: #2C3E50;'>Analyse et Visualisation Avancées</h1>", unsafe_allow_html=True)

        uploaded_file = st.file_uploader("<h3 style='color: #16A085;'>📂 Importez vos données (CSV ou Excel) :</h3>", type=["csv", "xlsx"], label_visibility="collapsed", accept_multiple_files=False, help="Formats acceptés : CSV et Excel.", key="file_upload")

        if uploaded_file:
            df = pd.read_csv(uploaded_file) if uploaded_file.name.endswith(".csv") else pd.read_excel(uploaded_file)

            st.markdown("<h3 style='color: #2980B9;'>🔍 Recommandations Basées sur l'IA</h3>", unsafe_allow_html=True)
            if st.button("🚀 Lancer la Génération des Recommandations"):
                with st.spinner("Analyse en cours, merci de patienter..."):
                    recommendations = generate_recommendations(df, API_KEY)
                    st.success("✅ Recommandations créées avec succès !")
                    st.markdown(f"<div style='font-size: 1.1em;'>{recommendations}</div>", unsafe_allow_html=True)

            st.markdown("<h3 style='color: #E74C3C;'>⚠️ Détection Automatique des Anomalies</h3>", unsafe_allow_html=True)
            if st.button("🔎 Identifier les Anomalies"):
                with st.spinner("Recherche d'anomalies en cours..."):
                    anomalies = detect_anomalies(df, API_KEY)
                    st.success("✅ Anomalies détectées avec succès !")
                    st.markdown(f"<div style='font-size: 1.1em;'>{anomalies}</div>", unsafe_allow_html=True)

            st.markdown("<h3 style='color: #8E44AD;'>📊 Visualisations Personnalisées avec IA</h3>", unsafe_allow_html=True)
            user_prompt = st.text_area("📝 Décrivez votre visualisation :", placeholder="Exemple : Afficher un graphique à barres des ventes trimestrielles")

            

            if st.button("🎨 Générer la Visualisation"):
                if user_prompt.strip():
                    with st.spinner("⏳ Génération de votre visualisation..."):
                        try:
                            # Appel de l'IA pour générer le code de visualisation
                            generated_code = call_llm_for_viz(df, user_prompt, API_KEY)

                            st.markdown("<h4 style='color: #34495E;'>🖥️ Code Python Généré</h4>", unsafe_allow_html=True)
                            st.code(generated_code, language="python")

                            # Extraction et exécution du code Python
                            match = re.search(r"```python\n(.*?)\n```", generated_code, re.DOTALL)
                            if match:
                                python_code = match.group(1)
                                safe_code = python_code.replace("plt.show()", "st.pyplot(plt)")

                                st.markdown("<h4 style='color: #27AE60;'>📈 Résultat de la Visualisation</h4>", unsafe_allow_html=True)
                                try:
                                    # Ajout des bibliothèques nécessaires au code d'exécution
                                    exec(safe_code, {'df': df, 'plt': plt, 'sns': __import__("seaborn"), 'pd': pd, 'st': st})
                                except Exception as e:
                                    st.error(f"⚠️ Une erreur s'est produite lors de l'exécution de la visualisation : {e}")
                                    logger.error(f"⚠️ Une erreur s'est produite lors de l'exécution de la visualisation : {e}")
                            else:
                                st.warning("⚠️ Aucun code de visualisation valide détecté dans la réponse de l'IA.")
                        except Exception as e:
                            st.error(f"❌ Une erreur est survenue lors de la génération de la visualisation : {e}")
                            logger.error(f"❌ Une erreur est survenue lors de la génération de la visualisation : {e}")
                else:
                    st.warning("⚠️ Veuillez décrire la visualisation à générer avant de continuer.")

if __name__ == "__main__":
    main()
