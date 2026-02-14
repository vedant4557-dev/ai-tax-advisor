from pydantic import BaseModel, field_validator


class TaxRequest(BaseModel):
    gross_income: float
    tax_year: str
    deductions: float = 0.0

    @field_validator("gross_income")
    @classmethod
    def validate_income(cls, v):
        if v <= 0:
            raise ValueError("Gross income must be positive")
        return v

    @field_validator("tax_year")
    @classmethod
    def validate_year(cls, v):
        supported_years = ["2024-25", "2025-26"]
        if v not in supported_years:
            raise ValueError(f"Supported tax years: {supported_years}")
        return v

    @field_validator("deductions")
    @classmethod
    def validate_deductions(cls, v):
        if v < 0:
            raise ValueError("Deductions cannot be negative")
        return v

