import requests
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from typing import List, Dict
import json

class RiskEventAnalyzer:
    def __init__(self, base_url: str = "http://localhost:8000"):
        self.base_url = base_url
        self.risk_events = None

    def fetch_risk_events(self) -> List[Dict]:
        """Fetch all risk events from the API"""
        response = requests.get(f"{self.base_url}/risk-events")
        response.raise_for_status()
        self.risk_events = response.json()
        return self.risk_events

    def get_risk_event(self, policy_id: str) -> Dict:
        """Fetch a specific risk event by policy ID"""
        response = requests.get(f"{self.base_url}/risk-events/{policy_id}")
        response.raise_for_status()
        return response.json()

    def to_dataframe(self) -> pd.DataFrame:
        """Convert risk events to a pandas DataFrame"""
        if not self.risk_events:
            self.fetch_risk_events()
        return pd.DataFrame(self.risk_events)

    def analyze_risk_by_location(self) -> pd.DataFrame:
        """Analyze risk events by location"""
        df = self.to_dataframe()
        return df.groupby('insured_location').agg({
            'property_value': ['count', 'sum', 'mean'],
            'event_type': 'count'
        }).reset_index()

    def plot_risk_distribution(self):
        """Create visualizations for risk event distribution"""
        df = self.to_dataframe()
        
        # Set up the figure and axes
        fig, axes = plt.subplots(2, 2, figsize=(15, 10))
        
        # Plot 1: Property Value Distribution
        sns.histplot(data=df, x='property_value', ax=axes[0, 0])
        axes[0, 0].set_title('Property Value Distribution')
        
        # Plot 2: Event Types by Location
        event_counts = df.groupby(['insured_location', 'event_type']).size().unstack()
        event_counts.plot(kind='bar', stacked=True, ax=axes[0, 1])
        axes[0, 1].set_title('Event Types by Location')
        axes[0, 1].tick_params(axis='x', rotation=45)
        
        # Plot 3: Average Property Value by Location
        location_avg = df.groupby('insured_location')['property_value'].mean()
        location_avg.plot(kind='bar', ax=axes[1, 0])
        axes[1, 0].set_title('Average Property Value by Location')
        axes[1, 0].tick_params(axis='x', rotation=45)
        
        # Plot 4: Claim History Analysis
        claim_counts = df['claim_history'].apply(len)
        sns.histplot(data=claim_counts, ax=axes[1, 1])
        axes[1, 1].set_title('Number of Claims per Policy')
        
        plt.tight_layout()
        return fig

    def generate_risk_report(self) -> Dict:
        """Generate a comprehensive risk report"""
        df = self.to_dataframe()
        
        report = {
            "total_policies": len(df),
            "total_property_value": df['property_value'].sum(),
            "average_property_value": df['property_value'].mean(),
            "locations": {
                loc: {
                    "count": len(group),
                    "total_value": group['property_value'].sum(),
                    "event_types": group['event_type'].value_counts().to_dict()
                }
                for loc, group in df.groupby('insured_location')
            },
            "risk_metrics": {
                "highest_value_location": df.groupby('insured_location')['property_value'].sum().idxmax(),
                "most_common_event": df['event_type'].mode()[0],
                "average_claims_per_policy": df['claim_history'].apply(len).mean()
            }
        }
        
        return report

# Example usage in Databricks:
if __name__ == "__main__":
    # Initialize the analyzer
    analyzer = RiskEventAnalyzer()
    
    # Fetch and display risk events
    risk_events = analyzer.fetch_risk_events()
    print("Fetched Risk Events:")
    print(json.dumps(risk_events, indent=2))
    
    # Convert to DataFrame and display
    df = analyzer.to_dataframe()
    display(df)
    
    # Generate and display analysis
    location_analysis = analyzer.analyze_risk_by_location()
    display(location_analysis)
    
    # Generate and display visualizations
    fig = analyzer.plot_risk_distribution()
    plt.show()
    
    # Generate and display risk report
    risk_report = analyzer.generate_risk_report()
    print("\nRisk Report:")
    print(json.dumps(risk_report, indent=2)) 