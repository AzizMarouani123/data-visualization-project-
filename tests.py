import streamlit as st
import pandas as pd
import numpy as np

def check_missing_values(df):
    """ Vérifie les valeurs manquantes dans le DataFrame """
    missing_values = df.isnull().sum()
    missing_percentage = (missing_values / len(df)) * 100
    missing_data = pd.DataFrame({"Valeurs Manquantes": missing_values, "Pourcentage (%)": missing_percentage})
    
    st.subheader("🔍 Vérification des Valeurs Manquantes")
    if missing_values.sum() > 0:
        st.warning("⚠️ Certaines colonnes contiennent des valeurs manquantes.")
        st.dataframe(missing_data[missing_data["Valeurs Manquantes"] > 0])
    else:
        st.success("✅ Aucune valeur manquante détectée dans les données.")

def check_duplicates(df):
    """ Vérifie les doublons dans le DataFrame """
    duplicates = df.duplicated().sum()
    
    st.subheader("🔄 Vérification des Doublons")
    if duplicates > 0:
        st.warning(f"⚠️ {duplicates} lignes dupliquées ont été trouvées.")
    else:
        st.success("✅ Aucune donnée dupliquée détectée.")

def check_low_variance_columns(df):
    """ Vérifie les colonnes avec une seule valeur unique """
    unique_counts = df.nunique()
    low_variance_cols = unique_counts[unique_counts == 1]

    st.subheader("⚠️ Vérification des Colonnes Peu Informatives")
    if not low_variance_cols.empty:
        st.warning("Ces colonnes contiennent une seule valeur et peuvent être supprimées :")
        st.write(low_variance_cols)
    else:
        st.success("✅ Toutes les colonnes ont des valeurs variées.")

def check_high_missing_percentage(df, threshold=50):
    """ Vérifie les colonnes avec un fort taux de valeurs manquantes (> 50%) """
    missing_percentage = (df.isnull().sum() / len(df)) * 100
    high_missing_cols = missing_percentage[missing_percentage > threshold]

    st.subheader(f"📉 Colonnes avec plus de {threshold}% de valeurs manquantes")
    if not high_missing_cols.empty:
        st.warning("Ces colonnes ont trop de valeurs manquantes et pourraient être supprimées :")
        st.write(high_missing_cols)
    else:
        st.success(f"✅ Aucune colonne ne dépasse {threshold}% de valeurs manquantes.")

def check_outliers(df):
    """ Vérifie la présence de valeurs aberrantes (outliers) via la méthode IQR """
    numeric_cols = df.select_dtypes(include=[np.number])
    
    if numeric_cols.empty:
        st.warning("Aucune colonne numérique pour détecter les valeurs aberrantes.")
        return

    st.subheader("📊 Vérification des Valeurs Aberrantes (Outliers)")
    outliers_detected = False

    for col in numeric_cols.columns:
        Q1 = np.percentile(df[col].dropna(), 25)
        Q3 = np.percentile(df[col].dropna(), 75)
        IQR = Q3 - Q1
        lower_bound = Q1 - 1.5 * IQR
        upper_bound = Q3 + 1.5 * IQR
        outliers = df[(df[col] < lower_bound) | (df[col] > upper_bound)]

        if not outliers.empty:
            outliers_detected = True
            st.warning(f"⚠️ La colonne **{col}** contient des valeurs aberrantes : {len(outliers)} détectées.")

    if not outliers_detected:
        st.success("✅ Aucune valeur aberrante détectée.")

# --------- Interface Streamlit ---------------
st.set_page_config(page_title="🔍 Data Quality Checker", layout="wide")

st.title("🔍 Vérification de la Qualité des Données")
st.write("📝 **Importez un fichier CSV ou Excel pour analyser la qualité des données**")

uploaded_file = st.file_uploader("📂 Téléchargez un fichier CSV ou Excel :", type=["csv", "xlsx"])

if uploaded_file:
    df = pd.read_csv(uploaded_file) if uploaded_file.name.endswith(".csv") else pd.read_excel(uploaded_file)

    st.subheader("📊 Aperçu des Données")
    st.dataframe(df.head())

    if st.button("🚀 Lancer les Tests de Qualité"):
        check_missing_values(df)
        check_duplicates(df)
        check_low_variance_columns(df)
        check_high_missing_percentage(df)
        check_outliers(df)
