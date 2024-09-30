@router.get("/posts/{post_id}", response_model=PostResponse)
async def get_post_by_id(post: Mapping = Depends(valid_post_id)):
    return post
