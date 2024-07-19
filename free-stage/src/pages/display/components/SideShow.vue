<script setup lang="ts">
import Text from '@/components/Text.vue'
import VerticalMargin from '@/components/VerticalMargin.vue';
</script>

<template>
    <div class="centered-col">
        <Text :size="50"> 自由舞台 </Text>
        <VerticalMargin :top="50" :bottom="40">
            <img class="img-margin" src="/src/assets/logo-white.svg" width="400" />
        </VerticalMargin>
        <Text :size="25"> STARLIGHT ONLY<br>1st in SHANGHAI </Text>
    </div>
</template>