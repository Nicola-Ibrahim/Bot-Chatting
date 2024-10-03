from typing import Annotated

from fastapi import APIRouter, FastAPI, Path, Query, WebSocket
from fastapi.responses import FileResponse

router = APIRouter(prefix="/v1")


@router.get("/")
async def get():
    return FileResponse("src/templates/index.html")


@router.get("/f")
async def getf():
    return FileResponse("src/templates/index.html")


@router.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    print(websocket)
    await websocket.accept()
    while True:
        data = await websocket.receive_text()
        await websocket.send_text(f"Message text was: {data}")


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
