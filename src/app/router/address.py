from typing import Union
from app.customer.schemas import CustomerResponse
from fastapi import FastAPI
from fastapi import APIRouter, HTTPException, Request, status
from app.deps import SessionDep

app = FastAPI()
router = APIRouter(prefix="/device")


@router.post(f"/user", response_model=CustomerResponse)
def create_customer(
    session: SessionDep

        
)
@router.get(f"/user/{id}", response_model=ListProductResponse)
def get_products(
    session: SessionDep,
    skip: int = 0,
    limit: int = 100
) -> Any:
    statement = select()
    count_statement = select(func.count()).select_from(Product)
    statement = statement.offset(skip).limit(limit)
    products = session.exec(statement).all()
    count = session.exec(count_statement).one()

    return ListProductResponse(data=devices, count=count)

@router.post('sales-products')
async def create_sales_products(
    session: SessionDep, 
    discount: DiscountCreate, 
    product_ids: List[int]
):

    new_discount = Discount.model_validate(productRequest)
    session.add(new_discount)
    session.refresh(new_discount)
    
    return new_discount
