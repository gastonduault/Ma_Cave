<template>
  <ion-page v-if="showComponent && cellar.id">
    <ion-header class="header">
      <img src="@/assets/img/back.webp" alt="arrow back" class="back" @click="back"/>
      <img :src="`${API_URL}${cellar.profile_picture}`" alt="profil picture" class="pp"/>
      <h3>
        {{ cellar.nom }}
      </h3>
      <button class="update-cellar" @click="editCellar = true"></button>
    </ion-header>
    <div class="content">
      <div class="search-bottle">
        <input v-model="search" :placeholder="$t('search')"/>
        <button v-if="search !== ''" @click="search = ''"></button>
      </div>
      <button class="historique-btn" @click="historique"></button>
      <p v-if="bottles && bottles.length === 0" class="no-bottle">
        {{ $t('no_bottle.msg_1')}} <br /> {{ $t('no_bottle.msg_2')}}
        <span class="add-link" @click="addBottle">{{ $t('no_bottle.msg_3')}}</span>.
      </p>
      <div class="bottles">
        <div v-for="bottle in bottles"
             @click="bottleSelected = bottle"
             :key="bottle.id"
             class="bottle">
          <img class="category"
               :src="'/img/grape_'+bottle.categorie+'.webp'"
               alt="bunch of grapes"/>
          <img class="bottle-img"
               v-if="bottle.imaga && bottle.image.id"
               :src="bottle.image.url"
               alt=" image of bottle"/>
          <img class="bottle-img"
               :class="{'rose': bottle.categorie === 'rose'}"
               v-else :src="'/img/bouteille_'+bottle.categorie+'.webp'"
               alt="image of bottle"/>
          <p>{{ bottle.nom }}</p>
        </div>
      <button class="add-bottle" @click="addBottle">
        <img src="@/assets/img/ajouter.webp" alt="add bottle" />
      </button>
      </div>
    </div>
    <Loader v-if="loading" />
    <AddBottle v-if="addBottleOpen" @close-add-bottle="addBottleOpen = false" />
    <Bottle v-if="bottleSelected !== null"
            @close-modale="bottleSelected = null"
            :bottle="bottleSelected"/>
    <EditCellar v-if="editCellar"
                :cellar="cellar"
                @close-modal="editCellar = false" />
  </ion-page>
</template>

<script lang="ts">
import { IonContent, IonHeader, IonPage, IonTitle, IonToolbar } from '@ionic/vue';
import {Storage} from "@ionic/storage";
import store from '@/store';
import config from '@/store/modules/config'
import router from "@/router";
import Bottle from "@/views/Bottle.vue"
import Loader from "@/components/loader.vue";
import AddBottle from "@/views/AddBottle.vue";
import EditCellar from "@/components/editCellar.vue";

export default {
  name: "CaveList",
  components: {
    IonContent, IonHeader, IonPage, IonTitle,
    IonToolbar, Loader, AddBottle, Bottle, EditCellar
  },
  data() {
    return {
      storage: new Storage,
      addBottleOpen: false,
      bottleSelected: null,
      search: "",
      editCellar: false,
      showComponent: true,
      API_URL: config.API_URL,
    }
  },
  async created() {
    this.storage = new Storage();
    await this.storage.create();
  },
  computed: {
    connected: () => store.getters['user/getConnected'],
    utilisateur: () => store.getters["user/getUSer"],
    cellar: () => store.getters['cellar/getCellarSelected'],
    bottles () {
      const allBottles = store.getters['bottles/getBottles']
      if(this.search === "") {
        return allBottles
      }else {
        return allBottles.filter(bottle =>
            bottle.nom.toLowerCase().includes(this.search.toLowerCase())
        )
      }
    },
    loading: () => store.getters['bottles/getLoading']
  },
  async mounted() {
    await this.init()
  },
  methods: {
    async init() {
      if(!this.cellar ) {
        const cellar = {
          id: await this.storage.get('cellar_selected_id'),
          nom: await this.storage.get('cellar_selected_nom'),
        }
        await store.dispatch('cellar/updtaeCellarSelected', cellar)
      }
      store.dispatch('bottles/bottles', this.cellar.id)
      await this.storage.create();
      const account_id = await this.storage.get('uid');
      if(account_id && !this.connected) await store.dispatch('user/login', account_id)
    },
    async back() {
      router.push('/caveList')
      await this.storage.remove("cave_selected_id")
      await this.storage.remove("cave_selected_nom");
    },
    addBottle() { this.addBottleOpen = true },
    historique() {
      store.dispatch('history/bottles', this.cellar.id)
      router.push("/Historique")
    },
    async deleteCellar() {
      this.showComponent = false

      this.showComponent = true
    }
  }
}

</script>

<style scoped>
.header {
  align-items: center;
  padding: 5px;
  display: flex;
  flex-direction: row;
  justify-content: center;
  justify-items: center;
  height: 60px !important;
}

.header img.pp {
  width: 37px;
  border-radius: 5px 5px;
  margin-right: 10px;
}

.header img.back {
  width: 30px;
  position: absolute;
  left: 15px;
  border-radius: 50%;
  padding: 3px 3px;
  cursor: pointer;
  transition: .3s;
}

.header img.back:focus,
.header img.back:active,
.header img.back:hover{
  background-color: #fce5e5;
  box-shadow: rgba(0, 0, 0, 0.16) 0px 1px 4px;
}

.header h3 {
  margin: 1px 0 0 0;
  font-size: 1.2em;
  position: relative;
}

button.update-cellar {
  width: 33px;
  height: 33px;
  position: absolute;
  top: 13px;
  right: 10px;
  background-color: transparent;
  background-image: url("@/assets/img/parameter.webp");
  background-size: 22px;
  background-repeat: no-repeat;
  background-position: center;
  border-radius: 25px 25px;
  transition: 0.2s;
}

button.update-cellar:focus {
  box-shadow: rgba(0, 0, 0, 0.02) 0px 1px 3px 0px, rgba(27, 31, 35, 0.15) 0px 0px 0px 1px;
  transform: rotateZ(30deg);
}

.content {
  width: 100%;
  height: calc(100% - 30px);
  overflow-y: auto;
  text-align: center;
  padding: 10px 10px;
}

.bottles {
  display: flex;
  justify-content: center;
  align-items: start;
  align-content: start;
  flex-wrap: wrap;
  gap: 20px;
  padding-bottom: 50px;
}

div.search-bottle {
  margin: 5px auto 25px auto;
  position: relative;
  width: 90%;
}

div.search-bottle input{
  background-color: var(--background-grey);
  border: solid 1px var(--background-grey);
  border-radius: 25px 25px;
  padding: 13px 15px;
  width: 100%;
}

div.search-bottle button {
  width: 34px;
  height: 34px;
  padding: 5px 5px;
  background-image: url("@/assets/img/close.webp");
  background-size: 20px;
  background-position: center;
  background-repeat: no-repeat;
  background-color: var(--background-dark);
  border-radius: 25px 25px;
  position: absolute;
  top: 6px;
  right: 6px;
  transition: 0.2s;
  animation: btn-search 0.2s;
}

@keyframes btn-search {
  0% {
    transform: translateX(-20px);
  } 100% {
    transform: translateX(0px);
  }
}

.no-bottle {
  margin-top: 35vh;
  line-height: 70px;
}

.historique-btn {
  position: fixed;
  z-index: 2;
  width: 42px;
  height: 42px;
  right: 3%;
  top: 23%;
  background-color: var(--background-color);
  background-image: url("@/assets/img/historique.webp");
  background-position: center;
  background-size: 23px;
  background-repeat: no-repeat;
  border-radius: 25px 25px;
}

.historique-btn:focus {
  background-color: #e5cdcd;
}

.bottle {
  display: flex;
  position: relative;
  flex-direction: column;
  align-items: center;
  justify-content: space-between;
  padding: 12px 12px;
  background-color: var(--background-grey);
  border-radius: 5px;
  width: 130px;
  height: 150px;
  border: solid 1px transparent;
  transition: .1s;
}

.bottle:hover,
.bottle:active,
.bottle:focus{
  border-color: var(--font-black);
}

.bottle .category {
  width: 20px;
  position: absolute;
  left: 5px;
}

.bottle .bottle-img {
  margin-top: 20px;
  width: 20%;
}

.bottle .bottle-img.rose {
  width: 15%;
}

.bottle p {
  margin: 10px 0 0 0;
}

.add-bottle {
  padding: 8px 8px;
  border-radius: 50%;
  background-color: var(--font-pink);
  position: absolute;
  display: flex;
  align-items: center;
  justify-content: center;
  bottom: 4vh;
}

.add-bottle img {
  width: 23px;
}

</style>
