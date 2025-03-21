from qatp_engine import QATPEngine, QuantumExcitonTransportChain, PolaritonCondensate, QuantumBattery, NQPU

class TestQATPSystem(unittest.TestCase):
    
    def setUp(self):
        """Set up test environment before each test."""
        self.qatp = QATPSystem()

    def test_exciton_transport_chain(self):
        """Test if energy transport maintains efficiency."""
        chain = QuantumExcitonTransportChain(length=5, base_efficiency=0.95)
        input_energy = 10.0
        output_energy = chain.transport_energy(input_energy)
        expected_energy = input_energy * (0.95 ** 5)  # 5 steps of 95% efficiency
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
        """Test charging and discharging of quantum battery."""
        battery = QuantumBattery(max_energy=5.0)
        charged = battery.charge(3.0)
        self.assertEqual(charged, 3.0)
        self.assertEqual(battery.energy, 3.0)

        discharged = battery.discharge(2.0)
        self.assertEqual(discharged, 2.0)
        self.assertEqual(battery.energy, 1.0)

        # Trying to discharge more than available
        discharged = battery.discharge(2.0)
        self.assertEqual(discharged, 1.0)  # Only 1 left to discharge
        self.assertEqual(battery.energy, 0.0)

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
        result = self.qatp.energy_cycle(3.0)
        self.assertIsInstance(result, bool)  # Should return True or False

    def test_hybrid_processing(self):
        """Test hybrid quantum-classical processing."""
        classical_input = 2.5
        output = self.qatp.hybrid_process(classical_input)
        self.assertGreater(output, classical_input)  # Should be at least 2.5 + (1 or 0)

if __name__ == '__main__':
    unittest.main()
