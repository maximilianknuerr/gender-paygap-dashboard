<template>
  <div id="piechart"></div>
</template>

<script>
import * as d3 from "d3"
export default {
name: "PieChart",
  id: "piechart",
  data: () => ({
    width: 450,
    height: 450,
    margin: 40,


  }),
  props: ["dataa"],
  watch: {
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
      var color = d3.scale.ordinal()
            .domain(this.dataa)
            .range(["#98abc5", "#a05d56"])
      var pie = d3.layout.pie().value(function(d) {return d.value; })
      var data_ready = pie(d3.entries(this.dataa))
      this.svg
          .selectAll('whatever')
          .data(data_ready)
          .enter()
          .append('path')
          .attr('d', d3.svg.arc()
              .innerRadius(0)
              .outerRadius(this.radius)
          )
          .attr('fill', function(d){ return(color(d.data.key)) })
          .attr("stroke", "black")
          .style("stroke-width", "2px")
          .style("opacity", 1)
    }
  },
  mounted() {
    this.draw()
  }
}
</script>

<style scoped>

</style>