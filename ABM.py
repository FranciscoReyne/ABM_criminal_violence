"""
What should this code do?  
- Defines a simulation with agents representing criminal groups.  
- Compares two scenarios:  
  - **Without Selective Dismantling:** Criminal groups grow and increase their violence without restrictions.  
  - **With Selective Dismantling:** The most aggressive groups are identified and weakened, reducing violence.  
- Generates a graph showing how violence levels evolve in each scenario.

"""

import matplotlib.pyplot as plt
from mesa import Agent, Model
from mesa.time import RandomActivation

class CriminalGroup(Agent):
    """Represents a criminal group with strength and aggression levels."""
    
    def __init__(self, unique_id, model):
        super().__init__(unique_id, model)
        self.strength = model.random.randint(5, 20)  # Initial power
        self.aggression = model.random.randint(1, 10)  # Initial violence

    def step(self):
        """Defines the group's behavior each time step."""
        if self.model.selective_dismantling and self.aggression > 5:
            # Intervention weakens violent groups
            self.strength *= 0.8  
            self.aggression *= 0.5  
        else:
            # No intervention: groups grow in strength and violence
            self.strength += 1
            self.aggression += 1

class CrimeModel(Model):
    """Simulates criminal competition with or without selective dismantling."""
    
    def __init__(self, num_groups, selective_dismantling):
        self.selective_dismantling = selective_dismantling
        self.schedule = RandomActivation(self)
        self.violence_levels = []

        # Create criminal groups
        for i in range(num_groups):
            self.schedule.add(CriminalGroup(i, self))

    def step(self):
        """Advances the simulation by one time step."""
        self.schedule.step()
        self.violence_levels.append(sum(agent.aggression for agent in self.schedule.agents))

def run_simulation(steps, num_groups):
    """Runs and compares the two scenarios."""
    
    models = {
        "Without Selective Dismantling": CrimeModel(num_groups, False),
        "With Selective Dismantling": CrimeModel(num_groups, True)
    }

    for _ in range(steps):
        for model in models.values():
            model.step()

    # Plot results
    for label, model in models.items():
        plt.plot(model.violence_levels, label=label)

    plt.xlabel("Time Steps")
    plt.ylabel("Total Violence Level")
    plt.title("Comparison: Criminal Violence with and without Selective Dismantling")
    plt.legend()
    plt.show()

# Run the simulation
run_simulation(100, 10)
