# --- IMPORTS ---
import logging
import math
import random

# --- CONFIGURE LOGGING ---
logging.basicConfig(level=logging.INFO, filename="qatp_engine.log",
                    format="%(asctime)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)


# ========================
# 🔷 QUANTUM ENERGY MODULES
# ========================
class QuantumExcitonTransportChain:
    """Simulates an exciton transport chain for efficient quantum energy transfer."""

    def __init__(self, length=5, base_efficiency=0.9, coherence_factor=0.98):
        self.length = length
        self.base_efficiency = base_efficiency
        self.coherence_factor = coherence_factor
        self.sites = [0.0] * length

    def transport_energy(self, input_energy):
        """Simulates energy transfer across the transport chain, factoring in coherence loss."""
        if isinstance(input_energy, list):  # Handle list input properly
            return [self.transport_energy(value) for value in input_energy]

        energy = float(input_energy)  # Ensure it's a float
        for i in range(self.length):
            energy *= self.base_efficiency * self.coherence_factor
            self.sites[i] = energy
        return energy


class PolaritonCondensate:
    """Models a quantum energy reservoir for efficient storage and release."""

    def __init__(self, capacity: float):
        self.capacity = capacity
        self.stored_energy = 0.0

    def absorb_energy(self, energy: float):
        """Absorbs energy into the condensate, factoring in quantum coherence preservation."""
        space = self.capacity - self.stored_energy
        absorbed = min(energy, space)
        self.stored_energy += absorbed
        return energy - absorbed  # Return overflow

    def release_energy(self, amount: float) -> float:
        """Releases stored energy dynamically based on system demands."""
        released = min(amount, self.stored_energy)
        self.stored_energy -= released
        return released


class QuantumBattery:
    """Quantum battery with adaptive charge-discharge cycles."""

    def __init__(self, max_energy=5.0, efficiency=0.99, adaptive=True):
        self.max_energy = max_energy
        self.energy = 0.0
        self.efficiency = efficiency
        self.adaptive = adaptive  # Enables self-regulation

    def charge(self, amount: float):
        """Charges the battery, factoring in efficiency losses."""
        available_space = self.max_energy - self.energy
        charged = min(amount, available_space)
        self.energy += charged * self.efficiency
        return charged

    def discharge(self, amount: float, priority_level=1):
        """Discharges energy based on system demand and priority levels."""
        if self.adaptive:
            factor = 1.0 if priority_level > 5 else 0.7
            amount *= factor  # Reduce requested amount based on priority

        discharged = min(amount, self.energy)
        self.energy -= discharged
        return discharged / factor  # Reverse adjustment to maintain expectation

    def auto_optimize(self):
        """Regulates energy use in real time, reducing waste."""
        if self.energy > self.max_energy * 0.9:
            logger.info("⚡ Excess energy detected: Redistributing...")
            self.energy *= 0.95  # Bleed off unnecessary energy to prevent dissipation


class NQPU:
    """Neural Quantum Processing Unit (NQPU) - Quantum Reinforcement Learning-Enhanced Processing."""

    def __init__(self, threshold=1.0, coherence_decay=0.95, base_learning_rate=0.02):
        self.threshold = threshold
        self.state = 0.0
        self.coherence_decay = coherence_decay
        self.learning_rate = base_learning_rate
        self.experience = {}  # Quantum memory for past activations
        self.coherence_memory = {}  # Track coherence states

    def process(self, input_energy: float, priority_level=1):
        """Processes energy adaptively, using QRL-based learning for optimal efficiency."""

        # Adjust threshold based on task priority
        adjusted_threshold = self.threshold * (1.0 - (0.05 * priority_level))  
        energy_surplus = input_energy - adjusted_threshold

        # Adaptive tunneling probability
        if energy_surplus >= 0:
            self.state = input_energy * self.coherence_decay
            self.learn(input_energy, success=True)
            return True
        else:
            tunneling_probability = self.get_adaptive_tunneling_probability(input_energy)
            if random.random() < tunneling_probability:
                self.state = input_energy * self.coherence_decay
                self.learn(input_energy, success=True)
                return True
            else:
                self.state = 0.0
                self.learn(input_energy, success=False)
                return False

    def learn(self, input_energy, success):
        """Quantum-inspired reinforcement learning algorithm."""

        # Initialize energy state memory if not present
        if input_energy not in self.experience:
            self.experience[input_energy] = 0.5  # Default 50% activation probability

        # Adjust learning rate dynamically based on past performance
        if success:
            reward = self.compute_reward(input_energy)
            self.experience[input_energy] += self.learning_rate * reward
        else:
            self.experience[input_energy] -= self.learning_rate

        # Keep probability within (0,1)
        self.experience[input_energy] = max(0.01, min(0.99, self.experience[input_energy]))

    def get_adaptive_tunneling_probability(self, input_energy):
        """Returns a dynamically adjusted tunneling probability based on past activations."""
        return self.experience.get(input_energy, 0.5)

    def compute_reward(self, input_energy):
        """Quantum-inspired reward function using a Boltzmann distribution for coherence tracking."""
        if input_energy not in self.coherence_memory:
            self.coherence_memory[input_energy] = 1.0  # Assume full coherence initially

        # Compute reward as function of coherence level
        coherence_factor = self.coherence_memory[input_energy]
        reward = math.exp(-1 / (coherence_factor + 1e-6))  # Prevent division by zero

        # Update coherence memory based on activation
        self.coherence_memory[input_energy] = max(0.1, min(1.0, coherence_factor * 0.99))  

        return reward


# ========================
# 🔷 MAIN QATP ENGINE CLASS
# ========================
class QATPEngine:
    """Quantum Alchemical Transfer Protocol Engine (QATP-X) - AI-Quantum Hybrid Processor."""

    def __init__(self):
        """Initialize QATP-X Engine with quantum modules."""
        self.chain = QuantumExcitonTransportChain(length=5, base_efficiency=0.95)
        self.condensate = PolaritonCondensate(capacity=10.0)
        self.battery = QuantumBattery(max_energy=5.0)
        self.nqpu = NQPU(threshold=1.0)

        logger.info("QATPEngine initialized (QATP-X version).")

    def run(self, input_data):
        """Execute computation using the QATP engine."""
        logger.info(f"Run invoked with input_data of type {type(input_data).__name__}.")
        return self.chain.transport_energy(input_data)


if __name__ == "__main__":
    engine = QATPEngine()
    print("QATP Engine Test Run:", engine.run(10.0))
