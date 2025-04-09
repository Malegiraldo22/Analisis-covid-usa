# 📊 Análisis del Impacto del COVID-19 en Estados Unidos

## 🌐 Demo en línea

Puedes acceder a la versión en vivo de la app aquí:

🔗 [Abrir aplicación desplegada en Streamlit Cloud](https://malegiraldo22-analisis-covid-usa-dashboard-mha1tq.streamlit.app/)
---
Este proyecto es una aplicación interactiva desarrollada con [Streamlit](https://streamlit.io/) que permite visualizar y analizar el impacto del COVID-19 en Estados Unidos desde diversas perspectivas: hospitalizaciones, ocupación de camas UCI, muertes por estado, escasez de personal médico, y más.

> 📌 **Proyecto desarrollado durante el Bootcamp de Data Science de Henry.**

---

## 🧰 Tecnologías utilizadas

- **Python 3.10**
- **Pandas** y **NumPy** para manipulación de datos
- **Matplotlib** y **Seaborn** para visualización estática
- **Plotly** para visualización interactiva
- **Streamlit** para construir el dashboard
- **Sodapy** y **Requests** para acceso a datos públicos

---

## 🚀 ¿Qué puedes hacer con esta app?

- Visualizar la evolución de casos de COVID-19 en EE. UU. desde enero de 2020.
- Ver los estados con mayor ocupación hospitalaria y UCI.
- Analizar la relación entre la falta de personal médico y las muertes por COVID.
- Explorar mapas interactivos con datos estatales.
- Seleccionar rangos de fechas para comparar situaciones hospitalarias.
- Leer interpretaciones y recomendaciones basadas en los datos.

---

## 📦 Instalación y ejecución local

1. Clona este repositorio:

```bash
git clone https://github.com/tu-usuario/dashboard-covid-henry.git
cd dashboard-covid-henry
```

2. Crea un entorno virtual (recomendado con `conda`)
```
conda create -n covid_dashboard python=3.10
conda activate covid_dashboard
```
3. Instala las dependencias
```
pip install -r requirements.txt
```
4. Ejecuta la app
```
streamlit run dashboard.py
```
---
## 🗂️ Estructura del proyecto
```
.
├── dashboard.py           # Script principal de la app Streamlit
├── requirements.txt       # Lista de dependencias
└── README.md              # Este archivo
```
---
## 📊 Fuentes de datos
* [HealthData.gov – U.S. Department of Health & Human Services](https://healthdata.gov/)
* [The New York Times – COVID-19 Data Repository](https://github.com/nytimes/covid-19-data)
---
## 🧑‍🎓 Sobre el proyecto
Este proyecto fue realizado como parte del Bootcamp de Data Science de Henry, aplicando herramientas de análisis, visualización y despliegue de dashboards interactivos para contar historias con datos y apoyar la toma de decisiones informadas en temas de salud pública.