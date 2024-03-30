from fastapi import APIRouter, HTTPException, Query
from .models import Product
from .db_config import get_product_collection
from typing import List, Optional, Any, Dict

product_router = APIRouter()

@product_router.get("/product/{id}", response_model=Product)
async def get_product(id:str) -> Any:
    try:
        if id is not None:
            # Assuming get_product_collection() returns a list of Product objects
            data = await get_product_collection().find_one({"id": int(id)})
            if data:
                return data  # Return single Product object
            else:
                raise HTTPException(status_code=404, detail="Product not found")
        else:
            raise HTTPException(status_code=404, detail="Product Id not given")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@product_router.get("/products/bulk",response_model=List[Product])
async def getBulkProducts(ids: str = Query(...)):
    try:
        ids_list = ids.split(',')
        products = []
        for id in ids_list:
            product = await get_product_collection().find_one({"id": int(id)})
            if product:
                products.append(product)
        return products;
    except:
        print('An exception occurred')


@product_router.get("/products", response_model=Dict[str, Any])
async def get_products(
    sortBy: Optional[str] = Query(None, description="Sort field (e.g., 'title', 'price')"),
    sortType: Optional[str] = Query(None, description="Sort type ('asc' for ascending, 'desc' for descending)"),
    page: Optional[int] = Query(1, description="Page number (default: 1)"),
    limit: Optional[int] = Query(20, description="Number of products per page (default: 20, max: 100)"),
    search: Optional[str] = Query(None, description="Search products by title")
) -> Any:
    collection = get_product_collection()
    try:
        # Default filters
        filters = {}
        if search:
            filters["title"] = {"$regex": f".*{search}.*", "$options": "i"}

        # Sorting
        sort_criteria = []
        if sortBy:
            sort_criteria.append((sortBy, 1 if sortType != 'desc' else -1))  # 1 for ascending, -1 for descending
        else:
            sort_criteria.append(("id", 1))  # Default sorting by ID ascending

        # Count total matching documents
        total_products = await collection.count_documents(filters)

        # Calculate start and end index for pagination
        start_index = (page - 1) * limit
        end_index = start_index + limit

        # Retrieve products based on filters, sorting, and pagination
        products_cursor = collection.find(filters).sort(sort_criteria).skip(start_index).limit(limit)
        products_data = await products_cursor.to_list(None)

        # Convert MongoDB documents to Product instances
        products = [Product(**product_data) for product_data in products_data]
        meta = {
            "total": total_products,
            "per_page": limit,
            "current_page": page,
            "last_page": (total_products + limit - 1) // limit,
            "first_page": 1,
            "first_page_url": f"/products?page=1",
            "last_page_url": f"/products?page={(total_products + limit - 1) // limit}",
            "next_page_url": f"/products?page={page + 1}" if page < (total_products + limit - 1) // limit else None,
            "previous_page_url": f"/products?page={page - 1}" if page > 1 else None
        }

        return {"meta": meta, "data": products}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


