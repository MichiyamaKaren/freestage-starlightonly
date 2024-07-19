import sqlite3
from enum import Enum

from typing import List, Dict


class DBTableEnum(Enum):
    SONGS = 0
    ALBUMS = 1


class SongDB:
    TABLE_NAME = {
        DBTableEnum.SONGS: 'songs',
        DBTableEnum.ALBUMS: 'albums'
    }
    TABLE_COLUMNS = {
        DBTableEnum.SONGS: ['id', 'title', 'artist', 'path', 'album_id'],
        DBTableEnum.ALBUMS: ['id', 'name', 'cover_path']
    }

    def __init__(self, db_path: str) -> None:
        self.db_connection = sqlite3.connect(db_path)
        self.cursor = self.db_connection.cursor()

    def close(self):
        self.db_connection.commit()
        self.db_connection.close()

    def parse_query(self, query: str | None, table: DBTableEnum):
        table_columns = self.TABLE_COLUMNS[table]
        if query is None:
            return table_columns
        query_cols = query.split(',')
        return [col for col in query_cols if col in table_columns]

    def query(self, cols: List[str], query_id: int, table: DBTableEnum):
        album = self.cursor.execute('SELECT {} FROM {} WHERE id=(?)'.format(
            ','.join(cols), self.TABLE_NAME[table]), (query_id,)).fetchone()
        return dict(zip(cols, album))

    def query_song_in_album(self, cols: List[str], album_id: int):
        songs = self.cursor.execute('SELECT {} FROM songs WHERE album_id=(?)'.format(','.join(cols)), (album_id,)).fetchall()
        return [dict(zip(cols, s)) for s in songs]

    def get_all_album(self):
        albums = self.cursor.execute(
            'SELECT id, name, cover_path FROM albums').fetchall()
        return [{'id': a[0], 'name': a[1], 'cover_url': a[2]} for a in albums]

    def update(self, query_id: int, update_dict: Dict, table: DBTableEnum):
        update_cols = [col for col in update_dict.keys() if col in self.TABLE_COLUMNS[table]]
        update_values = [update_dict[col] for col in update_cols]
        self.cursor.execute('UPDATE {} SET {} WHERE id=(?)'.format(
            self.TABLE_NAME[table], ','.join([f'{col}=(?)' for col in update_cols])), update_values + [query_id])
        self.db_connection.commit()