<script setup lang="ts">
const props = defineProps({
  top: {
    type: Number,
    required: true
  },
  bottom: {
    type: [Number, null],
    default: null
  }
})

const getStyle = (top: number, bottom: number | null) => {
    if (bottom === null) {
        bottom = top;
    }
    return `margin-top: ${top}px; margin-bottom: ${bottom}px;`;
}

</script>

<template>
    <div :style="getStyle(top, bottom)"> <slot></slot> </div>
</template>