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

def load_reference_params(filepath: str) -> pd.DataFrame:
    """Function for loading the reference dataframe and extracting the description.

    Args:
        filepath: location and filename of the reference dataframe.
    Returns:
        Array pd.DataFrame with statistical summary (output of describe())
    """
    ref_df = pd.read_csv(filepath)
    params = ref_df.describe()
    return params

def generate_normal_column(params: pd.DataFrame,
                           col_name: str,
                           size: int) -> np.ndarray:
    """Helper function for generating the parameters needed for the base signal
    function.

    Args:
        params: Array with al the parameters
        col_name: Header of the column
        size: Number of values to be created
    Returns:
        np.ndarray of generated values clipped between min and max
    """

    mean = params.at['mean', col_name]
    std = params.at['std', col_name]
    min_val = params.at['min', col_name]
    max_val = params.at['max', col_name]
    normal_column = np.clip(np.random.normal(mean, std, size), min_val, max_val)  # type: ignore
    return normal_column

def generate_outside_temp(timestamps: pd.DatetimeIndex) -> pd.Series:
    """Generate monthly average outside temperature for each timestamp.

    Based on KNMI long-term climate averages for the Netherlands.

    Args:
        timestamps: Sequence of datetime values defining the time axis.

    Returns:
        pd.Series of monthly average temperatures in degrees Celsius.
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
    outside_temp = pd.Series(timestamps.month).map(monthly_temp_nl)
    return outside_temp

def generate_base_signals(
        timestamps: pd.DatetimeIndex,
        outside_temp: pd.Series,
        catalyst_activity: np.ndarray,
        filepath: str) -> pd.DataFrame:
    """
    Generate all base process signals for the synthetic FCC dataset.

    Columns generated via normal distribution use statistical parameters
    derived from the reference dataset. Reactor_Temperature, Product_Yield,
    Conversion_Rate, and Air_Flow_Rate use custom logic due to process
    dependencies and seasonal effects.

    Args:
        timestamps: Sequence of datetime values defining the time axis.
        outside_temp: Monthly average outside temperature per timestamp
            in degrees Celsius (from generate_outside_temp()).
        catalyst_activity: Array of catalyst activity values per timestamp
            (from generate_catalyst_activity()).
        filepath: Path to the reference CSV dataset for parameter extraction.

    Returns:
        pd.DataFrame with one row per timestamp and one column per signal.
    """
    params = load_reference_params(filepath)
    exclude_cols = [
        'Outside_Temp',
        'Air_Flow_Rate',
        'Catalyst_Activity',
        'Reactor_Temperature',
        'Product_Yield',
        'Conversion_Rate',
        'Feed_Change_Event',
        'Catalyst_Replacement',
        'External_Disturbance_Type',
        ]
    df = {}

    for col in params.columns:
        if col not in exclude_cols:
            df[col] = generate_normal_column(params, col, len(timestamps))

    df = pd.DataFrame(df)

    reactor_temperature = np.clip(np.random.normal(loc=520,
                                                   scale=23,
                                                   size=len(timestamps)),
                                                   480, 560)
    gaussian_output = np.exp(-((reactor_temperature - 520) ** 2) / (2 * 13 **2))
    product_yield = 40 + (gaussian_output * 20)
    conversion_rate = 70 + (gaussian_output * 20)

    # Colder air is denser, requiring less volumetric flow to deliver
    # the same oxygen mass. Effect: ~6% variation over NL seasonal range.
    # Scale factor: 6% of mean flow / 16°C temp range = ~244 per degree C
    # NL annual mean temperature = 11°C (KNMI climate data)
    # Used as baseline: deviations above/below drive air flow adjustment
    temp_effect = (outside_temp - 11) * -244
    air_flow_rate = np.clip(np.random.normal(65258 + temp_effect,
                                             7481,
                                             len(timestamps)),
                                             50023, 79948)

    df['Outside_Temp'] = outside_temp
    df['Air_Flow_Rate'] = air_flow_rate
    df['Catalyst_Activity'] = catalyst_activity
    df['Reactor_Temperature'] = reactor_temperature
    df['Product_Yield'] = product_yield
    df['Conversion_Rate'] = conversion_rate
    return df

def generate_events(timestamps: pd.DatetimeIndex) -> pd.DataFrame:
    """
    Function for generating random events that influences the process conditions.

	Args:
		timestamps: sequence of datetime values defining the time axis of the dataset
		event_frequency: random generated event.
	Returns:
		DataFrame containing columns: Feed_Change_Event, Catalyst_Replacement, External_Disturbance_Type
    """
    df = pd.DataFrame()
    feed_change_event = np.random.choice([0, 1], size=len(timestamps), p=[0.905, 0.095])
    catalyst_replacement = np.random.choice([0, 1], size=len(timestamps), p=[0.957, 0.043])
    external_disturbance_type = np.random.choice(['AirFlowFluctuation',
                                                  'PowerDip',
                                                  'None'],
                                                  size=len(timestamps),
                                                  p=[0.0915, 0.0461, 0.8624])

    df['Feed_Change_Event'] = feed_change_event
    df['Catalyst_Replacement'] = catalyst_replacement
    df['External_Disturbance_Type'] = external_disturbance_type

    return df
# %%
