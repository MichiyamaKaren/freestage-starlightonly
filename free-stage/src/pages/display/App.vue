<script setup lang="ts">
import { ref } from 'vue';
import type { Ref } from 'vue';

import {SongList, type Song} from './ts/SongList';

import SideShow from './components/SideShow.vue';
import AudioPlayer from './components/AudioPlayer.vue';
import SongListComp from './components/SongList.vue';

const songlist = ref(new SongList());
const songPlaying: Ref<Song | null> = ref(null);

const onAppendSong = (song_id: number) => {
  fetch(`/api/song/${song_id}`)
    .then(response => response.json())
    .then(data => {
      let song: Song = {
        'id': data.id,
        'artist': data.artist,
        'title': data.title,
        'url': `/content/${data.path}`,
        'album_id': data.album_id
      };
      if (songPlaying.value === null) {
        songPlaying.value = song;
      }
      else {
        songlist.value.appendSong(song);
      }
    });
}

const onNextSong = () => {
  if (songlist.value.songs.length == 0) {
    songPlaying.value = null;
  }
  else {
    songPlaying.value = songlist.value.popFirst();
  }
}
</script>

<template>
  <el-row align="middle" class="main-frame">
    <el-col :span="6" :offset="1">
      <SideShow />
    </el-col>

    <el-col :span="8" :offset="1">
      <AudioPlayer :songPlaying="songPlaying"
        @nextSong="onNextSong" />
    </el-col>

    <el-col :span="6" :offset="1">
      <SongListComp :songlist="songlist"
        @append-song="onAppendSong"
        @del-song="(i) => { songlist.delSong(i); } " />
    </el-col>
  </el-row>
</template>

<style>
.main-frame {
  width: 100%;
  height: 100%;
  position: absolute;
}

.centered-col {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  text-align: center;
}

.el-table__header-wrapper tr .cell {
  font-size: 20px;
  font-weight: bold;
}

</style>