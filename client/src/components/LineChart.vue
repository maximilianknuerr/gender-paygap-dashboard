<template>
  <div id="linechart"></div>
</template>

<script>
import * as d3 from "d3"
export default {
  name: "uebung",
  data () {
    return {

      id: "linechart",
      margin: {top: 10, right: 30, bottom: 30, left: 60},
      width: 460,
      height: 400

    }
  },
  mounted() {

      const svg = d3.select('#linechart').append("svg").attr("width", this.width).attr("height", this.height)
          .append("g").attr("transform", "translate(" + this.margin.left + "," + this.margin.top + ")");

      d3.csv("https://raw.githubusercontent.com/holtzy/data_to_viz/master/Example_dataset/3_TwoNumOrdered_comma.csv",
          (d) => {return {date: d3.timeParse("%Y-%m-%d")(d.date), value : d.value }}
      ).then((data) => {
        let x = d3.scaleTime()
            .domain(d3.extent(data, function(d) { return d.date; }))
            .range([ 0, this.width ]);
        svg.append("g")
            .attr("transform", "translate(0," + this.height + ")")
            .call(d3.axisBottom(x));

        // Add Y axis
        let y = d3.scaleLinear()
            .domain([0, d3.max(data, function(d) { return d.value; })])
            .range([ this.height, 0 ]);
        svg.append("g")
            .call(d3.axisLeft(y));

        // Add the line
        svg.append("path")
            .datum(data)
            .attr("fill", "none")
            .attr("stroke", "steelblue")
            .attr("stroke-width", 1.5)
            .attr("d", d3.line()
                .x(function(d) { return x(d.date) })
                .y(function(d) { return y(d.value) })
            )

      })


    },



}
</script>

<style scoped>

</style>