<template>
  <div class="container">
    <div class="header">
      <h1>T20Web — Fichas Tormenta20</h1>
    </div>

    <div class="card">
      <FichaForm />
    </div>

    <div style="height:20px"></div>
    <div class="small">* Campos com * são obrigatórios.</div>
  </div>
</template>

<script setup>
import FichaForm from './components/FichaForm.vue'
</script>
