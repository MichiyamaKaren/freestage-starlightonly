import asyncio

from fastapi import FastAPI, APIRouter
from pydantic import BaseModel


from .db import SongDB, DBTableEnum
from .sse import SSEBackend
from .config import SERVER_ROOT_PATH, DB_PATH, HEARTBEAT_INTERVAL


app = FastAPI(root_path=SERVER_ROOT_PATH)
router = APIRouter()

db_use = SongDB(DB_PATH)

@router.get("/albums")
async def get_albums():
    return db_use.get_all_album()

@router.get("/album/{album_id}")
async def get_album(album_id: int, q: str|None = None):
    cols = db_use.parse_query(q, DBTableEnum.ALBUMS)
    return db_use.query(cols, album_id, DBTableEnum.ALBUMS)

@router.get("/song/{song_id}")
async def get_song(song_id: int, q: str|None = None):
    cols = db_use.parse_query(q, DBTableEnum.SONGS)
    return db_use.query(cols, song_id, DBTableEnum.SONGS)

@router.post("/album/{album_id}")
async def update_album(album_id: int, post_data: dict):
    db_use.update(album_id, DBTableEnum.ALBUMS, post_data)
    return {'status': 'ok'}

@router.post("/song/{song_id}")
async def update_song(song_id: int, post_data: dict):
    db_use.update(song_id, DBTableEnum.SONGS, post_data)
    return {'status': 'ok'}

@router.get("/album/{album_id}/songs")
async def get_songs_in_album(album_id: int, q: str|None = None):
    cols = db_use.parse_query(q, DBTableEnum.SONGS)
    return db_use.query_song_in_album(cols, album_id)


append_event = asyncio.Event()
appended_song_id: int = None

class SongID(BaseModel):
    id: int

@router.post("/append-song")
async def append_song(song_id: SongID):
    global appended_song_id
    appended_song_id = song_id.id
    append_event.set()
    return {'status': 'ok'}

sse = SSEBackend(router, '/listen-new-songs')

@sse.register('heartbeat')
async def heartbeat():
    await asyncio.sleep(HEARTBEAT_INTERVAL)
    return {}

@sse.register('appendSong')
async def await_append_song():
    await append_event.wait()
    append_event.clear()
    return {'id': appended_song_id}

sse.router_register()


app.include_router(router)