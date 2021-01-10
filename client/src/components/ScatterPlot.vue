<template>
  <div id="scatterplot"></div>
</template>

<script>
import * as d3 from "d3";


export default {
name: "ScatterPlot",
  data: () => ({
      selected: this.dataa,
  }),
  props: ["dataa"],
  watch: {
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

      // Color scale: give me a specie name, I return a color
      var color = d3.scaleOrdinal()
          .domain(['Male', 'Female' ])
          .range([ "#98abc5", "#a05d56" ])

      // Add a tooltip div. Here I define the general feature of the tooltip: stuff that do not depend on the data point.
      // Its opacity is set to 0: we don't see it by default.
      // var tooltip = d3.select("#scatterplot")
      //     .append("div")
      //     .style("opacity", 0)
      //     .attr("class", "tooltip")
      //     .style("background-color", "white")
      //     .style("border", "solid")
      //     .style("border-width", "1px")
      //     .style("border-radius", "5px")
      //     .style("padding", "10px")
      //
      // // A function that change this tooltip when the user hover a point.
      // // Its opacity is set to 1: we can now see it. Plus it set the text and position of tooltip depending on the datapoint (d)
      // var mouseclick = function() {
      //   tooltip
      //       .style("opacity", 1)
      // }
      // var mousemove = function(d) {
      //   tooltip
      //       .html("Gender: " + d.Gender + ", Job Title: " + d.JobTitle + ", Pay plus Bonus: " + d.PayPlusBonus)
      //       .style("left", (d3.mouse(this)[0]+90) + "px") // It is important to put the +90: other wise the tooltip is exactly where the point is an it creates a weird effect
      //       .style("top", (d3.mouse(this)[1]) + "px")
      // }
      //
      // // A function that change this tooltip when the leaves a point: just need to set opacity to 0 again
      // var mouseleave = function() {
      //   tooltip
      //       .transition()
      //       .duration(200)
      //       .style("opacity", 0)
      // }
      //
      // // Highlight the specie that is hovered
      // var highlight = function(d) {
      //   var selected_gender = d.Gender
      //
      //   d3.selectAll(".dot")
      //       .transition()
      //       .duration(200)
      //       .style("fill", "lightgrey")
      //       .attr("r", 1)
      //
      //   d3.selectAll("." + selected_gender)
      //       .transition()
      //       .duration(200)
      //       .style("fill", color(selected_gender))
      //       .attr("r", 5)
      // }
      // // Highlight the specie that is hovered
      // var doNotHighlight = function () {
      //   mouseleave()
      //   d3.selectAll(".dot")
      //       .transition()
      //       .duration(200)
      //       .style("fill", function (d) { return color(d.Gender) } )
      //       .attr("r", 3 )
      // }
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
            this.selected = this.dataa
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
        d3.selectAll(".dot")
            .transition()
            .duration(200)
            .style("fill", "lightgrey")
            .attr("r", 1)

        dots.transition()
            .duration(200)
            .style("fill", function (d) { return color(d.Gender) } )
            .attr("r", 5)

        this.selected = dots.data()
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
          // .on("mouseover", highlight)
          // .on("mouseleave", doNotHighlight)
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