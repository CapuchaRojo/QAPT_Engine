import math

class QuantumExcitonTransportChain:
    """Simulates an exciton transport chain for real-time energy adaptation."""
    
    def __init__(self, length=5, base_efficiency=0.9, coherence_factor=0.98):
        self.length = length
        self.base_efficiency = base_efficiency
        self.coherence_factor = coherence_factor
        self.sites = [0.0] * length
    
    def transport_energy(self, input_energy: float) -> float:
        """Adapts energy transport dynamically based on real-time coherence metrics."""
        energy = input_energy
        for i in range(self.length):
            energy *= self.base_efficiency * self.coherence_factor  # Adjust based on coherence loss
            if energy < 0.01:  # Prevent unnecessary calculations for minimal energy levels
                break
            self.sites[i] = energy
        return energy

    def dynamic_coherence_adjustment(self, system_load: float):
        """Adjusts coherence factors dynamically to optimize transport under load conditions."""
        self.coherence_factor = max(0.95, min(1.0, 1 - math.exp(-system_load / 10)))  # Smooth adaptation
