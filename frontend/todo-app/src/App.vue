<template>
  <div id="app">
    <ToDoList />
  </div>
</template>

<script>
import ToDoList from "@/components/ToDoList.vue";

export default {
  components: {
    ToDoList,
  },
};
</script>

<style>
#app {
  font-family: Arial, sans-serif;
  text-align: center;
  margin-top: 50px;
}
</style>
