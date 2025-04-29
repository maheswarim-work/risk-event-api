from fastapi import FastAPI, HTTPException, Path
from typing import List
from pydantic import BaseModel, Field

app = FastAPI(
    title="Risk Event API",
    description="API for managing and analyzing risk events for actuarial purposes",
    version="1.0.0",
    docs_url="/api/docs",
    redoc_url="/api/redoc",
)

# Define the structure of a risk event
class RiskEvent(BaseModel):
    policy_id: str = Field(..., description="Unique identifier for the insurance policy", example="P12345")
    property_value: float = Field(..., description="Monetary value of the insured property", example=500000)
    insured_location: str = Field(..., description="Geographic location of the insured property", example="Florida")
    event_type: str = Field(..., description="Type of risk event", example="Hurricane")
    claim_history: List[str] = Field(default_factory=list, description="List of previous claims associated with the policy", example=["2021-HurricaneMinor", "2023-HurricaneMajor"])

    model_config = {
        "json_schema_extra": {
            "example": {
                "policy_id": "P12345",
                "property_value": 500000,
                "insured_location": "Florida",
                "event_type": "Hurricane",
                "claim_history": ["2021-HurricaneMinor", "2023-HurricaneMajor"]
            }
        }
    }

# Simulate a database (in-memory for demo purposes)
risk_events_db = [
    {
        "policy_id": "P12345",
        "property_value": 500000,
        "insured_location": "Florida",
        "event_type": "Hurricane",
        "claim_history": ["2021-HurricaneMinor", "2023-HurricaneMajor"]
    },
    {
        "policy_id": "P67890",
        "property_value": 250000,
        "insured_location": "California",
        "event_type": "Earthquake",
        "claim_history": []
    }
]

@app.get(
    "/risk-events",
    response_model=List[RiskEvent],
    tags=["Risk Events"],
    summary="Get all risk events",
    description="Retrieve a list of all risk events in the system",
    response_description="List of risk events with their details"
)
async def get_risk_events():
    """Return all risk events for actuarial analytics."""
    return risk_events_db

@app.get(
    "/risk-events/{policy_id}",
    response_model=RiskEvent,
    tags=["Risk Events"],
    summary="Get risk event by policy ID",
    description="Retrieve a specific risk event using its policy ID",
    response_description="Risk event details",
    responses={
        200: {
            "description": "Risk event found",
            "content": {
                "application/json": {
                    "example": {
                        "policy_id": "P12345",
                        "property_value": 500000,
                        "insured_location": "Florida",
                        "event_type": "Hurricane",
                        "claim_history": ["2021-HurricaneMinor", "2023-HurricaneMajor"]
                    }
                }
            }
        },
        404: {
            "description": "Policy not found",
            "content": {
                "application/json": {
                    "example": {"error": "Policy not found"}
                }
            }
        }
    }
)
async def get_risk_event(
    policy_id: str = Path(..., description="The policy ID to search for", example="P12345")
):
    """Return a single risk event based on policy ID."""
    event = next((item for item in risk_events_db if item["policy_id"] == policy_id), None)
    if event:
        return event
    else:
        raise HTTPException(status_code=404, detail="Policy not found")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)