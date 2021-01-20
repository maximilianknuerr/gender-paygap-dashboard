<template>
  <div id="piechart"></div>
</template>

<script>
/* eslint-disable no-debugger,no-unused-vars */

import * as d3 from "d3"
export default {
name: "PieChart",
  id: "piechart",
  data: () => ({
    width: 400,
    height: 400,
    margin: 40,
    selected: ''

  }),
  props: ["dataa"],
  watch: {
    selected() {
      this.$emit('selected', this.selected)
    },
    dataa() {
      this.draw()
    }
  },
  computed: {

    // color: function() {
    //   return d3.scale.ordinal()
    //       .domain(this.dataa)
    //       .range(["#98abc5", "#a05d56"])
    // },
    radius: function () {
      return Math.min(this.width, this.height) / 2 - this.margin
    },
    svg: function () {
      return d3.select("#piechart")
          .append("svg")
          .attr("width", this.width)
          .attr("height", this.height)
          .append("g")
          .attr("transform", "translate(" + this.width / 2 + "," + this.height / 2 + ")")
    },

  },
  methods: {
    draw() {
      var my = this
      var arc = d3.arc()
          .innerRadius(0)
          .outerRadius(this.radius)
      var color = d3.scaleOrdinal()
            .domain("Male", "Female")
            .range(["#98abc5", "#a05d56"])
      var group = d3.scaleOrdinal()
          .domain("Male", "Female")
          .range(["Male", "Female"])
      var pie = d3.pie().value(function(d) {return d.value; })
      var data_ready = pie(d3.entries(this.dataa))
      this.svg.selectAll('path').remove()
      this.svg.selectAll('text').remove()
      this.svg
          .selectAll('whatever')
          .data(data_ready)
          .enter()
          .append('path')
          .attr("class", "arc")
          .attr('d', d3.arc()
              .innerRadius(0)
              .outerRadius(this.radius)
          )
          .attr('fill', function(d){ return(color(d.data.key)) })
          .style("opacity", 0.9)
          .on("click", function(d) {
            if(my.selected !== group(d.data.key)) {
              my.selected = group(d.data.key)
              d3.selectAll(".arc")
                  .style("opacity", 0.3)
                  .attr("stroke", "none")
                  .attr("stroke-width", "none")
              d3.select(this)
                  .attr("stroke", "#fff")
                  .attr("stroke-width", "3px")
                  .style("opacity", 1)
            }else {
              my.selected = ""
              d3.selectAll(".arc")
                  .style("opacity", 0.9)
                  .attr("stroke", "none")
                  .attr("stroke-width", "none")
              d3.select(this)
                  .attr("stroke", "none")
                  .attr("stroke-width", "none")

            }

          })

      this.svg
          .selectAll('whatever')
          .data(data_ready)
          .enter()
          .append('text')
          .text(function(d){ return group(d.data.key) + ": " + d.data.value})
          .attr("transform", function(d) { return "translate(" + arc.centroid(d) + ")";  })
          .style("text-anchor", "middle")
          .style("font-size", 17)

    },

  },
  mounted() {
    this.draw()
  }
}
</script>

<style scoped>

</style>