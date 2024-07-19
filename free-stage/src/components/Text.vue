<script setup lang="ts">
const props = defineProps({
  size: {
    type: Number,
    required: true
  },
  bold: {
    type: Boolean,
    default: true
  },
  color: {
    type: String,
    default: 'white'
  }
})

const getStyle = (size: number, bold: boolean, color: string) => {
    let style=`font-size: ${size}px; color: ${color};`;
    if (bold) {
        style += 'font-weight: bold;';
    }
    return style;
}

</script>

<template>
    <span :style="getStyle(size, bold, color)"> <slot></slot> </span>
</template>