<template v-if="allData">
<v-container>
  <v-row>
    <v-col cols="3">
      <v-select @change="changeAge" :items="ageItems" label="Age"></v-select>
    </v-col>
    <v-col cols="3">
      <v-select @change="changeEducation" :items="educationItems" label="Education"></v-select>
    </v-col>
    <v-col cols="3">
      <v-select @change="changeJobTitle" :items="jobTitleItems" label="Beruf"></v-select>
    </v-col>
  </v-row>
  <v-row>
    <PieChart v-if="maleFemale" :dataa="maleFemale"></PieChart>
  </v-row>
</v-container>
</template>

<script>
import PieChart from "@/components/PieChart";
import getData from "@/helpers/DataFetcher";
export default {
name: "Home",
  components: {
    PieChart,
  },
  data: () => ({
    allData: null,
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
    fetchData () {
      getData({Education: this.selectedEducation, JobTitle: this.selectedJobTitle, Age: this.selectedAge})
        .then((data) => {
          console.log(data)
          this.allData = data[0]
          this.maleFemale = data[1]
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