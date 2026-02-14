from fastapi import FastAPI, HTTPException
from fastapi.responses import JSONResponse
from models.request import TaxRequest # type: ignore
from services.tax_service import TaxService

app = FastAPI(
    title="Indian Tax AI Engine",
    version="1.0.0",
    description="AI-powered Indian Income Tax Comparison Engine"
)


# ---------------------------------------
# Health Check
# ---------------------------------------
@app.get("/")
def health_check():
    return {
        "status": "success",
        "message": "Indian Tax AI Engine Running",
        "version": "1.0.0"
    }


# ---------------------------------------
# Compare Tax Regimes
# ---------------------------------------
@app.post("/compare-regimes")
def compare_tax(request: TaxRequest):
    try:
        result = TaxService.compare_regimes(
    basic_salary=request.basic_salary,
    hra_received=request.hra_received,
    special_allowance=request.special_allowance,
    other_income=request.other_income,
    annual_rent_paid=request.annual_rent_paid,
    metro_city=request.metro_city,
    section_80c=request.section_80c,
    section_80d=request.section_80d,
    home_loan_interest=request.home_loan_interest,
    nps_80ccd1b=request.nps_80ccd1b,
    tax_year=request.tax_year
)
        

        return JSONResponse(
            status_code=200,
            content={
                "status": "success",
                "data": result
            }
        )

    except ValueError as ve:
        raise HTTPException(
            status_code=400,
            detail=str(ve)
        )

    except Exception:
        raise HTTPException(
            status_code=500,
            detail="Internal Server Error"
        )
