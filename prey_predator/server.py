from mesa.visualization.ModularVisualization import ModularServer
from mesa.visualization.modules import CanvasGrid, ChartModule
from mesa.visualization.UserParam import UserSettableParameter

from prey_predator.agents import Wolf, Sheep, GrassPatch
from prey_predator.model import WolfSheep


def wolf_sheep_portrayal(agent):
    if agent is None:
        return

    portrayal = {}

    if type(agent) is Sheep:
        portrayal = {"Shape": "rect",
                 "Color": "red",
                 "Filled": "true",
                 "Layer": 1,
                 "h": 0.5,
                 "w" : 0.5}
        
    elif type(agent) is Wolf:
        portrayal = {"Shape": "rect",
                 "Color": "black",
                 "Filled": "true",
                 "Layer": 2,
                 "h": 0.5,
                 "w" : 0.5}
        
    elif type(agent) is GrassPatch:
        if agent.fully_grown == 1:
            portrayal = {"Shape": "rect",
                    "Color": "green",
                    "Filled": "true",
                    "Layer": 0,
                    "h": 1,
                    "w" : 1}
        else:
            portrayal = {}
        
    
    return portrayal


canvas_element = CanvasGrid(wolf_sheep_portrayal, 20, 20, 500, 500)
chart_element = ChartModule(
    [{"Label": "Wolves", "Color": "#AA0000"}, {"Label": "Sheep", "Color": "#666666"}]
)

model_params = {
    "width":20, 
    "height":20,
    "initial_sheep" : 10,
    "initial_wolves" : 10,
    "sheep_reproduce" : 0.1,
    "wolf_reproduce" : 0.05,
    "wolf_gain_from_food" : 20,
    "grass" : False,
    "grass_regrowth_time" : 30,
    "sheep_gain_from_food" : 4    
}

server = ModularServer(
    WolfSheep, [canvas_element, chart_element], "Prey Predator Model", model_params
)
server.port = 8521
