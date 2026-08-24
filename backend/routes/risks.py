"""
routes/risks.py
---------------
Route: POST /risk-assessment
Returns a rule-based prototype risk assessment for a crop and farm conditions.
"""

from fastapi import APIRouter
from models.risk import RiskAssessmentInput, RiskAssessmentResponse
from services.risk_service import get_risk_assessment

router = APIRouter()


@router.post(
    "/risk-assessment",
    response_model=RiskAssessmentResponse,
    summary="Get Risk Assessment",
    description=(
        "Returns a prototype risk assessment for the specified crop and farm conditions. "
        "Evaluates water risk, soil suitability, pH suitability, seasonal suitability, "
        "and general pest/disease risk. "
        "This is a rule-based prototype — NOT real-time weather or satellite data."
    ),
)
def risk_assessment(data: RiskAssessmentInput) -> RiskAssessmentResponse:
    """Perform rule-based risk assessment and return results."""
    return get_risk_assessment(data)
