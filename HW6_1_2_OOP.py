from HW6_1_OOP import ResistorNetwork, Resistor, VoltageSource, Loop
from scipy.optimize import fsolve


class ResistorNetwork2(ResistorNetwork):
    def AnalyzeCircuit(self):
        # Your new implementation for the second circuit analysis goes here.
        # This may involve defining a new initial guess and potentially new equations
        # if the topology of the circuit has changed.
        # For example, if there are more currents to solve for:
        i0 = [0.01, 0.01, 0.01, 0.01, 0.01]  # Example initial guess for 4 currents
        i = fsolve(self.GetKirchoffVals, i0)
        # print output to the screen
        print("I1 = {:0.1f} A".format(i[0]))
        print("I2 = {:0.1f} A".format(i[1]))
        print("I3 = {:0.1f} A".format(i[2]))
        print("I4 = {:0.1f} A".format(i[3]))
        print("I5 = {:0.1f} A".format(i[4]))
        return i

    def GetKirchoffVals(self, i):
        # Define currents through each resistor
        self.GetResistorByName('ad').Current = i[0]  # I1, through ad
        self.GetResistorByName('bc').Current = i[0]  # I1, through bc (same direction as I1)
        self.GetResistorByName('cd').Current = i[2] - i[0]  # I3 - I1, through cd
        self.GetResistorByName('ce').Current = -i[1]  # -I2, through ce (opposite direction to I2)
        self.GetResistorByName('de').Current = i[3]  # I4, through the new 5Ω resistor de

        # Apply KVL for the loops in the circuit, taking into account the voltage source directions
        Loop_L1_DeltaV = self.GetElementDeltaV('ab') - \
                         self.GetElementDeltaV('bc') - \
                         self.GetElementDeltaV('cd') - \
                         self.GetElementDeltaV('ad')  # Loop L1: abcd

        # Loop L2 needs to consider both the voltage source and the new resistor
        Loop_L2_DeltaV = -self.GetElementDeltaV('cd') + \
                         self.GetElementDeltaV('de') + \
                         self.GetElementDeltaV('ce')  # Loop L2: cde, traversal is c -> d -> e -> c

        # Apply KCL at the nodes, assuming I4 is the current through the new 5Ω resistor and I5 is the total current from e to d
        Node_c_Current = i[0] - (i[2] - i[0])  # Node c: I1 - (I3 - I1) = 0
        Node_d_Current = (i[2] - i[0]) - i[1] - i[3]  # Node d: (I3 - I1) - I2 - I4 = 0
        Node_e_Current = i[1] + i[3] - i[
            4]  # Node e: I2 + I4 - I5 = 0, assuming I5 is the current leaving node e to the voltage source

        # Return all the KVL and KCL equations
        return [Loop_L1_DeltaV, Loop_L2_DeltaV, Node_c_Current, Node_d_Current, Node_e_Current]

    def GetElementDeltaV(self, name):
        for r in self.Resistors:
            if name == r.Name:
                return -r.DeltaV()  # Assuming voltage drop
            elif name[::-1] == r.Name:  # Reverse name check, might not be needed based on your naming conventions
                return r.DeltaV()
        for v in self.VSources:
            if name == v.Name:
                return v.Voltage
            elif name[::-1] == v.Name:
                return -v.Voltage
        print(f"Warning: No component found with name {name}")
        return 0  # Return 0 instead of None to avoid TypeError


# Usage of ResistorNetwork2 to analyze the second circuit
if __name__ == "__main__":
    net2 = ResistorNetwork2()
    net2.BuildNetworkFromFile('ResistorNetwork2.txt')  # Use the new circuit's file
    net2.AnalyzeCircuit()
