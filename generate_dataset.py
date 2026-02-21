# %%
import pandas as pd
import numpy as np

def generate_timestamps(duration_days: int) -> pd.DatetimeIndex:
    """
    Generates a sequence of timestamps at 5-minute intervals for a given number of days.

	Args:
		duration_days: days for determining count of timestamps. default = 365
	Returns:
		timestamps: type DateTime
    """
    calc_periods = 12*24*duration_days
    timestamps = pd.date_range(start="2025-01-01", periods = calc_periods, freq="5min")
    return timestamps

def generate_catalyst_activity(timestamps: pd.DatetimeIndex) -> np.ndarray:
    """
    Function that generates catalyst degradation. Catalyst degradation causes yield to
    decrease over time. Conversion to desired products declines, while undesired
    products increase.
	Activity declines to 70-76% after 24 hours, stabilizes with mean 72-73%.
    Replacement under 65%.


	Args:
		timestamps: sequence of datetime values defining the time axis of the dataset

	Returns:
		Catalyst_Activity in type float
    """
    cycle_length = 30 * 24 * 12
    n_cycles = len(timestamps) // cycle_length # = 12
    remainder = len(timestamps) % cycle_length # remaining timestamp
    last_cycle_length = cycle_length + remainder
    activity_cycles = []

    for i in range(n_cycles):
        current_cycle_length = last_cycle_length if i == n_cycles - 1 else cycle_length
        # TODO: replace linspace with exponential decay for more realistic degradation
        cat_degradation_lin = np.linspace(100, 72, current_cycle_length)
        cat_degradation_noise = np.random.normal(loc=0, scale=2,
                                                    size=current_cycle_length)
        cat_degradation = cat_degradation_lin + cat_degradation_noise
        cat_degradation_clipped = np.clip(cat_degradation, 65, 100)
        activity_cycles.append(cat_degradation_clipped)

    catalyst_activity = np.concatenate(activity_cycles)
    return catalyst_activity


timestamps = generate_timestamps(365)
activity = generate_catalyst_activity(timestamps)

print(f"Length: {len(activity)}")
print(f"Min: {activity.min():.2f}")
print(f"Max: {activity.max():.2f}")
print(f"Mean: {activity.mean():.2f}")
