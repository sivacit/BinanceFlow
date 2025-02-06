<template>
  <div id="app">
    <TodoList />
  </div>
</template>

<script>
import TodoList from "./components/TodoList.vue";

export default {
  components: {
    TodoList
  }
};
</script>

<style>
#app {
  font-family: Arial, sans-serif;
  margin-top: 50px;
}
</style>
