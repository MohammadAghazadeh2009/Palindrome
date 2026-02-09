from fastapi import FastAPI, status, Form, Body, Path
from fastapi.responses import JSONResponse
from fastapi.exceptions import HTTPException
import uuid
from pydantic import BaseModel

app = FastAPI()

product_list = [
    {
        "id":"f217cfe5-98e5-4164-afe6-80d9c54bab11",
        "name":"apple",
        "price":200
    }
]

class ProductModel(BaseModel):
    name:str
    price:int

@app.get("/products")
async def products_list():
    return product_list

@app.post("/products")
async def product_create(request : ProductModel):
    product_list.append(
        {
            "id":uuid.uuid4(),
            "name":request.name,
            "price":request.price
        }
    )
    return JSONResponse({"detail":"product added successfully"},status_code=status.HTTP_201_CREATED)
 
@app.delete("/products/{product_id}")
async def product_delete(product_id:str=Path()):
    global product_list

    product_list = [product for product in product_list if product["id"] != product_id]

    return JSONResponse({"detail":"product deleted successfully"})

@app.get("/products/{product_id}")
async def product_detail(product_id:str=Path()):
    for product in product_list:
        if product_id == product["id"]:
            return product
        
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="No such a product")

@app.put("/products/{product_id}")
async def product_detail(request : ProductModel, product_id:str=Path()):
    for product in product_list:
        if product_id == product["id"]:
            product["name"] = request.name
            product["price"] = request.price
            return product
        
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="No such a product")