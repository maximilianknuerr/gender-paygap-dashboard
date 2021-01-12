<template>
  <div>
    <div class="toolTip"></div>
    <div id="barplot"></div>
  </div>

</template>

<script>
/* eslint-disable no-debugger,no-unused-vars */

import * as d3 from 'd3'
export default {
name: "BarPlot",
  id: "barplot",
  data: function(){
    return {
      selected: ""
    }
  },
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
    margin: function() {
      return {top: 10, right: 30, bottom: 20, left: 50}
    },
    width: function() {
      return 460 - this.margin.left - this.margin.right
    },
    height: function() {
      return 400 - this.margin.top - this.margin.bottom
    },
    svg: function() {
      return d3.select("#barplot")
          .append("svg")
          .attr("width", this.width + this.margin.left + this.margin.right)
          .attr("height", this.height + this.margin.top + this.margin.bottom)
          .append("g")
          .attr("transform",
              "translate(" + this.margin.left + "," + this.margin.top + ")")
    }
  },
  methods: {
    draw() {
      var my = this
      var height = 400 - this.margin.top - this.margin.bottom
      // List of groups = species here = value of the first column called group -> I show them on the X axis
      var groups = ["High School", "College", "Masters", "PhD"]
      var subgroups = ["Male", "Female"]
      var newData = []
      var length = []
      for(let i in this.dataa) {
          if(!(newData.filter(e => e.group === this.dataa[i].Education).length > 0)) {
            newData.push({group: this.dataa[i].Education, subgroup: 'Male', value: 0})
            newData.push({group: this.dataa[i].Education, subgroup: 'Female', value: 0})
            length.push({value: 0})
            length.push({value: 0})
          }

          var objIndex = newData.findIndex(obj => (obj.group === this.dataa[i].Education & obj.subgroup === this.dataa[i].Gender))
          newData[objIndex].value += this.dataa[i].PayPlusBonus
          length[objIndex].value += 1

      }
      for(let i in newData) {
        newData[i].value = newData[i].value / length[i].value

      }
      var divTooltip = d3.select("div.toolTip")
      divTooltip.style("position", "fixed")
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
      // Add X axis
      var x = d3.scaleBand()
          .domain(groups)
          .range([0, this.width])
          .padding([0.2])
      this.svg.append("g")
          .attr("transform", "translate(0," + this.height + ")")
          .call(d3.axisBottom(x).tickSize(0));

      // Add Y axis
      var y = d3.scaleLinear()
          .domain([0, 150000])
          .range([ this.height, 0 ]);
      this.svg.append("g")
          .call(d3.axisLeft(y));

      // Another scale for subgroup position?
      var xSubgroup = d3.scaleBand()
          .domain(subgroups)
          .range([0, x.bandwidth()])
          .padding([0.05])

      // color palette = one color per subgroup
      var color = d3.scaleOrdinal()
          .domain(["Male", "Female"])
          .range([ "#98abc5", "#a05d56" ])

      this.svg.selectAll("rect").remove()
      // Show the bars
      this.svg.append("g")
          .selectAll("g")
          // Enter in data = loop group per group
          .data(newData)
          .enter()
          .append("g")
          .attr("transform", function(d) { return "translate(" + x(d.group) + ",0)"; })
          .selectAll("rect")
          .data(function(d) { return newData.map(function() { return {group: d.group, key: d.subgroup, value: Math.floor(d.value)}}) })
          .enter().append("rect")
          .attr("x", function(d) {
            return xSubgroup(d.key); })
          .attr("class", function(d){return d.group})
          .attr("y", function(d) { return y(d.value); })
          .attr("width", xSubgroup.bandwidth())
          .attr("height", function(d) {return height - y(d.value); })
          .attr("fill", function(d) { return color(d.key); })
          .on("click", function(d) {
            this.selected = d.group
            if(my.selected !== d.group) {
              my.selected = d.group
              d3.selectAll("rect")
                  .style("opacity", 0.1)

              d3.selectAll("." + d.group)
                  .style("opacity", 1)
            }else {
              my.selected = ""
              d3.selectAll("rect")
                  .style("opacity", 0.9)

            }
          })
          .on("mousemove", function(d){
            var pageX = d3.event.pageX
            var pageY = d3.event.pageY
            divTooltip.style("left", pageX + 10 + "px")
            divTooltip.style("top", pageY - 25 + "px")
            divTooltip.style("display", "inline-block")
            divTooltip.style("opacity", "0.9")

            divTooltip.html((d.group)+"<br>"+d.key+"<br>"+d.value);

          })
          .on("mouseout", function(d){
            divTooltip.style("display", "none")
          })

    }
  },
  mounted() {
    this.draw()
  }
}
</script>

<style>
toolTip {
  position: fixed;
  display: none;
  width: auto;
  height: auto;
  background: #515A5A;
  border: 0 none;
  border-radius: 4px;
  color: #F8786B;
  font: 12px sans-serif;
  padding: 5px;
  text-align: center;
}
</style>