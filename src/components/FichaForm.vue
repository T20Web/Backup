<template>
  <div class="card">
    <div class="header">
      <h2>Ficha T20</h2>
      <div>
        <button class="btn" @click="onSaveLocal">Salvar</button>
        <button class="btn secondary" @click="onLoadLocal">Carregar</button>
        <button class="btn secondary" @click="onReset">Nova Ficha</button>
      </div>
    </div>

    <div v-if="message" class="notice">{{ message }}</div>

    <div class="grid">
      <div>
        <section class="field">
          <label>Jogador</label>
          <input type="text" v-model="s.ficha.jogador" />
        </section>

        <section class="row">
          <div style="flex:1">
            <label>Personagem*</label>
            <input type="text" v-model="s.ficha.personagem" />
          </div>
          <div style="width:140px">
            <label>Nível*</label>
            <input type="number" min="1" v-model.number="s.ficha.nivel" />
          </div>
        </section>

        <div class="row">
          <div style="flex:1" class="field">
            <label>Raça*</label>
            <input type="text" v-model="s.ficha.raca" />
          </div>
          <div style="flex:1" class="field">
            <label>Classe*</label>
            <input type="text" v-model="s.ficha.classe" />
          </div>
        </div>

        <section class="field">
          <label>Tendência</label>
          <input type="text" v-model="s.ficha.tendencia" />
        </section>

        <hr style="margin:12px 0" />

        <h3>Atributos</h3>
        <div class="row">
          <div v-for="(key,label) in attrs" :key="key" style="flex:1">
            <label>{{ label }}</label>
            <input type="number" v-model.number="s.ficha[key]" min="1" max="30" />
            <div class="small">Mod: {{ modifier(s.ficha[key]) }}</div>
          </div>
        </div>

        <hr style="margin:12px 0" />

        <h3>Pontos</h3>
        <div class="row">
          <div style="flex:1"><label>PV Máx</label><input type="number" v-model.number="s.ficha.pv_max" /></div>
          <div style="flex:1"><label>PV Atual</label><input type="number" v-model.number="s.ficha.pv_atual" /></div>
          <div style="flex:1"><label>PM Máx</label><input type="number" v-model.number="s.ficha.pm_max" /></div>
          <div style="flex:1"><label>PM Atual</label><input type="number" v-model.number="s.ficha.pm_atual" /></div>
        </div>

        <hr style="margin:12px 0" />

        <section>
          <label>Anotações</label>
          <textarea v-model="s.ficha.anotacoes"></textarea>
        </section>

        <section class="field">
          <label>Equipamento / Inventário</label>
          <textarea v-model="inventarioText" placeholder="Um item por linha: Nome | qtd | peso | obs"></textarea>
          <div class="small">Formato de importação rápido. Clique em "Salvar" para persistir.</div>
        </section>

      </div>

      <aside>
        <div class="card">
          <h4>Defesa</h4>
          <div class="field"><label>Base</label><input type="number" v-model.number="s.ficha.defesa_base" /></div>
          <div class="field"><label>Armadura</label><input type="number" v-model.number="s.ficha.armadura" /></div>
          <div class="field"><label>Escudo</label><input type="number" v-model.number="s.ficha.escudo" /></div>
          <div class="field"><label>Outros</label><input type="number" v-model.number="s.ficha.outros_modificadores_defesa" /></div>
          <div class="field small">Defesa Calculada: <strong>{{ defesaCalculada }}</strong></div>
        </div>

        <div style="height:12px"></div>

        <div class="card">
          <h4>Perícias (rápido)</h4>
          <div class="small">Adicione perícias no formato: Nome|treinado(true/false)|outros</div>
          <textarea v-model="periciasText" placeholder="Atletismo|true|0
Percepção|false|2"></textarea>
          <div class="row" style="margin-top:8px">
            <button class="btn" @click="parsePericias">Aplicar</button>
            <button class="btn secondary" @click="clearPericias">Limpar</button>
          </div>
        </div>

        <div style="height:12px"></div>

        <div class="card">
          <h4>Export / Import</h4>
          <button class="btn" @click="onExport">Exportar JSON</button>
          <input type="file" @change="onFile" accept="application/json" style="margin-top:8px" />
          <div style="height:8px"></div>
          <button class="btn" @click="onFetchDefault">Carregar Ficha Padrão (server)</button>
          <button class="btn secondary" @click="saveToServer" style="margin-top:8px">Salvar no servidor</button>
        </div>

      </aside>
    </div>
  </div>
</template>

<script setup>
import { computed, ref, watch } from 'vue'
import { useFichaStore } from '../store/ficha'

const s = useFichaStore()
const message = ref('')

const attrs = { forca:'FOR', destreza:'DES', constituicao:'CON', inteligencia:'INT', sabedoria:'SAB', carisma:'CAR' }

function modifier(val) { return Math.floor((val - 10)/2) }

const inventarioText = ref('')
const periciasText = ref('')

watch(() => s.ficha.inventario, (v) => {
  if (Array.isArray(v)) inventarioText.value = v.map(i => `${i.nome||i}|${i.qtd||1}|${i.peso||0}|${i.obs||''}`).join('\n')
}, { immediate:true })

function parsePericias(){
  const lines = periciasText.value.split('\n').map(l => l.trim()).filter(Boolean)
  const obj = {}
  for(const ln of lines){
    const parts = ln.split('|').map(p=>p.trim())
    const nome = parts[0]
    const treinado = parts[1] ? parts[1].toLowerCase() === 'true' : false
    const outros = parts[2] ? Number(parts[2]) : 0
    obj[nome] = { treinado, outros }
  }
  s.ficha.pericias = obj
  message.value = 'Perícias aplicadas.'
  setTimeout(()=>message.value='',2000)
}

function clearPericias(){ s.ficha.pericias = {}; periciasText.value=''; }

function onSaveLocal(){
  try{ s.saveLocal(); message.value='Ficha salva no navegador.' } catch(e){ alert(e.message) }
  setTimeout(()=>message.value='',2000)
}
function onLoadLocal(){
  try{ s.loadLocal(); message.value='Ficha carregada do navegador.' } catch(e){ alert(e.message) }
  setTimeout(()=>message.value='',2000)
}
function onReset(){ s.resetFicha(true); message.value='Ficha resetada.'; setTimeout(()=>message.value='',2000) }

function onExport(){ s.exportJson() }
function onFile(e){
  const file = e.target.files[0]
  if (!file) return
  s.importFromFile(file).then(()=>{ message.value='Ficha importada com sucesso.' }).catch(err=>alert(err.message))
}

const defesaCalculada = computed(()=> s.calcDefesa())

async function onFetchDefault(){
  try{ await s.fetchDefaultFromServer(); message.value='Ficha padrão carregada do servidor.' } catch(e){ alert('Falha ao buscar padrão: '+e.message) }
}

async function saveToServer(){
  try{ await s.saveToServer(); message.value='Ficha salva no servidor.' } catch(e){ alert('Erro ao salvar no servidor: '+(e.response?.data||e.message)) }
}
</script>

<style scoped>
.card{padding:14px}
aside .card{margin-bottom:12px}
</style>
