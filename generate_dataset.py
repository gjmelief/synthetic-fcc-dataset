import pandas as pd

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