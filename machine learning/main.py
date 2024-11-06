import os
os.environ['LOKY_MAX_CPU_COUNT'] = '4'
import pandas as pd
from sklearn.cluster import KMeans
import matplotlib.pyplot as plt

# Cargar el archivo CSV llamado 'data.csv'
data = pd.read_csv('data.csv')

# Seleccionar solo las columnas numéricas para el agrupamiento
X = data[['Ventas_Mundiales', 'Puntaje_Criticos', 'Año']]

# Crear y ajustar el modelo de KMeans con 3 grupos
kmeans = KMeans(n_clusters=3, random_state=42)
kmeans.fit(X)

# Agregar los resultados al DataFrame original
data['Grupo'] = kmeans.labels_

# Mostrar los juegos agrupados
print(data)

# Ordenar obtener el top 5 por ventas mundiales
top_juegos = data.sort_values(by='Ventas_Mundiales', ascending=False).head(5)
print("\nTop 5 juegos por ventas mundiales:\n", top_juegos[['Titulo', 'Ventas_Mundiales']])

# Analisis de Juegos top
plt.figure(figsize=(10, 6))
plt.scatter(data['Ventas_Mundiales'], data['Puntaje_Criticos'], c=data['Grupo'], cmap='viridis', s=50)
plt.xlabel('Ventas Mundiales (millones)')
plt.ylabel('Puntaje de Críticos')
plt.title('Agrupamiento de Juegos de Super Nintendo')

# Añadir nombre de títulos en la gráfica
for i, txt in enumerate(data['Titulo']):
    plt.annotate(txt, (data['Ventas_Mundiales'].iloc[i], data['Puntaje_Criticos'].iloc[i]), fontsize=8, alpha=0.7)

plt.colorbar(label='Grupo')
plt.show()

#Top 5 juegos por ventas mundiales
plt.figure(figsize=(10, 5))
plt.barh(top_juegos['Titulo'], top_juegos['Ventas_Mundiales'], color='teal')
plt.xlabel('Ventas Mundiales (millones)')
plt.title('Top 5 Juegos de Super Nintendo por Ventas Mundiales')
plt.gca().invert_yaxis()  # Invertir el eje Y para que el top 1 esté en la parte superior
plt.show()
