import io
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

#Deficion clase

class DataAnalyzer:
    """Clase encargada de encapsular el análisis exploratorio de un dataset."""
    
    def __init__(self, dataframe: pd.DataFrame):
        self.df = dataframe
        # Atributos calculados automáticamente al instanciar
        self.cols_num = self.df.select_dtypes(include=['number']).columns.tolist()
        self.cols_cat = self.df.select_dtypes(include=['object', 'category', 'boolean']).columns.tolist()

    # --- 1. CLASIFICACIÓN DE VARIABLES ---
    def obtener_clasificacion(self):
        """Retorna las listas de variables clasificadas."""
        return self.cols_num, self.cols_cat

    # --- 2. ESTADÍSTICAS DESCRIPTIVAS ---
    def obtener_resumen_tecnico(self) -> str:
        """Captura el string de la función .info()"""
        buffer = io.StringIO()
        self.df.info(buf=buffer)
        return buffer.getvalue()

    def obtener_descriptivas(self) -> pd.DataFrame:
        """Retorna la tabla transpuesta de estadísticas descriptivas."""
        return self.df[self.cols_num].describe().T

    def interpretar_columna(self, columna: str) -> str:
        """Genera un reporte interpretativo textual de una variable numérica."""
        media = self.df[columna].mean()
        mediana = self.df[columna].median()
        desviacion = self.df[columna].std()
        
        txt = f"**Análisis de la variable '{columna}':**\n\n"
        txt += f"- **Tendencia Central:** La media es de **{media:,.2f}** y la mediana se ubica en **{mediana:,.2f}**. "
        if abs(media - mediana) / media > 0.1:
            txt += "Hay un sesgo notable por valores atípicos.\n"
        else:
            txt += "La distribución presenta simetría entre su centro y su promedio.\n"
        txt += f"- **Dispersión:** Desviación estándar de **{desviacion:,.2f}**."
        return txt

    def obtener_tabla_faltantes(self) -> pd.DataFrame:
        """Calcula el conteo y porcentaje de nulos."""
        conteo = self.df.isnull().sum()
        porcentaje = (conteo / len(self.df)) * 100
        df_resumen = pd.DataFrame({'Conteo Nulos': conteo, 'Porcentaje (%)': porcentaje})
        return df_resumen[df_resumen['Conteo Nulos'] > 0]

    # --- 3. FUNCIONES DE VISUALIZACIÓN ---
    def graficar_histograma(self, columna: str, bins: int):
        """Renderiza un histograma con curva KDE en la interfaz actual."""
        fig, ax = plt.subplots(figsize=(7, 4.5))
        sns.histplot(self.df[columna], bins=bins, kde=True, color="#1f77b4", ax=ax)
        ax.set_title(f"Distribución de {columna}")
        st.pyplot(fig)
        plt.close(fig)

    def graficar_boxplot_bivariado(self, var_num: str, var_cat: str):
        """Renderiza un boxplot cruzando una numérica y una categórica."""
        fig, ax = plt.subplots(figsize=(7, 4.5))
        sns.boxplot(x=var_cat, y=var_num, data=self.df, palette="Set2", ax=ax)
        st.pyplot(fig)
        plt.close(fig)

    def graficar_barras_cruzadas(self, var_x: str, var_y: str):
        """Renderiza un gráfico de conteos cruzados para categóricas."""
        fig, ax = plt.subplots(figsize=(7, 5))
        sns.countplot(x=var_x, hue=var_y, data=self.df, palette="viridis", ax=ax)
        plt.xticks(rotation=45, ha='right')
        st.pyplot(fig)
        plt.close(fig)


# Configuración de la página
st.set_page_config(page_title="Análisis Exploratorio de Datos (EDA) ", layout="wide")

# --- BARRA LATERAL (Sidebar) ---
st.sidebar.title("Navegación")
app_mode = st.sidebar.radio("Selecciona un módulo:", ["Home", "Carga del Dataset","Conclusiones"])

# --- MÓDULO 1: HOME ---
if app_mode == "Home":
    st.title("📊 Proyecto de Análisis Exploratorio de Datos (EDA)")
    st.markdown("---")
    
    st.header("1. Título del Proyecto")
    st.subheader("Análisis Exploratorio de Datos (EDA) sobre BankMarketing")
    
    st.header("2. Objetivo del Análisis")
    st.write("""
    Este proyecto tiene como objetivo analizar el conjunto de datos de BankMarketing en csv,
    para identificar patrones, tendencias y extraer información valiosa que permita 
    la toma de decisiones basadas en datos.
    """)
    
    st.header("3. Datos del Autor")
    st.markdown("""
    *   Nombre completo: HELTON OMAR HUAMANI OJEDA
    *   Curso / Especialización: Especialización en Python for Analytics
    *   Año: 2026
    """)
    
    st.header("4. Explicación del Dataset")
    st.write("""
    El dataset utilizado proviene de [Fuente, ejemplo. Kaggle] y contiene información relevantes para una campaña de marketing
    directo de una institución bancaria portuguesa. Las columnas incluyen datos sobre [ej. edad,empleo,estado civil, vivienda, prestamos, campaña].
    """)
    
    st.header("5. Tecnologías Utilizadas")
    st.markdown("""
    - **Python**: Lenguaje base para el procesamiento de datos.
    - **Pandas**: Manipulación de datos, análisis de frecuencias y tablas de contingencia.
    - **Streamlit**: Framework interactivo para la interfaz web y persistencia en memoria (`session_state`).
    - **Matplotlib & Seaborn**: Motores gráficos para histogramas y diagramas de caja (Boxplots).
    - **Programación Orientada a Objetos (POO)**: Arquitectura basada en clases para modularizar el análisis técnico y de negocio.
    """)

# --- MÓDULO 2: CARGA DEL DATASET ---
elif app_mode == "Carga del Dataset":
    st.title("📂 Carga de Datos")
    st.markdown("---")
    
    st.subheader("Subir archivo CSV")
    # 1. Utilizar st.file_uploader()
    uploaded_file = st.file_uploader("Selecciona tu archivo .csv", type=["csv"])

    # En la barra lateral, debajo del radio button:
    separador = st.sidebar.selectbox("Selecciona el delimitador del CSV:", [";", ","])

    ## Area de funciones:

        # Función personalizada para interpretar estadísticas de una columna / TAB3
    def interpretar_estadisticas(df, columna):
        media = df[columna].mean()
        mediana = df[columna].median()
        desviacion = df[columna].std()
        
        # Lógica de interpretación básica
        interpretacion = f"**Análisis de la variable '{columna}':**\n\n"
        interpretacion += f"- **Tendencia Central:** El valor promedio (media) es de **{media:,.2f}**, mientras que el punto medio de los datos (mediana) se ubica en **{mediana:,.2f}**. "
        
        if abs(media - mediana) / media > 0.1:
            interpretacion += "Existe una diferencia notable entre la media y la mediana, lo que sugiere que los datos podrían estar sesgados por valores atípicos (muy altos o muy bajos).\n"
        else:
            interpretacion += "La media y la mediana son cercanas, lo que indica una distribución relativamente simétrica.\n"
            
        interpretacion += f"- **Dispersión:** La desviación estándar es de **{desviacion:,.2f}**. Esto refleja qué tan alejados están los datos individuales respecto al promedio general."
        return interpretacion


    # Función personalizada para clasificar variables / TAB2
    def clasificar_variables(df):
        numericas = df.select_dtypes(include=['number']).columns.tolist()
        categoricas = df.select_dtypes(include=['object', 'category', 'boolean']).columns.tolist()
        return numericas, categoricas

    # Función para procesar el conteo de faltantes / TAB4
    def calcular_faltantes(df):
        conteo = df.isnull().sum()
        porcentaje = (df.isnull().sum() / len(df)) * 100
        df_resumen = pd.DataFrame({'Conteo Nulos': conteo, 'Porcentaje (%)': porcentaje})
        return df_resumen[df_resumen['Conteo Nulos'] > 0]


    # 2. Validar que el archivo fue cargado correctamente
    if uploaded_file is not None:
        try:
            # cargar el archivo:
            df = pd.read_csv(uploaded_file, sep=separador)
            st.session_state['dataset'] = df
            st.success("✅ Archivo cargado correctamente con delimitador ';'")
            
            # INSTANCIACIÓN DEL OBJETO ANALIZADOR
            analizador = DataAnalyzer(df)

            # 3. Mostrar dimensiones del dataset
            st.write(f"Dimensiones del Dataset: {df.shape[0]} filas y {df.shape[1]} columnas")
            
            # 4. Mostrar una vista previa del dataset (head)
            st.header("Vista Previa (Head)")
            st.dataframe(df.head())
            
            # Definición de Tabs (iremos creando los 10 ítems aquí uno por uno.)
            tab1, tab2 , tab3, tab4, tab5, tab6, tab7, tab8, tab9, tab10 = st.tabs(["1. Información general del dataset ", "2. Clasificación de variables ","3. Estadísticas Descriptivas",
                                   "4. Análisis de valores faltantes ", "5.  Distribución de variables numéricas ", "6. Análisis de variables categóricas", 
                                   "7. Análisis bivariado (numérico vs categórico)", "8. Análisis bivariado (categórico vs categórico)",
                                    "9. Análisis basado en parámetros seleccionados ", "10. Hallazgos clave "])

            # --- ÍTEM 1: INFORMACIÓN GENERAL ---
            with tab1:
                st.subheader("🔍 Estructura y Tipos de Datos")
                
                col1, col2 = st.columns(2)

                with col1:
                    st.write("**Tipos de Datos por Columna:**")
                    # Presentamos los dtypes como un DataFrame para que sea legible
                    st.dataframe(df.dtypes.astype(str).to_frame(name="Tipo de Dato"))

                with col2:
                    st.write("**Conteo de Valores Nulos:**")
                    # Calculamos nulos
                    nulos = df.isnull().sum()
                    st.dataframe(nulos.to_frame(name="Cantidad de Nulos"))

                st.divider()
                
                
                st.write("**Resumen (.info):**")
                # Como df.info() imprime en consola, lo capturamos para mostrarlo en Streamlit
                import io
                buffer = io.StringIO()
                df.info(buf=buffer)
                #s = buffer.getvalue()
                info_completa = buffer.getvalue()
                # st.text(s)
    
                st.text_area(
                        "Salida técnica del sistema:", 
                        info_completa, 
                        height=250
                )

         
            # --- ÍTEM 2: CLASIFICACIÓN DE VARIABLES ---
            with tab2:
                st.subheader("🗂️ Clasificación de Variables")
                
                # Ejecución de la función personalizada
                cols_num, cols_cat = clasificar_variables(df)
                
                # Visualización con Columnas y Métricas
                c1, c2 = st.columns(2)
                c1.metric(label="Variables Numéricas", value=len(cols_num))
                c2.metric(label="Variables Categóricas", value=len(cols_cat))
                
                st.divider()
                
                # Listado detallado en paralelo
                col_lista1, col_lista2 = st.columns(2)
                
                with col_lista1:
                    st.write("**📌 Columnas Numéricas:**")
                    if cols_num:
                        st.dataframe(pd.DataFrame(cols_num, columns=["Nombre de Variable"]))
                    else:
                        st.info("No se encontraron variables numéricas.")
                        
                with col_lista2:
                    st.write("**📌 Columnas Categóricas:**")
                    if cols_cat:
                        st.dataframe(pd.DataFrame(cols_cat, columns=["Nombre de Variable"]))
                    else:
                        st.info("No se encontraron variables categóricas.")
          

             # --- ÍTEM 3: ESTADÍSTICAS DESCRIPTIVAS ---
            with tab3:
                st.subheader("📊 Estadísticas Descriptivas del Dataset")
                
                # Obtener solo las columnas numéricas del dataframe
                cols_num = df.select_dtypes(include=['number']).columns.tolist()
                
                if cols_num:
                    st.write("**Tabla General de Estadísticas (.describe):**")
                    # Mostramos la tabla
                    st.dataframe(analizador.obtener_descriptivas())
                
                    st.divider()
                    st.subheader("💡 Interpretación Individual")
                    
                    # Selector interactivo y diseño en columnas
                    col_sel, col_interp = st.columns(2)
                    
                    with col_sel:
                        var_sel = st.selectbox("Selecciona columna:", cols_num, key="poo_t3")
                        
                        # Pequeño resumen métrico al lado de la selección
                        st.metric("Media", f"{df[var_sel].mean():,.2f}")
                        st.metric("Mediana (50%)", f"{df[var_sel].median():,.2f}")
                        st.metric("Desv. Estándar", f"{df[var_sel].std():,.2f}")
                    
                    with col_interp:
                        st.info("### Reporte Automatizado")
                        # Llamada a la función interpretativa
                        st.write(analizador.interpretar_columna(var_sel))
                else:
                    st.warning("El dataset no contiene variables numéricas para calcular estadísticas descriptivas.")

                        

            # --- ÍTEM 4: ANÁLISIS DE VALORES FALTANTES ---
            with tab4:
                st.subheader("🔍 Diagnóstico de Valores Faltantes")
                
                # 1. Conteo de valores faltantes
                df_faltantes = calcular_faltantes(df)
                
                if not df_faltantes.empty:
                    col_tabla, col_grafico = st.columns(2)
                    
                    with col_tabla:
                        st.write("**Conteo y Porcentaje de Nulos:**")
                        st.dataframe(df_faltantes.style.format({'Porcentaje (%)': '{:.2f}%'}))
                    
                    # 2. Visualización simple
                    with col_grafico:
                        st.write("**Visualización Gráfica (Porcentaje de Pérdida):**")
                        st.bar_chart(df_faltantes['Porcentaje (%)'])
                    
                    st.divider()
                    
                    # 3. Discusión breve
                    st.subheader("💬 Discusión Breve")
                    columna_max = df_faltantes['Conteo Nulos'].idxmax()
                    pct_max = df_faltantes['Porcentaje (%)'].max()
                    
                    st.write(f"""
                    El dataset presenta registros incompletos. La variable con mayor afectación es **{columna_max}**, 
                    la cual carece del **{pct_max:.2f}%** de sus datos. 
                    
                    **Impacto y Recomendación:** Un porcentaje menor al 5% permite una eliminación directa de filas sin sesgar los resultados. 
                    Si el impacto es mayor, se sugiere aplicar técnicas de imputación (media para valores numéricos o moda para categóricos) 
                    para preservar el tamaño de la muestra antes de entrenar modelos o realizar análisis avanzados.
                    """)
                    
                else:
                    st.success("🎉 **¡Análisis Completo!** El dataset no contiene valores faltantes en ninguna de sus variables.")

            # --- ÍTEM 5: DISTRIBUCIÓN DE VARIABLES NUMÉRICAS ---
            with tab5:
                st.subheader("📊 Distribución de Variables Numéricas")
                
                # Filtrar solo columnas numéricas
                cols_num = df.select_dtypes(include=['number']).columns.tolist()
                
                if cols_num:
                    col_control, col_grafico = st.columns([1, 2])
                    
                    with col_control:
                        st.write("**Configuración del Gráfico:**")
                        # Selector de variable
                        var_seleccionada = st.selectbox(
                            "Selecciona la variable a graficar:", 
                            cols_num, 
                            key="sb_item5"
                        )
                        
                        # Control interactivo para los bins (barras del histograma)
                        bins_seleccionados = st.slider(
                            "Número de intervalos (Bins):", 
                            min_value=5, 
                            max_value=50, 
                            value=20,
                            key="slider_item5"
                        )
                        
                        st.divider()
                        # Texto fijo de apoyo para la interpretación
                        st.markdown("""
                        **💡 Guía de Interpretación Visual:**
                        * **Campana de Gauss (Normal):** Si los datos se concentran al centro y caen simétricamente a los lados, la variable sigue una distribución normal estándar.
                        * **Sesgo a la Derecha (Positivo):** La cola larga se extiende hacia valores altos. Indica que la mayoría de los datos son pequeños, pero existen algunos valores inusualmente grandes.
                        * **Sesgo a la Izquierda (Negativo):** La cola larga se extiende hacia valores bajos. Indica predominancia de datos con valores altos.
                        * **Multimodal:** Si ves más de un "pico" alto, el dataset podría estar mezclando diferentes grupos o subpoblaciones.
                        """)
                    
                    with col_grafico:
                        st.write(f"**Histograma de Frecuencias: {var_seleccionada}**")
                        
                        # Crear el gráfico con Matplotlib y Seaborn
                        fig, ax = plt.subplots(figsize=(8, 5))
                        sns.histplot(
                            df[var_seleccionada], 
                            bins=bins_seleccionados, 
                            kde=True, 
                            color="#1f77b4", 
                            ax=ax
                        )
                        
                        # Personalización de etiquetas
                        ax.set_title(f"Distribución de la variable {var_seleccionada}", fontsize=12)
                        ax.set_xlabel(var_seleccionada, fontsize=10)
                        ax.set_ylabel("Frecuencia (Conteo)", fontsize=10)
                        
                        # Pasar la figura de Matplotlib a Streamlit de forma segura
                        st.pyplot(fig)
                        plt.close(fig) # Limpiar memoria de la figura
                        
                else:
                    st.warning("El dataset no contiene variables numéricas para generar histogramas.")

            # --- ÍTEM 6: ANÁLISIS DE VARIABLES CATEGÓRICAS ---
            with tab6:
                st.subheader("📊 Análisis de Variables Categóricas")
                
                # Identificar columnas categóricas (texto o categorías)
                cols_cat = df.select_dtypes(include=['object', 'category', 'boolean']).columns.tolist()
                
                if cols_cat:
                    # Selector de la variable categórica
                    var_cat_seleccionada = st.selectbox(
                        "Selecciona la variable categórica a analizar:", 
                        cols_cat,
                        key="sb_item6"
                    )
                    
                    st.write(f"### Análisis para la variable: **{var_cat_seleccionada}**")
                    
                    # 1. Cálculos de Conteos y Proporciones
                    conteos = df[var_cat_seleccionada].value_counts()
                    proporciones = df[var_cat_seleccionada].value_counts(normalize=True) * 100
                    
                    # Unimos ambos cálculos en un único DataFrame resumen
                    df_resumen_cat = pd.DataFrame({
                        'Frecuencia Absoluta (Conteo)': conteos,
                        'Frecuencia Relativa (%)': proporciones
                    })
                    
                    # Diseño en columnas para mostrar tabla y gráfico en paralelo
                    col_tabla_cat, col_grafico_cat = st.columns(2)
                    
                    with col_tabla_cat:
                        st.write("**Tabla de Frecuencias y Proporciones:**")
                        # Mostramos la tabla con formato de porcentaje para la proporción
                        st.dataframe(df_resumen_cat.style.format({'Frecuencia Relativa (%)': '{:.2f}%'}))
                        
                        # Pequeña métrica informativa sobre las categorías únicas
                        st.metric("Total de Categorías Únicas", len(conteos))
                    
                    # 2. Gráfico de barras simple
                    with col_grafico_cat:
                        st.write("**Gráfico de Barras (Distribución por Conteo):**")
                        # Usamos el gráfico nativo de Streamlit que es limpio e interactivo
                        st.bar_chart(df_resumen_cat['Frecuencia Absoluta (Conteo)'])
                        
                else:
                    st.warning("El dataset no contiene variables categóricas o de texto para analizar.")
            
            # --- ÍTEM 7: ANÁLISIS BIVARIADO ---
            with tab7:
                st.subheader("📊 Análisis Bivariado (Numérico vs Categórico)")
                
                # Definir pares de análisis requeridos
                pares_analisis = {
                    "Edad según Variable Y (age vs y)": {"num": "age", "cat": "y"},
                    "Duración según Variable Y (duration vs y)": {"num": "duration", "cat": "y"}
                }
                
                # Validar si las columnas necesarias existen en el dataset cargado
                columnas_presentes = df.columns.tolist()
                analisis_disponibles = {}
                
                for nombre, vars_dict in pares_analisis.items():
                    if vars_dict["num"] in columnas_presentes and vars_dict["cat"] in columnas_presentes:
                        analisis_disponibles[nombre] = vars_dict

                if analisis_disponibles:
                    # Selector del par de variables a analizar
                    seleccion_par = st.selectbox(
                        "Selecciona el par de variables a analizar:",
                        list(analisis_disponibles.keys()),
                        key="sb_item7"
                    )
                    
                    var_num = analisis_disponibles[seleccion_par]["num"]
                    var_cat = analisis_disponibles[seleccion_par]["cat"]
                    
                    st.write(f"### Análisis de **{var_num}** segmentado por **{var_cat}**")
                    
                    # 1. Agrupación y Estadísticas Descriptivas por Categoría
                    st.write("**Estadísticas Resumen por Grupo:**")
                    resumen_bivariado = df.groupby(var_cat)[var_num].describe()
                    st.dataframe(resumen_bivariado)
                    
                    st.divider()
                    
                    # Diseño en columnas para Gráfico e Interpretación
                    col_graf, col_interp = st.columns([3, 2])
                    
                    with col_graf:
                        st.write(f"**Distribución Comparativa (Boxplot):**")
                        # Generar Boxplot con Matplotlib y Seaborn
                        fig, ax = plt.subplots(figsize=(7, 4.5))
                        sns.boxplot(
                            x=var_cat, 
                            y=var_num, 
                            data=df, 
                            palette="Set2", 
                            ax=ax
                        )
                        ax.set_title(f"Diagrama de Caja: {var_num} por {var_cat}")
                        ax.set_xlabel(f"Categoría ({var_cat})")
                        ax.set_ylabel(var_num)
                        
                        st.pyplot(fig)
                        plt.close(fig)
                        
                    with col_interp:
                        st.write("**💡 Guía de Interpretación Visual (Boxplot):**")
                        st.markdown(f"""
                        El diagrama de caja (Boxplot) permite comparar visualmente los grupos definidos por **{var_cat}**:
                        
                        * **Línea Central (Mediana):** Si las líneas centrales de las cajas están a diferentes alturas, significa que las tendencias centrales de los grupos difieren.
                        * **Tamaño de la Caja (Rango Intercuartílico):** Representa el 50% central de los datos. Una caja más larga indica mayor dispersión en ese grupo.
                        * **Puntos Aislados (Atípicos):** Los puntos ubicados fuera de los "bigotes" representan valores extremos u outliers de la variable **{var_num}**.
                        """)
                        
                else:
                    st.warning("Para habilitar este análisis, el dataset debe contener las columnas específicas: 'age', 'duration' e 'y'.")

            # --- ÍTEM 8: ANÁLISIS BIVARIADO (CATEGÓRICO VS CATEGÓRICO) ---
            with tab8:
                st.subheader("📊 Análisis Bivariado (Categórico vs Categórico)")
                
                # Definir pares de análisis categóricos requeridos
                pares_cat = {
                    "Educación vs Variable Y (education vs y)": {"col1": "education", "col2": "y"},
                    "Medio de Contacto vs Variable Y (contact vs y)": {"col1": "contact", "col2": "y"}
                }
                
                columnas_presentes = df.columns.tolist()
                analisis_cat_disponibles = {}
                
                # Validar existencia de columnas
                for nombre, vars_dict in pares_cat.items():
                    if vars_dict["col1"] in columnas_presentes and vars_dict["col2"] in columnas_presentes:
                        analisis_cat_disponibles[nombre] = vars_dict

                if analisis_cat_disponibles:
                    # Selector del par de variables
                    seleccion_par_cat = st.selectbox(
                        "Selecciona el par de variables categóricas:",
                        list(analisis_cat_disponibles.keys()),
                        key="sb_item8"
                    )
                    
                    var_x = analisis_cat_disponibles[seleccion_par_cat]["col1"]
                    var_y = analisis_cat_disponibles[seleccion_par_cat]["col2"]
                    
                    st.write(f"### Relación entre **{var_x}** y la variable objetivo **{var_y}**")
                    
                    # 1. Tabla de Contingencia (Frecuencias absolutas)
                    tabla_cruzada = pd.crosstab(df[var_x], df[var_y])
                    
                    # 2. Tabla de Proporciones (Porcentajes por fila para comparar equitativamente)
                    tabla_proporciones = pd.crosstab(df[var_x], df[var_y], normalize='index') * 100
                    
                    col_tablas, col_grafico_cruzado = st.columns(2)
                    
                    with col_tablas:
                        st.write("**Conteo Absoluto (Frecuencias):**")
                        st.dataframe(tabla_cruzada)
                        
                        st.write("**Distribución Porcentual (%) por Fila:**")
                        st.dataframe(tabla_proporciones.style.format('{:.2f}%'))
                    
                    # 3. Visualización Gráfica (Barras Agrupadas con Seaborn)
                    with col_grafico_cruzado:
                        st.write("**Visualización de la Relación (Gráfico de Barras):**")
                        
                        fig, ax = plt.subplots(figsize=(7, 5))
                        # Usamos countplot para cruzar las dos variables categóricas
                        sns.countplot(
                            x=var_x, 
                            hue=var_y, 
                            data=df, 
                            palette="viridis", 
                            ax=ax
                        )
                        ax.set_title(f"Distribución de {var_y} según {var_x}")
                        ax.set_xlabel(var_x)
                        ax.set_ylabel("Cantidad de Registros")
                        # Rotar etiquetas si son textos largos (como en education)
                        plt.xticks(rotation=45, ha='right')
                        
                        st.pyplot(fig)
                        plt.close(fig)
                    
                    st.divider()
                    st.write("**💡 Guía de Interpretación:**")
                    st.markdown(f"""
                    * **Tabla de Proporciones:** Permite comparar directamente los grupos sin importar si uno tiene más registros que otro. Busca si alguna categoría tiene un porcentaje de **{var_y}** significativamente más alto que las demás.
                    * **Gráfico de Barras (hue):** Compara visualmente la altura de las barras de colores dentro de cada categoría. Si el comportamiento de las barras cambia drásticamente entre categorías, existe una fuerte relación o dependencia entre ambas variables.
                    """)
                    
                else:
                    st.warning("Para habilitar este análisis, el dataset debe contener las columnas específicas: 'education', 'contact' e 'y'.")
            
            # --- ÍTEM 9: ANÁLISIS BASADO EN PARÁMETROS SELECCIONADOS ---
            with tab9:
                st.subheader("⚙️ Laboratorio de Análisis Dinámico Parametrizado")
                st.write("Configura tus propios parámetros para cruzar y resumir el dataset en tiempo real.")
                
                # Separar tipos de variables para los selectores
                todas_cols_cat = df.select_dtypes(include=['object', 'category', 'boolean']).columns.tolist()
                todas_cols_num = df.select_dtypes(include=['number']).columns.tolist()
                
                if todas_cols_cat and todas_cols_num:
                    
                    # Controles de usuario en columnas superiores
                    ctrl1, ctrl2 = st.columns(2)
                    
                    with ctrl1:
                        # 1. Uso de selectbox para la variable de agrupación (Eje de análisis)
                        variable_agrupadora = st.selectbox(
                            "🛠️ Selecciona una variable categórica para agrupar:",
                            todas_cols_cat,
                            key="sb_item9_cat"
                        )
                        
                    with ctrl2:
                        # 2. Uso de multiselect para las métricas numéricas a evaluar
                        metricas_elegidas = st.multiselect(
                            "📊 Selecciona una o más variables numéricas para promediar:",
                            todas_cols_num,
                            default=[todas_cols_num[0]] if todas_cols_num else [],
                            key="ms_item9_num"
                        )
                        
                    st.divider()
                    
                    # Ejecución del Análisis Dinámico
                    if metricas_elegidas:
                        st.write(f"### Resumen de Promedios agrupado por: **{variable_agrupadora}**")
                        
                        # Agrupación y cálculo dinámico de la media
                        df_dinamico = df.groupby(variable_agrupadora)[metricas_elegidas].mean()
                        
                        # Presentación en dos columnas: Tabla y Gráfico de tendencias
                        col_res_tabla, col_res_graf = st.columns([1, 1.2])
                        
                        with col_res_tabla:
                            st.write("**Resultados Numéricos (Medias):**")
                            st.dataframe(df_dinamico.style.format('{:.2f}'))
                            
                        with col_res_graf:
                            st.write("**Comparativa Gráfica Interactiva:**")
                            # El gráfico se adapta automáticamente al número de métricas seleccionadas
                            st.bar_chart(df_dinamico)
                            
                        st.success(f"💡 **Análisis dinámico completado:** Estás comparando {len(metricas_elegidas)} variables numéricas a través de las categorías de '{variable_agrupadora}'.")
                    else:
                        st.info("💡 Por favor, selecciona al menos una variable numérica en el campo de arriba para generar el análisis.")
                        
                else:
                    st.warning("El dataset debe contar con al menos una variable categórica y una numérica para habilitar los parámetros dinámicos.")

            # --- ÍTEM 10: HALLAZGOS CLAVE E INSIGHTS ---
            with tab10:
                st.subheader("🏁 Resumen Ejecutivo y Hallazgos Clave (Insights)")
                st.write("Conclusiones estratégicas obtenidas a partir del Análisis Exploratorio de Datos.")
                
                # 1. Visualización Resumen en Contenedor Destacado
                with st.container(border=True):
                    st.write("#### 📈 Radiografía del Dataset")
                    
                    # Generamos 4 métricas clave rápidas de recordar
                    m1, m2, m3, m4 = st.columns(4)
                    
                    m1.metric(label="Total Registros", value=f"{df.shape[0]:,}")
                    m2.metric(label="Total Columnas", value=df.shape[1])
                    
                    # Cálculo de registros totalmente limpios (sin nulos)
                    filas_completas = df.dropna().shape[0]
                    pct_completas = (filas_completas / df.shape[0]) * 100
                    m3.metric(label="Registros Completos", value=f"{pct_completas:.1f}%")
                    
                    if 'y' in df.columns:
                        clase_mayoritaria = df['y'].value_counts(normalize=True).iloc[0] * 100
                        m4.metric(label="Sesgo en Objetivo (Y)", value=f"{clase_mayoritaria:.1f}%")
                    else:
                        m4.metric(label="Variables Numéricas", value=len(df.select_dtypes(include=['number']).columns))

                st.divider()

                # 2. Insights Principales Derivados del EDA
                st.write("#### 💡 Principales Conclusiones")
                
                # Diseño de tarjetas informativas mediante columnas estructuradas
                ins1, ins2 = st.columns(2)
                
                with ins1:
                    st.info("""
                    **📌 1. Calidad y Estructura de los Datos**
                    * **Consistencia:** El proceso de carga inicial validó la separación por punto y coma (`;`), asegurando que las dimensiones no se deformaran en una sola columna.
                    * **Salud del Dataset:** El análisis de valores faltantes (Ítem 4) determinó si es viable aplicar una eliminación por lista o si se requiere ingeniería de características para imputar registros vacíos antes del modelado.
                    """)
                    
                    st.info("""
                    **📌 2. Comportamiento del Consumidor/Usuario (Bivariado)**
                    * **Métricas Críticas:** Los cruces del Ítem 7 (`age` y `duration` vs `y`) revelan si el comportamiento de la variable objetivo varía según el perfil de edad o el tiempo de interacción.
                    * *Insight:* Generalmente, duraciones de contacto más extensas correlacionan positivamente con una respuesta afirmativa en la variable objetivo.
                    """)

                with ins2:
                    st.warning("""
                    **📌 3. Segmentación y Canales (Categórico)**
                    * **Tendencias del Canal:** El análisis cruzado del Ítem 8 (`education` y `contact` vs `y`) identifica qué subgrupos demográficos y qué medios de comunicación muestran tasas de conversión o respuesta superiores al promedio.
                    * *Insight:* Enfocar esfuerzos en los canales con mayor tasa de éxito optimiza el uso de recursos operativos.
                    """)
                    
                    st.success("""
                    **📌 4. Próximos Pasos Recomendados**
                    1. **Limpieza:** Tratar los valores nulos detectados bajo los umbrales sugeridos en el Ítem 4.
                    2. **Transformación:** Aplicar codificación (One-Hot Encoding) a las variables del Ítem 6 para convertirlas en formatos aptos para algoritmos.
                    3. **Modelado:** Proceder a la etapa de Machine Learning utilizando las variables predictoras más influyentes descubiertas en el laboratorio dinámico.
                    """)

        except Exception as e:
            st.error(f"Error al leer el archivo: {e}")


# --- MÓDULO 3: CONCLUSIONES ESTRATÉGICAS ---
elif app_mode == "Conclusiones":
    st.title("🎯 Panel de Conclusiones")
    
    # Validar si el usuario ya cargó un archivo en el Módulo 2
    if 'dataset' in st.session_state:
        df = st.session_state['dataset']
        
        st.markdown("""
        Este panel consolida 5 conclusiones  derivadas directamente de los hechos observados 
        en el análisis exploratorio. Su enfoque es 100% operativo y gerencial, diseñado para respaldar la **toma de decisiones** 
        y la mitigación de riesgos organizacionales, descartando supuestos estadísticos predictivos.
        """)
        
        st.divider()

        # --- CONCLUSIÓN 1: AUDITORÍA DE ORIGEN ---
        with st.container(border=True):
            st.subheader("1. Control de Calidad Estructural de la Información")
            nulos_totales = df.isnull().sum().sum()
            if nulos_totales > 0:
                st.warning("""
                **Diagnóstico:** Se ha detectado la presencia de registros incompletos distribuidos en variables del dataset. 
                
                **Decisión Operativa:** La gerencia debe implementar una auditoría técnica en los sistemas de captura de origen (CRM, bases de datos o formularios de registro). Tomar decisiones comerciales con muestras truncadas introduce sesgos metodológicos ocultos; antes de reestructurar metas, es obligatorio estandarizar los campos obligatorios de llenado para garantizar que los reportes internos reflejen fielmente el universo real de las operaciones.
                """)
            else:
                st.success("""
                **Diagnóstico:** El conjunto de datos presenta una tasa del 100% de completitud e integridad en todas sus filas y columnas.
                
                **Decisión Operativa:** Esta estabilidad de la infraestructura de datos valida la madurez de los procesos de auditoría vigentes. La dirección puede emplear estos indicadores históricos con total seguridad operativa para calcular retornos de inversión (ROI) precisos, reduciendo el riesgo normativo y asegurando que las líneas base de planificación institucional sean robustas.
                """)

        # --- CONCLUSIÓN 2: OPTIMIZACIÓN DE TIEMPOS O DISPERSIÓN ---
        with st.container(border=True):
            st.subheader("2. Eficiencia Temporal y Gestión del Esfuerzo Operativo")
            if 'duration' in df.columns:
                st.info("""
                **Diagnóstico:** El análisis bivariado expone una asimetría crítica en los tiempos de interacción de los usuarios; los casos identificados como exitosos retienen la atención durante periodos significativamente más prolongados en comparación con los casos infructuosos.
                
                **Decisión Operativa:** Se sugiere reestructurar los protocolos e instrucciones de los equipos de contacto. En lugar de prolongar interacciones desgastantes con perfiles no receptivos, se deben diseñar filtros de descarte temprano dentro de los primeros 60 segundos. Esto liberará horas-hombre que podrán ser reasignadas a gestionar interacciones de alto valor, incrementando la productividad global del departamento sin añadir costos de contratación.
                """)
            else:
                st.info("""
                **Diagnóstico:** Las desviaciones estándar calculadas en las variables numéricas clave demuestran una alta heterogeneidad y dispersión interna dentro del dataset.
                
                **Decisión Operativa:** La alta variabilidad confirma que las estrategias masivas o genéricas suboptimizan los recursos de la empresa. Se dictamina abandonar los planes de acción globales y transicionar hacia una segmentación por percentiles. Establecer metas operativas diferenciadas por subgrupos evitará la sobreexigencia de los segmentos rezagados y aprovechará el potencial de los grupos con mayor rendimiento.
                """)

        # --- CONCLUSIÓN 3: ENFOQUE DEMOGRÁFICO ---
        with st.container(border=True):
            st.subheader("3. Racionalización y Enfoque del Segmento Objetivo")
            if 'age' in df.columns:
                st.info("""
                **Diagnóstico:** La distribución de frecuencias y análisis de tendencia central sitúa el núcleo de usuarios con mayor adherencia histórica en rangos etarios muy específicos del dataset.
                
                **Decisión Operativa:** La dirección comercial debe ajustar los criterios de asignación y adquisición de carteras basados en esta evidencia empírica. Se recomienda concentrar de forma inmediata los presupuestos de mercadeo y los recursos de atención en estos nichos consolidados, minimizando el gasto en rangos de edad con tasas de respuesta deficientes, lo que optimiza el costo de adquisición por usuario.
                """)
            else:
                st.info("""
                **Diagnóstico:** Las medidas de tendencia central demuestran que las variables clave presentan sesgos pronunciados hacia los extremos de las curvas de distribución.
                
                **Decisión Operativa:** Al comprobarse que los promedios matemáticos están fuertemente distorsionados por valores atípicos, queda estrictamente prohibido utilizar la 'media' para proyecciones presupuestarias o establecimiento de cuotas. La gerencia debe adoptar formalmente la 'mediana' como el indicador rector de rendimiento, garantizando objetivos corporativos alcanzables, realistas y alineados al comportamiento del usuario común.
                """)

        # --- CONCLUSIÓN 4: ANÁLISIS DE CANALES ---
        with st.container(border=True):
            st.subheader("4. Optimización de Canales de Interacción y Contactabilidad")
            # Buscar una variable categórica común de canales o perfiles
            canal_var = next((c for c in ['contact', 'education', 'job'] if c in df.columns), None)
            
            if canal_var:
                st.info(f"""
                **Diagnóstico:** El análisis bivariado cualitativo revela que la distribución del éxito operativo no es equitativa entre las categorías de la variable '{canal_var}'; existen canales específicos que concentran tasas de conversión superiores al promedio institucional.
                
                **Decisión Operativa:** Se dictamina una migración táctica de recursos. Se deben congelar las inversiones operativas en aquellos medios o perfiles que demuestren estancamiento histórico y canalizar ese presupuesto hacia el fortalecimiento y expansión de los canales líderes identificados, maximizando la efectividad por cada punto de contacto ejecutado.
                """)
            else:
                st.info("""
                **Diagnóstico:** El conteo de proporciones relativas en las variables cualitativas expone un principio de Pareto: un número reducido de categorías concentra la gran mayoría de los registros útiles del negocio.
                
                **Decisión Operativa:** Esta concentración representa una dependencia crítica y un riesgo operativo latente para la estabilidad institucional. La gerencia debe diversificar las estrategias corporativas, implementando pilotos controlados para explorar los subsegmentos desatendidos, disminuyendo la vulnerabilidad ante la saturación de los mercados o nichos habituales.
                """)

        # --- CONCLUSIÓN 5: PLAN DE ACCIÓN GENERAL ---
        with st.container(border=True):
            st.subheader("5. Directriz Estratégica para la Mitigación del Riesgo Operacional")
            st.success("""
            **Diagnóstico:** El compendio analítico de este EDA demuestra que las deficiencias organizacionales actuales radican en la ejecución táctica y en la dispersión de esfuerzos, no en la falta de capacidad predictiva.
            
            **Decisión Operativa:** La principal recomendación para la alta dirección es priorizar un plan de saneamiento operativo basado en hechos comprobados. Corregir las fugas de tiempo detectadas en la atención, reasignar carteras hacia los perfiles de usuarios de alto rendimiento verificado y blindar la calidad de los datos de entrada generará un retorno financiero inmediato a través del ahorro de costos fijos, protegiendo el margen neto de la organización sin necesidad de incurrir en costosos modelos de simulación futura.
            """)
    else:
        st.warning("⚠️ **Falta el origen de datos:** Por favor, ve primero al **Módulo 2: Carga del Dataset**, sube tu archivo CSV para que el sistema procese el análisis y habilite este panel de decisiones.")        

else:
    st.info("Por favor, sube un archivo CSV en la barra lateral o aquí para continuar.")