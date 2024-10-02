from typing import Annotated

from fastapi import APIRouter, Path, Query

router = APIRouter()


@router.get("/")
def hello():
    return "hii"


@router.get("/dd")
def hello():
    return "hii"


# @router.get("/posts/{post_id}", response_model=PostResponse)
# async def get_post_by_id(post: Mapping = Depends(valid_post_id)):
#     return post


# @router.post("/items/")
# async def create_item(item: Item):
#     item_as_dict = dict(item)
#     print(item.price)
#     if item.price:
#         item_as_dict.update({"price_w_tax": item.price + item.tax})

#     return item_as_dict


# @router.get("/items/{item_id}")
# async def read_items(
#     item_id: Annotated[int, Path(title="The ID of the item to get")],
#     q: Annotated[str | None, Query(alias="item-query")] = None,
# ):
#     results = {"item_id": item_id}
#     if q:
#         results.update({"q": q})
#     return results
