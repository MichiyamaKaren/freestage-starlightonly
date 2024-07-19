<script setup lang="ts">
import { ref, onMounted, onUnmounted } from 'vue';
import type { Ref } from 'vue';

import {SongList, type Song} from '../ts/SongList';

import Text from '@/components/Text.vue'
import VerticalMargin from '@/components/VerticalMargin.vue';

const props = defineProps({
  songlist: {
    type: SongList,
    required: true
  }
});

const emit = defineEmits(['appendSong', 'delSong']);

let eventSource: EventSource | null = null;

let reconnectTimeoutID: number | undefined = undefined;

const setReconnectTimeout = () => {
  reconnectTimeoutID = setTimeout(() => {
    console.log('Not recieving heartbeat, reconnecting to SSE...');
    if (eventSource) {
      eventSource.close();
    }
    initSSE();
  }, 5500);
};

const initSSE = () => {
  eventSource = new EventSource('/api/listen-new-songs');

  eventSource.onopen = (event) => {
    setReconnectTimeout();
  };
  
  eventSource.addEventListener('appendSong', (event) => {
    const data = JSON.parse(event.data);
    console.log('New song id:', data.id);
    emit('appendSong', data.id);
  });

  eventSource.addEventListener('heartbeat', (event) => {
    window.clearTimeout(reconnectTimeoutID);
    setReconnectTimeout();
  });

  eventSource.onerror = (error) => {
    console.error('SSE error:', error);
    eventSource.close();
  };
};

onMounted(() => {
  initSSE();
});

onUnmounted(() => {
  if (eventSource) {
    eventSource.close();
  }
});

const listHeight = `${window.innerHeight - 100}px`;
</script>

<template>
    <div class="centered-col">
    <VerticalMargin :top="30" :bottom="30" style="width:100%">
        <Text :size="30"> Song List </Text>
    </VerticalMargin>
    <el-scrollbar :height="listHeight">
    <div v-for="(song, i) in songlist.songs" :key="i" class="scrollbar-item">
      <div class="scrollbar-text"> <span> {{ song.title }} </span> </div>
      <el-icon :size="25" color="red" class="scrollbar-close-icon" @click="$emit('delSong', i);"> <CircleClose /> </el-icon>
    </div>
    </el-scrollbar>
    </div>
</template>

<style>
.el-scrollbar {
  width: 100%;
}

.scrollbar-item {
  display: flex;
  align-items: center;
  height: 70px;
  margin-bottom: 20px;
    border-radius: 4px;
    background: var(--el-color-primary-light-9);

  .scrollbar-text {
    font-size: 20px;
    font-weight: bold;
    color: var(--main-bg-color);
    display: flex;
    justify-content: center;
    text-align: center;
    align-items: center;
    height: 100%;
    width: 100%;
  }

  .scrollbar-close-icon {
    margin-left: 10px;
    margin-right: 10px;
  }
}
</style>