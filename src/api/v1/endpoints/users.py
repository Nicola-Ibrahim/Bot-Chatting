from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, Path, Query, responses

router = APIRouter(
    prefix="/v1/users",
    tags=["users"],
    responses={404: {"description": "Not found"}},
)


fake_users_db = {"1": {"name": "Nicola"}, "2": {"name": "Sal"}}


@router.get("/")
async def get_users() -> dict:
    return fake_users_db


@router.get("/{user_id}")
async def get_user(user_id: str):

    # Calling user service to return the user from the data base
    # user = user_service.retrieve_user_by_id(user_id=user_id)

    # Serialize the user obj and convert it to json-like structure, using schema

    # Return the json response

    if user_id not in fake_users_db:
        raise HTTPException(status_code=403, detail="User not found")

    return {"user_id": user_id, "name": fake_users_db.get(user_id)["name"]}


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
