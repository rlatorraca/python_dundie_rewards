import httpx
from decimal import Decimal
from typing import List, Dict
from dundie.settings import API_BASE_URL
from pydantic import BaseModel, Field


class UsdRate(BaseModel):
    code: str = Field(default="USD")
    codein: str = Field(default="USD")
    name: str = Field(default="Dolar/Dolar")
    value: Decimal = Field(alias="high")


def get_rates(currencies: List[str]) -> Dict[str, UsdRate]:
    """Get the current rates of dolar in each currency"""
    return_data = {}
    for currency in currencies:
        if currency == "USD":
            return_data[currency] = UsdRate(high=Decimal('1.0'))
        else:
            response = httpx.get(API_BASE_URL.format(currency=currency))
            if response.status_code == 200:
                data = response.json()["USD" + currency]
                data["high"] = Decimal(data["high"])
                return_data[currency] = UsdRate(**data)
            else:
                return_data[currency] = UsdRate(name="API/ERROR", high=Decimal('0.0'))
    return return_data
