import numpy as np

def draw_demand(t, demand_type="sinusoidal", params=None):
    """
    Generates demand based on the specified type and parameters.

    Args:
        t (int): Current timestamp.
        demand_type (str): Type of demand pattern (e.g., "sinusoidal", "constant", "random").
        params (dict): Dictionary of parameters specific to the demand type.

    Returns:
        float: Generated demand.
    """
    if params is None:
        params = {}

    # Default parameter values
    mean = params.get("mean", 1000)
    amplitude = params.get("amplitude", 400)
    frequency = params.get("frequency", 1 / 48)
    noise_std = params.get("noise_std", 20)

    if demand_type == "sinusoidal":
        phase_shift = -0.9 * np.pi
        # Sinusoidal demand
        demand = mean + amplitude * np.sin(2 * np.pi * frequency * t + phase_shift)
        demand += np.random.normal(0, noise_std)
    elif demand_type == "constant":
        # Constant demand (mean value with optional noise)
        demand = mean
    elif demand_type == "random":
        # Random demand (normal distribution)
        demand = np.random.normal(mean, amplitude)
    else:
        raise ValueError(f"Unsupported demand_type: {demand_type}")


    # Ensure non-negative demand
    return max(demand, 0)
