import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import datetime
from data import *
from schedule import *
from classes import *

# Plot arrivals and departures
def plot_trains(events, color, marker="o", linestyle=" ", markerfacecolor=None, real_events=None,marker2=None,color2=None):
    for i, event in enumerate(events):
        if event:
            plt.plot(i, event, marker=marker, color=color, markerfacecolor=markerfacecolor)

    if real_events and any(real_events):
        for i, real_event in enumerate(real_events):
            if real_event:
                plt.plot(i, real_event, marker=marker2, color=color2)
            
# Connect the ATD with ATA
def connect(tren,departures, arrivals, real_departures):
    for i in range(len(departures) - 1):  # Evitar index fuera de rango

        if tren<=6:
            departure_to_connect = departures[i]  # Valor predeterminado para la salida
            if real_departures[i]:  # Verifica si hay salida real
                departure_to_connect = real_departures[i]

            if departure_to_connect and arrivals[i + 1]:  # Conectar si hay salida y llegada
                plt.plot([i, i + 1], [departure_to_connect, arrivals[i + 1]], linestyle="--", color="gray")

        else:
            departure_to_connect = departures[i+1]  # Valor predeterminado para la salida
            if real_departures[i+1]:  # Verifica si hay salida real
                departure_to_connect = real_departures[i+1]
            if departure_to_connect and arrivals[i]:  # Conectar si hay salida y llegada
                plt.plot([i+1, i], [departure_to_connect,arrivals[i]], linestyle="--", color="gray")


# Add train lables
def add_train_labels(arrivals, departures, train_name, color, reverse=False):
    indices = range(len(arrivals))
    if reverse:  # Invertir el rango si es necesario
        indices = reversed(indices)
    
    for i in indices:
        if arrivals[i] or departures[i]:  # Si hay un dato válido
            if int(train_name)>6:
                plt.text(i+0.5, (arrivals[i] or departures[i]), "Train " + train_name, color=color, fontsize=9, ha='left', va='center')
            else:
                plt.text(i-0.5, (arrivals[i] or departures[i]), "Train " + train_name, color=color, fontsize=9, ha='right', va='center')                
            break




# Get arrival and departure times
arrivals1 = [entry["ATA"] for entry in data1]
departures1 = [entry.get("ETD") for entry in data1]
real_departures1= [entry.get("ATD") for entry in data1]

arrivals2 = [entry["ATA"] for entry in data2]
departures2 = [entry.get("ETD") for entry in data2]
real_departures2= [entry.get("ATD") for entry in data2]


arrivals3 = [entry["ATA"] for entry in data3]
departures3 = [entry.get("ETD") for entry in data3]
real_departures3= [entry.get("ATD") for entry in data3]


arrivals4 = [entry["ATA"] for entry in data4]
departures4 = [entry.get("ETD") for entry in data4]
real_departures4= [entry.get("ATD") for entry in data4]


arrivals5 = [entry["ATA"] for entry in data5]
departures5 = [entry.get("ETD") for entry in data5]
real_departures5= [entry.get("ATD") for entry in data5]


arrivals6 = [entry["ATA"] for entry in data6]
departures6 = [entry.get("ETD") for entry in data6]
real_departures6= [entry.get("ATD") for entry in data6]


arrivals7 = [entry["ATA"] for entry in data7]
departures7 = [entry.get("ETD") for entry in data7]
real_departures7= [entry.get("ATD") for entry in data7]


arrivals8 = [entry["ATA"] for entry in data8]
departures8 = [entry.get("ETD") for entry in data8]
real_departures8= [entry.get("ATD") for entry in data8]

arrivals9 = [entry["ATA"] for entry in data9]
departures9 = [entry.get("ETD") for entry in data9]
real_departures9= [entry.get("ATD") for entry in data9]

arrivals10 = [entry["ATA"] for entry in data10]
departures10 = [entry.get("ETD") for entry in data10]
real_departures10= [entry.get("ATD") for entry in data10]

arrivals11 = [entry["ATA"] for entry in data11]
departures11 = [entry.get("ETD") for entry in data11]
real_departures11= [entry.get("real_departure") for entry in data11]

arrivals12 = [entry["ATA"] for entry in data12]
departures12 = [entry.get("ETD") for entry in data12]
real_departures12= [entry.get("ATD") for entry in data12]

arrivals1_ = [entry["ATA"] for entry in data1_]
departures1_ = [entry.get("ETD") for entry in data1_]
real_departures1_= [entry.get("ATD") for entry in data1_]

arrivals2_ = [entry["ATA"] for entry in data2_]
departures2_ = [entry.get("ETD") for entry in data2_]
real_departures2_= [entry.get("ATD") for entry in data2_]


arrivals3_ = [entry["ATA"] for entry in data3_]
departures3_= [entry.get("ETD") for entry in data3_]
real_departures3_= [entry.get("ATD") for entry in data3_]


arrivals4_ = [entry["ATA"] for entry in data4_]
departures4_ = [entry.get("ETD") for entry in data4_]
real_departures4_= [entry.get("ATD") for entry in data4_]


arrivals5_ = [entry["ATA"] for entry in data5_]
departures5_ = [entry.get("ETD") for entry in data5_]
real_departures5_= [entry.get("ATD") for entry in data5_]


arrivals6_ = [entry["ATA"] for entry in data6_]
departures6_ = [entry.get("ETD") for entry in data6_]
real_departures6_= [entry.get("ATD") for entry in data6_]


arrivals7_ = [entry["ATA"] for entry in data7_]
departures7_ = [entry.get("ETD") for entry in data7_]
real_departures7_= [entry.get("ATD") for entry in data7_]


arrivals8_ = [entry["ATA"] for entry in data8_]
departures8_ = [entry.get("ETD") for entry in data8_]
real_departures8_= [entry.get("ATD") for entry in data8_]

arrivals9_ = [entry["ATA"] for entry in data9_]
departures9_ = [entry.get("ETD") for entry in data9_]
real_departures9_= [entry.get("ATD") for entry in data9_]

arrivals10_ = [entry["ATA"] for entry in data10_]
departures10_ = [entry.get("ETD") for entry in data10_]
real_departures10_= [entry.get("ATD") for entry in data10_]

arrivals11_ = [entry["ATA"] for entry in data11_]
departures11_ = [entry.get("ETD") for entry in data11_]
real_departures11_= [entry.get("real_departure") for entry in data11_]

arrivals12_ = [entry["ATA"] for entry in data12_]
departures12_ = [entry.get("ETD") for entry in data12_]
real_departures12_= [entry.get("ATD") for entry in data12_]



# Crear la gráfica
plt.figure(figsize=(15, 10))

# Convertir stations a posiciones numéricas
x_positions = range(len(stations_all))

# Graficar llegadas de los dos conjuntos de datos
color_ata="#ADD8E6"
plot_trains(arrivals1, color_ata)
plot_trains(arrivals2, color_ata)
plot_trains(arrivals3, color_ata)
plot_trains(arrivals4, color_ata)
plot_trains(arrivals5, color_ata)
plot_trains(arrivals6, color_ata)
plot_trains(arrivals7, color_ata)
plot_trains(arrivals8, color_ata)
plot_trains(arrivals9, color_ata)
plot_trains(arrivals10, color_ata)
plot_trains(arrivals11, color_ata)
plot_trains(arrivals12, color_ata)



# Graficar salidas de los dos conjuntos de datos
color_etd="#4682B4"
color_atd="#FF6347"
plot_trains(departures1, color_etd, markerfacecolor="none",real_events=real_departures1,marker2="x",color2=color_atd)
plot_trains(departures2, color_etd, markerfacecolor="none", real_events=real_departures2,marker2="x",color2=color_atd)
plot_trains(departures3, color_etd, markerfacecolor="none", real_events=real_departures3,marker2="x",color2=color_atd)
plot_trains(departures4, color_etd, markerfacecolor="none", real_events=real_departures4,marker2="x",color2=color_atd)
plot_trains(departures5, color_etd, markerfacecolor="none", real_events=real_departures5,marker2="x",color2=color_atd)
plot_trains(departures6, color_etd, markerfacecolor="none", real_events=real_departures6,marker2="x",color2=color_atd)
plot_trains(departures7, color_etd, markerfacecolor="none", real_events=real_departures7,marker2="x",color2=color_atd)
plot_trains(departures8, color_etd, markerfacecolor="none", real_events=real_departures8,marker2="x",color2=color_atd)
plot_trains(departures9, color_etd, markerfacecolor="none", real_events=real_departures9,marker2="x",color2=color_atd)
plot_trains(departures10, color_etd, markerfacecolor="none", real_events=real_departures10,marker2="x",color2=color_atd)
plot_trains(departures11, color_etd, markerfacecolor="none", real_events=real_departures11,marker2="x",color2=color_atd)
plot_trains(departures12, color_etd, markerfacecolor="none", real_events=real_departures12,marker2="x",color2=color_atd)

color_ott="#A9A9A9"
plot_trains(departures1_,  color_ott, markerfacecolor="none",real_events=real_departures1_)
plot_trains(departures2_,  color_ott, markerfacecolor="none", real_events=real_departures2_)
plot_trains(departures3_,  color_ott, markerfacecolor="none", real_events=real_departures3_)
plot_trains(departures4_,  color_ott, markerfacecolor="none", real_events=real_departures4_)
plot_trains(departures5_,  color_ott, markerfacecolor="none", real_events=real_departures5_)
plot_trains(departures6_,  color_ott, markerfacecolor="none", real_events=real_departures6_)
plot_trains(departures7_,  color_ott, markerfacecolor="none", real_events=real_departures7_)
plot_trains(departures8_,  color_ott, markerfacecolor="none", real_events=real_departures8_)
plot_trains(departures9_,  color_ott, markerfacecolor="none", real_events=real_departures9_)
plot_trains(departures10_,  color_ott, markerfacecolor="none", real_events=real_departures10_)
plot_trains(departures11_,  color_ott, markerfacecolor="none", real_events=real_departures11_)
plot_trains(departures12_, color_ott, markerfacecolor="none", real_events=real_departures12_)
plot_trains(arrivals1_, color_ott, markerfacecolor="none")
plot_trains(arrivals2_, color_ott, markerfacecolor="none")
plot_trains(arrivals3_, color_ott, markerfacecolor="none")
plot_trains(arrivals4_, color_ott, markerfacecolor="none")
plot_trains(arrivals5_, color_ott, markerfacecolor="none")
plot_trains(arrivals6_, color_ott, markerfacecolor="none")
plot_trains(arrivals7_, color_ott, markerfacecolor="none")
plot_trains(arrivals8_, color_ott, markerfacecolor="none")
plot_trains(arrivals9_, color_ott, markerfacecolor="none")
plot_trains(arrivals10_, color_ott, markerfacecolor="none")
plot_trains(arrivals11_, color_ott, markerfacecolor="none")
plot_trains(arrivals12_, color_ott, markerfacecolor="none")



# Conectar salidas con llegadas de la estación siguiente para ambos conjuntos de datos
connect(1,departures1, arrivals1, real_departures1)
connect(2,departures2, arrivals2, real_departures2)
connect(3,departures3, arrivals3, real_departures3)
connect(4,departures4, arrivals4, real_departures4)
connect(5,departures5, arrivals5, real_departures5)
connect(6,departures6, arrivals6, real_departures6)
connect(7,departures7, arrivals7, real_departures7)
connect(8,departures8, arrivals8, real_departures8)
connect(9,departures9, arrivals9, real_departures9)
connect(10,departures10, arrivals10, real_departures10)
connect(11,departures11, arrivals11, real_departures11)
connect(12,departures12, arrivals12, real_departures12)


# Añadir etiquetas a cada tren
add_train_labels(arrivals1, departures1, "1", "black")
add_train_labels(arrivals2, departures2, "2", "black")
add_train_labels(arrivals3, departures3, "3", "black")
add_train_labels(arrivals4, departures4, "4", "black")
add_train_labels(arrivals5, departures5, "5", "black")
add_train_labels(arrivals6, departures6, "6", "black")
add_train_labels(arrivals7, departures7, "7", "black", reverse=True)
add_train_labels(arrivals8, departures8, "8", "black", reverse=True)
add_train_labels(arrivals9, departures9, "9", "black", reverse=True)
add_train_labels(arrivals10, departures10, "10", "black", reverse=True)
add_train_labels(arrivals11, departures11, "11", "black", reverse=True)
add_train_labels(arrivals12, departures12, "12", "black", reverse=True)


# Configurar ejes
plt.xticks(ticks=x_positions, labels=stations_all, rotation=90)
plt.gca().xaxis.set_major_locator(plt.MultipleLocator(1))
plt.ylabel("Time")
plt.xlabel("Stations")
plt.title(str(D))

# Formatear el eje de tiempo
plt.gca().yaxis.set_major_formatter(mdates.DateFormatter("%H:%M"))
plt.gca().yaxis_date()

# Añadir leyenda
Legend = [
    plt.Line2D([0], [0], marker="o", color=color_ata, lw=0, markersize=10, label="ATA"),  # Actual Time of Arrival
    plt.Line2D([0], [0], marker="o", color=color_etd, lw=0, markerfacecolor="none", markersize=10, label="ETD"),  # Estimated Time of Departure
    plt.Line2D([0], [0], marker="x", color=color_atd, lw=0, markersize=10, label="ATD"),  # Actual Time of Departure
    plt.Line2D([0], [0], linestyle="--", color="gray", lw=2, markersize=10, label="route"),  # Route
    plt.Line2D([0], [0], marker="o", color=color_ott, lw=0,markerfacecolor="none", markersize=10, label="OTT")  # Original Timetable
]

# Añadimos la leyenda personalizada al gráfico
leyenda=plt.legend(handles=Legend, loc="upper right")
leyenda.set_draggable(True)

# Mostrar la gráfica
##plt.tight_layout()
plt.subplots_adjust(left=0.08, right=0.95, top=0.95, bottom=0.2) #Helps to distribute the graphic in the screen
plt.show()
