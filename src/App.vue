<template>
  <div class="container">
    <div class="header">
      <h1>T20Web — Fichas Tormenta20</h1>
      <div class="small">Frontend em Vue 3 · Backend (opcional) Django/DRF</div>
    </div>

    <div class="card">
      <FichaForm />
    </div>

    <div style="height:20px"></div>
    <div class="small">* Campos com * são obrigatórios. Este MVP salva no localStorage e pode integrar com o backend.</div>
  </div>
</template>

<script setup>
import FichaForm from './components/FichaForm.vue'
</script>
