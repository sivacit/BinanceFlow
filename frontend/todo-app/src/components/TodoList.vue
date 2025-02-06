<template>
    <div class="todo-app">
      <h2>To-Do List ({{ tasks.length }})</h2>
      <input v-model="newTask" @keyup.enter="addTask" placeholder="Add a new task" />
      <button @click="addTask">Add</button>
      <ul>
        <li v-for="(task, index) in tasks" :key="index">
          <span :class="{ completed: task.completed }" @click="toggleTask(index)">{{ task.text }}</span>
          <button @click="removeTask(index)">❌</button>
        </li>
      </ul>
    </div>
  </template>
  
  <script>
  export default {
    data() {
      return {
        newTask: '',
        tasks: []
      };
    },
    methods: {
      addTask() {
        if (this.newTask.trim() !== '') {
          this.tasks.push({ text: this.newTask, completed: false });
          this.newTask = '';
        }
      },
      toggleTask(index) {
        this.tasks[index].completed = !this.tasks[index].completed;
      },
      removeTask(index) {
        this.tasks.splice(index, 1);
      }
    }
  };
  </script>
  
  <style>
  .todo-app {
    max-width: 400px;
    margin: auto;
    text-align: center;
  }
  .completed {
    text-decoration: line-through;
    color: gray;
  }
  ul {
    list-style: none;
    padding: 0;
  }
  li {
    display: flex;
    justify-content: space-between;
    margin: 5px 0;
  }
  </style>
  