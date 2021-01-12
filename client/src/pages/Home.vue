<template v-if="allData">
<v-container fill-height>
  <v-row>
    <v-col cols="6">
      <ScatterPlot v-if="allData" :dataa="allData" @selected="changeScatterSelected"></ScatterPlot>
    </v-col>
    <v-col cols="6">
      <PieChart v-if="maleFemale" :dataa="maleFemale"></PieChart>
    </v-col>
  </v-row>
  <v-row>
    <v-col cols="6">
      <RidgeLinePlot v-if="ridgeData" :dataa="ridgeData"></RidgeLinePlot>
    </v-col>
    <v-col cols="6">
      <BarPlot v-if="barData" :dataa="barData"></BarPlot>
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
    fetchData () {
      getData({Education: this.selectedEducation, JobTitle: this.selectedJobTitle, Age: this.selectedAge})
        .then((data) => {
          console.log(data)
          this.allData = data[0]
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