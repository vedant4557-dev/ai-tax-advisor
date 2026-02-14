# api/routes.py

from fastapi import APIRouter, HTTPException
from models.request import TaxRequest
from services.tax_service import TaxService

router = APIRouter()


@router.post("/compare-regimes")
def compare_regimes(request: TaxRequest):
    try:
        result = TaxService.compare_regimes(
            gross_income=request.gross_income,
            tax_year=request.tax_year,
            deductions=request.deductions,
        )

        return {
            "status": "success",
            "data": result
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
