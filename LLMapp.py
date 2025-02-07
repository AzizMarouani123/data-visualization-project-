import anthropic
import streamlit as st
import logging
import base64
import pandas as pd
from io import BytesIO

# Configuration du journal de logs
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)

def initialize_ai_client(api_key):
    """
    Initialiser le client Anthropic (Claude).
    """
    return anthropic.Anthropic(api_key=api_key)

def generate_recommendations(df, api_key):
    """
    Générer des recommandations basées sur les données en utilisant un modèle LLM.

    Args:
        df: DataFrame à analyser.
        api_key: Clé API pour accéder à l'API Claude.

    Returns:
        Recommandations générées par l'IA.
    """
    try:
        client = initialize_ai_client(api_key)

        dataset_summary = f"""
        **Aperçu du Jeu de Données :**
        - Colonnes : {', '.join(df.columns)}
        - Statistiques descriptives :
        {df.describe(include='all').to_string()}
        """

        detailed_prompt = f"""
        Tu es un expert en analyse de données. À partir des informations suivantes :

        {dataset_summary}

        1. Identifie les principales tendances et anomalies dans les données.
        2. Suggère des actions basées sur ces insights pour améliorer les performances.
        3. Mets en évidence toute relation inattendue entre les variables.

        Génère un rapport concis sous forme de points clés.
        """

        logger.info("✅ Envoi de la requête à l'IA pour les recommandations.")

        response = client.messages.create(
            model="claude-3-5-sonnet-20241022",
            max_tokens=2000,
            messages=[{"role": "user", "content": detailed_prompt}]
        )

        return response.content[0].text

    except Exception as e:
        logger.error(f"❌ Erreur lors de l'analyse IA : {e}")
        st.error(f"Erreur lors de l'analyse IA : {str(e)}")
        return None

def detect_anomalies(df, api_key):
    """
    Détecter des anomalies dans les données en utilisant un modèle LLM.

    Args:
        df: DataFrame à analyser.
        api_key: Clé API pour accéder à l'API Claude.

    Returns:
        Résultats de détection des anomalies.
    """
    try:
        client = initialize_ai_client(api_key)

        dataset_summary = f"""
        **Aperçu des Données :**
        - Colonnes : {', '.join(df.columns)}
        - Statistiques descriptives :
        {df.describe(include='all').to_string()}
        """

        anomaly_prompt = f"""
        Tu es un spécialiste en détection d'anomalies. Sur la base des données suivantes :

        {dataset_summary}

        Identifie les anomalies potentielles, en expliquant pourquoi elles pourraient être considérées comme telles. Donne des suggestions sur la manière de gérer ces anomalies.
        """

        logger.info("✅ Détection des anomalies en cours.")

        response = client.messages.create(
            model="claude-3-5-sonnet-20241022",
            max_tokens=2000,
            messages=[{"role": "user", "content": anomaly_prompt}]
        )

        return response.content[0].text

    except Exception as e:
        logger.error(f"❌ Erreur lors de la détection des anomalies : {e}")
        st.error(f"Erreur lors de la détection des anomalies : {str(e)}")
        return None

def call_llm_for_viz(df, user_prompt, api_key):
    """
    Appelle l'IA pour générer du code Python de visualisation basé sur les données et la requête utilisateur.

    Args:
        df (pd.DataFrame): Les données à visualiser.
        user_prompt (str): Description de la visualisation souhaitée par l'utilisateur.
        api_key (str): Clé API pour accéder à l'API Claude.

    Returns:
        str: Code Python généré pour la visualisation.
    """
    try:
        client = initialize_ai_client(api_key)

        dataset_summary = f"""
        Colonnes et types :
        {df.dtypes.to_string()}

        Description du jeu de données :
        {df.describe(include='all').to_string()}
        """

        prompt = f"""
        Tu es un expert en visualisation de données avec Python. En utilisant le DataFrame suivant :
        
        {dataset_summary}

        Crée un code Python pour générer la visualisation suivante :
        {user_prompt}

        Contraintes :
        - Utilise uniquement matplotlib, seaborn, ou plotly.
        - Ne donne aucun commentaire, uniquement le code Python entre balises ```python.
        - Le DataFrame est déjà chargé sous le nom 'df'.
        - Remplace plt.show() par st.pyplot(plt) pour compatibilité avec Streamlit.
        - Inclure des visualisations populaires comme les histogrammes, les heatmaps, les diagrammes de corrélation, et d'autres types de graphiques pertinents pour le jeu de données.
        """

        logger.info("✅ Envoi de la requête à l'IA pour générer la visualisation.")

        response = client.messages.create(
            model="claude-3-5-sonnet-20241022",
            max_tokens=1500,
            messages=[{"role": "user", "content": prompt}]
        )

        return response.content[0].text
    except Exception as e:
        logger.error(f"❌ Erreur lors de la génération de la visualisation : {e}")
        return f"Erreur : {str(e)}"


def exec_generated_code(code: str, df: pd.DataFrame):
    """
    Exécuter du code Python généré dynamiquement pour afficher une visualisation.

    Args:
        code (str): Le code Python généré à exécuter.
        df (pd.DataFrame): Le DataFrame utilisé par le code généré.
    """
    try:
        # Définit l'environnement global pour que df soit accessible au code généré
        exec_globals = {
            "st": st,
            "pd": pd,
            "plt": __import__("matplotlib.pyplot"),
            "sns": __import__("seaborn"),
            "px": __import__("plotly.express"),
            "df": df
        }

        # Exécute le code généré dans cet environnement global
        exec(code, exec_globals)
    except Exception as e:
        logger.error(f"❌ Erreur lors de l'exécution du code généré : {e}")
        st.error(f"Erreur lors de l'exécution du code généré : {e}")
