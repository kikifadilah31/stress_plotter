import streamlit as st
import pandas as pd
import plotly.express as px

st.title("MIDAS STRESS PLOTTER")
st.markdown("_BETA TEST_")


@st.cache_data
def load_data(file):
    data = pd.read_excel(file)
    return data

uploaded_file_stress = st.file_uploader("Upload Excel Ouput Midas")
if uploaded_file_stress is None:
    st.info("Masukan Data")
    st.stop()

uploaded_file_station = st.file_uploader("Upload Excel Stationing")
if uploaded_file_station is None:
    st.info("Masukan Data")
    st.stop()

column_select = "Sig-xx(Summation) (kN/m²)"

df_stress_input = load_data(uploaded_file_stress) ## Data Upload Input
df_station = load_data(uploaded_file_station) ## Data Upload Stationing
column_list=list(df_stress_input.columns.values)

df_load_case = list(df_stress_input["Load"].unique()) ## List Load Case
df_stress_point = list(df_stress_input["Section Position"].unique()) ## List Stress Point


## SIDEBAR
with st.sidebar:
    # PILIH LOAD COMBO
    st.markdown("# STRESS POINT")
    stress_point = st.radio(
    "Pilih Stress Point",
    df_stress_point)
    st.markdown("# PILIH TEGANGAN")
    column_select = st.radio(
    "Pilih Tegangan",
    column_list)


## TAMPILAN WEB
st.markdown("# DATA YANG DI INPUT")
st.dataframe(df_stress_input) ## Menampilkan Data Input
st.markdown("# LOAD CASE")
options_load_case = st.multiselect(
    "Pilih Load Case",df_load_case)
st.markdown("# STATIONING")
st.dataframe(df_station) ## Menampilkan Data Stationing
# Filter Data Per Stress Point
df_berdasarkan_stress_point = df_stress_input[(df_stress_input["Section Position"]==stress_point)][["Load",column_select]]

# Mengubah Tegangan Menjadi Per Kolom
new_data = {}
for load_case in df_load_case:
    df_wrap_col = df_berdasarkan_stress_point[df_berdasarkan_stress_point["Load"] == load_case][column_select]
    new_data[load_case] = df_wrap_col.values  # Mengambil nilai sebagai array

df_wrap_col_result = pd.DataFrame(new_data) # Data Tegangan Per Loadcase
df_selected_load_comb = df_wrap_col_result[options_load_case] # Data Hanya Load case yang dipilih


st.markdown("# TEGANGAN PER LOAD CASE")
st.dataframe(pd.concat([df_station,df_wrap_col_result],axis=1)) #Menampilkan data tegangan kombinasi yang dipilih

df_stationing_for_plot = df_station["X"] # Data Stationing
df_plot_stress = pd.concat([df_stationing_for_plot,df_selected_load_comb],axis=1) # Data Yang Di Plotkan Ke Diagram

# DIAGRAM TEGANGAN
col_A1,col_A2=st.columns(2)
with col_A1:
    range_ver_axis = st.number_input("Masukan Interval Untuk Vertical Axis",
                                    value=1000,step=500)
    range_hor_axis = st.number_input("Masukan Interval Untuk Horizontal Axis",
                                    value=10,step=10)
with col_A2:
    tension_limit = st.number_input("Masukan Batasan Tegangan Tarik",
                                    value=3000,
                                    help="Positif Tarik")
    compression_limit = st.number_input("Masukan Batasan Tegangan Tekan",
                                    value=-20000,
                                    help="Negatif Tarik")
    tittle = st.text_input("Masukan Judul Diagram",
                           key="Judul Diagram")
fig_1 = px.line(
                df_plot_stress,
                x="X",
                y=options_load_case)
fig_1.update_layout(
    title={
        'text': tittle,
        'x':0.5,
        'xanchor': 'center',
        'font': {
            'family': "Bahnschrift",
            'size': 24,
            'color': "Black",
        }
    },
    yaxis=dict(
        tickformat=",",
        dtick = range_ver_axis,
        title=column_select,
        titlefont=dict(
            family ="Bahnschrift",
            color ="black"
        ),
        tickfont=dict(
            family ="Bahnschrift",
            color ="black"
        ),
        showgrid = True,
        gridcolor= "LightGray",
        gridwidth=1,
        zeroline=True,
        zerolinecolor='Black',
        zerolinewidth=2,
    ),
    xaxis=dict(
        tickformat=",",
        dtick=range_hor_axis,
        title="Stationing (m)",
        titlefont=dict(
            family ="Bahnschrift",
            color ="black"
        ),
        tickfont=dict(
            family ="Bahnschrift",
            color ="black"
        ),
        showgrid = True,
        gridcolor= "LightGray",
        gridwidth=1,
        minor=dict(
            showgrid=True,
        )
    ),
)

fig_1.add_shape(
    type="line",
    x0=0,x1=df_stationing_for_plot.max(),
    y0=tension_limit,y1=tension_limit,
    line=dict(
        color="red",
        width=3,
        dash="dashdot"
    )
)
fig_1.add_shape(
    type="line",
    x0=0,x1=df_stationing_for_plot.max(),
    y0=compression_limit,y1=compression_limit,
    line=dict(
        color="red",
        width=3,
        dash="dashdot"
    )
)

st.plotly_chart(fig_1,True)