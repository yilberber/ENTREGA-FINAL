from dash import Dash, html,dcc, Input, Output
import dash_bootstrap_components as dbc
import plotly.graph_objs as go

app = Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])

#Base de datos
from pymongo.mongo_client import MongoClient
uri = "mongodb+srv://cagomezj:1234@cluster0.lg8bsx8.mongodb.net/?retryWrites=true&w=majority"
# Create a new client and connect to the server
client = MongoClient(uri)
# Send a ping to confirm a successful connection
try:
    client.admin.command('ping')
    print("Pinged your deployment. You successfully connected to MongoDB!")
except Exception as e:
    print(e)

db = client.sensores.sensor_1
result = 0

# Declarar data_dist fuera de la función para evitar el UnboundLocalError
data_dist = []

# App layout
app.layout = dbc.Container(
    [ 

        html.H1("Asenta-Tiem-Re", style={'text-align': 'center'}),
        html.H5('Hemos creado esta página para ofrecerte una experiencia única: la posibilidad de visualizar los asentamientos en tiempo real. Esta plataforma te permite monitorear de cerca lo que sucede en el suelo, brindándote una ventana directa a la evolución de proyectos de construcción y desarrollo.'),
        html.Hr(),
        html.H2("Asentamiento Tuneladora", style={'text-align': 'center', 'color':'#001BBD'}),
    
        html.H4(id='distancia-actual', style={'text-align': 'center'}),
        dcc.Graph(id='asentamiento'),
        dcc.Interval(
            id='interval-component',
            interval=1 * 500,  # en milisegundos, actualiza cada 1 segundo
            n_intervals=0
        ),
        html.Div(id='alerta-texto', style={'text-align': 'center', 'margin-top': '10px'}),   
        html.Hr(), 
        html.H2('Datos del proyecto'),
            html.Label('Nombre:'),
            dbc.Input(value="Nombre"),
            html.Label('Localización:'),
            dbc.Input(value="Localización"),
            html.Label('Fecha Inicio:'),
            dbc.Input(value="Fecha", type="date"),
            html.Label('Fecha Fin:'),
            dbc.Input(value="Fecha", type="date"),
            html.Hr(),
    ],
    style={'background-color':'#15B5D5'},
)

@app.callback(
    [Output('asentamiento', 'figure'),
     Output('distancia-actual', 'children'),
     Output('alerta-texto', 'children')],
    [Input('interval-component', 'n_intervals')]
)
def consultar(n):
    
    # Utilizar la variable global data_dist
    global data_dist , result , db
    result = db.find_one(sort=[('updated_at', -1)])
    distancia = int(result['distancia'])
    data_dist.append(distancia)
    
    # Crear el objeto de figura de Plotly
    fig = go.Figure(data=[go.Scatter(y=data_dist, mode='lines+markers')])
    
     # Agregar una línea horizontal en y=5
    fig.add_shape(
        type="line",
        x0=0,
        x1=len(data_dist),
        y0=1600,
        y1=1600,
        line=dict(color="red", width=2),    
    )
    
    # Agregar un texto según la condición
    if distancia >= 1600:
        alerta_texto = html.Span("ALERTA", style={'color': 'red', 'font-size': '24px'})
    else:
        alerta_texto = html.Span("VAMOS BIEN", style={'color': 'green', 'font-size': '24px'})
    
    
    # Formatear la distancia para mostrarla en el H1
    distancia_texto = f"El asentamiento fue: {distancia} cm"
    
    return fig, distancia_texto,alerta_texto


if __name__ == "__main__":
    app.run_server(debug=True)