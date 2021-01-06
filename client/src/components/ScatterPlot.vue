<template>

</template>

<script>
import * as d3 from "d3";

export default {
name: "ScatterPlot",
  data: () => ({
    margin: {top: 10, right: 30, bottom: 30, left: 60},
    width: 460 - this.margin.left - this.margin.right,
    height: 400 - this.margin.top - this.margin.bottom
  }),
  props: ["dataa"],
  watch: {
    dataa() {
      this.draw()
    }
  },
  computed: {

    svg: function () {
      return d3.select("#my_dataviz")
          .append("svg")
          .attr("width", this.width + this.margin.left + this.margin.right)
          .attr("height", this.height + this.margin.top + this.margin.bottom)
          .append("g")
          .attr("transform",
              "translate(" + this.margin.left + "," + this.margin.top + ")")
    },

  },
  methods: {
    draw() {
      // Add X axis
      var x = d3.scale.linear()
          .domain([4, 8])
          .range([ 0, this.width ]);
      this.svg.append("g")
          .attr("transform", "translate(0," + this.height + ")")
          .call(d3.axisBottom(x));

      // Add Y axis
      var y = d3.scale.linear()
          .domain([0, 9])
          .range([ this.height, 0]);
      this.svg.append("g")
          .call(d3.axisLeft(y));

      // Color scale: give me a specie name, I return a color
      var color = d3.scale.ordinal()
          .domain(['Male', 'Female' ])
          .range([ "#440154ff", "#21908dff"])

      // Add dots
      this.svg.append('g')
          .selectAll("dot")
          .data(this.dataa)
          .enter()
          .append("circle")
          .attr("cx", function (d) { return x(d.Sepal_Length); } )
          .attr("cy", function (d) { return y(d.Petal_Length); } )
          .attr("r", 5)
          .style("fill", function (d) { return color(d.Species) } )
    }
  },
  mounted() {
    this.draw()
  }
}
</script>

<style scoped>

</style>