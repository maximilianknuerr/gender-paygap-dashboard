<template>
  <v-app>
    <Home></Home>
  </v-app>
</template>

<script>
import Home from './pages/Home.vue';

export default {
  name: 'App',

  components: {
    Home,
  },

  data: () => ({
    csvData: [],
  }),
  methods: {
    readCSV () {

    },
  },
  mounted () {
    this.readCSV();
  }
};
</script>
