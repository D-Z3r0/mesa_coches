import mesa
import seaborn as sns
import numpy as np
import pandas as pd
import random

class SidewalkAgent(mesa.Agent):
    """An agent representing a sidewalk."""
    def __init__(self, unique_id, model):
        super().__init__(unique_id, model)
        print(f"Banqueta Agent Created {str(self.unique_id)}.")




class StreetAgent(mesa.Agent):
    """An agent representing a street lane."""
    def __init__(self, unique_id, model):
        super().__init__(unique_id, model)
        print(f"Calle Agent Created {str(self.unique_id)}.")




class CarAgent(mesa.Agent):
    """An agent representing a car."""
    def __init__(self, unique_id, model):
        super().__init__(unique_id, model)
        self.direction = "N"
        self.collided = False  # Añade una bandera para indicar si el agente ha colisionado
        self.collision_countdown = 0

    def detect_collision(self, new_position):
        cellmates = self.model.grid.get_cell_list_contents(new_position)
        for occupant in cellmates:
            if isinstance(occupant, CarAgent) and occupant is not self:
                # Marca ambos coches como colisionados
                occupant.collided = True
                occupant.collision_countdown = 60  # Inicia el contador para la recuperación
                self.collided = True
                self.collision_countdown = 60
                return True  # Retorna True si hay una colisión
        return False  # Retorna False si no hay colisión
    
    def check_for_car_ahead(self, position):
        # Revisa la celda directamente en frente del agente para ver si contiene un coche
        cell_contents = self.model.grid.get_cell_list_contents(position)
        return any(isinstance(obj, CarAgent) for obj in cell_contents)
    
    def is_sidewalk(self, position):
        # Implementa la lógica para determinar si una posición es banqueta
        # Por ejemplo, podrías comprobar si la 'x' está fuera de los límites de la calle
        x, y = position
        return x < self.model.street_start or x >= self.model.street_end

    def move(self):
        if not self.collided:
            current_x, current_y = self.pos
            forward = (current_x, (current_y + 1) % self.model.grid.height)
            left = ((current_x - 1) % self.model.grid.width, (current_y + 1) % self.model.grid.height)
            right = ((current_x + 1) % self.model.grid.width, (current_y + 1) % self.model.grid.height)
            
            # Define las probabilidades predeterminadas
            probabilities = [0.9, 0.05, 0.05]

            # Comprueba si hay un coche en frente
            car_ahead = self.check_for_car_ahead(forward)

             # Comprueba si las posiciones adelante, izquierda y derecha son banquetas
            forward_is_sidewalk = self.is_sidewalk(forward)
            left_is_sidewalk = self.is_sidewalk(left)
            right_is_sidewalk = self.is_sidewalk(right)
            
            # Si hay un coche adelante o la posición adelante es banqueta, ajusta las probabilidades
            if car_ahead or forward_is_sidewalk:
                probabilities = [0, 0.5, 0.5] if not forward_is_sidewalk else [0, 1, 1]
                # Ajusta las probabilidades si alguna de las direcciones laterales es banqueta
                if left_is_sidewalk:
                    probabilities[1] = 0
                if right_is_sidewalk:
                    probabilities[2] = 0
            
            # Normaliza las probabilidades para que sumen 1
            total = sum(probabilities)
            probabilities = [p / total for p in probabilities]
            
            # Elige el próximo movimiento
            move = random.choices(["forward", "left", "right"], weights=probabilities, k=1)[0]
            new_position = {'forward': forward, 'left': left, 'right': right}[move]
            
            # Realiza el movimiento si no hay colisión y no es una banqueta
            if not self.detect_collision(new_position) and not self.is_sidewalk(new_position):
                self.model.grid.move_agent(self, new_position)

    def step(self):
         # Si el coche ha colisionado, incrementa el contador de colisión
        if self.collided:
            self.collision_countdown -= 1
            if self.collision_countdown <= 0:  # Si el contador llega a cero, el coche se recupera
                self.collided = False
        else:
            self.move()  # Mueve el coche solo si no ha colisionado
        # Otras funciones relacionadas con el coche aquí




    

class TaxiAgent(CarAgent):
    def __init__(self, unique_id, model, lane = None):
        super().__init__(unique_id, model)
        # Atributo para rastrear cuánto tiempo ha estado esperando el taxi
        self.wait_time = 0
        # Inicialmente lane puede ser None, y se establecerá después de la colocación
        self.lane = lane

    def move(self):
        if not self.collided and self.wait_time == 0:
            # Los taxis solo se mueven hacia adelante
            new_y = (self.pos[1] + 1) % self.model.grid.height
            new_position = (self.lane, new_y)
            # Verifica si la nueva posición es válida antes de mover al agente
            # Usa el método del modelo para verificar si la celda está ocupada
            if not self.model.is_cell_occupied_by_vehicle(self.lane, new_y):
                self.model.grid.move_agent(self, new_position)

    def step(self):
        # Primero, maneja la lógica de espera si el taxi está recogiendo pasajeros
        if self.wait_time > 0:
            # El taxi está esperando, decrementa el tiempo de espera
            self.wait_time -= 1
        else:
            # Decide aleatoriamente si el taxi debe recoger pasajeros
            if random.randint(1, 10) == 1:  # Hay un 10% de probabilidad en cada paso
                # Establece el tiempo de espera aleatoriamente entre 5 y 10 pasos
                self.wait_time = random.randint(5, 10)
            elif not self.collided:
                # Si no está colisionado y no está esperando, entonces se mueve
                self.move()
        
        # Luego, maneja la lógica de colisión y recuperación
        super().step()



class DrunkDriverAgent(CarAgent):
    """An agent that simulates a drunk driver."""

    def __init__(self, unique_id, model):
        super().__init__(unique_id, model)

    def move(self):
        if not self.collided:
            current_x, current_y = self.pos

            # Define las posiciones posibles dentro de los límites de la calle
            forward = (current_x, (current_y + 1) % self.model.grid.height)
            left = ((current_x - 1 + self.model.grid.width) % self.model.grid.width, (current_y + 1) % self.model.grid.height) if not self.is_sidewalk((current_x - 1, current_y)) else forward
            right = ((current_x + 1) % self.model.grid.width, (current_y + 1) % self.model.grid.height) if not self.is_sidewalk((current_x + 1, current_y)) else forward
            
            # Define las probabilidades para cada movimiento
            probabilities = [0.5, 0.25, 0.25]  # 50% adelante, 25% izquierda (si no es banqueta), 25% derecha (si no es banqueta)
            
            # Asegúrate de que las posiciones laterales no sean banquetas
            if self.is_sidewalk(left):
                probabilities[1] = 0  # No puede moverse hacia la izquierda si hay banqueta
            if self.is_sidewalk(right):
                probabilities[2] = 0  # No puede moverse hacia la derecha si hay banqueta
            
            # Normaliza las probabilidades para que sumen 1
            probabilities = [p / sum(probabilities) for p in probabilities]
            
            possible_steps = ["forward", "left", "right"]
            move = random.choices(possible_steps, weights=probabilities, k=1)[0]
            new_position = {'forward': forward, 'left': left, 'right': right}[move]
            
            # Mueve el agente si la nueva posición es válida y no es banqueta
            if not self.detect_collision(new_position) and not self.is_sidewalk(new_position):
                self.model.grid.move_agent(self, new_position)

    def step(self):
        # Aquí podrías incluir cualquier comportamiento adicional que el conductor ebrio deba realizar
        # Por ejemplo, podría cambiar de dirección aleatoriamente
        if self.collided:
            # Incrementa el contador si el coche ha colisionado
            self.collision_countdown += 1
            # Si han pasado 60 pasos desde la colisión, el coche puede moverse nuevamente
            if self.collision_countdown >= 60:
                self.collided = False
                self.collision_countdown = 0
        else:
            self.move()  # Llama al método move que ha sido sobrescrito para tener distintas probabilidades





# Modificación del modelo
class CityModel(mesa.Model):
    def __init__(self, num_cars, num_lanes, grid_width, grid_height):
        # Create scheduler and assign it to the model
        self.grid = mesa.space.MultiGrid(grid_width, grid_height, True)
        self.schedule = mesa.time.RandomActivation(self)
        self.num_steps = 0  # Añade un contador de pasos

        # Create agents

        # Calcula el inicio y fin de la calle en la cuadrícula
        self.street_start = (grid_width - num_lanes) // 2
        self.street_end = self.street_start + num_lanes

        # Agregar calle y banquetas
        for x in range(grid_width):
            for y in range(grid_height):
                # Si la posición 'x' está dentro de los límites de la calle, es parte de la calle
                if self.street_start <= x < self.street_end:
                    # Crear y colocar un agente de calle
                    street_agent = StreetAgent((x, y), self)
                    self.grid.place_agent(street_agent, (x, y))
                else:
                    # De lo contrario, es banqueta
                    sidewalk_agent = SidewalkAgent((x, y), self)
                    self.grid.place_agent(sidewalk_agent, (x, y))

        # Inicializa los coches en la parte inferior de la calle
        # y = grid_height - (grid_height)  # Índice para la fila inferior

        # Inicializa los coches en la parte inferior de la calle
        for i in range(num_cars):
            car = CarAgent(i, self)
            # Elige una posición 'x' dentro de los límites de la calle
            x = self.random.randrange(self.street_start, self.street_end)
            self.grid.place_agent(car, (x, 0))
            self.schedule.add(car)

    def add_vehicle(self, agent_type):
        unique_id = max(agent.unique_id for agent in self.schedule.agents) + 1
        # Para TaxiAgent, elige un carril extremo basado en dónde comienza y termina la calle
        if agent_type is TaxiAgent:
            x = random.choice([self.street_start, self.street_end - 1])
        else:
            # Para otros agentes, elige cualquier posición x dentro de la calle
            x = self.random.randrange(self.street_start, self.street_end)
        y = 0  # La fila donde se añadirán los nuevos vehículos (parte inferior del grid)
        
        # Verifica si la celda está ocupada por algún vehículo
        if not self.is_cell_occupied_by_vehicle(x, y):
            # Crea un nuevo vehículo y colócalo en el grid
            if agent_type is TaxiAgent:
                # Crea un taxi y asigna el carril extremo al atributo 'lane'
                new_vehicle = agent_type(unique_id, self)
                new_vehicle.lane = x  # Asigna el carril extremo
            else:
                # Crea un vehículo que no es taxi (CarAgent o DrunkDriverAgent)
                new_vehicle = agent_type(unique_id, self)

            self.grid.place_agent(new_vehicle, (x, y))
            self.schedule.add(new_vehicle)
            print("vehículo añadido")

    def is_cell_occupied_by_vehicle(self, x, y):
        cellmates = self.grid.get_cell_list_contents((x, y))
        return any(isinstance(agent, (CarAgent, TaxiAgent, DrunkDriverAgent)) for agent in cellmates)

    def step(self):
        """Advance the model by one step."""
        self.num_steps += 1
        # Verificar y añadir un CarAgent cada 20 pasos
        if self.num_steps % 20 == 0:
            self.add_vehicle(CarAgent)
        # Verificar y añadir un TaxiAgent cada 30 pasos
        if self.num_steps % 30 == 0:
            self.add_vehicle(TaxiAgent)
            print("aniadir taxi")
        # Verificar y añadir un DrunkDriverAgent cada 50 pasos
        if self.num_steps % 50 == 0:
            self.add_vehicle(DrunkDriverAgent)
            print("aniadir borracho")
        # Actualizar todos los agentes
        self.schedule.step()
