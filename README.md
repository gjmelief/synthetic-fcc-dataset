# Synthetic FCC Dataset Generator

Synthetic dataset generator for catalytic cracking (FCC) process data — 105,120 rows, 1 year, 5-minute intervals. Built as part of a data analyst portfolio.

## Reference Dataset
This generator is based on the [Catalytic Cracking Process Control Dataset](https://www.kaggle.com/datasets/programmer3/catalytic-cracking-process-control-dataset) by programmer3, licensed under [CC0 1.0 Public Domain](https://creativecommons.org/publicdomain/zero/1.0/).

## About

This project generates a realistic synthetic dataset simulating one year of Fluid Catalytic Cracking (FCC) process operations. The generated dataset is based on real-world value ranges and behavioral patterns derived from a reference Kaggle dataset, including catalyst activity degradation, seasonal temperature variation, and process disturbances.

The dataset is used as the foundation for a Manufacturing Quality Analysis project.

## Features

- 105,120 rows of process data at 5-minute intervals
- Realistic catalyst activity degradation curve with periodic replacement events
- Seasonal variation in Air_Flow_Rate driven by NL KNMI monthly climate data
- Random process disturbances (air flow fluctuations, power dips)
- Physically realistic correlations between reactor temperature, yield and conversion rate
- Event probabilities derived from reference dataset using `value_counts()`

## Dataset Columns

| Column | Description | Unit |
|---|---|---|
| Timestamp | Date and time of measurement | YYYY-MM-DD HH:MM:SS |
| Reactor_Temperature | Reactor operating temperature | °C |
| Regenerator_Temperature | Regenerator operating temperature | °C |
| Reactor_Pressure | Reactor operating pressure | kPa |
| Feed_Flow_Rate | Feedstock flow rate | t/h |
| Catalyst_to_Oil_Ratio | Ratio of catalyst to feedstock | - |
| Catalyst_Activity | Current catalyst activity level | % |
| Air_Flow_Rate | Air supply to regenerator | m³/h |
| Fractionator_Top_Temp | Fractionator top temperature | °C |
| Fractionator_Bottom_Temp | Fractionator bottom temperature | °C |
| Feedstock_Quality_Index | Quality index of feedstock | - |
| Setpoint_Reactor_Temp | Reactor temperature setpoint | °C |
| Setpoint_Regenerator_Temp | Regenerator temperature setpoint | °C |
| PID_Kp | PID proportional gain | - |
| PID_Ki | PID integral gain | - |
| PID_Kd | PID derivative gain | - |
| Fuzzy_Adjustment_Factor | Fuzzy logic control adjustment | - |
| Product_Yield | Yield of desired products | % |
| Conversion_Rate | Overall feedstock conversion rate | % |
| Energy_Consumption | Total energy consumption | MWh |
| Emissions_NOx | NOx emissions | mg/Nm³ |
| Emissions_SOx | SOx emissions | mg/Nm³ |
| Control_Stability_Index | Process control stability metric | - |
| Reward_Score | Optimization reward score | - |
| Feed_Change_Event | Feed composition change event | bool |
| Catalyst_Replacement | Catalyst replacement event | bool |
| External_Disturbance_Type | Type of external disturbance | str |

## Project Structure

```
synthetic-fcc-dataset/
├── DESIGN.md                       # Technical design document
├── generate_dataset.py             # Main dataset generator script
├── catalytic_cracking_dataset.csv  # Reference dataset (CC0 license)
├── README.md
├── .gitignore
└── LICENSE
```

## Usage

```bash
python generate_dataset.py
```

## Requirements

- Python 3.x
- pandas
- numpy

## Background

Built by a process operator transitioning to data analyst. Domain knowledge of FCC operations is used to ensure realistic process behavior in the synthetic data.

## License

MIT