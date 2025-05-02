
"""
I've incorporated noise into the model by adding random fluctuations to aggression and strength levels at each step. 
This simulates the unpredictability of criminal activity due to external factors like law enforcement pressure, economic changes, or internal conflicts

Enhancements With Noise
- Random fluctuations added to aggression and strength to simulate external uncertainties.
- Ensured stability by bounding values, preventing extreme crashes.
- More realistic dynamics reflecting crime volatility.

This improves tge model while keeping it simple.


"""
import numpy as np
import matplotlib.pyplot as plt
from mesa import Agent, Model
from mesa.time import RandomActivation

class CriminalGroup(Agent):
    """Represents a criminal group with strength and aggression levels, incorporating random noise."""
    
    def __init__(self, unique_id, model):
        super().__init__(unique_id, model)
        self.strength = model.random.randint(5, 20)  # Initial power
        self.aggression = model.random.randint(1, 10)  # Initial violence

    def step(self):
        """Defines the group's behavior each time step with noise added."""
        noise = np.random.normal(0, 2)  # Random noise with mean 0 and standard deviation 2

        if self.model.selective_dismantling and self.aggression > 5:
            # Intervention weakens violent groups
            self.strength *= max(0.8 + noise / 20, 0.5)  # Ensure values don't drop too much
            self.aggression *= max(0.5 + noise / 10, 0.2)  
        else:
            # No intervention: groups grow unpredictably
            self.strength += max(1 + noise, 0)  
            self.aggression += max(1 + noise / 2, 0)  

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
    plt.title("Comparison: Criminal Violence with and without Selective Dismantling (with Noise)")
    plt.legend()
    plt.show()

# Run the simulation
run_simulation(100, 10)
