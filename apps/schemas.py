from typing import List
from pydantic import BaseModel, Field

client_id_desc = "Unique identifier for the client"

class FetchClientRecentSales(BaseModel):
    client: str = Field(..., description=client_id_desc)
    limit: int = Field(..., description="limit of the recent sales data")

class FetchSupplierRecentSales(BaseModel):
    limit: int = Field(..., description="limit of the recent sales data")

class RegularProduct(BaseModel):
    product_id: str = Field(..., description="Unique identifier of the product")
    quantity: int = Field(..., gt=0, description="Quantity of the product (must be > 0)")

class RegularProductsRequest(BaseModel):
    client_id: str = Field(..., description=client_id_desc)
    products: List[RegularProduct] = Field(..., description="List of products with IDs and quantities")

class AddPayment(BaseModel, extra="allow"):
    client_id: str = Field(..., description=client_id_desc)
    amount: int = Field(..., description="Paymnet amount by the client") 

class FetchPaymentHistory(BaseModel, extra="allow"):
    client_id: str = Field(..., description=client_id_desc)