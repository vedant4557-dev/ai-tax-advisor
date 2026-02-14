from pydantic import BaseModel


class TaxRequest(BaseModel):
    tax_year: str

    # Salary components
    basic_salary: float
    hra_received: float
    special_allowance: float
    other_income: float
    annual_rent_paid: float
    metro_city: bool

    # Deductions (Old regime)
    sec_80c: float
    sec_80d: float
    home_loan_interest: float
    nps_extra: float
