<script setup lang="ts">
import { ref, type Ref, computed, watch } from 'vue';
import type { Song } from '../ts/SongList';

import Text from '@/components/Text.vue';
import VerticalMargin from '@/components/VerticalMargin.vue';

const props = defineProps({
    songPlaying: {
        type: Object as () => Song | null,
        required: true
    }
});
const emit = defineEmits(['nextSong']);

const audio: Ref<HTMLAudioElement | null> = ref(null);

const onEndPlay = (event: Event) => {
    console.log("Audio play completed");
    setTimeout(() => {
        emit('nextSong');
    }, 500);
};

const onAudioLoaded = (event: Event) => {
    if (audio.value !== null) {
        audio.value.play();
    }
}

const coverURL = ref("");

const titleShow = computed(() => {
    if (props.songPlaying === null) {
        return "IDLE";
    }
    return props.songPlaying.title;
});

const songURL = computed(() => {
    if (props.songPlaying === null) {
        return "";
    }
    return props.songPlaying.url;
});

watch(() => props.songPlaying, async (newSong, oldSong) => {
    if (newSong !== null) {
        let response = await fetch(`/api/album/${newSong.album_id}?q=cover_path`);
        let data = await response.json()
        coverURL.value = `/content/${data.cover_path}`;
    }
    else {
        coverURL.value = "";
    }
});

</script>

<template>
<div class="centered-col">
    <Text :size="25"> NOW PLAYING </Text>
    <VerticalMargin :top="40" :bottom="0">
        <Text :size="35"> {{ titleShow }} </Text>
    </VerticalMargin>
    <VerticalMargin :top="40" :bottom="40">
        <img :src="coverURL" width="400" height="400"/>
    </VerticalMargin>
    <div class="audio-div">
        <audio controls ref="audio" :src="songURL" @ended="onEndPlay" @loadeddata="onAudioLoaded"></audio>
        <el-icon :size="40" @click="$emit('nextSong')"><ArrowRightBold /></el-icon>
    </div>
</div>
</template>

<style>

.audio-div {
    width: 100%;
    justify-content: center;
    align-items: center;
    display: flex;

    .el-icon {
        background-color: red;
        margin-left: 40px;
    }
}
</style>