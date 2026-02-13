from pydantic import BaseModel
from typing import Optional


class TaxRequest(BaseModel):
    gross_income: float
    tax_year: str
    deductions: Optional[float] = 0.0
