# Synthetic FCC Dataset Generator — Design Document

## 1. Output

A synthetic CSV dataset simulating one year of catalytic cracking (FCC) process data
at 5-minute intervals (~26,280 rows, 27 columns), based on the structure and ranges
of the reference Kaggle dataset.

## 2. Input

| Parameter | Description |
|---|---|
| `duration_days` | Number of days to generate (default: 365) |
| `event_frequency` | Frequency of Feed_Change and Disturbance events |
| `outside_temp` | External temperature data influencing process conditions |

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
- - Process conditions follow monthly average outside temperature (NL climate data)
- `External_Disturbance_Type` is `None` the majority of the time
- All values must stay within defined min/max ranges

## 4. Functions

```python
def generate_timestamps(duration_days: int) -> pd.DatetimeIndex:
    """
    Generates a sequence of timestamps at 5-minute intervals for a given number of days.

	Args:
		duration_days: days for determining count of timestamps. default = 365
	Returns:
		timestamps: type DateTime
    """
    pass


def generate_catalyst_activity(timestamps: pd.DatetimeIndex) -> np.ndarray:
    """
    Function that generates catalyst degradation. Catalyst degradation causes yield to decrease over time. Conversion to desired products declines, while undesired products increase.
	Activity declines to 70-76% after 24 hours, stabilizes with mean 72-73%. Replacement under 65%.


	Args:
		timestamps: sequence of datetime values defining the time axis of the dataset

	Returns:
		Catalyst_Activity in type float
    """
    pass


def generate_base_signals(
        timestamps: pd.DatetimeIndex,
        outside_temp,
        catalyst_activity: np.ndarray) -> pd.DataFrame:
    """
    Function for generating all base signals.

	Args:
		timestamps: sequence of datetime values defining the time axis of the dataset
		outside_temp: outside temperature influencing the 'Air_FLow_Rate', 'Regenerator_Temperature' and 'Energy_Consumption'
		catalyst_activity: state of catalyst that influences quality and output
	Returns:
		All base signals in type float
    """
    pass


def generate_events(timestamps: pd.DatetimeIndex, event_frequency: float) -> pd.DataFrame:
    """
    Function for generating random events that influences the process conditions.

	Args:
		timestamps: sequence of datetime values defining the time axis of the dataset
		event_frequency: random generated event.
	Returns:
		DataFrame containing columns: Feed_Change_Event, Catalyst_Replacement, External_Disturbance_Type
    """
    pass


def apply_correlations(df: pd.DataFrame) -> pd.DataFrame:
    """
    Function to apply Gaussian/bell curve to the yield and conversion rate.

	Args:
		df: DataFrame containing all process variables, including Reactor_Temperature as input for correlation calculations
	Returns:
		Yield and conversion rate in correlation with Reactor temperature.
    """
    pass
```
