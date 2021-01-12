<template>
  <div>
    <div class="tooltip"></div>
    <div id="scatterplot"></div>
  </div>

</template>

<script>
/* eslint-disable no-unused-vars,no-debugger */

import * as d3 from "d3";


export default {
name: "ScatterPlot",
  data: function(){
    return {
      selected: this.dataa,
  }},
  props: ["dataa"],
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
      return {top: 30, right: 30, bottom: 30, left: 50}
    },
    width: function () {
      return 650 - this.margin.left - this.margin.right
    },
    height: function () {
      return 400 - this.margin.top - this.margin.bottom
    },
    svg: function () {
      return d3.select("#scatterplot")
          .append("svg")
          .attr("width", this.width + this.margin.left + this.margin.right)
          .attr("height", this.height + this.margin.top + this.margin.bottom)
          .append("g")
          .attr("transform",
              "translate(" + this.margin.left + "," + this.margin.top + ")")
    },
    x: function() {
      return d3.scaleLinear()
          .domain([15, 70])
          .range([ 0, this.width ]);
    },
    y: function() {
      return d3.scaleLinear()
          .domain([0, 200000])
          .range([ this.height, 0]);
    },

  },
  methods: {
    drawAxis() {

      this.svg.append("g")
          .attr("transform", "translate(0," + this.height + ")")
          .call(d3.axisBottom(this.x))
          .call(g => g.append("text")
              .attr("x", this.width)
              .attr("y", this.margin.bottom - 4)
              .attr("fill", "#263c54")
              .attr("text-anchor", "end")
              .text("Age"))

      this.svg.append("g")
          .call(d3.axisLeft(this.y))
          .call(g => g.append("text")
              .attr("x", -this.margin.left + 5)
              .attr("y", -15)
              .attr("fill", "#263c54")
              .attr("text-anchor", "start")
              .attr("font-family", "Lato")
              .attr("font-weight", 400)
              .text("Pay plus Bonus"))

    },
    draw() {
      var my = this
      // Color scale: give me a specie name, I return a color
      var color = d3.scaleOrdinal()
          .domain(['Male', 'Female' ])
          .range([ "#98abc5", "#a05d56" ])

      // Add a tooltip div. Here I define the general feature of the tooltip: stuff that do not depend on the data point.
      // Its opacity is set to 0: we don't see it by default.
      var tooltip = d3.select("div.tooltip")
          tooltip.style("position", "fixed")
              .style("opacity", 0)
              .style("display", "none")
              .style("width", "auto")
              .style("height", "auto")
              .style("background", "#515A5A")
              .style("border", "none")
              .style("border-radius", "4px")
              .style("color", "#fff")
              .style("font", "12px sans-serif")
              .style("padding", "5px")
              .style("text-align", "center")


      const brush = d3.brush()
          .extent([[0,0], [this.width, this.height]]);

      function isBrushed(brush_coords, cx, cy) {

        var x0 = brush_coords[0][0],
            x1 = brush_coords[1][0],
            y0 = brush_coords[0][1],
            y1 = brush_coords[1][1];

        return x0 <= cx && cx <= x1 && y0 <= cy && cy <= y1;
      }

      var handleBrushed = function() {
        if (!d3.event.selection) {
          my.selected = my.dataa
          d3.selectAll(".dot")
              .transition()
              .duration(200)
              .style("fill", function (d) { return color(d.Gender) } )
              .attr("r", 3 )
          return;
        }

        var brush_coords = d3.brushSelection(this);
        console.log("coords: " + brush_coords)
        var dots = d3.selectAll(".dot").filter(function (){
            var cx = d3.select(this).attr("cx"),
                cy = d3.select(this).attr("cy");
            return isBrushed(brush_coords, cx, cy);
          })
        var dotsData = dots.data()
        d3.select(this).call(brush.move, null)
        d3.selectAll(".dot")
            .transition()
            .duration(200)
            .style("fill", "lightgrey")
            .attr("r", 1)

        dots.transition()
            .duration(200)
            .style("fill", function (d) { return color(d.Gender) } )
            .attr("r", 5)
        my.selected = dotsData
      }
      var x = d3.scaleLinear()
          .domain([15, 70])
          .range([ 0, this.width ]);
      var y = d3.scaleLinear()
          .domain([0, 200000])
          .range([ this.height, 0]);
      // Add dots
      this.svg.selectAll("circle").remove()
      this.svg.append('g')
          .attr("class", "brush")
          .call(brush.on("end", handleBrushed))
          .selectAll("dot")
          .data(this.dataa)
          .enter()
          .append("circle")
          // .on("click", mouseclick)
          .attr("class", function (d) { return "dot " + d.Gender } )
          .attr("cx", function (d) { return x(d.Age); } )
          .attr("cy", function (d) { return y(d.PayPlusBonus); } )
          .attr("r", 3)
          .style("fill", function (d) { return color(d.Gender) } )
          .on("mouseover", function (d){
            var pageX = d3.event.pageX
            var pageY = d3.event.pageY
            tooltip.style("left", pageX + 10 + "px")
            tooltip.style("top", pageY - 25 + "px")
            tooltip.style("display", "inline-block")
            tooltip.style("opacity", "0.9")
            tooltip.html("Gender: " + d.Gender+"<br>"+"Job Title: " + d.JobTitle+"<br>"+"Pay plus Bonus: " + d.PayPlusBonus+"<br>"+"Age: " + d.Age+"<br>"+"Education: " + d.Education)
          })
          .on("mouseleave", function (d) {
            tooltip.style("display", "none")
          })
          // .on("mousemove", mousemove)


    }
  },
  mounted() {
    this.drawAxis()
    this.draw()
  }
}
</script>

<style scoped>

</style>