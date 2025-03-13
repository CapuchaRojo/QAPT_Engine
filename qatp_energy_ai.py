import numpy as np

class QuantumEnergyAI:
    """AI-powered energy optimization for real-time self-regulation."""

    def __init__(self):
        self.energy_history = []  # Tracks past charge/discharge patterns
    
    def predict_usage(self, recent_usage: list):
        """Predicts upcoming energy demands based on historical usage."""
        if len(recent_usage) < 5:
            return np.mean(recent_usage) if recent_usage else 1.0  # Default base usage

        weights = np.linspace(0.2, 1, len(recent_usage))  # Weighted average for recent trends
        return np.dot(recent_usage, weights) / np.sum(weights)

    def optimize_discharge(self, battery, system_load):
        """Optimizes battery discharge dynamically based on demand forecasts."""
        predicted_demand = self.predict_usage(self.energy_history[-10:])
        if system_load > predicted_demand:
            return battery.discharge(predicted_demand * 1.1)  # Slight over-discharge to compensate for spikes
        return battery.discharge(predicted_demand * 0.9)  # Slight under-discharge to preserve energy
    
    def log_usage(self, usage):
        """Stores energy usage trends for future AI adaptation."""
        self.energy_history.append(usage)
        if len(self.energy_history) > 100:
            self.energy_history.pop(0)  # Keep history manageable
