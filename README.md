# campus-energy-dashboard-Aarav

## Objective
This project builds an end-to-end pipeline to analyze and visualize electricity consumption across campus buildings. The goal is to provide the facilities team with actionable insights for energy-saving opportunities through data ingestion, aggregation, object-oriented modeling, visualization, and reporting.

## Dataset Source
Sample datasets are provided in the `/data/` folder. Each CSV file represents one building’s monthly usage data with columns:
- `timestamp` (date and time of reading)
- `kwh` (electricity consumed)

If building or month metadata is missing, it is inferred from the filename and timestamp.

## Methodology
The project is implemented in Python and divided into five tasks:

1. **Data Ingestion and Validation**  
   - Read multiple CSV files from `/data/`  
   - Merge into a single DataFrame  
   - Handle missing or corrupt files with exception handling  

2. **Core Aggregation Logic**  
   - Calculate daily and weekly totals using `resample()`  
   - Generate building-wise summary statistics (mean, min, max, total)  

3. **Object-Oriented Modeling**  
   - Define `Building`, `MeterReading`, and `BuildingManager` classes  
   - Add readings, calculate total consumption, and generate reports  

4. **Visualization**  
   - Create a dashboard with three charts using Matplotlib:  
     - Trend line of daily consumption  
     - Bar chart of average weekly usage per building  
     - Scatter plot of peak-hour consumption  
   - Save as `dashboard.png` in `/output/`  

5. **Persistence and Summary**  
   - Export cleaned dataset to `cleaned_energy_data.csv`  
   - Export building summary to `building_summary.csv`  
   - Generate `summary.txt` with:  
     - Total campus consumption  
     - Highest-consuming building  
     - Peak load time  
     - Sample weekly and daily trends  

## Insights
- The dashboard highlights daily and weekly consumption patterns across buildings.  
- Building-wise summaries identify the highest and lowest energy users.  
- Peak load times provide clues for targeted energy-saving measures.  
- The automated report consolidates findings for administrative decision-making.
