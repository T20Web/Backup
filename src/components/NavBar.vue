<template>
  <nav class="navbar">
    <router-link to="/">🏠 Home</router-link>
    <router-link to="/nova">➕ Nova Ficha</router-link>
    <router-link to="/fichas">📜 Minhas Fichas</router-link>
  </nav>
</template>

<style scoped>
.navbar {
  display: flex;
  gap: 1rem;
  background: #222;
  padding: 1rem;
}
.navbar a {
  color: #fff;
  text-decoration: none;
}
.navbar a.router-link-active {
  font-weight: bold;
  border-bottom: 2px solid #f00;
}
</style>
