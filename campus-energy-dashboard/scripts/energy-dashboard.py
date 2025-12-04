# Data Ingestion and Validation

import pandas as pd
import os
from pathlib import Path

def ingest_and_validate_data(data_dir="data"):
    all_files = Path(data_dir).glob("*.csv")
    df_list = []
    for file in all_files:
        try:
            df = pd.read_csv(file, on_bad_lines='skip')
            # Add metadata if missing
            if 'building' not in df.columns:
                df['building'] = file.stem
            if 'month' not in df.columns:
                df['month'] = pd.to_datetime(df['timestamp']).dt.month
            df_list.append(df)
        except FileNotFoundError:
            print(f"Missing file: {file}")
        except Exception as e:
            print(f"Error reading {file}: {e}")
    df_combined = pd.concat(df_list, ignore_index=True)
    return df_combined

df_combined = ingest_and_validate_data()
print(df_combined.head())



# Core Aggregation Logic

def calculate_daily_totals(df):
    df['timestamp'] = pd.to_datetime(df['timestamp'])
    daily = df.resample('D', on='timestamp')['kwh'].sum()
    return daily

def calculate_weekly_aggregates(df):
    df['timestamp'] = pd.to_datetime(df['timestamp'])
    weekly = df.resample('W', on='timestamp')['kwh'].sum()
    return weekly

def building_wise_summary(df):
    summary = df.groupby('building')['kwh'].agg(['mean','min','max','sum'])
    return summary

daily_totals = calculate_daily_totals(df_combined)
weekly_totals = calculate_weekly_aggregates(df_combined)
building_summary = building_wise_summary(df_combined)

print(building_summary)



# Object-Oriented Modeling

class MeterReading:
    def __init__(self, timestamp, kwh):
        self.timestamp = timestamp
        self.kwh = kwh

class Building:
    def __init__(self, name):
        self.name = name
        self.meter_readings = []

    def add_reading(self, reading):
        self.meter_readings.append(reading)

    def calculate_total_consumption(self):
        return sum(r.kwh for r in self.meter_readings)

    def generate_report(self):
        total = self.calculate_total_consumption()
        return f"Building {self.name} consumed {total} kWh in total."

class BuildingManager:
    def __init__(self):
        self.buildings = {}

    def add_building(self, building):
        self.buildings[building.name] = building

    def get_reports(self):
        return [b.generate_report() for b in self.buildings.values()]


# Example usage

manager = BuildingManager()
b1 = Building("Library")
b1.add_reading(MeterReading("2025-01-01", 120))
b1.add_reading(MeterReading("2025-01-02", 150))
manager.add_building(b1)

print(manager.get_reports())



# Visual Output with Matplotlib

import matplotlib.pyplot as plt

fig, axs = plt.subplots(3, 1, figsize=(10, 12))

# Trend Line – daily consumption

axs[0].plot(daily_totals.index, daily_totals.values, label="Daily Consumption")
axs[0].set_title("Daily Consumption Trend")
axs[0].set_xlabel("Date")
axs[0].set_ylabel("kWh")
axs[0].legend()

# Bar Chart – weekly usage across buildings

weekly_building = df_combined.groupby(['building']).resample('W', on='timestamp')['kwh'].mean().unstack()
weekly_building.mean(axis=1).plot(kind='bar', ax=axs[1])
axs[1].set_title("Average Weekly Usage per Building")
axs[1].set_ylabel("kWh")

# Scatter Plot – peak-hour consumption

df_combined['hour'] = pd.to_datetime(df_combined['timestamp']).dt.hour
axs[2].scatter(df_combined['hour'], df_combined['kwh'], c=df_combined['building'].astype('category').cat.codes)
axs[2].set_title("Peak-Hour Consumption")
axs[2].set_xlabel("Hour of Day")
axs[2].set_ylabel("kWh")

plt.tight_layout()
plt.savefig(r"C:\Users\aarav\Desktop\campus-energy-dashboard\output\dashboard.png")




# Persistence and Executive Summary


# Export cleaned dataset

df_combined.to_csv(r"C:\Users\aarav\Desktop\campus-energy-dashboard\output\cleaned_energy_data.csv", index=False)


# Export building summary

building_summary.to_csv(r"C:\Users\aarav\Desktop\campus-energy-dashboard\output\building_summary.csv")


# Generate summary report

total_consumption = df_combined['kwh'].sum()
highest_building = building_summary['sum'].idxmax()
peak_load_time = df_combined.loc[df_combined['kwh'].idxmax(), 'timestamp']

summary_text = f"""
Campus Energy Summary Report
----------------------------
Total Campus Consumption: {total_consumption} kWh
Highest Consuming Building: {highest_building}
Peak Load Time: {peak_load_time}
Weekly Trend (sample): {weekly_totals.head()}
Daily Trend (sample): {daily_totals.head()}
"""

with open(r"C:\Users\aarav\Desktop\campus-energy-dashboard\output\summary.txt", "w") as f:
    f.write(summary_text)

print(summary_text)