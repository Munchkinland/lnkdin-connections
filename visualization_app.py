import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import networkx as nx
from collections import defaultdict
from tkinter import Tk, filedialog, StringVar, OptionMenu, Button, messagebox, Frame, Label
import webbrowser
import os
import numpy as np
import matplotlib.pyplot as plt

class VisualizationApp:
    def __init__(self, master):
        self.master = master
        self.master.title("Visualizador de Conexiones de LinkedIn")
        self.master.geometry("600x300")
        self.master.configure(bg="#f0f0f0")

        self.file_path = ""
        self.visualization_var = StringVar()

        # Crear un marco para organizar el contenido
        frame = Frame(master, bg="#f0f0f0")
        frame.pack(pady=20)

        # Etiqueta de título
        title_label = Label(frame, text="Visualizador de Conexiones de LinkedIn", font=("Helvetica", 16, "bold"), bg="#f0f0f0")
        title_label.pack(pady=10)

        # Crear un menú desplegable para seleccionar el tipo de visualización
        self.visualization_var.set("Seleccione Visualización")  # Valor por defecto
        option_menu = OptionMenu(frame, self.visualization_var, "Gráfico de Compañía", "Gráfico de Puestos", "Gráfico de Red", "Conexiones por Fecha")
        option_menu.config(bg="#ffffff", font=("Helvetica", 12))
        option_menu.pack(pady=10)

        # Botón para cargar archivo
        self.load_button = Button(frame, text="Cargar CSV", command=self.load_file, bg="#4CAF50", fg="white", font=("Helvetica", 12))
        self.load_button.pack(pady=5)

        # Botón para mostrar visualización
        self.visualize_button = Button(frame, text="Mostrar Visualización", command=self.show_visualization, bg="#2196F3", fg="white", font=("Helvetica", 12))
        self.visualize_button.pack(pady=5)

    def load_file(self):
        self.file_path = filedialog.askopenfilename(filetypes=[("CSV files", "*.csv")])
        
        # Desactivar el botón de carga después de seleccionar el archivo
        if self.file_path:
            self.load_button.config(state="disabled")

    def show_visualization(self):
        if not self.file_path:
            messagebox.showerror("Error", "Por favor, carga un archivo CSV primero.")
            return

        # Cargar el archivo CSV, saltando las primeras filas que parecen ser metadatos
        csv_file = self.file_path

        try:
            # Leer el CSV con separador ',' y saltar las primeras filas hasta encontrar los encabezados
            df = pd.read_csv(csv_file, skiprows=3)

            # Limpiar los nombres de las columnas
            df.columns = df.columns.str.strip()

            # Mostrar los primeros 5 registros
            print(df.head())

            # Ejecutar la visualización seleccionada
            visualization_type = self.visualization_var.get()
            if visualization_type == "Gráfico de Compañía":
                self.plot_top_companies(df)
            elif visualization_type == "Gráfico de Puestos":
                self.plot_top_positions(df)
            elif visualization_type == "Gráfico de Red":
                self.plot_network_graph(df)
            elif visualization_type == "Conexiones por Fecha":
                self.plot_connections_by_date(df)
            else:
                messagebox.showwarning("Advertencia", "Por favor, selecciona un tipo de visualización.")
        except Exception as e:
            messagebox.showerror("Error", f"Ocurrió un error al procesar el archivo CSV: {str(e)}")

    def plot_top_companies(self, df):
        # Contar conexiones por empresa
        company_count = df['Company'].value_counts().reset_index()
        company_count.columns = ['Company', 'Connections']
        company_count = company_count.head(20)  # Limitar a las 20 principales

        # Gráfico de barras para conexiones por empresa
        fig = px.bar(company_count, x='Company', y='Connections', title='Conexiones por Empresa', color='Connections', 
                     labels={'Connections': 'Número de Conexiones', 'Company': 'Empresa'},
                     color_continuous_scale=px.colors.sequential.Viridis)
        fig.show()

    def plot_top_positions(self, df):
        # Contar conexiones por cargo
        position_count = df['Position'].value_counts().reset_index()
        position_count.columns = ['Position', 'Connections']
        position_count = position_count.head(20)  # Limitar a las 20 principales

        # Gráfico de barras para conexiones por cargo
        fig = px.bar(position_count, x='Position', y='Connections', title='Conexiones por Cargo', color='Connections', 
                     labels={'Connections': 'Número de Conexiones', 'Position': 'Cargo'},
                     color_continuous_scale=px.colors.sequential.Viridis)
        fig.show()

    def plot_network_graph(self, df):
        G = nx.Graph()
        company_position_count = defaultdict(int)

        # Contar ocurrencias de cada combinación compañía-puesto
        for _, row in df.iterrows():
            company = row['Company']
            position = row['Position']
            company_position_count[(company, position)] += 1

        # Ordenar y limitar a 100
        top_100_company_position = sorted(company_position_count.items(), key=lambda x: x[1], reverse=True)[:100]

        # Añadir nodos y aristas al grafo
        for (company, position), count in top_100_company_position:
            G.add_node(company, bipartite=0)
            G.add_node(position, bipartite=1)
            G.add_edge(company, position, weight=count)

        # Separar nodos de compañías y posiciones
        company_nodes = {n for n, d in G.nodes(data=True) if d['bipartite'] == 0}
        position_nodes = set(G.nodes()) - company_nodes

        # Crear una nueva figura
        fig, ax = plt.subplots(figsize=(20, 20))

        # Definir el layout circular
        pos = nx.circular_layout(G)

        # Dibujar los nodos
        nx.draw_networkx_nodes(G, pos, nodelist=company_nodes, node_color='lightgreen', node_size=100, ax=ax)
        nx.draw_networkx_nodes(G, pos, nodelist=position_nodes, node_color='lightblue', node_size=100, ax=ax)

        # Dibujar las aristas con grosor basado en el peso
        edge_widths = [G[u][v]['weight'] / 5 for u, v in G.edges()]
        nx.draw_networkx_edges(G, pos, ax=ax, alpha=0.5, width=edge_widths)

        # Añadir etiquetas
        for node, (x, y) in pos.items():
            angle = np.arctan2(y, x)
            if angle < 0:
                angle += 2 * np.pi
            if 0 <= angle < np.pi / 2 or 3 * np.pi / 2 <= angle <= 2 * np.pi:
                ha = 'left'
                rotation = angle * 180 / np.pi
            else:
                ha = 'right'
                rotation = (angle - np.pi) * 180 / np.pi
            plt.text(1.1 * x, 1.1 * y, node, rotation=rotation,
                     ha=ha, va='center', rotation_mode='anchor', fontsize=8)

        # Quitar los ejes
        ax.axis('off')

        # Ajustar el diseño
        plt.tight_layout()

        # Guardar la figura
        plt.savefig('circular_network_plot.jpg', bbox_inches='tight', dpi=150)

        # Mostrar el gráfico (opcional)
        plt.show()

        # Imprimir el nombre del archivo creado
        print("Created/Modified files during execution:")
        print("circular_network_plot.jpg")

    def plot_connections_by_date(self, df):
        # Asegurarnos de que la columna 'Connected On' esté en formato de fecha
        df['Connected On'] = pd.to_datetime(df['Connected On'], errors='coerce')

        # Contar conexiones por fecha
        connections_by_date = df['Connected On'].value_counts().reset_index()
        connections_by_date.columns = ['Date', 'Connections']
        connections_by_date = connections_by_date.sort_values('Date')

        # Gráfico de líneas para conexiones por fecha
        fig2 = px.line(connections_by_date, x='Date', y='Connections', title='Conexiones por Fecha', markers=True)
        fig2.show()


if __name__ == "__main__":
    root = Tk()
    app = VisualizationApp(root)
    root.mainloop()