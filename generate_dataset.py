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

def generate_base_signals(
        timestamps: pd.DatetimeIndex,
        outside_temp,
        catalyst_activity: np.ndarray) -> pd.DataFrame:
    """
    Function for generating all base signals.

	Args:
		timestamps: sequence of datetime values defining the time axis of the dataset
		outside_temp: outside temperature influencing the 'Air_FLow_Rate', 'Regenerator_Temperature' and 'Energy_Consumption'
	Returns:
		All base signals in type float
    """

    monthly_temp_nl = {
    1: 3.5,   # January
    2: 4.0,   # February
    3: 7.0,   # March
    4: 10.5,  # April
    5: 14.0,  # May
    6: 17.0,  # June
    7: 19.5,  # July
    8: 19.5,  # August
    9: 16.0,  # September
    10: 12.0, # October
    11: 7.5,  # November
    12: 4.5   # December
    }
    # %%
    avg_temp_month = pd.Series(timestamps.month).map(monthly_temp_nl)
    reactor_temperature = np.clip(np.random.normal(loc=520,
                                                   scale=23,
                                                   size=len(timestamps)),
                                                   480, 560)
    gaussian_output = np.exp(-((reactor_temperature - 520) ** 2) / (2 * 13 **2))
    product_yield = 40 + (gaussian_output * 20)
    conversion_rate = 70 + (gaussian_output * 20)
    regenerator_temperature = np.clip(np.random.normal(700, 25, len(timestamps)), 650, 750)
    fractionator_top_temp = np.clip(np.random.normal(176, 12, len(timestamps)), 150, 200)
    fractionator_bottom_temp = np.clip(np.random.normal(330, 15, len(timestamps)), 300, 360)
    setpoint_reactor_temp = np.clip(np.random.normal(520, 10, len(timestamps)), 500, 540)
    setpoint_regenerator_temp = np.clip(np.random.normal(700, 10, len(timestamps)), 680, 720)
    df = pd.DataFrame({
        'Reactor_Temperature': reactor_temperature,
        'Product_Yield': product_yield,
        'Conversion_Rate': conversion_rate,
        'Outside_Temp': avg_temp_month,
        'Regenerator_Temperature': regenerator_temperature,
        'Fractionator_Top_Temp': fractionator_top_temp,
        'Fractionator_Bottom_Temp': fractionator_bottom_temp,
        'Setpoint_Reactor_Temp': setpoint_reactor_temp,
        'Setpoint_Regenerator_Temp': setpoint_regenerator_temp
        })


# %%
