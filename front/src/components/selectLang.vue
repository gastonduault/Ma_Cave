<template>
  <div :class="{'open': open}">
    <img src="@/assets/img/dropdown.png" class="dropdown" alt="dropdown"/>
    <img @click="changeLanguage(langSelected)"
         :src="'/src/assets/img/'+langSelected+'.png'"
         :alt="langSelected" />
    <img v-for="lang in langs.filter(l => l !== langSelected)"
         :key="lang"
         @click="changeLanguage(lang)"
         :src="'/src/assets/img/'+lang+'.png'"
         :alt="lang" />
  </div>
</template>

<script>
import { ref, onMounted } from 'vue'
import { useI18n } from 'vue-i18n'
import { Storage } from '@ionic/storage'

export default {
  name: 'SelectLang',

  setup() {
    const langs = ref(['fr', 'en'])
    const langSelected = ref('fr')
    const open = ref(false)
    const { locale } = useI18n()
    let storage = null

    const initStorage = async () => {
      storage = new Storage()
      await storage.create()
    };

    const changeLanguage = async (lang) => {
      open.value = !open.value;
      locale.value = lang;
      langSelected.value = lang;

      if (storage) {
        await storage.set('lang', lang)
      }
    }

    onMounted(async () => {
      await initStorage()
      const lang_selected = await storage.get('lang');
      if (lang_selected) {
        open.value = true
        changeLanguage(lang_selected)
      }
    });

    return {
      langs,
      langSelected,
      open,
      changeLanguage
    };
  }
};
</script>



<style scoped>
  div {
    display: flex;
    align-items: center;
    flex-direction: column;
    gap: 4px 0;
    overflow-x: initial;
    overflow-y: clip;
    height: 29px;
    position: relative;
    padding: 4px 4px;
    transition: 0.3s;
    border-radius: 3px 3px;
  }

  div.open {
    height: 54px;
    background-color: var(--background-grey);
  }

  div.open img.dropdown{
    transform: rotateZ(180deg);
  }

  img.dropdown {
    transition: transform 0.2s;
    position: absolute;
    right: -10px;
    top: 3px;
    width: 11px;
    height: 11px;
  }

  div img {
    margin: 0 0;
    padding: 0 0;
    width: 32px;
    height: 32px;
    position: initial;
  }
</style>