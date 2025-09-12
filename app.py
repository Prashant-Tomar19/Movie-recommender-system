import streamlit as st
import pandas as pd
import ast

# --- function ---
def convert3(text):
    L = []
    counter = 0
    
    # If text is a string, parse it
    if isinstance(text, str):
        try:
            text = ast.literal_eval(text)
        except:
            return []
    
    # Now text is expected to be a list (of dicts or strings)
    for i in text:
        if counter == 3:  # only take first 3
            break
        if isinstance(i, dict) and 'name' in i:
            L.append(i['name'])
        elif isinstance(i, str):
            L.append(i)
        counter += 1
    return L


# --- Streamlit app ---
st.title("🎬 Movies Cast Extractor")

# Upload dataset
uploaded_file = st.file_uploader("Upload your movies CSV", type=["csv"])

if uploaded_file is not None:
    movies = pd.read_csv(uploaded_file)
    st.write("📊 Dataset Preview:")
    st.dataframe(movies.head())

    if "cast" in movies.columns:
        movies["cast"] = movies["cast"].apply(convert3)

        st.write("✅ Cast column after conversion:")
        st.dataframe(movies[["title", "cast"]].head(20))

        # Option to download processed CSV
        csv = movies.to_csv(index=False).encode("utf-8")
        st.download_button(
            label="📥 Download Processed CSV",
            data=csv,
            file_name="movies_processed.csv",
            mime="text/csv",
        )
    else:
        st.error("❌ The dataset does not contain a 'cast' column.")
