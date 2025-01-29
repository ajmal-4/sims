from typing import List
from pydantic import BaseModel, Field

class RegularProduct(BaseModel):
    product_id: str = Field(..., description="Unique identifier of the product")
    quantity: int = Field(..., gt=0, description="Quantity of the product (must be > 0)")

class RegularProductsRequest(BaseModel):
    client_id: str = Field(..., description="Unique identifier for the client")
    products: List[RegularProduct] = Field(..., description="List of products with IDs and quantities")