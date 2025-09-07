<template>
  <div>
    <button @click="exportJson">Exportar JSON</button>
    <input type="file" @change="onFile" accept=".json" />
  </div>
</template>

<script setup>
import { useFichaStore } from '../store/ficha'
const s = useFichaStore()

function exportJson() {
  const blob = new Blob([JSON.stringify(s.ficha)], { type: 'application/json' })
  const url = URL.createObjectURL(blob)
  const a = document.createElement('a')
  a.href = url
  a.download = `${s.ficha.nome || 'ficha'}-t20.json`
  a.click()
  URL.revokeObjectURL(url)
}

function onFile(e) {
  const file = e.target.files[0]
  if (!file) return
  const reader = new FileReader()
  reader.onload = () => {
    try {
      const obj = JSON.parse(reader.result)
      s.ficha = obj
      alert('Ficha importada com sucesso')
    } catch {
      alert('Arquivo JSON inválido')
    }
  }
  reader.readAsText(file)
}
</script>
