from mesa import Agent
from prey_predator.random_walk import RandomWalker
import random

class Sheep(RandomWalker):
    """
    A sheep that walks around, reproduces (asexually) and gets eaten.

    The init is the same as the RandomWalker.
    """

    energy = None
    energy_step = 1
    energy_growth = 1

    def __init__(self, unique_id, pos, model, moore, energy=None):
        super().__init__(unique_id, pos, model, moore=moore)
        self.energy = energy

    def eat(self, grass_agent):
        grass_agent.fully_grown = 0
        self.energy += self.model.sheep_gain_from_food


    def reproduce(self):
        child_pos = self.pos
        a = Sheep(self.model.next_id(), child_pos , self.model, moore=True, energy=10)
        self.model.schedule.add(a)
        # Add the agent to a random grid cell
        self.model.grid.place_agent(a, child_pos)

    def die(self):
        self.model.grid.remove_agent(self)
        self.model.schedule.remove(self)

    def step(self):
        """
        A model step. Move, then eat grass and reproduce.
        """
        self.random_move()
        self.energy -= self.energy_step

        # Manger
        cellmates = self.model.grid.get_cell_list_contents([self.pos])
        if len(cellmates) > 1:
            for agent in cellmates:
                if type(agent) is GrassPatch:
                    if agent.fully_grown:
                        self.eat(agent)

        # Reproduction
        prob=random.random()
        if self.energy > self.energy_growth and prob<=self.model.sheep_reproduce:
            self.reproduce()
        
        # Mort
        if self.energy<=0:
            self.die()


class Wolf(RandomWalker):
    """
    A wolf that walks around, reproduces (asexually) and eats sheep.
    """

    energy = None
    energy_step = 1
    energy_growth = 5

    def __init__(self, unique_id, pos, model, moore, energy=None):
        super().__init__(unique_id, pos, model, moore=moore)
        self.energy = energy

    def eat(self, sheep_agent):
        sheep_agent.die()
        self.energy += self.model.wolf_gain_from_food

    def reproduce(self):
        x = self.pos[0]
        y = self.pos[1]
        a = Wolf(self.model.next_id(), (x,y), self.model, moore=True, energy=10)
        self.model.schedule.add(a)
        # Add the agent to a random grid cell
        self.model.grid.place_agent(a, (x, y))

    def die(self):
        self.model.grid.remove_agent(self)
        self.model.schedule.remove(self)

    def step(self):
        self.random_move()
        self.energy=self.energy-1

        # Manger
        cellmates = self.model.grid.get_cell_list_contents([self.pos])
        if len(cellmates) > 1:
            for agent in cellmates:
                if type(agent) is Sheep:
                    self.eat(agent)
                    break

        # Reproduction
        prob=random.random()
        if self.energy > self.energy_growth and prob<self.model.wolf_reproduce:
            self.reproduce()

        #Mort
        if self.energy<=0:
            self.die()


class GrassPatch(Agent):
    """
    A patch of grass that grows at a fixed rate and it is eaten by sheep
    """

    def __init__(self, unique_id, pos, model, fully_grown, countdown):
        """
        Creates a new patch of grass

        Args:
            fully_grown: (boolean) Whether the patch of grass is fully grown or not
            countdown: Time for the patch of grass to be fully grown again
        """
        super().__init__(unique_id, model)
        self.fully_grown = fully_grown
        self.countdown = countdown
        self.pos = pos 

    def step(self):
        if self.fully_grown == 0:
            if self.countdown > 0:
                self.countdown -= 1
                self.fully_grown = 0
            else:
                self.countdown = self.model.grass_regrowth_time
                self.fully_grown = 1