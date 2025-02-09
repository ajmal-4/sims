from enum import Enum

class HTMLPAGES:
    LOGIN_PAGE = 'login.html'
    ERROR_PAGE = 'error.html'
    SUPPLIER_HOME_PAGE = 'supplier_home.html' 
    SALES_PAGE = 'sales.html'

class SuccessMessages:
    DELETE_CLIENT = 'Client deleted successfully'
    EDIT_CLIENT = 'Client updated successfully'
    ADD_INVOICE = 'Invoice saved successfully!'
    UPDATE_REGULAR_PRODUCTS = "Client regular product details updated successfully"
    ADD_SALES_PAYMENT = "Updated payment information"


class ErrorMessages:
    ADD_CLIENT = 'Could not add the client at the moment'
    EDIT_CLIENT = 'Could not update the client at the moment'
    DELETE_CLIENT = 'Could not delete the client at the moment'
    ADD_INVOICE = 'Could not save the invoice at the moment'
    FETCH_LAST_SALES_DATA = 'Invoice does not found for the client'
    FETCH_RECENT_SALES_DATA = 'Recent Invoices does not found for the client'
    FETCH_CLIENTS = "Failed to fetch clients"
    UPDATE_REGULAR_PRODUCTS = "Error updating client regular products"
    FETCH_REGULAR_PRODUCTS = "Could not fetch the regular products"
    ADD_SALES_PAYMENT = "Failed to update sales payment"
    FETCH_RECENT_MONEY_TRANSACTIONS = "Failed to fetch recent money transactions"

class Limits:
    LAST_SALE_DATA_LIMIT = 1
    RECENT_SALE_DATA_LIMIT = 10
    RECENT_PAYMENT_HISTORY = 10

class Projections:
    EXCLUDE_ID = {"_id": 0}

class PaymentStatus(Enum):
    CREDITED = "credited"
    SETTLED = "settled"
    PENDING = "pending"

class TransactionType(Enum):
    SALE = "sale"
    CREDIT = "credit"


