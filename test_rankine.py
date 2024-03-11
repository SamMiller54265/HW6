from Rankine import rankine

def main() -> None:
    """
    A test program for Rankine power cycles.

    This program creates two Rankine cycle objects:
    - R1: Rankine cycle with turbine inlet of saturated vapor.
    - R2: Rankine cycle with turbine inlet of superheated vapor.

    It calculates the efficiency for both cycles and prints their summaries.
    """
    # Define a Rankine cycle with saturated steam at the inlet
    R1 = rankine(p_high=8000, p_low=8, name='Rankine cycle - saturated steam inlet')
    R1.calc_efficiency()

    # Calculate the temperature for superheating
    Tsat = R1.state1.T

    # Define a Rankine cycle with superheated steam at the inlet
    R2 = rankine(p_high=8000, p_low=8, t_high=1.7 * Tsat, name='Rankine cycle - superheated steam inlet')
    R2.calc_efficiency()

    # Print summaries for both cycles
    R1.print_summary()
    R2.print_summary()

if __name__ == "__main__":
    main()
