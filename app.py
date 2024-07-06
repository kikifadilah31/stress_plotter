import streamlit as st
import pandas as pd

st.title("PLOTTER STRES")
st.markdown("_test_")


@st.cache_data
def load_data(file):
    data = pd.read_excel(file)
    return data

uploaded_file = st.file_uploader("Pilih Excel")

if uploaded_file is None:
    st.info("Aya Data")
    st.stop()

df_stress_input = load_data(uploaded_file)
df_load_case = df_stress_input["Load"].unique()
st.dataframe(df_stress_input)
options_load_case = st.multiselect(
    "Pilih Load Case",df_load_case,
    default=df_load_case)
df_test=df_stress_input.groupby(by=["Load"])
df=df_test.get_group((options)).reset_index(drop=True)