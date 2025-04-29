# Risk Event API Databricks POC

This Proof of Concept demonstrates how to use Databricks to analyze risk event data from our FastAPI service.

## Setup

1. Install the required dependencies in your Databricks environment:
```python
%pip install -r requirements.txt
```

2. Make sure the Risk Event API is running and accessible from your Databricks environment.

## Usage

1. Import and initialize the RiskEventAnalyzer:
```python
from risk_event_analysis import RiskEventAnalyzer

# Initialize with your API URL if different from default
analyzer = RiskEventAnalyzer(base_url="http://your-api-url:8000")
```

2. Fetch and analyze risk events:
```python
# Fetch all risk events
risk_events = analyzer.fetch_risk_events()

# Convert to DataFrame
df = analyzer.to_dataframe()

# Generate location-based analysis
location_analysis = analyzer.analyze_risk_by_location()

# Create visualizations
fig = analyzer.plot_risk_distribution()

# Generate comprehensive risk report
risk_report = analyzer.generate_risk_report()
```

## Features

The POC includes the following analysis capabilities:

1. **Data Collection**
   - Fetch all risk events
   - Get specific risk events by policy ID
   - Convert data to pandas DataFrame

2. **Location Analysis**
   - Count of policies by location
   - Total property value by location
   - Average property value by location
   - Event type distribution by location

3. **Visualizations**
   - Property value distribution
   - Event types by location
   - Average property value by location
   - Claim history analysis

4. **Risk Reporting**
   - Total policies and property value
   - Location-specific metrics
   - Risk metrics (highest value location, most common events, etc.)

## Example Notebook

The `risk_event_analysis.py` file includes example usage that can be run directly in a Databricks notebook. The example demonstrates:
- Data fetching
- DataFrame conversion
- Location analysis
- Visualization generation
- Risk report generation

## Notes

- Make sure your Databricks cluster has access to the Risk Event API
- Adjust the `base_url` parameter if your API is hosted at a different location
- The visualizations are optimized for Databricks notebook display
- The analysis can be extended by adding new methods to the `RiskEventAnalyzer` class 