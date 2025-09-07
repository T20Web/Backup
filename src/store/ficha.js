import { defineStore } from 'pinia'
import { reactive, toRaw } from 'vue'
import axios from 'axios'

const STORAGE_KEY = 't20web:ficha'
const API_BASE = 'http://127.0.0.1:8000/api'

export const useFichaStore = defineStore('ficha', () => {
  const ficha = reactive({
    schema_version: '1.0',
    jogador: '',
    personagem: '',
    raca: '',
    origem: '',
    classe: '',
    nivel: 1,
    tendencia: '',
    divindade: '',
    forca: 10, destreza: 10, constituicao: 10, inteligencia: 10, sabedoria: 10, carisma: 10,
    pv_max: 0, pv_atual: 0, pm_max: 0, pm_atual: 0,
    defesa_base: 10, armadura: 0, escudo: 0, penalidade_armadura: 0, outros_modificadores_defesa: 0,
    pericias: {},
    poderes: [],
    magias: [],
    inventario: [],
    anotacoes: '',
    tesouro: '',
    carga: ''
  })

  function validateRequired() {
    const missing = []
    if (!ficha.personagem || !ficha.personagem.trim()) missing.push('Personagem')
    if (!ficha.raca || !ficha.raca.trim()) missing.push('Raça')
    if (!ficha.classe || !ficha.classe.trim()) missing.push('Classe')
    if (!ficha.nivel || ficha.nivel < 1) missing.push('Nível (>=1)')
    return missing
  }

  function saveLocal() {
    const missing = validateRequired()
    if (missing.length) throw new Error('Campos obrigatórios faltando: ' + missing.join(', '))
    localStorage.setItem(STORAGE_KEY, JSON.stringify(toRaw(ficha)))
  }

  function loadLocal() {
    const raw = localStorage.getItem(STORAGE_KEY)
    if (!raw) throw new Error('Nenhuma ficha salva no navegador.')
    const obj = JSON.parse(raw)
    Object.assign(ficha, obj)
  }

  function resetFicha(confirmDialog = true) {
    if (confirmDialog) {
      const ok = confirm('Criar nova ficha? Os dados atuais serão apagados.')
      if (!ok) return
    }
    localStorage.removeItem(STORAGE_KEY)
    Object.assign(ficha, {
      schema_version: '1.0', jogador:'', personagem:'', raca:'', origem:'', classe:'', nivel:1, tendencia:'', divindade:'',
      forca:10, destreza:10, constituicao:10, inteligencia:10, sabedoria:10, carisma:10,
      pv_max:0,pv_atual:0,pm_max:0,pm_atual:0, defesa_base:10,armadura:0,escudo:0,penalidade_armadura:0,outros_modificadores_defesa:0,
      pericias:{}, poderes:[], magias:[], inventario:[], anotacoes:'', tesouro:'', carga:''
    })
  }

  function exportJson(filename = null) {
    const data = JSON.stringify(toRaw(ficha), null, 2)
    const blob = new Blob([data], { type: 'application/json' })
    const url = URL.createObjectURL(blob)
    const a = document.createElement('a')
    a.href = url
    a.download = (filename || (ficha.personagem || 'ficha')) + '-t20.json'
    a.click()
    URL.revokeObjectURL(url)
  }

  function importFromFile(file) {
    return new Promise((resolve, reject) => {
      const reader = new FileReader()
      reader.onload = () => {
        try {
          const obj = JSON.parse(reader.result)
          // basic validation: check required keys
          if (!obj.personagem || !obj.classe || !obj.raca) {
            reject(new Error('JSON inválido: faltam campos obrigatórios (personagem/classe/raça).'))
            return
          }
          Object.assign(ficha, obj)
          resolve()
        } catch (e) { reject(e) }
      }
      reader.onerror = () => reject(new Error('Falha ao ler o arquivo'))
      reader.readAsText(file)
    })
  }

  function calcDefesa() {
    const modDes = Math.floor((ficha.destreza - 10) / 2)
    return ficha.defesa_base + modDes + ficha.armadura + ficha.escudo + ficha.outros_modificadores_defesa
  }

  async function fetchDefaultFromServer() {
    try {
      const res = await axios.get(`${API_BASE}/fichas/default/`)
      Object.assign(ficha, res.data)
    } catch (e) {
      throw e
    }
  }

  async function saveToServer() {
    const payload = toRaw(ficha)
    try {
      if (payload.id) {
        const res = await axios.put(`${API_BASE}/fichas/${payload.id}/`, payload)
        Object.assign(ficha, res.data)
      } else {
        const res = await axios.post(`${API_BASE}/fichas/`, payload)
        Object.assign(ficha, res.data)
      }
    } catch (e) { throw e }
  }

  async function exportFromServer(id) {
    const res = await axios.get(`${API_BASE}/fichas/${id}/export/`)
    return res.data
  }

  return { ficha, saveLocal, loadLocal, resetFicha, exportJson, importFromFile, calcDefesa, fetchDefaultFromServer, saveToServer, exportFromServer }
})
