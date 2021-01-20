<template>
<div id="ridgeline"></div>
</template>

<script>
/* eslint-disable no-debugger */

import * as d3 from 'd3'
export default {
name: "RidgeLinePlot",
  data: function () {
    return {
      selected: ""
    }
  },
  props:["dataa"],
  watch: {
    selected() {
      this.$emit("selected", this.selected)
    },
    dataa() {
      this.draw()
    }
  },
  computed: {
    margin: function (){
      return {top: 30, right: 30, bottom: 20, left: 100}
    },
    width: function () {
      return 800 - this.margin.left - this.margin.right
    },
    height: function () {
      return 400 - this.margin.top - this.margin.bottom
    },
    svg: function() {
      return d3.select("#ridgeline")
          .append("svg")
          .attr("width", this.width + this.margin.left + this.margin.right)
          .attr("height", this.height + this.margin.top + this.margin.bottom)
          .append("g")
          .attr("transform",
              "translate(" + this.margin.left + "," + this.margin.top + ")")
    },
    
  },
  methods: {
    drawAxis() {
      var margin = {top: 30, right: 30, bottom: 20, left: 100}
      var width = 600 - margin.left - margin.right
      var height = 400 - margin.top - margin.bottom

      // var svg = d3.select("#ridgeline")
      //     .append("svg")
      //     .attr("width", width + margin.left + margin.right)
      //     .attr("height", height + margin.top + margin.bottom)
      //     .append("g")
      //     .attr("transform",
      //         "translate(" + margin.left + "," + margin.top + ")")
      var categories = ["IT", "Software Engineer", "Financial Analyst", "Sales Associate", "Marketing Associate", "Driver", "Manager", "Graphic Designer", "Warehouse Associate", "Data Scientist"]

      // Add X axis
      var x = d3.scaleLinear()
          .domain([50000, 200000])
          .range([ 0, width ]);
      this.svg.append("g")
          .attr("class", "xAxis")
          .attr("transform", "translate(0," + height + ")")
          .call(d3.axisBottom(x).tickValues([ 50000, 100000, 150000, 200000]).tickSize(-height) )
          .select(".domain").remove()

      // Add X axis label:
      this.svg.append("text")
          .attr("text-anchor", "end")
          .attr("x", width)
          .attr("y", height + 40)
          // .text("Pay Plus Bonus");



      // Create the Y axis for names
      var yName = d3.scaleBand()
          .domain(categories)
          .range([0, height])
          .paddingInner(1)

      this.svg.append("g")
          .call(d3.axisLeft(yName).tickSize(0))
          .select(".domain").remove()
    },
    draw() {
      var my = this
      var margin = {top: 30, right: 30, bottom: 20, left: 100}
      var width = 600 - margin.left - margin.right
      var height = 400 - margin.top - margin.bottom

      // var svg = d3.select("#ridgeline")
      //     .append("svg")
      //     .attr("width", width + margin.left + margin.right)
      //     .attr("height", height + margin.top + margin.bottom)
      //     .append("g")
      //     .attr("transform",
      //         "translate(" + margin.left + "," + margin.top + ")")
      var categories = ["IT", "Software Engineer", "Financial Analyst", "Sales Associate", "Marketing Associate", "Driver", "Manager", "Graphic Designer", "Warehouse Associate", "Data Scientist"]

      // Add X axis
      var x = d3.scaleLinear()
          .domain([50000, 200000])
          .range([ 0, width ]);


      // Create a Y scale for densities
      var y = d3.scaleLinear()
          .domain([0, 0.1])
          .range([ height, 0]);
      // Create the Y axis for names
      var yName = d3.scaleBand()
          .domain(categories)
          .range([0, height])
          .paddingInner(1)

      // var myColor = d3.scaleSequential()
      //     .domain([0, 200000])
      //     .interpolator(d3.interpolateViridis)
      var myColor = d3.scaleOrdinal()
          .domain(['Male', 'Female' ])
          .range([ "#98abc5", "#a05d56" ])

      var maleData = []
      for (let i in categories) {
        let categoryData = []

        for (let j in this.dataa) {
          if (this.dataa[j].JobTitle === categories[i] && this.dataa[j].Gender === "Male") {
            categoryData.push(this.dataa[j])
          }
        }
        maleData.push(categoryData)
      }

      var femaleData = []
      for (let i in categories) {
        let categoryData = []

        for (let j in this.dataa) {
          if (this.dataa[j].JobTitle === categories[i] && this.dataa[j].Gender === "Female") {
            categoryData.push(this.dataa[j])
          }
        }
        femaleData.push(categoryData)
      }

      var maleMeans = []
      for (let i in categories) {
        let mean = d3.mean(maleData[i], function (d) {

          return +d.PayPlusBonus
        })
        maleMeans.push(mean)
      }
      var femaleMeans = []
      for (let i in categories) {
        let mean = d3.mean(femaleData[i], function (d) {

          return +d.PayPlusBonus
        })
        femaleMeans.push(mean)
      }

      // This is what I need to compute kernel density estimation
      function kernelDensityEstimator(kernel, X) {
        return function(V) {
          return X.map(function(x) {
            return [x, d3.mean(V, function(v) {
              return kernel(x - v); })];
          });
        };
      }
      function kernelEpanechnikov(k) {
        return function(v) {

          return Math.abs(v /= k) <= 0.6 ? (0.5 * (1 - v * v) / k)*350 : 0;
        };
      }
      // Compute kernel density estimation for each column:
      var kde = kernelDensityEstimator(kernelEpanechnikov(1000), x.ticks(90)) // increase this 40 for more accurate density.
      var maleDensity = []
      for (let i = 0; i < categories.length; i++) {
        let key = categories[i]
        let data = maleData[i]
        let density = kde( data.map(function(d){
          return d.PayPlusBonus }) )
        density[0].push(categories[i])
        maleDensity.push({key: key, density: density})
      }
      var femaleDensity = []
      for (let i = 0; i < categories.length; i++) {
        let key = categories[i]
        let data = femaleData[i]
        let density = kde( data.map(function(d){
          return d.PayPlusBonus }) )
        density[0].push(categories[i])
        femaleDensity.push({key: key, density: density})
      }
      this.svg.selectAll("path").remove()
      // Add areas
      this.svg.selectAll("areas")
          .data(maleDensity)
          .enter()
          .append("path")
          .attr("class",  function(d) {return ("fuckoff " +  d.key.replace(" ", ""))})
          .attr("transform", function (d) {
            return ("translate(0," + (yName(d.key) - height) + ")")
          })
          .attr("fill", function () {
            let color = myColor("Male")
            return color
          }).on("click", function(d) {

            if(my.selected !== d[0][2]) {
              my.selected = d[0][2]
              d3.selectAll(".fuckoff")
                  .style("opacity", 0.1)

              d3.selectAll("." + d[0][2].replace(" ", ""))
                  .style("opacity", 1)
            }else {
              my.selected = ""
              d3.selectAll(".fuckoff")
                  .style("opacity", 0.7)

            }
          })
          .datum(function (d) {
            return (d.density)
          })
          .attr("opacity", 1)
          .attr("stroke", "#000")
          .attr("stroke-width", 0.1)
          .attr("d", d3.line()
              .curve(d3.curveBasis)
              .x(function (d) {
                return x(d[0]);
              })
              .y(function (d) {
                return y(d[1])
              })
          )



      this.svg.selectAll("areas")
          .data(femaleDensity)
          .enter()
          .append("path")
          .attr("class",  function(d) {return ("fuckoff " +  d.key.replace(" ", ""))})
          .attr("transform", function (d) {
            return ("translate(0," + (yName(d.key) - height) + ")")
          })
          .attr("fill", function () {

            let color = myColor("Female")
            return color
          }).on("click", function(d) {

            if(my.selected !== d[0][2]) {
              my.selected = d[0][2]
              d3.selectAll(".fuckoff")
                  .style("opacity", 0.1)

              d3.selectAll("." + d[0][2].replace(" ", ""))
                  .style("opacity", 1)
            }else {
              my.selected = ""
              d3.selectAll(".fuckoff")
                  .style("opacity", 0.7)

            }
          })
          .datum(function (d) {
            return (d.density)
          })
          .attr("opacity", 0.7)
          .attr("stroke", "#000")
          .attr("stroke-width", 0.1)
          .attr("d", d3.line()
              .curve(d3.curveBasis)
              .x(function (d) {
                return x(d[0]);
              })
              .y(function (d) {
                return y(d[1])
              })
          )
          // .on("mouseover", function (d){
          //
          // })
          // .on("mouseleave", function (d) {
          // })

    }
  },
  mounted () {
    this.drawAxis()
    this.draw()
  }

}
</script>

<style scoped>

</style>