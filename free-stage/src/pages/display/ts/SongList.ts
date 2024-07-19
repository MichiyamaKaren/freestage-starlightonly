export interface Song {
    id: number;
    title: string;
    artist: string;
    url: string;
    album_id: number;
}

export class SongList {
    songs: Song[];
    constructor() { 
        this.songs = [];
    }

    appendSong (song: Song) {
        this.songs.push(song);
    }

    delSong (i: number) {
        return this.songs.splice(i, 1)[0];
    };

    popFirst () {
        return this.songs.splice(0, 1)[0];
    };
}