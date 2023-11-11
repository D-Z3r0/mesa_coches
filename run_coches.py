import seaborn as sns
import pandas as pd
import matplotlib.pyplot as plt
from coches_model import CityModel

import seaborn as sns
import matplotlib.pyplot as plt
import pandas as pd

def run_model():
    model = CityModel(num_cars=10, num_lanes=4, grid_width=20, grid_height=20)
    for i in range(300):
        model.step()
    data = model.datacollector.get_model_vars_dataframe()
    total_collisions = data.iloc[-1]['Total Collisions']
    return total_collisions, data

# Ejecutar la simulación 100 veces y almacenar los totales de colisiones y los DataFrames
total_collisions_per_run = []
all_runs_data = []
for _ in range(100):
    total_collisions, data = run_model()
    total_collisions_per_run.append(total_collisions)
    all_runs_data.append(data)

# Concatenar todos los DataFrames en uno solo
all_runs_df = pd.concat(all_runs_data, ignore_index=True)

# Crear una figura con dos subgráficos
fig, axes = plt.subplots(nrows=2, ncols=1, figsize=(10, 15))



# Primera gráfica: Lineplot del total de colisiones en cada ejecución
sns.lineplot(data=total_collisions_per_run, ax=axes[0])
axes[0].set_title('Total Collisions per Run')
axes[0].set_xlabel('Run Number')
axes[0].set_ylabel('Total Collisions')



# Preparar datos para la gráfica de barras
total_car_collisions = all_runs_df['Car Collisions'].sum()
total_taxi_collisions = all_runs_df['Taxi Collisions'].sum()
total_drunk_driver_collisions = all_runs_df['DrunkDriver Collisions'].sum()

collisions_data = {
    'Agent Type': ['Cars', 'Taxis', 'Drunk Drivers'],
    'Total Collisions': [total_car_collisions, total_taxi_collisions, total_drunk_driver_collisions]
}
collisions_df = pd.DataFrame(collisions_data)

# Segunda gráfica: Barplot de colisiones totales por tipo de agente
sns.barplot(x='Agent Type', y='Total Collisions', data=collisions_df, ax=axes[1])
axes[1].set_title('Total Collisions by Agent Type Across All Runs')
axes[1].set_xlabel('Agent Type')
axes[1].set_ylabel('Total Collisions')

# Mostrar las gráficas
plt.tight_layout()
plt.show()