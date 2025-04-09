import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px
from matplotlib import lines
from matplotlib import patches
from matplotlib.patheffects import withStroke
import plotly.offline as po
import plotly.graph_objs as pg
from sodapy import Socrata
import requests
from requests.structures import CaseInsensitiveDict
import csv
import io
import datetime as dt
import streamlit as st
from streamlit_option_menu import option_menu

st.set_page_config(
    page_title="Análisis Impacto Covid EEUU",
    layout="wide"
)

st.title("Análisis Impacto COVID19 EEUU")

@st.cache_data
def get_data():
    headers = CaseInsensitiveDict()
    headers["Accept"] = "application/json"
    headers['X-App-Token'] = 'IMOet43b8hwoSHaZuEUxhiEId'


    url = 'https://healthdata.gov/resource/g62h-syeh.csv?$limit=48000'

    data = requests.get(url, headers=headers)
    data_df = pd.read_csv(io.StringIO(data.text), parse_dates=['date'])
    data_df.sort_values('date', inplace=True)
    data_df.reset_index(inplace=True, drop=True)
    data_df = data_df[data_df['date'] <= '2022-08-01']
    return data_df

df = get_data()

with st.sidebar:
    choose = option_menu("Menú", ['Introducción', 'Dashboard', 'Top 5 Ocupación hospitalaria', 
                         'Ocupación hospitalaria Nueva York', 'Ocupación camas UCI 2020',
                         'Ocupación hospitalaria pediatría 2020', 'Porcentaje ocupación camas UCI casos covid',
                         'Muertes por estado, 2021', 'Relación personal médico faltante y muertes',
                         'Peor més de la pandemia', 'Recomendaciones'],
                         icons=['info-square', 'arrow-right-circle', 'arrow-right-circle', 'arrow-right-circle',
                          'arrow-right-circle', 'arrow-right-circle', 'arrow-right-circle', 'arrow-right-circle',
                           'arrow-right-circle', 'arrow-right-circle', 'arrow-right-circle'],
                         menu_icon="app", default_index=0,
                         styles={"nav-link": {"font-size": "16px", "text-align": "left", "margin":"0px", "--hover-color": "#1BF744"}, 
                         "nav-link-selected": {"background-color": "#02ab21"}})

if choose == 'Introducción':
    st.subheader('¿Qué es el COVID19?')
    st.markdown(
        """
        <div style="text-align: justify;">
        La pandemia del COVID-19 ha afectado el planeta desde el 2020. El primer caso de 
        esta enfermedad fue reportado en Wuhan, China el 31 de diciembre de 2019. Es una 
        enfermedad infecciosa causada por el SARS-CoV-2, produce síntomas que incluyen 
        fiebre, tos, dificultad respiratoria, dolor muscular y fatiga. En casos graves 
        puede producir neumonía, síndrome de dificultad respiratoria aguda, sepsis y 
        choque circulatorio.

        Según la OMS la infección mortal es entre el 0.5% y el 1% de los casos.

        La transmisión del virus se produce mediante pequeñas gotas que se emiten al hablar, 
        estornudar, toser o espirar, que al ser despedidas por un portador pasan directamente 
        a otra persona mediante la inhalación o mediante el contacto con objetos y/o superficies 
        contaminadas, mediante el contacto con las membranas de las mucosas orales, nasales y oculares.


        Se estima que los síntomas aparecen entre dos y catorce días, con un promedio de cinco días, 
        después de la infección. El contagio se puede prevenir con el lavado de manos frecuente, con la 
        desinfección de las manos con alcohol y el uso de tapabocas.
        """, unsafe_allow_html=True)

    st.subheader("COVID19 en EEUU")
    st.markdown("""
        <div style="text-align: justify;">
        En Estados Unidos el primer caso fue reportado el 21 de enero de 2020. Dos días después la 
        administración del Presidente Trump declaró una emergencia de salud pública y anunció restricciones 
        a los viajeros provenientes de China. Al día de hoy se estiman 92 millones de casos confirmados y 1 
        millón de fallecidos.

        Una de las razones por la que en Estados Unidos se ha tenido un crecimiento desproporcionado en los 
        casos de COVID-19 se atribuye a la división partidista con respecto a la pandemia. Una encuesta realizada 
        por medios de comunicación a mediados de marzo, mostró que el 76% de los demócratas consideraba la enfermedad 
        como una amenaza real, mientras que solo el 40% de los republicanos estaban de acuerdo. En otra encuesta realizada 
        en marzo por la Kaiser Family Foundation mostró que el 83% de los demócratas había tomado precauciones contra el virus 
        mientras que solo el 53% de los republicanos había hecho lo mismo.

        Dicha división y otros factores llevaron a que la tasa de infección incrementara hasta el punto de saturar las instituciones 
        médicas del país, haciendo que estas tuvieran que transferir pacientes e incluso rechazar y/o terminar el tratamiento de 
        pacientes con alto riesgo de fallecimiento. También se presentó una escasez de productos médicos, lo que conllevó a protestas 
        del personal médico. Adicionalmente los inventarios de existencia de equipos de protección personal no eran los suficientes 
        al inicio de la pandemia. Todo esto conllevó a que el personal médico también se viera infectado y de esta manera se redujo la 
        disponibilidad de servicios médicos y de la atención disponible.

        Hoy en día Estados Unidos es uno de los países con mayor tasa de vacunación del mundo, también con uno de los inventarios más 
        enormes de vacunas. Se estima que para este año hay 262 millones de ciudadanos con al menos una dosis de la vacuna y 223 millones 
        vacunados completamente.

        El siguiente gráfico muestra la distribución de casos en Estados Unidos desde Enero del 2021 a hoy
        </div>
        """, unsafe_allow_html=True
    )

    @st.cache_data
    def casos_totales():
        data_us = pd.read_csv('https://raw.githubusercontent.com/nytimes/covid-19-data/master/us.csv', parse_dates=['date'])
        fig, ax = plt.subplots(figsize=(16, 5), dpi=600)
        sns.lineplot(x='date', y='cases', data=data_us, ax=ax)

        ax.set_xticklabels(ax.get_xticklabels(), rotation=45)
        ax.set_xlabel('')
        ax.set_ylabel('Número de casos (10 millones)')
        ax.set_title('Casos COVID19 Estados Unidos Enero 2020 a hoy', fontsize=16)
        sns.despine(ax=ax, left=False, bottom=False)

        return fig

    st.pyplot(casos_totales())

elif choose == 'Top 5 Ocupación hospitalaria':

    def top():
        data = df.copy()
        data = data[['state', 'date', 'inpatient_beds_used_covid',
        'total_adult_patients_hospitalized_confirmed_covid',
        'staffed_icu_adult_patients_confirmed_covid',
        'total_pediatric_patients_hospitalized_confirmed_covid',
        'staffed_icu_pediatric_patients_confirmed_covid']]

        data.rename(columns={
            'inpatient_beds_used_covid': 'beds_covid',
            'total_adult_patients_hospitalized_confirmed_covid': 'adults_hospt',
            'staffed_icu_adult_patients_confirmed_covid': 'adults_uci',
            'total_pediatric_patients_hospitalized_confirmed_covid': 'children_hospt',
            'staffed_icu_pediatric_patients_confirmed_covid': 'children_uci'
        }, inplace=True)

        data.fillna(0, inplace=True)
        data['total_cases'] = df.iloc[:, 3:7].sum(axis=1)

        data = data[data['date'] < '2020-07-01']
        data['month_string'] = [d.strftime('%b') for d in data.date]
        df_group = data.groupby('state')[['beds_covid','total_cases']].sum()
        df_group.sort_values('beds_covid', ascending=False, inplace=True)
        top_5 = df_group.head(5).copy()
        top_5['beds_covid'] = [int(i) for i in top_5['beds_covid']]
        top_5['states_full'] = ['Nueva York', 'California', 'Florida', 'Texas', 'Illinois']

        return top_5

    def fig_top_5(top):

        fig,ax = plt.subplots(figsize=(10, 5))
        sns.barplot(x='beds_covid', y='states_full', data=top_5)

        ax.set_axisbelow(True)
        ax.grid(axis = "x", color="#A8BAC4", lw=1.2)
        ax.spines["right"].set_visible(False)
        ax.spines["top"].set_visible(False)
        ax.spines["bottom"].set_visible(False)
        ax.spines["left"].set_lw(1.5)
        ax.xaxis.set_tick_params(labelbottom=False, labeltop=True, length=0)

        plt.ylabel('')
        plt.xlabel('')

        fig.subplots_adjust(left=0.005, right=1, top=0.8, bottom=0.1)
        fig.text(
            0, 0.925, "Número de camas ocupadas", 
            fontsize=16, fontweight="bold"
        )
        fig.text(
            0, 0.875, "Periodo 2020-01-01 a 2020-06-30", 
            fontsize=14
        )
        source = "Fuente: U.S. Department of Health & Human Services - HealthData.gov"
        fig.text(
            0, 0.06, source, color="#a2a2a2", 
            fontsize=14, fontfamily="Econ Sans Cnd"
        )
        fig.add_artist(lines.Line2D([0, 1], [1, 1], lw=3, color='red', solid_capstyle="butt"))
        fig.add_artist(patches.Rectangle((0, 0.975), 0.05, 0.025, color='red'))
    
        return fig

    top_5 = top()
    st.write(fig_top_5(top_5))

    st.table(top_5)
    
    st.markdown("""
    <div style="text-align: justify;">
    Los 5 estados con mayor ocupación de camas son New York, California, Florida, Texas e Illinois. 
    No se usó la columna de rango etario, ya que mostraba información incompleta. Analizando los 
    resultados encontrados, se observa grandes cantidades de usos de camas para, relativamente, pocos 
    casos. Esto puede ser a que la información no está bien cargada, o las columnas usadas para realizar 
    el cálculo del número de casos no aportaban la información correcta. Aun así se puede realizar un 
    análisis, los estados con más camas ocupadas son cinco de los seis estados más poblados de Estados 
    Unidos, también son estados que sufrieron brotes muy grandes al inicio de la pandemia, llegando a 
    tener incluso problemas en la atención de pacientes con COVID-19
    </div>
    """, unsafe_allow_html=True)

elif choose == 'Ocupación hospitalaria Nueva York':
    def ny_plot(data_df):
        df_ny = data_df[((data_df['date'] >= '2020-03-20') & (data_df['date'] <= '2020-08-31'))]
        df_ny = df_ny[df_ny['state'] == 'NY']
        fig, ax = plt.subplots(figsize=(15, 5))
        sns.lineplot(x='date', y='inpatient_beds_used_covid', data=df_ny)

        plt.axvline(pd.to_datetime('2020-06-13'), color='red', ls='--')

        ticks = [pd.to_datetime('2020-03-20'), pd.to_datetime('2020-04-01'), pd.to_datetime('2020-04-15'),
                pd.to_datetime('2020-04-30'), pd.to_datetime('2020-05-15'), pd.to_datetime('2020-05-31'),
                pd.to_datetime('2020-06-13'), pd.to_datetime('2020-06-30'), pd.to_datetime('2020-07-15'), 
                pd.to_datetime('2020-07-30'), pd.to_datetime('2020-08-15'), pd.to_datetime('2020-08-31')]

        plt.xticks(ticks, rotation=45)

        plt.xlabel('')
        plt.ylabel('Número de camas ocupadas')
        sns.despine(left=False, bottom=False)

        fig.subplots_adjust(left=0.005, right=1, top=0.8, bottom=0.1)
        fig.text(
            0, 0.925, "Ocupación de camas hospitalarias comunes durante el programa NYS on Pause",
            fontsize=16, fontweight="bold"
        )
        fig.text(
            0, 0.875, "2020-03-20 a 2020-06-13", 
            fontsize=14
        )
        source = "Fuente: U.S. Department of Health & Human Services - HealthData.gov"
        fig.text(
            0, -0.15, source, color="#a2a2a2", 
            fontsize=14, fontfamily="Econ Sans Cnd"
        )
        fig.add_artist(lines.Line2D([0, 1], [1, 1], lw=3, color='red', solid_capstyle="butt"))
        fig.add_artist(patches.Rectangle((0, 0.975), 0.05, 0.025, color='red'))

        return fig

    st.write(ny_plot(df))

    st.markdown(
        """
        <div style="text-align: justify;">
        Al iniciar el periodo de cuarentena se viene con un crecimiento lineal en el número de hospitalizaciones, 
        finalizando el mes de marzo, se inicia un periodo de crecimiento exponencial llegando a un primer pico de 
        10000 camas ocupadas. Este pico sigue incrementando hasta llegar a casi 13000 camas. Hacia el 15 de abril 
        se tiene el pico absoluto de camas ocupadas rozando las 14000. A partir de los días posteriores se ve un 
        decrecimiento general con picos en algunos momentos, el primero hacia el 20 de abril y el segundo hacia el 
        15 de mayo coincidiendo con la autorización de reuniones de más de 10 personas. La línea punteada muestra la 
        fecha del fin del programa, se agregó dos meses más de información para realizar una comparación con el programa, 
        encontrando de esta manera, un pico justo al finalizar el programa, que se debe a la reapertura del estado y su 
        economía, sin embargo este pico no dura más de dos semanas y el decrecimiento en la ocupación hospitalaria decrece 
        constantemente y casi que se estabiliza en aproximadamente 3500 camas. Algo adicional que se puede mencionar es el 
        aplanamiento de la curva, tal como se ve en el gráfico se pasó de un pico epidémico a una curva aplana en la que van 
        a haber pequeños picos a futuro.
        </div>
        """, unsafe_allow_html=True
    )


elif choose == 'Ocupación camas UCI 2020':
    def uci_plot(data_df):
        df = data_df[data_df['date'] < '2021-01-01']
        df = df[['state', 'staffed_icu_adult_patients_confirmed_covid']]
        df_group = df.groupby('state').sum()
        df_group.sort_values('staffed_icu_adult_patients_confirmed_covid', ascending=False, inplace=True)
        camas_icu = df_group.head(5).copy()
        camas_icu['states_full'] = ['Texas', 'California', 'Florida', 'Georgia', 'Ohio']
        fig,ax = plt.subplots(figsize=(12, 7))
        sns.barplot(x='staffed_icu_adult_patients_confirmed_covid', y='states_full', data=camas_icu)

        ax.set_axisbelow(True)
        ax.grid(axis = "x", color="#A8BAC4", lw=1.2)
        ax.spines["right"].set_visible(False)
        ax.spines["top"].set_visible(False)
        ax.spines["bottom"].set_visible(False)
        ax.spines["left"].set_lw(1.5)
        ax.xaxis.set_tick_params(labelbottom=False, labeltop=True, length=0)

        plt.ylabel('')
        plt.xlabel('')

        fig.subplots_adjust(left=0.005, right=1, top=0.8, bottom=0.1)
        fig.text(
            0, 0.925, "Número de camas ICU ocupadas", 
            fontsize=16, fontweight="bold"
        )
        fig.text(
            0, 0.875, "Periodo 2020-01-01 a 2020-12-31", 
            fontsize=14
        )
        source = "Fuente: U.S. Department of Health & Human Services - HealthData.gov"
        fig.text(
            0, 0.06, source, color="#a2a2a2", 
            fontsize=14, fontfamily="Econ Sans Cnd"
        )
        fig.add_artist(lines.Line2D([0, 1], [1, 1], lw=3, color='red', solid_capstyle="butt"))
        fig.add_artist(patches.Rectangle((0, 0.975), 0.05, 0.025, color='red'))

        return fig

    st.write(uci_plot(df))
    st.markdown(
        """
        <div style="text-align: justify;">
        Los estados de Texas, California, Florida, Georgia y Ohio son los estados con más ocupación 
        de camas UCI en los estados unidos durante el año 2020. De estos 5, solo Texas, California y 
        Florida aparecen en el top 5 con mayor ocupación hospitalaria. Se puede argumentar que Georgia 
        y Ohio tuvieron que enfrentar casos más graves de covid durante el año en mención. También es 
        interesante notar que Nueva York, que fue el estado que usó más camas comunes, no aparece en el 
        top 5 de uso de camas de cuidado intensivo, así que se puede asumir que Nueva York tuvo menos casos 
        graves y/o la atención dada en este estado a los pacientes con COVID-19 fue mejor evitando la admisión 
        de pacientes en UCI
        </div>
        """, unsafe_allow_html=True
    )

elif choose == 'Ocupación hospitalaria pediatría 2020':
    def peds_plot(data_df):
        df = data_df[data_df['date'] < '2021-01-01']
        df = df[['state', 'total_pediatric_patients_hospitalized_confirmed_covid']]
        df_group = df.groupby('state').sum()
        df_group.sort_values('total_pediatric_patients_hospitalized_confirmed_covid', ascending=False, inplace=True)
        peds = df_group.head(5).copy()
        peds['states_full'] = ['Texas', 'California', 'Florida', 'Arizona', 'Pensilvania']

        fig,ax = plt.subplots(figsize=(12, 7))
        sns.barplot(x='total_pediatric_patients_hospitalized_confirmed_covid', y='states_full', data=peds)

        ax.set_axisbelow(True)
        ax.grid(axis = "x", color="#A8BAC4", lw=1.2)
        ax.spines["right"].set_visible(False)
        ax.spines["top"].set_visible(False)
        ax.spines["bottom"].set_visible(False)
        ax.spines["left"].set_lw(1.5)
        ax.xaxis.set_tick_params(labelbottom=False, labeltop=True, length=0)

        plt.ylabel('')
        plt.xlabel('')

        fig.subplots_adjust(left=0.005, right=1, top=0.8, bottom=0.1)
        fig.text(
            0, 0.925, "Número de camas pediátricas ocupadas", 
            fontsize=16, fontweight="bold"
        )
        fig.text(
            0, 0.875, "Periodo 2020-01-01 a 2020-06-30", 
            fontsize=14
        )
        source = "Fuente: U.S. Department of Health & Human Services - HealthData.gov"
        fig.text(
            0, 0.06, source, color="#a2a2a2", 
            fontsize=14, fontfamily="Econ Sans Cnd"
        )
        fig.add_artist(lines.Line2D([0, 1], [1, 1], lw=3, color='red', solid_capstyle="butt"))
        fig.add_artist(patches.Rectangle((0, 0.975), 0.05, 0.025, color='red'))

        return fig

    st.write(peds_plot(df))
    st.markdown(
        """
        <div style="text-align: justify;">
       En el caso de camas pediátricas, Texas, California y Florida vuelven a aparecer, estos son 
       los 3 estados más poblados de la comunidad americana. Los sigue Arizona y Pensilvania, que 
       son el quinto y catorceavo estado en población respectivamente. Algo importante a decir es 
       que la Academia Americana de pediatría, solo recopila datos de 49 estados de los Estados 
       Unidos con respecto al covid, dentro de los cuales no se encuentra Texas, que solo reporta 
       una pequeña porción de los casos relacionados con menores de edad, por lo que los casos en 
       Texas pueden ser más de lo reportado. Así pues la información sobre la ocupación de camas de 
       pediatría no es muy confiable. Sin embargo, es preocupante la cantidad de camas ocupadas por 
       pacientes menores de edad.
        </div>
        """, unsafe_allow_html=True
    )

elif choose == 'Porcentaje ocupación camas UCI casos covid':
    def per_uci(data_df):
        df = data_df[['state', 'total_staffed_adult_icu_beds', 'staffed_adult_icu_bed_occupancy']].copy()
        df.rename(columns={
            'total_staffed_adult_icu_beds' : 'icu_beds_available',
            'staffed_adult_icu_bed_occupancy' : 'icu_beds_occupied'
        }, inplace=True)
        df_grouped = df.groupby('state').sum()
        df_grouped['%_occupation'] = round((df_grouped['icu_beds_occupied'] / df_grouped['icu_beds_available']) * 100, 3)
        df_grouped.sort_values('%_occupation', ascending=False, inplace=True)

        data_plot = {
            'type':'choropleth',
            'locations':df_grouped.index.values,
            'locationmode': 'USA-states',
            'z':df_grouped['%_occupation']
        }

        layout = {'title':'Porcentaje ocupación camas UCI desde Enero 2020 a hoy',
                'geo':{'scope':'usa'},
                'height': 600,
                'width': 900}

        x = pg.Figure(data = [data_plot], layout=layout)
        return x

    st.plotly_chart(per_uci(df))
    st.markdown("""
    <div style="text-align: justify;">
    Texas ocupa el primer lugar en el porcentaje de camas UCI ocupadas con un 87%, lo cual es interesante, 
    ya que como se ha mencionado anteriormente, Texas es el segundo estado con más población en los Estados 
    Unidos. Alabama ocupa el segundo lugar con una ocupación del 85%. Rhode Island ocupa la tercera posición 
    con un 83% de ocupación, le sigue Georgia y Nuevo México con un 82 y 81% respectivamente. Ninguno de estos 
    estados estuvo en una cuarentena obligatoria. En comparación el estado de Wyoming, que tampoco tuvo cuarentena, 
    es el estado con menor porcentaje de ocupación con apenas 41%. Esto se debe a que este estado es el que menos 
    población tiene (sin tener en cuenta los territorios insulares de Estados Unidos en el Atlántico y Pacífico)
    </div>
    """, unsafe_allow_html=True)

elif choose == 'Muertes por estado, 2021':
    def muertes_plot(data_df):
        df = data_df[(data_df['date'] >= '2021-01-01') & (data_df['date'] < '2022-01-01')].copy()
        df = df[['state', 'deaths_covid']]
        df_grouped = df.groupby('state').sum()
        df_grouped.sort_values('deaths_covid', inplace=True, ascending=False)
        data_plot = {
            'type':'choropleth',
            'locations':df_grouped.index.values,
            'locationmode': 'USA-states',
            'z':df_grouped['deaths_covid']
        }

        layout = {'title':'Muertes por estado desde Enero 2020 a hoy',
                'geo':{'scope':'usa'},
                'height': 600,
                'width': 900}

        x = pg.Figure(data = [data_plot], layout=layout)

        return x

    st.plotly_chart(muertes_plot(df))
    st.markdown("""
    <div style="text-align: justify;">
    Por tendencia los estados con mayor población ocupan los primeros lugares en 
    la cantidad de muertes por COVID-19. El caso más interesante es de Arizona que 
    ocupa el 14vo lugar en población, pero el quinto en número de fallecimientos. 
    Este estado no tuvo una cuarentena obligatoria y tampoco ha tenido éxito en su 
    plan de vacunación debido a la resistencia de las personas por razones políticas y religiosas.
    </div>
    """, unsafe_allow_html=True)

elif choose == 'Relación personal médico faltante y muertes':
    def relacion_plot(data_df):
        df = data_df[(data_df['date'] >= '2021-01-01') & (data_df['date'] < '2022-01-01')].copy()
        df = df[['state', 'deaths_covid', 'critical_staffing_shortage_today_yes']]
        df_grouped = df.groupby('state').sum()
        df_grouped.sort_values('deaths_covid', inplace=True, ascending=False)

        x = df_grouped['deaths_covid']
        y = df_grouped['critical_staffing_shortage_today_yes']

        fig,ax = plt.subplots(figsize=(7, 7))
        sns.scatterplot(x=x, y=y, data=df_grouped)
        ax.set_xlabel('Muertes por covid')
        ax.set_ylabel('Número de hospitales con falta de personal')

        fig.subplots_adjust(left=0.005, right=1, top=0.8, bottom=0.1)
        fig.text(
            0, 0.925, "Relación entre muertes por COVID-19 y Falta de personal médico", 
            fontsize=16, fontweight="bold"
        )
        fig.text(
            0, 0.875, "Periodo 2020-01-01 a 2020-06-30", 
            fontsize=14
        )
        source = "Fuente: U.S. Department of Health & Human Services - HealthData.gov"
        fig.text(
            0, 0, source, color="#a2a2a2", 
            fontsize=14, fontfamily="Econ Sans Cnd"
        )
        fig.add_artist(lines.Line2D([0, 1], [1, 1], lw=3, color='red', solid_capstyle="butt"))
        fig.add_artist(patches.Rectangle((0, 0.975), 0.05, 0.025, color='red'))
        sns.despine(left=False, bottom=False)

        return fig

    st.write(relacion_plot(df))
    st.markdown("""
    <div style="text-align: justify;">
    Para revisar la relación entre muertes por covid y la falta de personal médico se realizó un 
    diagrama de dispersión. Si bien no se encontró una relación lineal, se puede observar que en 
    ciertas cantidades de muertes hubo un número similar o cercano de hospitales con falta de personal. 
    Y lógicamente la falta de personal puede conllevar a que se deba cerrar unidades de cuidado intensivo, 
    priorizar atención a ciertos pacientes o incluso negar la atención de pacientes con casos graves.
    </div>
    """, unsafe_allow_html=True)


elif choose == 'Peor mes de la pandemia':

    def plot_info(data_df):
        df = data_df[['date', 'state', 'deaths_covid', 
         'critical_staffing_shortage_today_yes', 
         'total_staffed_adult_icu_beds', 
         'total_adult_patients_hospitalized_confirmed_covid',
         ]].copy()

        df['month'] = pd.DatetimeIndex(df['date']).month
        df['year'] = df['date'].dt.isocalendar().year
        df = df.drop(columns=['date'])
        cols_to_sum = ['deaths_covid', 'critical_staffing_shortage_today_yes',
               'staffed_adult_icu_bed_occupancy', 'total_adult_patients_hospitalized_confirmed_covid']

        df_grouped = df.groupby(['year', 'month'])[cols_to_sum].sum()
        df_grouped.sort_values(['deaths_covid'], inplace=True, ascending=False)
        df_grouped.reset_index(inplace=True)

        fig,ax = plt.subplots(2,2, figsize=(12, 7))
        ax = ax.flatten()
        df_grouped.year = pd.Categorical(df_grouped.year)
        sns.lineplot(ax=ax[0], x='month', y='deaths_covid', data=df_grouped, hue='year')
        sns.lineplot(ax=ax[1], x='month', y='critical_staffing_shortage_today_yes', data=df_grouped, hue='year')
        sns.lineplot(ax=ax[2], x='month', y='total_staffed_adult_icu_beds', data=df_grouped, hue='year')
        sns.lineplot(ax=ax[3], x='month', y='total_adult_patients_hospitalized_confirmed_covid', data=df_grouped, hue='year')


        ax[0].set_xlabel("")
        ax[0].set_ylabel("Muertes por Covid")

        ax[1].set_xlabel("")
        ax[1].set_ylabel("# Hospitales sin personal")

        ax[2].set_xlabel("")
        ax[2].set_ylabel("Total camas UCI ocupadas")

        ax[3].set_xlabel("")
        ax[3].set_ylabel("Total pacientes adultos hospitalizados")

        handles, labels = ax[0].get_legend_handles_labels()
        ax[0].legend(handles, labels, loc=1, bbox_to_anchor=(0.95,0.99), ncol=3, bbox_transform=fig.transFigure)
        ax[1].legend([],[], frameon=False)
        ax[2].legend([],[], frameon=False)
        ax[3].legend([],[], frameon=False)

        fig.subplots_adjust(left=0.005, right=1, top=0.8, bottom=0.1)
        fig.text(
            0, 0.910, "Muertes por covid, Número de hospitales sin personal disponible, \nTotal camas UCI ocupadas, Total adultos hospitalizados", 
            fontsize=16, fontweight="bold"
        )
        fig.text(
            0, 0.875, "Periodo 2020-01-01 a 2022-08-01", 
            fontsize=14
        )
        source = "Fuente: U.S. Department of Health & Human Services - HealthData.gov"
        fig.text(
            0, 0, source, color="#a2a2a2", 
            fontsize=14, fontfamily="Econ Sans Cnd"
        )
        fig.add_artist(lines.Line2D([0, 1], [1, 1], lw=3, color='red', solid_capstyle="butt"))
        fig.add_artist(patches.Rectangle((0, 0.975), 0.05, 0.025, color='red'))
        sns.despine(left=False, bottom=False)

        return fig

    st.write(plot_info(df))
    st.markdown("""
    <div style="text-align: justify;">
    Se graficó el número de muertes por covid, el número de hospitales sin personal disponible, el 
    total de camas UCI ocupadas y el total de pacientes adultos hospitalizados para evaluar su desempeño 
    durante los años que lleva la pandemia. Es interesante notar como todas las graficas incrementan 
    hacia el final del año 2020. En el caso del total de camas ocupadas el año 2021 se mantuvo relativamente 
    constante, disminuyendo un poco durante este año y luego ha tenido una caida dramatica, aunque se puede 
    argumentar que no se debe estar reportando los datos desde Julio de este año para este item.
    
    Algo en común que tienen las cuatro gráficas es que para el 2020 todas finalizan en picos y el 2021 
    inicia con dicho pico. A excepción del total de pacientes adultos hospitalizados cuyo mayor pico 
    ocurre en enero de 2022. Pero aún así teninedo en cuenta esto, se puede argumentar que los peores 
    meses de la pandemia son Diciembre y Enero de 2020 y 2021 respectivamante. Eso se debe a la falta 
    de prevención de los ciudadanos durante las fiestas de navidad y año nuevo.
    </div>
    """, unsafe_allow_html=True)

elif choose == 'Dashboard':

    tab1, tab2, tab3, tab4 = st.tabs(['Mapa hospitalizaciones', 'Uso camas UCI por estado', 
                                      'Estados con mayor ocupación hospitalaria', 
                                      'Cantidad de camas ocupadas por COVID-19'])

    with tab1:
        def hosp_plot(data_df):
            df = data_df[['state', 'total_adult_patients_hospitalized_confirmed_covid', 'staffed_icu_adult_patients_confirmed_covid',
                          'total_pediatric_patients_hospitalized_confirmed_covid']].copy()
            df['total_occupation'] = df[['total_adult_patients_hospitalized_confirmed_covid', 'staffed_icu_adult_patients_confirmed_covid',
                                    'total_pediatric_patients_hospitalized_confirmed_covid']].sum(axis=1)
            df_grouped = df.groupby('state').sum()
            df_grouped.sort_values('total_occupation', ascending=False, inplace=True)

            data_plot = {
                'type':'choropleth',
                'locations':df_grouped.index.values,
                'locationmode': 'USA-states',
                'z':df_grouped['total_occupation']
            }

            layout = {'title':'Total hospitalizados desde Enero 2020 a hoy',
                    'geo':{'scope':'usa'},
                    'height': 600,
                    'width': 900}

            x = pg.Figure(data = [data_plot], layout=layout)

            return x
        st.plotly_chart(hosp_plot(df))
        st.markdown("""
            <div style="text-align: justify;">
            Los estados con mayor población son los estados con mayor cantidad de pacientes 
            hospitalizados. Texas ocupa el primer lugar sobre California a pesar de ser el 
            segundo estado más poblado de Estados Unidos, sin embargo, es uno si no el principal 
            estado en oponerse a cualquier método de prevención de la COVID-19 debido a motivos 
            políticos y religiosos. Ahora bien, atribuir la cantidad de pacientes hospitalizados a 
            temas políticos y religiosos no es tan correcto cuando se evalúa el caso de California 
            con por lo menos 300.000 hospitalizaciones menos. Este fue uno de los estados con casos 
            más graves de ocupación hospitalaria en la que incluso se presentaron congestiones masivas 
            en las zonas de descarga de pacientes en las salas de emergencias y esto a pesar de que 
            este estado tuvo la cuarentena más larga del país, 453 días comprendidos entre el 19 de 
            marzo del 2020 hasta el 15 de junio del 2021. Florida ocupa el tercer lugar y es uno de 
            los estados en los que más polémica hubo debido a que al inicio de la pandemia no se 
            cerró el estado ni se controló la afluencia de turistas y fue considerado un foco de 
            expansión del virus durante las vacaciones de primavera. Nueva York, en el cuarto lugar, 
            también fue considerado como uno de los principales focos de infección en el país, pero a 
            diferencia de Florida, esto se da, ya que la mayoría de vuelos internacionales llegan a 
            este estado, adicionalmente la ciudad de Nueva York es una de las más concurridas del país.
            </div>
            """, unsafe_allow_html=True)

    with tab2:
        def per_uci(data_df):
            df = data_df[['state', 'staffed_icu_adult_patients_confirmed_covid', 'staffed_adult_icu_bed_occupancy']].copy()
            df_grouped = df.groupby('state').sum()
            df_grouped['icu_occupation'] = df_grouped[['staffed_icu_adult_patients_confirmed_covid', 
                                                    'staffed_adult_icu_bed_occupancy']].sum(axis=1)
            df_grouped.sort_values('icu_occupation', ascending=False, inplace=True)

            data_plot = {
                'type':'choropleth',
                'locations':df_grouped.index.values,
                'locationmode': 'USA-states',
                'z':df_grouped['icu_occupation']
            }

            layout = {'title':'Total ocupación camas UCI desde Enero 2020 a hoy',
                    'geo':{'scope':'usa'},
                    'height': 600,
                    'width': 900}

            x = pg.Figure(data = [data_plot], layout=layout)

            return x

        st.plotly_chart(per_uci(df))
        st.markdown("""
            <div style="text-align: justify;">
            En el caso de la ocupación de camas de cuidados intensivos tenemos la misma distribución 
            que la cantidad de hospitalizados, y es que a las unidades de cuidados intensivos llegaban 
            los casos graves de COVID-19. Es interesante que los números de ocupación de camas UCI y de 
            hospitalización son similares. Si bien la columna staffed_icu_adult_patients_confirmed_covid 
            se usó en el cálculo del número de hospitalizaciones, no se encuentra una explicación para haber 
            obtenido números similares a menos que se considere que Estados Unidos al día de hoy ha reportado 
            más de 92 millones de casos y debido a la gran cantidad de casos efectivamente 5 millones de personas 
            en Texas han ocupado una cama UCI.
            </div>
            """, unsafe_allow_html=True)

    with tab3:
        def top():
            data = df.copy()
            data = data[['state', 'date', 'inpatient_beds_used_covid',
            'total_adult_patients_hospitalized_confirmed_covid',
            'staffed_icu_adult_patients_confirmed_covid',
            'total_pediatric_patients_hospitalized_confirmed_covid',
            'staffed_icu_pediatric_patients_confirmed_covid']]

            data.rename(columns={
                'inpatient_beds_used_covid': 'beds_covid',
                'total_adult_patients_hospitalized_confirmed_covid': 'adults_hospt',
                'staffed_icu_adult_patients_confirmed_covid': 'adults_uci',
                'total_pediatric_patients_hospitalized_confirmed_covid': 'children_hospt',
                'staffed_icu_pediatric_patients_confirmed_covid': 'children_uci'
            }, inplace=True)

            data.fillna(0, inplace=True)
            data['total_cases'] = df.iloc[:, 3:7].sum(axis=1)

            data['month_string'] = [d.strftime('%b') for d in data.date]
            df_group = data.groupby('state')[['beds_covid','total_cases']].sum()
            df_group.sort_values('beds_covid', ascending=False, inplace=True)
            top_5 = df_group.head(5).copy()
            top_5['beds_covid'] = [int(i) for i in top_5['beds_covid']]
            return top_5

        def fig_top_5(top):

            fig,ax = plt.subplots(figsize=(10, 5))
            sns.barplot(x='beds_covid', y=top_5.index, data=top_5)

            ax.set_axisbelow(True)
            ax.grid(axis = "x", color="#A8BAC4", lw=1.2)
            ax.spines["right"].set_visible(False)
            ax.spines["top"].set_visible(False)
            ax.spines["bottom"].set_visible(False)
            ax.spines["left"].set_lw(1.5)
            ax.xaxis.set_tick_params(labelbottom=False, labeltop=True, length=0)

            plt.ylabel('')
            plt.xlabel('')

            fig.subplots_adjust(left=0.005, right=1, top=0.8, bottom=0.1)
            fig.text(
                0, 0.925, "Número de camas ocupadas", 
                fontsize=16, fontweight="bold"
            )
            fig.text(
                0, 0.875, "Periodo 2020-01-01 a 2022-08-01", 
                fontsize=14
            )
            source = "Fuente: U.S. Department of Health & Human Services - HealthData.gov"
            fig.text(
                0, 0.06, source, color="#a2a2a2", 
                fontsize=14, fontfamily="Econ Sans Cnd"
            )
            fig.add_artist(lines.Line2D([0, 1], [1, 1], lw=3, color='red', solid_capstyle="butt"))
            fig.add_artist(patches.Rectangle((0, 0.975), 0.05, 0.025, color='red'))
        
            return fig

        top_5 = top()
        st.write(fig_top_5(top_5))

        st.table(top_5)

    with tab4:
        def plot_camas(data_df):

            min_date = dt.date(year=2020,month=1,day=1)
            max_date = dt.date(year=2022,month=8,day=1)
            st.subheader("Seleccione un periodo de fechas")
            start_date, end_date = st.slider("Fechas disponibles", min_value=min_date, value=(min_date, max_date), 
                                            max_value=max_date, format="YYYY/MM/DD")
            
            start_date_trans = pd.to_datetime(start_date)
            end_date_trans = pd.to_datetime(end_date)

            df = data_df[(data_df['date'] >= start_date_trans) & (data_df['date'] <= end_date_trans)]
            df = df[['state', 'inpatient_beds_used_covid']]
            df_group = df.groupby('state').sum()
            df_group.sort_values('inpatient_beds_used_covid', ascending=False, inplace=True)
            camas = df_group.head(5).copy()
            fig,ax = plt.subplots(figsize=(12, 7))
            sns.barplot(x='inpatient_beds_used_covid', y=camas.index, data=camas)

            ax.set_axisbelow(True)
            ax.grid(axis = "x", color="#A8BAC4", lw=1.2)
            ax.spines["right"].set_visible(False)
            ax.spines["top"].set_visible(False)
            ax.spines["bottom"].set_visible(False)
            ax.spines["left"].set_lw(1.5)
            ax.xaxis.set_tick_params(labelbottom=False, labeltop=True, length=0)

            plt.ylabel('')
            plt.xlabel('')

            fig.subplots_adjust(left=0.005, right=1, top=0.8, bottom=0.1)
            fig.text(
                0, 0.925, "Número de camas ocupadas pacientes con COVID-19", 
                fontsize=16, fontweight="bold"
            )
            fig.text(
                0, 0.875, f"Periodo {start_date} a {end_date}", 
                fontsize=14
            )
            source = "Sources: U.S. Department of Health & Human Services - HealthData.gov"
            fig.text(
                0, 0.06, source, color="#a2a2a2", 
                fontsize=14, fontfamily="Econ Sans Cnd"
            )
            fig.add_artist(lines.Line2D([0, 1], [1, 1], lw=3, color='red', solid_capstyle="butt"))
            fig.add_artist(patches.Rectangle((0, 0.975), 0.05, 0.025, color='red'))
            return fig

        st.write(plot_camas(df))

elif choose == 'Recomendaciones':
    st.markdown("""
            <div style="text-align: justify;">
            Hay varias razones por las cuales Estados Unidos ha sido uno de los países más afectados por la pandemia del COVID-19. Tal vez una de las principales fue la falta de preparación para enfrentar la pandemia a pesar de ser uno de los países más ricos del mundo. Varias de las decisiones que llevaron a estos resultados fueron netamente políticas, como el cierre de la oficina de investigación y control de enfermedades en Wuhan por parte de la administración Trump, por el simple hecho de no querer tener relación alguna con China. Al igual que la salida de Estados Unidos de la Organización Mundial de la Salud. Ahora bien, este tipo de decisiones por parte de un mandatario son casi imposibles de controlar. Pero si se puede controlar asuntos como:


            1. La cantidad de insumos de protección personal almacenados en reservas estratégicas. El Departamento de Salud de los Estados Unidos estimó que la cantidad de reservas almacenadas era apenas el 1.2% de los 3500 millones de mascarillas faciales que se necesitaban para enfrentar la pandemia. Igualmente, un estudio de la CDC del 2015 encontró que se requerirían 7000 millones de mascarillas N95 para enfrentar un brote de enfermedad respiratoria severa. Así pues, se hace necesario incrementar la cantidad de equipos e insumos de protección personal almacenados como prevención a cualquier eventualidad



            2. Rastreo de contagios. Esta es una herramienta importante y que funcionó muy bien en países como Corea del Sur en el que se logró localizar y tomar muestras de clientes de bares nocturnos cuando se realizó la reapertura. Hay un debate muy importante sobre la privacidad de los usuarios al usar funcionalidades como la ubicación geográfica en tiempo real, pero esto se puede solucionar con una política de control de datos y con un software de código abierto que permita un adecuado control del sistema



            3. Testeo de contagios. Otro de los problemas presentados fue la demora en la realización de pruebas. Una encuesta realizada entre el 23 y 27 de marzo del 2020 en 323 hospitales de los estados unidos realizada por la oficina del Inspector General del Departamento de Salud de los Estados Unidos encontró que el tiempo de espera de los resultados podría sobrepasar los siete días. Lo que conllevaba a un incremento en el tiempo de ocupación de una cama hospitalaria, generando una reducción en la disponibilidad. Igualmente, esta demora conlleva a que no se pueda realizar un rastreo de contagios adecuado. Por lo tanto es necesario incrementar la disponibilidad de recursos y equipos para realizar testeos masivos en cortos periodos de tiempo



            4. Capacidad hospitalaria. El incontrolado contagio del virus llevó a varios centros médicos del país a rechazar la llegada de nuevos pacientes y a realizar traslados de pacientes, así como instaurar mandatos en los que se permitía rechazar el tratamiento de casos graves en pacientes con bajas opciones de recuperación. Junto con el adecuado rastreo y testeo de contagios se puede reducir la cantidad de personas que llegan a un hospital en busca de atención médica o de una prueba. Asimismo es necesario evaluar la duración de los programas de formación de médicos para evitar que el fallecimiento de personal médico impacte en la atención hospitalaria



            5. Flujo de Información. Si algo demostró la pandemia es el gran impacto de las noticias falsas en un evento de tal magnitud. Si bien es difícil controlar lo que un ciudadano pueda decir en sus redes sociales, el impacto de las noticias falsas puede ser disminuido si desde el mismo gobierno se entrega información clara y concisa sobre qué se sabe del virus, su comportamiento y los efectos que se esperan.
            </div>
            """, unsafe_allow_html=True)

elif choose == 'Peor més de la pandemia':
    def peor_plot(data_df):
        df = data_df[['date', 'state', 'deaths_covid', 
         'critical_staffing_shortage_today_yes', 
         'staffed_adult_icu_bed_occupancy', 
         'total_adult_patients_hospitalized_confirmed_covid',
         ]].copy()

        df['month'] = pd.DatetimeIndex(df['date']).month
        df['year'] = df['date'].dt.isocalendar().year

        df = df.drop(columns=['date'])

        df_grouped = df.groupby(['year', 'month']).sum()
        df_grouped.sort_values(['deaths_covid'], inplace=True, ascending=False)
        df_grouped.reset_index(inplace=True)

        fig,ax = plt.subplots(2,2, figsize=(12, 7))
        ax = ax.flatten()
        df_grouped.year = pd.Categorical(df_grouped.year)
        sns.lineplot(ax=ax[0], x='month', y='deaths_covid', data=df_grouped, hue='year')
        sns.lineplot(ax=ax[1], x='month', y='critical_staffing_shortage_today_yes', data=df_grouped, hue='year')
        sns.lineplot(ax=ax[2], x='month', y='staffed_adult_icu_bed_occupancy', data=df_grouped, hue='year')
        sns.lineplot(ax=ax[3], x='month', y='total_adult_patients_hospitalized_confirmed_covid', data=df_grouped, hue='year')


        ax[0].set_xlabel("")
        ax[0].set_ylabel("Muertes por Covid")

        ax[1].set_xlabel("")
        ax[1].set_ylabel("# Hospitales sin personal")

        ax[2].set_xlabel("")
        ax[2].set_ylabel("Total camas UCI ocupadas")

        ax[3].set_xlabel("")
        ax[3].set_ylabel("Total pacientes adultos hospitalizados")

        handles, labels = ax[0].get_legend_handles_labels()
        ax[0].legend(handles, labels, loc=1, bbox_to_anchor=(0.95,0.99), ncol=3, bbox_transform=fig.transFigure)
        ax[1].legend([],[], frameon=False)
        ax[2].legend([],[], frameon=False)
        ax[3].legend([],[], frameon=False)

        fig.subplots_adjust(left=0.005, right=1, top=0.8, bottom=0.1)
        fig.text(
            0, 0.910, "Muertes por covid, Número de hospitales sin personal disponible, \nTotal camas UCI ocupadas, Total adultos hospitalizados", 
            fontsize=16, fontweight="bold"
        )
        fig.text(
            0, 0.875, "Periodo 2020-01-01 a 2022-08-01", 
            fontsize=14
        )
        source = "Sources: U.S. Department of Health & Human Services - HealthData.gov"
        fig.text(
            0, 0, source, color="#a2a2a2", 
            fontsize=14, fontfamily="Econ Sans Cnd"
        )
        fig.add_artist(lines.Line2D([0, 1], [1, 1], lw=3, color='red', solid_capstyle="butt"))
        fig.add_artist(patches.Rectangle((0, 0.975), 0.05, 0.025, color='red'))
        sns.despine(left=False, bottom=False)

        return fig

    st.write(peor_plot(df))
    st.markdown("""
            <div style="text-align: justify;">
            Se graficó el número de muertes por covid, el número de hospitales sin personal disponible, el total de camas UCI ocupadas y el total de pacientes adultos hospitalizados para evaluar su desempeño durante los años que lleva la pandemia. Es interesante notar como todas las graficas incrementan hacia el final del año 2020. En el caso del total de camas ocupadas el año 2021 se mantuvo relativamente constante, disminuyendo un poco durante este año y luego ha tenido una caida dramatica, aunque se puede argumentar que no se debe estar reportando los datos desde Julio de este año para este item.
            Algo en común que tienen las cuatro gráficas es que para el 2020 todas finalizan en picos y el 2021 inicia con dicho pico. A excepción del total de pacientes adultos hospitalizados cuyo mayor pico ocurre en enero de 2022. Pero aún así teninedo en cuenta esto, se puede argumentar que los peores meses de la pandemia son Diciembre y Enero de 2020 y 2021 respectivamante. Eso se debe a la falta de prevención de los ciudadanos durante las fiestas de navidad y año nuevo.
            </div>
            """, unsafe_allow_html=True)
