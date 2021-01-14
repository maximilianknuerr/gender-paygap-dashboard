<template v-if="allData">
<v-container fill-height>
  <v-row>
    <v-col cols="6">
      <ScatterPlot v-if="scatterData" :dataa="scatterData" @selected="changeScatterSelected"></ScatterPlot>
    </v-col>
    <v-col cols="6">
      <PieChart v-if="maleFemale" :dataa="maleFemale" @selected="changePieSelected"></PieChart>
    </v-col>
  </v-row>
  <v-row>
    <v-col cols="6">
      <RidgeLinePlot v-if="ridgeData" :dataa="ridgeData" @selected="changeRidgeSelected"></RidgeLinePlot>
    </v-col>
    <v-col cols="6">
      <BarPlot v-if="barData" :dataa="barData" @selected="changeBarSelected"></BarPlot>
    </v-col>
  </v-row>
</v-container>
</template>

<script>
import PieChart from "@/components/PieChart";
import {getData, getGender} from "@/helpers/DataFetcher";
import ScatterPlot from "@/components/ScatterPlot";
import RidgeLinePlot from "@/components/RidgeLinePlot";
import BarPlot from "@/components/BarPlot";
export default {
name: "Home",
  components: {
    BarPlot,
    RidgeLinePlot,
    PieChart,
    ScatterPlot
  },
  data: () => ({
    allData: null,
    scatterData: null,
    barData: null,
    ridgeData: null,
    ageItems: ["18 - 25", "26 - 35", "36 - 50", "51 - 70", "Alle anzeigen"],
    selectedAge: "Alle anzeigen",
    educationItems: ["High School", "College", "Masters", "PhD", "Alle anzeigen"],
    selectedEducation: "Alle anzeigen",
    jobTitleItems: ["IT", "Software Engineer", "Financial Analyst", "Sales Associate", "Marketing Associate", "Driver", "Manager", "Graphic Designer", "Warehouse Associate", "Data Scientist", "Alle anzeigen"],
    selectedJobTitle: "Alle anzeigen",
    maleFemale: null

  }),
  methods: {
    changeAge (data) {
      this.selectedAge = data
      this.fetchData()
    },
    changeEducation (data) {
      this.selectedEducation = data
      this.fetchData()
    },
    changeJobTitle (data) {
      this.selectedJobTitle = data
      this.fetchData()
    },
    changeScatterSelected(data) {
      this.barData = data
      this.ridgeData = data
      this.fetchGender(data)
    },
    changeBarSelected(data) {
      getData({Education: data, JobTitle: "", Gender: ""})
          .then((data) => {
            console.log(data)
            this.barData = this.allData
            this.scatterData = data[0]
            this.ridgeData = data[0]
            this.maleFemale = [data[1], data[2]]
          })
    },
    changePieSelected(data) {
      getData({Education: "", JobTitle: "", Gender: data})
          .then((data) => {
            console.log(data)
            this.scatterData = data[0]
            this.ridgeData = data[0]
            this.barData = data[0]
            
          })
    },
    changeRidgeSelected(data) {
      getData({Education: "", JobTitle: data, Gender: ""})
          .then((data) => {
            console.log(data)
            this.ridgeData = this.allData
            this.scatterData = data[0]
            this.barData = data[0]
            this.maleFemale = [data[1], data[2]]

          })
    },
    fetchData () {
      getData({Education: "", JobTitle: "", Gender: ""})
        .then((data) => {
          console.log(data)
          this.allData = data[0]
          this.scatterData = this.allData
          this.barData = this.allData
          this.ridgeData = this.allData
          this.maleFemale = [data[1], data[2]]
        })

    },
    fetchGender(data) {
      getGender({Data: data})
          .then((data) => {
            console.log(data)
            this.maleFemale = [data[0], data[1]]
          })
    }
  },
  async mounted () {
    this.fetchData()
  }
}
</script>

<style scoped>

</style>