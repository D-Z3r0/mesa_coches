from coches_model import mesa, CityModel, CarAgent, TaxiAgent, DrunkDriverAgent, StreetAgent, SidewalkAgent

# Modificar la función de visualización
def agent_portrayal(agent):
    if isinstance(agent, TaxiAgent):  # Verifica primero TaxiAgent
        portrayal = {"Shape": "rect", "Filled": "true", "Color": "yellow", "Layer": 3, "w": 0.5, "h": 1}
        if agent.wait_time > 0:
            portrayal["Color"] = "orange"  # Los taxis recogiendo pasajeros se muestran en naranja
    elif isinstance(agent, DrunkDriverAgent):  # Luego verifica DrunkDriverAgent
        portrayal = {"Shape": "rect", "Filled": "true", "Color": "blue", "Layer": 4, "w": 0.5, "h": 1}
        if agent.collided:
            portrayal["Color"] = "black"  # Los conductores ebrios colisionados se muestran en negro
    elif isinstance(agent, CarAgent):  # Finalmente, verifica CarAgent
        portrayal = {"Shape": "rect", "Filled": "true", "Layer": 2, "w":0.5, "h":1}
        portrayal["Color"] = "black" if agent.collided else "red"  # Negro si colisionó, rojo de lo contrario
    elif isinstance(agent, StreetAgent):
        portrayal = {"Shape": "rect", "Filled": "true", "Color": "grey", "Layer": 1, "w": 1, "h": 1}
    elif isinstance(agent, SidewalkAgent):
        portrayal = {"Shape": "rect", "Filled": "true", "Color": "green", "Layer": 0, "w": 1, "h": 1}
    return portrayal

grid = mesa.visualization.CanvasGrid(agent_portrayal, 20, 20, 500, 500)

server = mesa.visualization.ModularServer(CityModel,
                       [grid],
                       "City Model",
                       {"num_cars":1, "num_lanes": 4, "grid_width":20, "grid_height":20})
server.port = 8521 # The default
server.launch()