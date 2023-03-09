from mesa.visualization.ModularVisualization import ModularServer
from mesa.visualization.modules import CanvasGrid, ChartModule, TextElement
from mesa.visualization.UserParam import UserSettableParameter

from prey_predator.agents import Wolf, Sheep, GrassPatch
from prey_predator.model import WolfSheep


def wolf_sheep_portrayal(agent):
    if agent is None:
        return

    portrayal = {}

    if type(agent) is Sheep:
        portrayal = {"Shape": "rect",
                 "Color": "black",
                 "Filled": "true",
                 "Layer": 1,
                 "h": 0.4,
                 "w" : 0.4}
        
    elif type(agent) is Wolf:
        portrayal = {"Shape": "rect",
                 "Color": "red",
                 "Filled": "true",
                 "Layer": 2,
                 "h": 0.7,
                 "w" : 0.7}
        
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
    "initial_sheep" : UserSettableParameter("slider", "Initial Sheep", 10, 1, 30, 1),
    "initial_wolves" : UserSettableParameter("slider", "Initial Wolf", 5, 1, 30, 1),
    "sheep_reproduce" : UserSettableParameter("slider", "Sheep Growth Rate", 0.04, 0, 0.2, 0.02),
    "wolf_reproduce" : UserSettableParameter("slider", "Wolf Growth Rate", 0.04, 0, 0.2, 0.02),
    "wolf_gain_from_food" : UserSettableParameter("slider", "Wolf Gain from Food", 20, 1, 50, 1),
    "grass" : False,
    "sheep_gain_from_food" : UserSettableParameter("slider", "Sheep Gain from Food", 4, 1, 20, 1),
    "grass_regrowth_time" : UserSettableParameter("slider", "Grass Regrowth Time", 30, 1, 50, 1)
}

server = ModularServer(
    WolfSheep, [canvas_element, chart_element], "Prey Predator Model", model_params
)
server.port = 8521
