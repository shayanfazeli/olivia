var Grapher;
(function (k) {
    var b = function (a) {
        this._selection = {};
        this._radiusScale = d3.scale.sqrt();
        this._element = d3.select(a);
        this._margin = {top: 20, right: 20, bottom: 80, left: 40};
        this._width = this._element.attr("width") - this._margin.right - this._margin.left;
        this._height = this._element.attr("height") - this._margin.top - this._margin.bottom;
        this.xScale = d3.scale.linear();
        this.yScale = d3.scale.linear()
    };
    Object.defineProperty(b.prototype, "dataSource", {
        set: function (a) {
            this._dataSource = a
        }, enumerable: !0, configurable: !0
    });
    Object.defineProperty(b.prototype,
        "labelData", {
            set: function (a) {
                this._labelData = a
            }, enumerable: !0, configurable: !0
        });
    Object.defineProperty(b.prototype, "xData", {
        set: function (a) {
            this._xData = a
        }, enumerable: !0, configurable: !0
    });
    Object.defineProperty(b.prototype, "yData", {
        set: function (a) {
            this._yData = a
        }, enumerable: !0, configurable: !0
    });
    Object.defineProperty(b.prototype, "radiusData", {
        set: function (a) {
            this._radiusData = a
        }, enumerable: !0, configurable: !0
    });
    Object.defineProperty(b.prototype, "colorData", {
        set: function (a) {
            this._colorData = a
        }, enumerable: !0,
        configurable: !0
    });
    Object.defineProperty(b.prototype, "startTime", {
        set: function (a) {
            this._startTime = a
        }, enumerable: !0, configurable: !0
    });
    Object.defineProperty(b.prototype, "endTime", {
        set: function (a) {
            this._endTime = a
        }, enumerable: !0, configurable: !0
    });
    Object.defineProperty(b.prototype, "xScale", {
        set: function (a) {
            this._xScale = a;
            this._xAxis = d3.svg.axis().orient("bottom").scale(this._xScale)
        }, enumerable: !0, configurable: !0
    });
    Object.defineProperty(b.prototype, "yScale", {
        set: function (a) {
            this._yScale = a;
            this._yAxis = d3.svg.axis().orient("left").scale(this._yScale)
        },
        enumerable: !0, configurable: !0
    });
    Object.defineProperty(b.prototype, "colorScale", {
        set: function (a) {
            this._colorScale = a
        }, enumerable: !0, configurable: !0
    });
    Object.defineProperty(b.prototype, "xAxis", {
        get: function () {
            return this._xAxis
        }, enumerable: !0, configurable: !0
    });
    Object.defineProperty(b.prototype, "yAxis", {
        get: function () {
            return this._yAxis
        }, enumerable: !0, configurable: !0
    });
    b.prototype.select = function (a) {
        this._selection[a] = !0
    };
    b.prototype.startTransition = function () {
        this._diagram || this.draw();
        this._timeSliderPlayButton.style("display",
            "none");
        this._timeSliderHead.style("display", "block");
        var a = this._startTime.getTime(), c = this._endTime.getTime(), e = this._currentTime.getTime(),
            a = 2E4 * (c - e) / (c - a), b = d3.interpolate(this._currentTime, this._endTime), d = this;
        this._diagram.transition().duration(a).ease("linear").tween("date", function () {
            return function (a) {
                d.update(new Date(b(a)))
            }
        }).each("end", function () {
            d.stopTransition()
        })
    };
    b.prototype.stopTransition = function () {
        this._diagram.transition().duration(0)
    };
    b.prototype.draw = function () {
        this.createScales();
        this.createColorAxis();
        this.createRadiusAxis();
        this.createTimeSlider();
        this._diagram = this._element.append("g").attr("transform", "translate(" + this._margin.left + "," + this._margin.top + ")");
        this.createRules();
        this.createItems()
    };
    b.prototype.createScales = function () {
        var a = this.computeDomain(this._xData), c = this.computeDomain(this._yData);
        this._radiusDomain = this.computeDomain(this._radiusData);
        this._colorDomain = this.computeDomain(this._colorData);
        this.computeTimeDomain();
        a = this._xScale.domain(a).range([30,
            this._width - 30 - 40]);
        this._xScale = this._xScale.domain([a.invert(0), a.invert(this._width)]).range([0, this._width]).clamp(!0);
        c = this._yScale.domain(c).range([30, this._height - 30]);
        this._yScale = this._yScale.domain([c.invert(0), c.invert(this._height)]).range([this._height, 0]).clamp(!0);
        this._radiusScale = this._radiusScale.domain([0, this._radiusDomain[1]]).range([2, 20]).clamp(!0);
        if (this._colorDomain) {
            var a = [{stop: 0, color: "#3e53ff"}, {stop: 0.33, color: "#2ff076"}, {
                    stop: 0.5,
                    color: "#d0ff2f"
                }, {stop: 0.66, color: "#ffff2f"},
                    {stop: 1, color: "#ff2f2f"}],
                e = this._element.append("defs").append("linearGradient").attr("id", "colorGradient").attr("x2", "1");
            a.forEach(function (a) {
                e.append("stop").attr("offset", a.stop).attr("stop-color", a.color)
            });
            c = a.map(function (a) {
                return a.stop
            });
            a = a.map(function (a) {
                return a.color
            });
            this._colorScale = d3.scale.linear().domain(c.map(d3.scale.linear().domain(this._colorDomain).invert)).range(a)
        }
        this._colorScale || (this._colorScale = d3.scale.category10())
    };
    b.prototype.createRules = function () {
        var a = this._diagram.append("g").classed("rules",
            !0);
        a.append("g").classed("axis", !0).attr("transform", "translate(0," + this._height + ")").call(this.xAxis.tickSize(2, 0, 2));
        a.append("g").classed("axis", !0).call(this.yAxis.tickSize(2, 0, 2));
        a.append("g").classed("grid", !0).attr("transform", "translate(0," + this._height + ")").call(this.xAxis.tickSize(-this._height, 0, -this._height).tickFormat(function () {
            return ""
        }));
        a.append("g").classed("grid", !0).call(this.yAxis.tickSize(-this._width, 0, -this._width).tickFormat(function () {
            return ""
        }));
        a.selectAll(".grid line").filter(function (a) {
            return 0 ==
                a
        }).classed("origin", !0);
        a.append("text").attr("text-anchor", "end").attr("x", this._width - 3).attr("y", this._height - 6).text(this._xData);
        a.append("text").attr("text-anchor", "end").attr("x", "-3").attr("y", 11).attr("transform", "rotate(-90)").text(this._yData)
    };
    b.prototype.createColorAxis = function () {
        if (this._colorDomain) {
            var a = 0.25 * this._width, c = this._margin.left, e = Number(this._element.attr("height")) - 30,
                b = d3.scale.linear().domain(this._colorDomain).range([0, a]),
                d = [0, 0.5, 1].map(d3.scale.linear().domain(this._colorDomain).invert),
                b = d3.svg.axis().orient("bottom").scale(b).tickSize(2, 0, 2).tickValues(d),
                c = this._element.append("g").attr("transform", "translate(" + c + "," + e + ")");
            c.append("g").classed("axis", !0).attr("transform", "translate(0,9)").call(b);
            c.append("rect").attr("y", -3).attr("width", a).attr("height", 10).style("fill", "url(#colorGradient)");
            c.append("text").attr("text-anchor", "start").attr("dy", -8).text(this._colorData)
        }
    };
    b.prototype.createRadiusAxis = function () {
        var a = 0.25 * this._width, c = this._margin.left + (this._colorDomain ?
            0.32 * this._width : 0), e = Number(this._element.attr("height")) - 30,
            b = d3.scale.linear().domain([0, this._radiusDomain[1]]).range([0, a]),
            d = [0, 0.5, 1].map(d3.scale.linear().domain([0, this._radiusDomain[1]]).invert),
            b = d3.svg.axis().orient("bottom").scale(b).tickSize(2, 0, 2).tickValues(d),
            c = this._element.append("g").attr("transform", "translate(" + c + "," + e + ")");
        c.append("g").classed("axis", !0).attr("transform", "translate(0,9)").call(b);
        for (e = 0; 5 > e; e++) c.append("circle").attr("cx", e * a / 4).attr("cy", 2).attr("r", e + 1).style("fill",
            "#888");
        c.append("text").attr("text-anchor", "start").attr("dy", -8).text(this._radiusData)
    };
    b.prototype.createTimeSlider = function () {
        var a = this._width * (this._colorDomain ? 0.32 : 0.64),
            c = this._element.attr("width") - this._margin.right - a, e = Number(this._element.attr("height")) - 30;
        this._timeScale = d3.time.scale().domain([this._startTime, this._endTime]).range([0, a]).clamp(!0);
        for (var b = this._colorDomain ? [0, 0.25, 0.5, 0.75, 1] : [0, 0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1], b = b.map(d3.scale.linear().domain([this._startTime,
            this._endTime]).invert), d = [], g = 0; g < b.length; g++) d[g] = new Date(b[g]);
        var b = d3.svg.axis().orient("bottom").scale(this._timeScale).tickSize(11, 0, 11).tickValues(d).tickFormat(function (a) {
            return "" //a.getFullYear()
        }), h = this._element.append("g").attr("transform", "translate(" + c + "," + e + ")"), f = this;
        h.append("g").classed("axis", !0).call(b);
        c = function () {
            return h.append("rect").attr("rx", 2).attr("ry", 2).attr("y", -1).attr("x", -3).attr("height", 6)
        };
        c().attr("width", a + 6).style("fill", "#fff");
        this._timeSlider = c().style("fill",
            "#ddd");
        c().attr("width", a + 6).style("fill", "none").style("stroke", "#888");
        this._timeSliderPosition = h.append("g");
        this._timeSliderPosition.append("line").attr("y2", -8).style("stroke", "#888");
        this._timeSliderPosition.append("text").attr("y", -10).attr("text-anchor", "middle");
        this._timeSliderHead = h.append("g").attr("pointer-events", "all").attr("cursor", "ew-resize");
        this._timeSliderHead.append("circle").attr("cy", 2).attr("r", 4).style("fill", "none").style("stroke", "#888").style("stroke-width", "5.5px");
        this._timeSliderHead.append("circle").attr("cy", 2).attr("r", 20).style("fill", "none").style("opacity", 1);
        this._timeSliderHead.style("display", "none");
        this._timeSliderHead.call(d3.behavior.drag().on("dragstart", function () {
            f._timeSliderDragged = !1
        }).on("drag", function () {
            f._timeSliderDragged = !0;
            f.stopTransition();
            var a = f._timeScale.invert(d3.event.x);
            f.update(a)
        }).on("dragend", function () {
            f._timeSliderDragged && 0 < f._endTime.getTime() - f._currentTime.getTime() && (f._timeSliderPlayButton.style("display", "block"),
                f._timeSliderHead.style("display", "none"))
        }));
        this._timeSliderPlayButton = h.append("g").attr("transform", "translate(0,2)").attr("pointer-events", "all").attr("cursor", "pointer");
        this._timeSliderPlayButton.append("circle").attr("cy", 0).attr("r", 6).style("fill", "#fff").style("stroke", "#888");
        this._timeSliderPlayButton.append("circle").attr("cy", 0).attr("r", 20).style("fill", "none").style("opacity", 1);
        this._timeSliderPlayButton.append("polygon").attr("points", "-2,-3 -2,3 4,0").style("fill", "#888");
        this._timeSliderPlayButton.on("click",
            function () {
                f.startTransition()
            })
    };
    b.prototype.updateTimeSlider = function (a) {
        var c = this._timeScale(a);
        this._timeSlider.attr("width", c + 6);
        this._timeSliderHead.attr("transform", "translate(" + c + ",0)");
        this._timeSliderPosition.attr("transform", "translate(" + c + ",0)");
        this._timeSliderPosition.selectAll("text").text(""); //getFullYear
        this._timeSliderPlayButton.attr("transform", "translate(" + c + ",2)");
        0 >= this._endTime.getTime() - a.getTime() && (this._timeSliderHead.style("display", "block"), this._timeSliderPlayButton.style("display",
            "none"))
    };
    b.prototype.createItems = function () {
        var a = this;
        this._items = this._diagram.append("g").selectAll(".item").data(this._dataSource).enter().append("g").classed("item", !0).each(function (c) {
            c = c[a._labelData];
            var b = d3.select(this);
            b.classed("selectedItem", a._selection[c]);
            b.append("text").classed("label", !0).attr("y", 1).text(c);
            b.append("circle")
        }).on("click", function () {
            d3.select(this).classed("selectedItem", !d3.select(this).classed("selectedItem"))
        });
        this.update(this._startTime)
    };
    b.prototype.computeDomain =
        function (a) {
            var c = this, b = !0;
            c._dataSource.forEach(function (c) {
                b = b && c[a] instanceof Array || "number" == typeof c[a]
            });
            if (!b) return null;
            var j = d3.min(this._dataSource, function (c) {
                return "number" == typeof c[a] ? c[a] : d3.min(c[a], function (a) {
                    return a[1]
                })
            }), d = d3.max(this._dataSource, function (c) {
                return "number" == typeof c[a] ? c[a] : d3.max(c[a], function (a) {
                    return a[1]
                })
            });
            c._dataSource.forEach(function (b) {
                if (b[a] instanceof Array) {
                    var e = b[a].map(function (a) {
                        return a[0]
                    }).map(function (a) {
                        return c.createDate(a)
                    }), d = b[a].map(function (a) {
                        return a[1]
                    });
                    b[a] = d3.time.scale().domain(e).range(d);
                    b[a].__min = e[0];
                    b[a].__max = e[e.length - 1]
                }
            });
            return [j, d]
        };
    b.prototype.createDate = function (a) {
        return "number" == typeof a ? new Date(a, 0, 1) : "string" == typeof a ? new Date(a) : a
    };
    b.prototype.computeTimeDomain = function () {
        var a = this, c = this._startTime, b = this._endTime;
        [a._xData, a._yData, a._radiusData, a._colorData].forEach(function (j) {
            a._dataSource.forEach(function (d) {
                d = d[j];
                "number" != typeof d && "string" != typeof d && d.domain().forEach(function (d) {
                    if (!a._startTime && (!c || c > d)) c =
                        d;
                    if (!a._endTime && (!b || b < d)) b = d
                })
            })
        });
        this._startTime = c;
        this._endTime = b
    };
    b.prototype.hasValue = function (a, c, b) {
        a = a[c];
        return "number" == typeof a || "string" == typeof a ? !0 : b >= a.__min && b <= a.__max
    };
    b.prototype.computeValue = function (a, c, b) {
        return (a = a[c]) && a.constructor && a.call && a.apply ? a(b) : a
    };
    b.prototype.update = function (a) {
        this._currentTime = a;
        this.updateTimeSlider(a);
        var c = this;
        this._items.each(function (b) {
            if (c.hasValue(b, c._xData, a) && c.hasValue(b, c._yData, a) && c.hasValue(b, c._radiusData, a)) {
                var j = c._xScale(c.computeValue(b,
                    c._xData, a)), d = c._yScale(c.computeValue(b, c._yData, a)),
                    g = c.computeValue(b, c._radiusData, a), g = c._radiusScale(0 > g ? 0 : g);
                b = c.hasValue(b, c._colorData, a) ? c._colorScale(c.computeValue(b, c._colorData, a)) : "#fff";
                var h = 1 + 1.1 * g;
                d3.select(this).style("display", "block");
                d3.select(this).attr("transform", "translate(" + j + "," + d + ")");
                d3.select(this).selectAll("circle").attr("r", g).style("fill", b);
                d3.select(this).selectAll("text").attr("transform", "translate(" + h + ",0)")
            } else d3.select(this).style("display", "none")
        });
        this._items.sort(function (a, b) {
            return b[c.radiusData] - a[c.radiusData]
        })
    };
    k.MotionChart = b
})(Grapher || (Grapher = {}));
var Grapher;
(function (k) {
    var b = function (a) {
        this._selection = {};
        this._radiusScale = d3.scale.sqrt();
        this._element = d3.select(a);
        this._margin = {top: 20, right: 20, bottom: 80, left: 40};
        this._width = this._element.attr("width") - this._margin.right - this._margin.left;
        this._height = this._element.attr("height") - this._margin.top - this._margin.bottom;
        this.xScale = d3.scale.linear();
        this.yScale = d3.scale.linear()
    };
    Object.defineProperty(b.prototype, "dataSource", {
        set: function (a) {
            this._dataSource = a
        }, enumerable: !0, configurable: !0
    });
    Object.defineProperty(b.prototype,
        "labelData", {
            set: function (a) {
                this._labelData = a
            }, enumerable: !0, configurable: !0
        });
    Object.defineProperty(b.prototype, "xData", {
        set: function (a) {
            this._xData = a
        }, enumerable: !0, configurable: !0
    });
    Object.defineProperty(b.prototype, "yData", {
        set: function (a) {
            this._yData = a
        }, enumerable: !0, configurable: !0
    });
    Object.defineProperty(b.prototype, "radiusData", {
        set: function (a) {
            this._radiusData = a
        }, enumerable: !0, configurable: !0
    });
    Object.defineProperty(b.prototype, "colorData", {
        set: function (a) {
            this._colorData = a
        }, enumerable: !0,
        configurable: !0
    });
    Object.defineProperty(b.prototype, "startTime", {
        set: function (a) {
            this._startTime = a
        }, enumerable: !0, configurable: !0
    });
    Object.defineProperty(b.prototype, "endTime", {
        set: function (a) {
            this._endTime = a
        }, enumerable: !0, configurable: !0
    });
    Object.defineProperty(b.prototype, "xScale", {
        set: function (a) {
            this._xScale = a;
            this._xAxis = d3.svg.axis().orient("bottom").scale(this._xScale)
        }, enumerable: !0, configurable: !0
    });
    Object.defineProperty(b.prototype, "yScale", {
        set: function (a) {
            this._yScale = a;
            this._yAxis = d3.svg.axis().orient("left").scale(this._yScale)
        },
        enumerable: !0, configurable: !0
    });
    Object.defineProperty(b.prototype, "colorScale", {
        set: function (a) {
            this._colorScale = a
        }, enumerable: !0, configurable: !0
    });
    Object.defineProperty(b.prototype, "xAxis", {
        get: function () {
            return this._xAxis
        }, enumerable: !0, configurable: !0
    });
    Object.defineProperty(b.prototype, "yAxis", {
        get: function () {
            return this._yAxis
        }, enumerable: !0, configurable: !0
    });
    b.prototype.select = function (a) {
        this._selection[a] = !0
    };
    b.prototype.startTransition = function () {
        this._diagram || this.draw();
        this._timeSliderPlayButton.style("display",
            "none");
        this._timeSliderHead.style("display", "block");
        var a = this._startTime.getTime(), c = this._endTime.getTime(), e = this._currentTime.getTime(),
            a = 2E4 * (c - e) / (c - a), b = d3.interpolate(this._currentTime, this._endTime), d = this;
        this._diagram.transition().duration(a).ease("linear").tween("date", function () {
            return function (a) {
                d.update(new Date(b(a)))
            }
        }).each("end", function () {
            d.stopTransition()
        })
    };
    b.prototype.stopTransition = function () {
        this._diagram.transition().duration(0)
    };
    b.prototype.draw = function () {
        this.createScales();
        this.createColorAxis();
        this.createRadiusAxis();
        this.createTimeSlider();
        this._diagram = this._element.append("g").attr("transform", "translate(" + this._margin.left + "," + this._margin.top + ")");
        this.createRules();
        this.createItems()
    };
    b.prototype.createScales = function () {
        var a = this.computeDomain(this._xData), c = this.computeDomain(this._yData);
        this._radiusDomain = this.computeDomain(this._radiusData);
        this._colorDomain = this.computeDomain(this._colorData);
        this.computeTimeDomain();
        a = this._xScale.domain(a).range([30,
            this._width - 30 - 40]);
        this._xScale = this._xScale.domain([a.invert(0), a.invert(this._width)]).range([0, this._width]).clamp(!0);
        c = this._yScale.domain(c).range([30, this._height - 30]);
        this._yScale = this._yScale.domain([c.invert(0), c.invert(this._height)]).range([this._height, 0]).clamp(!0);
        this._radiusScale = this._radiusScale.domain([0, this._radiusDomain[1]]).range([2, 20]).clamp(!0);
        if (this._colorDomain) {
            var a = [{stop: 0, color: "#3e53ff"}, {stop: 0.33, color: "#2ff076"}, {
                    stop: 0.5,
                    color: "#d0ff2f"
                }, {stop: 0.66, color: "#ffff2f"},
                    {stop: 1, color: "#ff2f2f"}],
                e = this._element.append("defs").append("linearGradient").attr("id", "colorGradient").attr("x2", "1");
            a.forEach(function (a) {
                e.append("stop").attr("offset", a.stop).attr("stop-color", a.color)
            });
            c = a.map(function (a) {
                return a.stop
            });
            a = a.map(function (a) {
                return a.color
            });
            this._colorScale = d3.scale.linear().domain(c.map(d3.scale.linear().domain(this._colorDomain).invert)).range(a)
        }
        this._colorScale || (this._colorScale = d3.scale.category10())
    };
    b.prototype.createRules = function () {
        var a = this._diagram.append("g").classed("rules",
            !0);
        a.append("g").classed("axis", !0).attr("transform", "translate(0," + this._height + ")").call(this.xAxis.tickSize(2, 0, 2));
        a.append("g").classed("axis", !0).call(this.yAxis.tickSize(2, 0, 2));
        a.append("g").classed("grid", !0).attr("transform", "translate(0," + this._height + ")").call(this.xAxis.tickSize(-this._height, 0, -this._height).tickFormat(function () {
            return ""
        }));
        a.append("g").classed("grid", !0).call(this.yAxis.tickSize(-this._width, 0, -this._width).tickFormat(function () {
            return ""
        }));
        a.selectAll(".grid line").filter(function (a) {
            return 0 ==
                a
        }).classed("origin", !0);
        a.append("text").attr("text-anchor", "end").attr("x", this._width - 3).attr("y", this._height - 6).text(this._xData);
        a.append("text").attr("text-anchor", "end").attr("x", "-3").attr("y", 11).attr("transform", "rotate(-90)").text(this._yData)
    };
    b.prototype.createColorAxis = function () {
        if (this._colorDomain) {
            var a = 0.25 * this._width, c = this._margin.left, e = Number(this._element.attr("height")) - 30,
                b = d3.scale.linear().domain(this._colorDomain).range([0, a]),
                d = [0, 0.5, 1].map(d3.scale.linear().domain(this._colorDomain).invert),
                b = d3.svg.axis().orient("bottom").scale(b).tickSize(2, 0, 2).tickValues(d),
                c = this._element.append("g").attr("transform", "translate(" + c + "," + e + ")");
            c.append("g").classed("axis", !0).attr("transform", "translate(0,9)").call(b);
            c.append("rect").attr("y", -3).attr("width", a).attr("height", 10).style("fill", "url(#colorGradient)");
            c.append("text").attr("text-anchor", "start").attr("dy", -8).text(this._colorData)
        }
    };
    b.prototype.createRadiusAxis = function () {
        var a = 0.25 * this._width, c = this._margin.left + (this._colorDomain ?
            0.32 * this._width : 0), e = Number(this._element.attr("height")) - 30,
            b = d3.scale.linear().domain([0, this._radiusDomain[1]]).range([0, a]),
            d = [0, 0.5, 1].map(d3.scale.linear().domain([0, this._radiusDomain[1]]).invert),
            b = d3.svg.axis().orient("bottom").scale(b).tickSize(2, 0, 2).tickValues(d),
            c = this._element.append("g").attr("transform", "translate(" + c + "," + e + ")");
        c.append("g").classed("axis", !0).attr("transform", "translate(0,9)").call(b);
        for (e = 0; 5 > e; e++) c.append("circle").attr("cx", e * a / 4).attr("cy", 2).attr("r", e + 1).style("fill",
            "#888");
        c.append("text").attr("text-anchor", "start").attr("dy", -8).text(this._radiusData)
    };
    b.prototype.createTimeSlider = function () {
        var a = this._width * (this._colorDomain ? 0.32 : 0.64),
            c = this._element.attr("width") - this._margin.right - a, e = Number(this._element.attr("height")) - 30;
        this._timeScale = d3.time.scale().domain([this._startTime, this._endTime]).range([0, a]).clamp(!0);
        for (var b = this._colorDomain ? [0, 0.25, 0.5, 0.75, 1] : [0, 0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1], b = b.map(d3.scale.linear().domain([this._startTime,
            this._endTime]).invert), d = [], g = 0; g < b.length; g++) d[g] = new Date(b[g]);
        var b = d3.svg.axis().orient("bottom").scale(this._timeScale).tickSize(11, 0, 11).tickValues(d).tickFormat(function (a) {
            return "" //a.getFullYear()
        }), h = this._element.append("g").attr("transform", "translate(" + c + "," + e + ")"), f = this;
        h.append("g").classed("axis", !0).call(b);
        c = function () {
            return h.append("rect").attr("rx", 2).attr("ry", 2).attr("y", -1).attr("x", -3).attr("height", 6)
        };
        c().attr("width", a + 6).style("fill", "#fff");
        this._timeSlider = c().style("fill",
            "#ddd");
        c().attr("width", a + 6).style("fill", "none").style("stroke", "#888");
        this._timeSliderPosition = h.append("g");
        this._timeSliderPosition.append("line").attr("y2", -8).style("stroke", "#888");
        this._timeSliderPosition.append("text").attr("y", -10).attr("text-anchor", "middle");
        this._timeSliderHead = h.append("g").attr("pointer-events", "all").attr("cursor", "ew-resize");
        this._timeSliderHead.append("circle").attr("cy", 2).attr("r", 4).style("fill", "none").style("stroke", "#888").style("stroke-width", "5.5px");
        this._timeSliderHead.append("circle").attr("cy", 2).attr("r", 20).style("fill", "none").style("opacity", 1);
        this._timeSliderHead.style("display", "none");
        this._timeSliderHead.call(d3.behavior.drag().on("dragstart", function () {
            f._timeSliderDragged = !1
        }).on("drag", function () {
            f._timeSliderDragged = !0;
            f.stopTransition();
            var a = f._timeScale.invert(d3.event.x);
            f.update(a)
        }).on("dragend", function () {
            f._timeSliderDragged && 0 < f._endTime.getTime() - f._currentTime.getTime() && (f._timeSliderPlayButton.style("display", "block"),
                f._timeSliderHead.style("display", "none"))
        }));
        this._timeSliderPlayButton = h.append("g").attr("transform", "translate(0,2)").attr("pointer-events", "all").attr("cursor", "pointer");
        this._timeSliderPlayButton.append("circle").attr("cy", 0).attr("r", 6).style("fill", "#fff").style("stroke", "#888");
        this._timeSliderPlayButton.append("circle").attr("cy", 0).attr("r", 20).style("fill", "none").style("opacity", 1);
        this._timeSliderPlayButton.append("polygon").attr("points", "-2,-3 -2,3 4,0").style("fill", "#888");
        this._timeSliderPlayButton.on("click",
            function () {
                f.startTransition()
            })
    };
    b.prototype.updateTimeSlider = function (a) {
        var c = this._timeScale(a);
        this._timeSlider.attr("width", c + 6);
        this._timeSliderHead.attr("transform", "translate(" + c + ",0)");
        this._timeSliderPosition.attr("transform", "translate(" + c + ",0)");
        this._timeSliderPosition.selectAll("text").text((a.getMonth() + 1) + "/" + (a.getDate()) + "/" + (a.getFullYear()));
        this._timeSliderPlayButton.attr("transform", "translate(" + c + ",2)");
        0 >= this._endTime.getTime() - a.getTime() && (this._timeSliderHead.style("display", "block"), this._timeSliderPlayButton.style("display",
            "none"))
    };
    b.prototype.createItems = function () {
        var a = this;
        this._items = this._diagram.append("g").selectAll(".item").data(this._dataSource).enter().append("g").classed("item", !0).each(function (c) {
            c = c[a._labelData];
            var b = d3.select(this);
            b.classed("selectedItem", a._selection[c]);
            b.append("text").classed("label", !0).attr("y", 1).text(c);
            b.append("circle")
        }).on("click", function () {
            d3.select(this).classed("selectedItem", !d3.select(this).classed("selectedItem"))
        });
        this.update(this._startTime)
    };
    b.prototype.computeDomain =
        function (a) {
            var c = this, b = !0;
            c._dataSource.forEach(function (c) {
                b = b && c[a] instanceof Array || "number" == typeof c[a]
            });
            if (!b) return null;
            var j = d3.min(this._dataSource, function (c) {
                return "number" == typeof c[a] ? c[a] : d3.min(c[a], function (a) {
                    return a[1]
                })
            }), d = d3.max(this._dataSource, function (c) {
                return "number" == typeof c[a] ? c[a] : d3.max(c[a], function (a) {
                    return a[1]
                })
            });
            c._dataSource.forEach(function (b) {
                if (b[a] instanceof Array) {
                    var e = b[a].map(function (a) {
                        return a[0]
                    }).map(function (a) {
                        return c.createDate(a)
                    }), d = b[a].map(function (a) {
                        return a[1]
                    });
                    b[a] = d3.time.scale().domain(e).range(d);
                    b[a].__min = e[0];
                    b[a].__max = e[e.length - 1]
                }
            });
            return [j, d]
        };
    b.prototype.createDate = function (a) {
        return "number" == typeof a ? new Date(a, 0, 1) : "string" == typeof a ? new Date(a) : a
    };
    b.prototype.computeTimeDomain = function () {
        var a = this, c = this._startTime, b = this._endTime;
        [a._xData, a._yData, a._radiusData, a._colorData].forEach(function (j) {
            a._dataSource.forEach(function (d) {
                d = d[j];
                "number" != typeof d && "string" != typeof d && d.domain().forEach(function (d) {
                    if (!a._startTime && (!c || c > d)) c =
                        d;
                    if (!a._endTime && (!b || b < d)) b = d
                })
            })
        });
        this._startTime = c;
        this._endTime = b
    };
    b.prototype.hasValue = function (a, c, b) {
        a = a[c];
        return "number" == typeof a || "string" == typeof a ? !0 : b >= a.__min && b <= a.__max
    };
    b.prototype.computeValue = function (a, c, b) {
        return (a = a[c]) && a.constructor && a.call && a.apply ? a(b) : a
    };
    b.prototype.update = function (a) {
        this._currentTime = a;
        this.updateTimeSlider(a);
        var c = this;
        this._items.each(function (b) {
            if (c.hasValue(b, c._xData, a) && c.hasValue(b, c._yData, a) && c.hasValue(b, c._radiusData, a)) {
                var j = c._xScale(c.computeValue(b,
                    c._xData, a)), d = c._yScale(c.computeValue(b, c._yData, a)),
                    g = c.computeValue(b, c._radiusData, a), g = c._radiusScale(0 > g ? 0 : g);
                b = c.hasValue(b, c._colorData, a) ? c._colorScale(c.computeValue(b, c._colorData, a)) : "#fff";
                var h = 1 + 1.1 * g;
                d3.select(this).style("display", "block");
                d3.select(this).attr("transform", "translate(" + j + "," + d + ")");
                d3.select(this).selectAll("circle").attr("r", g).style("fill", b);
                d3.select(this).selectAll("text").attr("transform", "translate(" + h + ",0)")
            } else d3.select(this).style("display", "none")
        });
        this._items.sort(function (a, b) {
            return b[c.radiusData] - a[c.radiusData]
        })
    };
    k.MotionChart = b
})(Grapher || (Grapher = {}));