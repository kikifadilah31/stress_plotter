import streamlit as st
import pandas as pd
import plotly.express as px
import requests

# FUNGSI -------------------------------------------------------------------------------------------------------------------------------------------
## FUNGSI Mengubah Tegangan Menjadi Per Kolom
def data_tegangan_per_column(dataframe_load_case, dataframe_input_stress, stress_point, stress):
    # Filter dataframe_input_stress berdasarkan 'Section Position' dan kolom stress
    df_filtered = dataframe_input_stress[dataframe_input_stress["Section Position"] == stress_point][["Load", stress]]
    
    # Inisialisasi dictionary untuk menyimpan hasil
    new_data = {}
    
    # Iterasi setiap load_case yang ada pada dataframe_load_case
    for load_case in dataframe_load_case:
        # Filter baris yang sesuai dengan load_case pada dataframe yang sudah difilter
        df_load_case_filtered = df_filtered[df_filtered["Load"] == load_case][stress]
        
        # Menyimpan hasil ke dictionary, pastikan hasilnya berupa array
        new_data[load_case] = df_load_case_filtered.to_numpy()  # Mengambil nilai sebagai array

    df_per_loadcase = pd.DataFrame(new_data)
    
    return df_per_loadcase

## SKEMA WARNA PLOTLY --------------------------------------------------------------------------------------------------------------------------------------------------------------------------
plotly_color_schemes = {
    "qualitative": [
        'Plotly', 'D3', 'G10', 'T10', 'Alphabet', 'Dark24', 'Light24', 'Pastel1', 
        'Pastel2', 'Set1', 'Set2', 'Set3', 'Prism', 'Safe', 'Vivid', 'Bold'
    ],
    "sequential": [
        'Viridis', 'Plasma', 'Inferno', 'Magma', 'Cividis', 'Blues', 'Greens', 'Oranges', 
        'Purples', 'Reds', 'Greys', 'YlGnBu', 'YlGn', 'YlOrRd', 'Turbo', 'Cividis'
    ],
    "diverging": [
        'BrBG', 'PRGn', 'PiYG', 'PuOr', 'RdBu', 'RdGy', 'RdYlBu', 'RdYlGn', 
        'Spectral', 'Temps'
    ],
    "cyclical": [
        'Edge', 'IceFire', 'Phase', 'Twilight', 'HSV', 'Mrybm', 'Mygbm'
    ],
    "carto": [
        'Antique', 'Bold', 'Pastel', 'Prism', 'Safe', 'Vivid', 'Earth', 
        'Teal', 'Temps', 'Dense', 'Deep'
    ],
    "colorbrewer": [
        'Blues', 'Greens', 'Oranges', 'Purples', 'Reds', 'Greys', 
        'PuBu', 'PuBuGn', 'BuPu', 'YlGn', 'YlGnBu', 'YlOrBr', 'YlOrRd', 
        'RdPu', 'GnBu', 'PuRd', 'OrRd', 'BuGn', 'RdYlBu', 'RdYlGn', 
        'Spectral', 'RdBu', 'PiYG', 'PRGn', 'BrBG', 'RdGy', 'PuOr', 'Set1', 
        'Set2', 'Set3', 'Paired', 'Pastel1', 'Pastel2', 'Dark2', 'Accent'
    ],
    "cmocean": [
        'Thermal', 'Haline', 'Solar', 'Ice', 'Gray', 'Deep', 'Dense', 'Algae', 
        'Matter', 'Turbid', 'Speed', 'Amp', 'Tempo', 'Phase', 'Top', 'Balance', 'Delta'
    ]
}
all_color_schemes = sum(plotly_color_schemes.values(), [])

## FUNGSI PLOT
import plotly.express as px

def stress_plot(data_frame,  # data 
                y_axis,  # data kolom yang di plot
                tittle,  # judul
                y_tick,  # tick atau range y axis
                x_tick,  # tick atau range x axis
                y_axis_title,  # judul y axis
                tension_limit, 
                compression_limit, 
                data_frame_stationing,
                vertical_lines,  # List garis vertikal yang akan ditambahkan
                color_scheme='Plotly'):  # Tambahkan parameter skema warna dengan default 'Plotly'
    
    # Pilih skema warna berdasarkan input pengguna atau default
    if hasattr(px.colors.qualitative, color_scheme):
        plotly_colors = getattr(px.colors.qualitative, color_scheme)
    else:
        plotly_colors = px.colors.qualitative.Plotly  # Default jika skema warna tidak ditemukan
    
    # Ambil warna dalam urutan dari skema yang dipilih (sesuai jumlah y_axis)
    colors = plotly_colors[:len(y_axis)]
    
    # Membuat grafik garis
    fig_1 = px.line(
        data_frame,
        x="X",
        y=y_axis,
        color_discrete_sequence=colors  # Menggunakan warna yang ditentukan
    )

    # Mengatur layout grafik
    fig_1.update_layout(
        title={
            'text': tittle,
            'x': 0.5,
            'xanchor': 'center',
            'font': {
                'family': "Bahnschrift",
                'size': 24,
                'color': "Black",
            }
        },
        yaxis=dict(
            tickformat=",",
            dtick=y_tick,
            title=y_axis_title,
            titlefont=dict(
                family="Bahnschrift",
                color="black"
            ),
            tickfont=dict(
                family="Bahnschrift",
                color="black"
            ),
            showgrid=True,
            gridcolor="LightGray",
            gridwidth=1,
            zeroline=True,
            zerolinecolor='Black',
            zerolinewidth=2,
        ),
        xaxis=dict(
            tickformat=",",
            dtick=x_tick,
            title="Stationing (m)",
            titlefont=dict(
                family="Bahnschrift",
                color="black"
            ),
            tickfont=dict(
                family="Bahnschrift",
                color="black"
            ),
            showgrid=True,
            gridcolor="LightGray",
            gridwidth=1,
            minor=dict(
                showgrid=True,
            )
        ),
        annotations=[
            dict(
                text="Midas Stress Ploter by Kiki Fadilah Tanjung",  # Watermark tetap
                xref="paper", yref="paper",  # Koordinat relatif ke plot
                x=0.5, y=0.05,  # Posisi watermark (tengah)
                showarrow=False,  # Tidak menampilkan panah
                font=dict(
                    size=40,  # Ukuran teks watermark
                    color="rgba(100, 100, 100)"  # Warna teks dengan transparansi
                ),
                xanchor="center",  # Penempatan teks pada sumbu X
                yanchor="middle",  # Penempatan teks pada sumbu Y
                opacity=0.3  # Transparansi teks watermark
            )
        ]
    )

    # Menambahkan garis batas tegangan
    fig_1.add_shape(
        type="line",
        x0=0, x1=data_frame_stationing.max(),
        y0=tension_limit, y1=tension_limit,
        line=dict(
            color="red",
            width=3,
            dash="dashdot"
        )
    )
    
    # Menambahkan garis batas kompresi
    fig_1.add_shape(
        type="line",
        x0=0, x1=data_frame_stationing.max(),
        y0=compression_limit, y1=compression_limit,
        line=dict(
            color="red",
            width=3,
            dash="dashdot"
        )
    )
    
    # Menambahkan beberapa garis vertikal dari daftar
    for line_x in vertical_lines:
        fig_1.add_shape(
            type="line",
            x0=line_x, x1=line_x,  # Garis vertikal memiliki x0 dan x1 yang sama
            y0=tension_limit,
            y1=compression_limit,
            line=dict(
                color="black",  # Warna garis vertikal (bisa disesuaikan)
                width=2,  # Ketebalan garis vertikal
            )
        )
    
    return fig_1




# OPENING ------------------------------------------------------------------------------------------------------------------------------------------
st.title("MIDAS STRESS & FORCE PLOTTER")
# DOWNLOAD FORMAT DATA
st.markdown("# Format Input Data")
st.link_button("Format Stationing", 'https://1drv.ms/x/s!AlOQzBonmyVTgahq57WTL43bheCZpg?e=M1EnHk')
st.link_button("Format Data", 'https://1drv.ms/x/s!AlOQzBonmyVTgahpvnZ9ccRRSvjvfQ?e=xw2VJm')


# INPUT DATA ------------------------------------------------------------------------------------------------------------------------------------------
st.markdown("# Input Data")
choose_displayed_data=st.radio("Pilih Data Yang Akan Di Tampilkan",
                                ["Tegangan"])
@st.cache_data
def load_data(file):
    data = pd.read_excel(file)
    return data

if choose_displayed_data == "Tegangan":
    uploaded_file_stress = st.file_uploader("Upload Excel Ouput Tegangan Midas")
    if uploaded_file_stress is None:
        st.info("Masukan Data")
        st.stop()
    uploaded_file_station = st.file_uploader("Upload Excel Stationing")
    if uploaded_file_station is None:
        st.info("Masukan Data")
        st.stop()

if choose_displayed_data == "Tegangan dan Momen":
    uploaded_file_stress = st.file_uploader("Upload Excel Ouput Tegangan Midas")
    if uploaded_file_stress is None:
        st.info("Masukan Data")
        st.stop()
    uploaded_file_force = st.file_uploader("Upload Excel Ouput Gaya Midas")
    if uploaded_file_force is None:
        st.info("Masukan Data")
        st.stop()
    uploaded_file_station = st.file_uploader("Upload Excel Stationing")
    if uploaded_file_station is None:
        st.info("Masukan Data")
        st.stop()

#DATA FRAME 1 --------------------------------------------------------------------------------------------------------------------------------------

df_stress_input = load_data(uploaded_file_stress) ## Upload Data Tegangan dari Midas
df_force_input = load_data(uploaded_file_stress) ## Upload Data Tegangan dari Midas
df_station = load_data(uploaded_file_station) ## Upload Data Stationing
column_list=list(df_stress_input.columns.values)[4:]

load_case_list = list(df_stress_input["Load"].unique()) ## List Load Case
stress_point_list = list(df_stress_input["Section Position"].unique()) ## List Stress Point


# SIDEBAR -------------------------------------------------------------------------------------------------------------------------------------------
with st.sidebar:
    # Menampilkan link profil LinkedIn
    st.title("Profil Developer")
    st.markdown("Dikembangkan Oleh : [Kiki Fadilah Tanjung](https://www.linkedin.com/in/kiki-fadilah-tanjung-88460b151/)")

    st.markdown("# Pilih tegangan")
    selected_stress = st.radio(
    "Pilih Tegangan",
    column_list)



# TAMPILAN WEB DATA HASIL INPUT ----------------------------------------------------------------------------------------------------------------------
st.markdown("# Data Tegangan Hasil Input")
st.dataframe(df_stress_input) ## Menampilkan Data Input

st.markdown("## Data Stationing Tegangan")
st.dataframe(df_station) ## Menampilkan Data Stationing

#st.markdown("## Data Tegangan Per Stress Point")
## Loop through each stress point and process the data
#for stress_point in stress_point_list:
#    st.markdown(f"### {selected_stress} Stress Point {stress_point}")
#    
#    # Menyiapkan dataframe untuk setiap stress point
#    df_tegangan_per_stress_point = data_tegangan_per_column(
#        load_case_list,
#        df_stress_input,
#        stress_point,
#        selected_stress
#    )
#    
#    # Menampilkan dataframe setiap stress point
#    st.dataframe(pd.concat([df_station, df_tegangan_per_stress_point], axis=1)) #Menampilkan data tegangan per kombinasi sesuai tegangan yang dipilih

st.markdown("# Plot Diagram")

st.markdown("## Parameter Tampilan Diagram")
# PARAMETER TAMPILAN DIAGRAM
col_A1,col_A2=st.columns(2)
with col_A1:
    tick_ver_axis = st.number_input("Masukan Interval Untuk Vertical Axis",
                                    value=1000,step=500)
    tick_hor_axis = st.number_input("Masukan Interval Untuk Horizontal Axis",
                                    value=10,step=10)
    skema_warna=st.selectbox("Pilih Skema Warna",all_color_schemes)
    vertical_lines_input = st.text_input("Nilai Sta Pier (pisahkan dengan koma):", 
                                         value="10, 20, 30")
    
    # Konversi input teks menjadi list angka
try:
    garis_pier = [float(x) for x in vertical_lines_input.split(",")]
except ValueError:
    st.error("Harap masukkan angka yang valid, dipisahkan dengan koma.")
    garis_pier = []


with col_A2:
    tension_limit = st.number_input("Masukan Batasan Tegangan Tarik",
                                    value=3000,
                                    help="Positif Tarik")
    compression_limit = st.number_input("Masukan Batasan Tegangan Tekan",
                                    value=-20000,
                                    help="Negatif Tarik")
    selected_stress_point_plot_diagram_gabungan = st.selectbox("Pilih Stress Point",
                                    stress_point_list)
    tittle = st.text_input("Masukan Judul Diagram",
                           key="Judul Diagram",
                           value=f"Tegangan Stress Point {selected_stress_point_plot_diagram_gabungan}")

    
df_stationing_for_plot = df_station["X"] # Data Stationing
## Dataframe tegangan per load case sesuai stress point yang dipilihi pada variabel "selected_stress_point_plot_diagram_gabungan"
df_tegangan_per_loadcase_selected_stress_point=data_tegangan_per_column(
    load_case_list,
    df_stress_input,
    selected_stress_point_plot_diagram_gabungan,
    selected_stress
)
st.markdown("## Diagram Gabungan")
# PLOT DIAGRAM ALL
df_plot_stress_all = pd.concat([df_stationing_for_plot,df_tegangan_per_loadcase_selected_stress_point],axis=1) # data frame tegangan yang di plot

DIAGRAM_ALL=stress_plot(
    df_plot_stress_all,# data tegangan
    load_case_list,# data load case yang di plot
    tittle,# judul
    tick_ver_axis,# tick atau range y axis
    tick_hor_axis,# tick atau range x axis
    selected_stress, # pilih tegangan yang akan di tampilkan
    tension_limit, #batas tarik
    compression_limit, #batas tekan
    df_stationing_for_plot,
    garis_pier,
    skema_warna
    )

st.plotly_chart(DIAGRAM_ALL,True)

st.markdown(f"## Tegangan {selected_stress} Stress Point {selected_stress_point_plot_diagram_gabungan}") #sub judul
st.dataframe(pd.concat([df_station,df_tegangan_per_loadcase_selected_stress_point],axis=1)) #Menampilkan data tegangan per kombinasi sesuai tegangan yang dipilih


st.markdown("## Diagram Per Load Case")
## Data Hanya Load case yang dipilih
col_B1,col_B2=st.columns(2)
with col_B1:
    load_case_selector = st.selectbox(
        "Pilih Load Case",load_case_list)
    skema_warna_2=st.selectbox("Pilih Skema Warna Untuk Diagram Di Bawah",all_color_schemes)
with col_B2:
    selected_stress_point_2 = st.multiselect("Pilih Stress ",
                                    stress_point_list,default="Pos-1")

## Dataframe untuk plot sesuai load case dan stress point yang dipilih pada multiselect diatas
# List untuk menyimpan DataFrame hasil per stress point
df_list = []

for stress_point in selected_stress_point_2:
    # Panggil fungsi untuk setiap stress point
    df_temp = data_tegangan_per_column(
        [load_case_selector],
        df_stress_input,
        stress_point,  # Stress point berbeda di setiap iterasi
        selected_stress
    )
    
    # Rename kolom sesuai stress point
    df_temp.columns = [f"{stress_point}"]
    
    # Tambahkan DataFrame ke dalam list
    df_list.append(df_temp)

# Concat semua DataFrame secara horizontal
df_tegangan_selected_stress_point_dan_loadcase_concat = pd.concat(df_list, axis=1)


df_tegangan_per_loadcase_selected_stress_point_horizontal_stacked=pd.concat([df_station,df_tegangan_selected_stress_point_dan_loadcase_concat], axis=1)

# Diagram per load-case
judul=f"Tegangan {load_case_selector}"
DIAGRAM_PER_LC=stress_plot(
    df_tegangan_per_loadcase_selected_stress_point_horizontal_stacked,# data tegangan
    selected_stress_point_2,# data load case yang di plot
    judul,# judul
    tick_ver_axis,# tick atau range y axis
    tick_hor_axis,# tick atau range x axis
    selected_stress, # pilih tegangan yang akan di tampilkan
    tension_limit, #batas tarik
    compression_limit, #batas tekan
    df_stationing_for_plot,
    garis_pier,
    skema_warna_2
    )
st.plotly_chart(DIAGRAM_PER_LC,True)

st.markdown("### Data Load Case Tegangan")
st.dataframe(df_tegangan_per_loadcase_selected_stress_point_horizontal_stacked) # Tampilkan hasil h stack
