# Synthetic FCC Dataset Generator — Design Document

## 1. Output

A synthetic CSV dataset simulating one year of catalytic cracking (FCC) process data
at 5-minute intervals (~105,120 rows, 27 columns), based on the structure and ranges
of the reference Kaggle dataset.

## 2. Input

| Parameter | Description |
|---|---|
| `duration_days` | Number of days to generate (default: 365) |

## 3. Constraints

### Value Ranges (based on reference Kaggle dataset)

| Column | Min | Mean | Max | Unit |
|---|---|---|---|---|
| Reactor_Temperature | 480 | 520 | 560 | °C |
| Regenerator_Temperature | 650 | 700 | 750 | °C |
| Reactor_Pressure | 150 | 201 | 250 | kPa |
| Feed_Flow_Rate | 50 | 84 | 120 | t/h |
| Catalyst_Activity | 60 | 80 | 100 | % |
| Product_Yield | 40 | 50 | 60 | % |
| Conversion_Rate | 70 | 80 | 90 | % |

### Behavioral Constraints

- `Catalyst_Activity` must show realistic degradation drift over time (declining trend, reset on `Catalyst_Replacement`)
- `Product_Yield` and `Conversion_Rate` follow a bell curve optimum relative to `Reactor_Temperature`
- Process conditions follow monthly average outside temperature (NL KNMI climate data)
- `Air_Flow_Rate` is inversely correlated with outside temperature (~6% seasonal variation)
- `External_Disturbance_Type` is `'None'` the majority of the time (~86%)
- All values must stay within defined min/max ranges

## 4. Functions

```python
def generate_timestamps(duration_days: int) -> pd.DatetimeIndex:
    """
    Generates a sequence of timestamps at 5-minute intervals for a given number of days.

    Args:
        duration_days: days for determining count of timestamps. default = 365
    Returns:
        timestamps: type DatetimeIndex
    """
    pass


def generate_catalyst_activity(timestamps: pd.DatetimeIndex) -> np.ndarray:
    """
    Generates catalyst degradation over time. Activity declines linearly over 30-day cycles
    from 100% to ~72%, with a reset on Catalyst_Replacement events. Replacement triggered
    below 65%.

    Args:
        timestamps: sequence of datetime values defining the time axis of the dataset
    Returns:
        Catalyst_Activity as np.ndarray of float
    """
    pass


def generate_outside_temp(timestamps: pd.DatetimeIndex) -> pd.Series:
    """
    Generates monthly average outside temperature based on NL KNMI climate data.
    Used to drive seasonal variation in Air_Flow_Rate and related process conditions.

    Args:
        timestamps: sequence of datetime values defining the time axis of the dataset
    Returns:
        Outside temperature as pd.Series of float (°C)
    """
    pass


def load_reference_params(filepath: str) -> pd.DataFrame:
    """
    Loads reference dataset and returns descriptive statistics (mean, std, min, max)
    per column. Used to parameterize signal generation without hardcoded values.

    Args:
        filepath: path to reference CSV file
    Returns:
        pd.DataFrame with describe() output (mean, std, min, max per column)
    """
    pass


def generate_normal_column(params: pd.DataFrame, col_name: str, size: int) -> np.ndarray:
    """
    Generates a normally distributed column clipped to min/max based on reference params.

    Args:
        params: DataFrame from load_reference_params()
        col_name: column name to extract mean/std/min/max for
        size: number of values to generate
    Returns:
        np.ndarray of float, clipped to [min, max]
    """
    pass


def generate_base_signals(
        timestamps: pd.DatetimeIndex,
        outside_temp: pd.Series,
        catalyst_activity: np.ndarray,
        filepath: str) -> pd.DataFrame:
    """
    Generates all base process signals. Most columns are generated via generate_normal_column().
    Special logic applied to:
    - Air_Flow_Rate: inversely correlated with outside temperature
    - Reactor_Temperature: Gaussian bell curve optimum for Product_Yield and Conversion_Rate

    Args:
        timestamps: sequence of datetime values defining the time axis of the dataset
        outside_temp: outside temperature as pd.Series (from generate_outside_temp)
        catalyst_activity: catalyst activity as np.ndarray (from generate_catalyst_activity)
        filepath: path to reference CSV file
    Returns:
        DataFrame with 24 base signal columns
    """
    pass


def generate_events(timestamps: pd.DatetimeIndex) -> pd.DataFrame:
    """
    Generates random process events based on occurrence rates derived from reference dataset.

    Probabilities:
    - Feed_Change_Event: 9.5% (bool)
    - Catalyst_Replacement: 4.3% (bool)
    - External_Disturbance_Type: AirFlowFluctuation 9.15%, PowerDip 4.61%, None 86.24% (str)

    Args:
        timestamps: sequence of datetime values defining the time axis of the dataset
    Returns:
        DataFrame containing columns: Feed_Change_Event, Catalyst_Replacement, External_Disturbance_Type
    """
    pass


def apply_correlations(df: pd.DataFrame) -> pd.DataFrame:
    """
    Applies Gaussian bell curve to Product_Yield and Conversion_Rate
    relative to Reactor_Temperature optimum.

    Args:
        df: DataFrame containing all process variables, including Reactor_Temperature
    Returns:
        DataFrame with updated Product_Yield and Conversion_Rate columns
    """
    pass
```