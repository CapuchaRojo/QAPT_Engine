import unittest
from qatp_engine import QATPEngine, QuantumExcitonTransportChain, PolaritonCondensate, QuantumBattery, NQPU

class TestQATPEngine(unittest.TestCase):

    def setUp(self):
        """Set up test environment before each test."""
        self.qatp = QATPEngine()  # Ensure we're using the correct class

    def transport_energy(self, input_energy):
        """Simulates energy transfer across the transport chain, factoring in coherence loss."""
        if isinstance(input_energy, list):  # Handle lists separately
            return [self.transport_energy(value) for value in input_energy]

        energy = float(input_energy)  # Ensure it's a number
        for i in range(self.length):
            energy *= self.base_efficiency * self.coherence_factor
            self.sites[i] = energy
        return energy

    def test_exciton_transport_chain(self):
        """Test if energy transport maintains efficiency."""
        chain = QuantumExcitonTransportChain(length=5, base_efficiency=0.95)
        input_energy = 10.0
        output_energy = chain.transport_energy(input_energy)

        # Corrected expected energy calculation with coherence factor
        expected_energy = input_energy * ((0.95 * 0.98) ** 5)

        self.assertAlmostEqual(output_energy, expected_energy, places=3)

    def test_polariton_condensate_storage(self):
        """Test energy storage and release in the condensate."""
        condensate = PolaritonCondensate(capacity=10.0)
        excess = condensate.absorb_energy(7.0)  # Store 7 units
        self.assertEqual(condensate.stored_energy, 7.0)
        self.assertEqual(excess, 0.0)  # No overflow

        excess = condensate.absorb_energy(5.0)  # Try to store more than capacity
        self.assertEqual(condensate.stored_energy, 10.0)  # Should be full
        self.assertEqual(excess, 2.0)  # 2 units should overflow

        released = condensate.release_energy(4.0)
        self.assertEqual(released, 4.0)
        self.assertEqual(condensate.stored_energy, 6.0)

    def test_quantum_battery_charging(self):
        """Test charging and discharging of quantum battery with adaptive priority scaling."""
        battery = QuantumBattery(max_energy=5.0, efficiency=0.99, adaptive=True)

        charged = battery.charge(3.0)
        expected_energy = 3.0 * battery.efficiency  # Account for efficiency loss
        self.assertAlmostEqual(battery.energy, expected_energy, places=3)

        # High-priority discharge (immediate full request)
        discharged = battery.discharge(2.0, priority_level=6)
        self.assertAlmostEqual(discharged, 2.0, places=3)

        # Low-priority discharge (adjusted request)
        expected_low_priority_request = 2.0 * 0.7  # The requested amount is scaled down
        expected_low_priority_actual = min(expected_low_priority_request, battery.energy)  # Can't discharge 	more than available
        expected_final_discharge = expected_low_priority_actual / 0.7  # Reverse adjust

        discharged = battery.discharge(2.0, priority_level=3)  # Low priority request
        self.assertAlmostEqual(discharged, expected_final_discharge, places=3)


    def discharge(self, amount: float, priority_level=1):
        """Discharges energy based on system demand and priority levels."""
        if self.adaptive:
            factor = 1.0 if priority_level > 5 else 0.7
            amount *= factor  # Reduce the requested amount based on priority

        discharged = min(amount, self.energy)
        self.energy -= discharged
        return discharged / factor  # Reverse adjustment to maintain expectation

    def test_auto_optimize(self):
        """Test automatic energy redistribution when battery reaches high capacity."""
        battery = QuantumBattery(max_energy=10.0, efficiency=1.0, adaptive=True)

        battery.charge(10.0)  # Fully charge the battery
        self.assertAlmostEqual(battery.energy, 10.0, places=3)

        battery.auto_optimize()  # Trigger optimization
        self.assertAlmostEqual(battery.energy, 9.5, places=3)  # Should reduce to 95% capacity


    def test_nqpu_activation(self):
        """Test if NQPU activates based on input energy."""
        nqpu = NQPU(threshold=1.0)
        
        # Full activation (input >= threshold)
        self.assertTrue(nqpu.process(1.2))

        # Below threshold but possible quantum tunneling
        tunneling_activations = sum(nqpu.process(0.5) for _ in range(100))
        self.assertGreater(tunneling_activations, 0)  # Should activate sometimes

        # Very low input should rarely activate
        low_energy_activations = sum(nqpu.process(0.1) for _ in range(100))
        self.assertLess(low_energy_activations, tunneling_activations)

    def test_qatp_energy_cycle(self):
        """Test a full energy cycle in QATP system."""
        result = self.qatp.run(3.0)  # Updated to match new method
        self.assertIsNotNone(result)  # Ensure it returns a value

    def test_hybrid_processing(self):
        """Test hybrid quantum-classical processing."""
        classical_input = [1, 2, 3, 4, 5]  # Example dataset
        output = self.qatp.run(classical_input)  # Updated method
        self.assertIsNotNone(output)  # Ensure we get a valid response

if __name__ == '__main__':
    unittest.main()
