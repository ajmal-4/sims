from typing import List
from pydantic import BaseModel, Field

client_id_desc = "Unique identifier for the client"
supplier_id_desc = "Unique identifier of the supplier"

class FetchClientRecentSales(BaseModel):
    client: str = Field(..., description=client_id_desc)
    limit: int = Field(..., description="limit of the recent sales data")

class FetchSupplierRecentSales(BaseModel):
    limit: int = Field(..., description="limit of the recent sales data")

class FetchClientStatus(BaseModel):
    client: str = Field(..., description=client_id_desc)

class RegularProduct(BaseModel):
    product_id: str = Field(..., description="Unique identifier of the product")
    quantity: int = Field(..., gt=0, description="Quantity of the product (must be > 0)")

class RegularProductsRequest(BaseModel):
    client_id: str = Field(..., description=client_id_desc)
    products: List[RegularProduct] = Field(..., description="List of products with IDs and quantities")

class FetchRegularProducts(BaseModel):
    client_id: str = Field(..., description=client_id_desc)

class AddPayment(BaseModel, extra="allow"):
    client_id: str = Field(..., description=client_id_desc)
    amount: int = Field(..., description="Payment amount by the client") 

class FetchPaymentHistory(BaseModel, extra="allow"):
    client: str = Field(..., description=client_id_desc)

class SupplyRegular(BaseModel, extra="allow"):
    client: str = Field(..., description=client_id_desc)

class FetchDailyClients(BaseModel, extra="allow"):
    date: str = Field(..., description="Chosen date of the supply")
    routes: list = Field(..., description="List of the route ids")

class SaveSales(BaseModel, extra="allow"):
    client: str = Field(..., description=client_id_desc)
    supplier: str = Field(..., description=supplier_id_desc)
    products: list = Field(..., description="List of products with IDs and quantities")
    total_amount: int = Field(..., description="Total amount of the products")
    date: str = Field(..., description="Date of the modification")

class UpdateSales(SaveSales, extra="allow"):
    sale_id: str = Field(..., description="Id of the sales data to be edited")

class AddDailyExpense(BaseModel, extra="allow"):
    date: str = Field(..., description="Chosen date of the supply")
    expense: dict = Field(..., description="List of expenses")

class GetDailyExpense(BaseModel, extra="allow"):
    date: str = Field(..., description="Chosen date of the supply")