<script setup lang="ts">
import { ref, onMounted } from 'vue';
import type { Ref } from 'vue';

interface Album {
    id: number;
    name: string;
    cover_url: string;
}

interface SongDisplay {
  id: number;
  title: string;
}

const albums: Ref<Album[]> = ref([]);

const fetchAlbums = async (): Promise<void> => {
  fetch(`/api/albums`)
    .then((response) => response.json())
    .then((data) => {
      albums.value = data;
    });
};

const activeAlbum: Ref<string[]> = ref([]);
const activeAlbumSongs: Ref<SongDisplay[]> = ref([]);

const fetchSongsInAlbum = async (albumId: number): Promise<void> => {
  fetch(`/api/album/${albumId}/songs?q=id,title`)
    .then((response) => response.json())
    .then((data) => {
      console.log(data);
      activeAlbumSongs.value = data;
    });
};

const onActiveAlbumChange = (albumId: number) => {
  fetchSongsInAlbum(albumId);
};

const appendSong = (song_id: number) => {
  fetch("/api/append-song", {
    method: "POST",
    headers: {
        'Content-Type': 'application/json'
    },
    body: JSON.stringify({ id: song_id }),
  }).catch((error) => {
    alert("Add song failed");
    console.error(error);
  });
}

onMounted(() => {
  fetchAlbums();
});

</script>

<template>
  <div class="card-content">
  <el-collapse v-model="activeAlbum" @change="onActiveAlbumChange" accordion>
    <el-collapse-item v-for="album in albums" :name="album.id">
      <template #title>
        <el-card
          class="card"
          shadow="hover"
        >
          <template #header>
            <span >{{ album.name }}</span>
          </template>
          <img :src="'/content/'+album.cover_url" >
        </el-card>
      </template>

      <div v-for="song in activeAlbumSongs" :key="song.id" class="songs-list">
        <div @click="appendSong(song.id)" class="songs-list-item"> {{ song.title }} </div>
      </div>
    </el-collapse-item>
  </el-collapse>
  </div>
</template>

<style>
:root {
  --albums-cover-width: 200px;
  --albums-page-width: 240px;
}

.el-collapse {
  /* width: var(--albums-page-width); */
  width: 100%;
  margin-left: 50px;
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(240px, 1fr));
  gap: 16px;
}

.el-collapse-item__header {
  height: auto;
}

/* .el-collapse-item {
}

.el-collapse-item__wrap {
  margin-left: 50px;
  width: var(--albums-page-width);
} */

.songs-list{
  margin-top: 20px;
}

.songs-list-item {
  height: 30px;
  margin-bottom: 5px;
  border-radius: 2px;
  width: 100%;
  background: var(--el-color-primary-light-9);
  cursor: pointer;

  font-weight: bold;
  justify-content: center;
  text-align: center;
}

.card-content {
  .el-card {
    cursor: pointer;
    transition: none;
    /* height: auto; */

    .el-card__header {
      width: var(--albums-page-width);
      height: 60px;
      margin: 0px;
      margin-top: 0px;
      top:0;
    }

    .el-card__body {
      padding: 0;
      display: flex;
      justify-content: center;
      align-items: center;

      img {
        width: var(--albums-cover-width);
        height: var(--albums-cover-width);
        object-fit: var(--albums-cover-width);
      }
    }
  }
}
</style>