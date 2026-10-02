// Papers-per-year stacked bar chart. Data: window.PUBS = [{year, main, small, collab}, ...]
// Large-collaboration papers (`collab`) would dwarf the rest, so they are only in the table.
(function () {
  var data = window.PUBS;
  var fig = document.getElementById("pubs-chart");
  if (!data || !fig) return;

  var SERIES = [
    { key: "main", label: "Major contribution", cls: "s1", color: "var(--series-1)" },
    { key: "small", label: "Other papers", cls: "s2", color: "var(--series-2)" },
  ].filter(function (s) {  // drop a series with no papers at all
    return data.some(function (d) { return d[s.key] > 0; });
  });
  var W = 760, H = 260, M = { top: 8, right: 4, bottom: 24, left: 28 };
  var GAP = 2; // surface gap between stacked segments
  var NS = "http://www.w3.org/2000/svg";
  var body = fig.querySelector(".chart-body");

  var max = Math.max.apply(null, data.map(function (d) { return d.main + d.small; })) || 1;
  var step = max > 20 ? 10 : max > 10 ? 5 : 2;
  var top = Math.ceil(max / step) * step;
  var iw = W - M.left - M.right, ih = H - M.top - M.bottom;
  var band = iw / data.length, bw = Math.min(36, band * 0.62);
  var y = function (v) { return M.top + ih - (v / top) * ih; };

  function el(name, attrs, parent) {
    var n = document.createElementNS(NS, name);
    for (var k in attrs) n.setAttribute(k, attrs[k]);
    if (parent) parent.appendChild(n);
    return n;
  }

  var svg = el("svg", { viewBox: "0 0 " + W + " " + H, role: "img",
    "aria-label": "Stacked bar chart of papers per year by type; the table below has the values." });

  for (var t = 0; t <= top; t += step) {
    el("line", { x1: M.left, x2: W - M.right, y1: y(t), y2: y(t), class: t === 0 ? "baseline" : "gridline" }, svg);
    var lbl = el("text", { x: M.left - 6, y: y(t) + 4, "text-anchor": "end" }, svg);
    lbl.textContent = t;
  }

  var every = data.length > 12 ? 2 : 1;
  var cols = [];
  data.forEach(function (d, i) {
    var cx = M.left + band * i + band / 2;
    var g = el("g", { class: "col" }, svg);
    var base = 0;
    var visible = SERIES.filter(function (s) { return d[s.key] > 0; });
    visible.forEach(function (s, j) {
      var v = d[s.key];
      var y0 = y(base), y1 = y(base + v);
      var isTop = j === visible.length - 1;
      var h = Math.max(0, y0 - y1 - (j > 0 ? GAP : 0));
      var yTop = y1;
      // Rounded 4px data-end on the top of the stack only; square elsewhere.
      var r = isTop ? Math.min(4, h / 2, bw / 2) : 0;
      var x0 = cx - bw / 2, x1 = cx + bw / 2, yb = yTop + h;
      var dPath = "M" + x0 + "," + yb + "V" + (yTop + r) +
        (r ? "Q" + x0 + "," + yTop + " " + (x0 + r) + "," + yTop : "") +
        "H" + (x1 - r) +
        (r ? "Q" + x1 + "," + yTop + " " + x1 + "," + (yTop + r) : "") +
        "V" + yb + "Z";
      el("path", { d: dPath, fill: s.color, class: "seg" }, g);
      base += v;
    });
    if (i % every === 0 || i === data.length - 1) {
      var tx = el("text", { x: cx, y: H - 6, "text-anchor": "middle" }, svg);
      tx.textContent = d.year;
    }
    // Hit target: the full column, wider than the bar.
    var hit = el("rect", { x: M.left + band * i, y: M.top, width: band, height: ih, class: "hit" }, g);
    cols.push(g);
    hit.addEventListener("mouseenter", function () { show(i, cx); });
    hit.addEventListener("mouseleave", hide);
  });
  body.appendChild(svg);

  var tip = document.createElement("div");
  tip.className = "tooltip";
  tip.hidden = true;
  fig.appendChild(tip);

  function show(i, cx) {
    var d = data[i];
    cols.forEach(function (c, j) { c.classList.toggle("dim", j !== i); });
    var total = d.main + d.small;
    tip.innerHTML = "<strong>" + d.year + " · " + total + " paper" + (total === 1 ? "" : "s") + "</strong>" +
      SERIES.map(function (s) {
        return '<div class="row"><i class="swatch ' + s.cls + '"></i>' + s.label + "<b>" + d[s.key] + "</b></div>";
      }).join("") +
      '<div class="row muted">+ collaboration papers<b>' + d.collab + "</b></div>";
    tip.hidden = false;
    var rect = svg.getBoundingClientRect(), frect = fig.getBoundingClientRect();
    var px = rect.left - frect.left + (cx / W) * rect.width;
    var left = px + 12;
    if (left + tip.offsetWidth > fig.clientWidth - 8) left = px - tip.offsetWidth - 12;
    tip.style.left = Math.max(8, left) + "px";
    tip.style.top = (rect.top - frect.top + 8) + "px";
  }
  function hide() {
    tip.hidden = true;
    cols.forEach(function (c) { c.classList.remove("dim"); });
  }
})();
