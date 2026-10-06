from contextlib import asynccontextmanager

from fastapi import FastAPI, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from Code.db import Post, create_db_tables, get_async_session
from Code.schemas import PostCreate, UpPut


@asynccontextmanager
async def lifespan(app: FastAPI):
    await create_db_tables()
    yield

app = FastAPI(lifespan=lifespan)

text_posts = {
    1: {
        "title": "Cats",
        "content": "Cats are the cutest and the best creatures to have as pets",
    },
    2: {
        "title": "Glazing Whiskers",
        "content": "A cat's whiskers shine like tiny antennas picking up cosmic signals of cuteness",
    },
    3: {
        "title": "Moonlit Cat",
        "content": "Under the moonlight, a cat's fur glows like polished silver",
    },
    4: {
        "title": "Golden Paws",
        "content": "Every step a cat takes looks like it's leaving behind trails of golden sparkles",
    },
    5: {
        "title": "Shiny Sleepyhead",
        "content": "A sleeping cat looks like a glossy loaf of pure peace",
    },
    6: {
        "title": "Glare of Royalty",
        "content": "Cats don't just look at you — they glare with the shine of ancient kings",
    },
    7: {
        "title": "Sparkle Sprint",
        "content": "When a cat runs, it's like a streak of shimmering lightning",
    },
    8: {
        "title": "Glossy Grooming",
        "content": "Cats groom themselves until their fur looks smoother than glass",
    },
    9: {
        "title": "Sunbeam Cat",
        "content": "A cat sitting in sunlight becomes a glowing masterpiece",
    },
    10: {
        "title": "The Glazing Majesty",
        "content": "Cats aren't just pets — they are glossy, glowing rulers of every home they enter",
    },
}


@app.get("/posts")
def get_all_posts(limit: int = None):
    if limit:
        return list(text_posts.values())[:limit]
    return text_posts

@app.get("/posts/{id}")
def get_post(id: int):
    if id not in text_posts:
        raise HTTPException(status_code=404, detail="Post not found")
    return text_posts.get(id)

@app.post("/posts")
def create_post(post: PostCreate):
    new_id = max(text_posts.keys(), default=0) + 1
    new_post = {"id": new_id, "title": post.title, "content": post.content}
    text_posts[new_id] = {"title": post.title, "content": post.content}
    return new_post

@app.put("/posts/{id}")
def update_post(id: int, upost: UpPut):
    if id not in text_posts:
        raise HTTPException(status_code=404, detail="Post not found")
    
    text_posts[id] = {"title": upost.title, "content": upost.content}
    updated_post = {"id": id, "title": upost.title, "content": upost.content}
    return updated_post

@app.delete("/posts/{id}")
def delete_post(id: int):
    if id not in text_posts:
        raise HTTPException(status_code=404, detail="Post not found")
    
    del text_posts[id]
    return {"detail": "Post deleted successfully"}