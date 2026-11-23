(() => {
  const host = document.getElementById("weeklyChanges");
  const weeks = JSON.parse(document.getElementById("catalog").textContent).history;
  const series = [
    ["added", "Added to the index", "#2d7258"],
    ["resumed", "Active again", "#946124"],
    ["released", "Projects with new releases", "#4a6796"]
  ];
  const day = stamp => stamp.slice(0, 10);
  const element = (tag, text, className) => {
    const node = document.createElement(tag);
    if (text !== undefined) node.textContent = text;
    if (className) node.className = className;
    return node;
  };
  const periods = weeks.filter(week => week.from);
  if (!periods.length) {
    host.append(element("p", weeks.length
      ? "The first snapshot was recorded on " + day(weeks[0].at) + ". Changes appear after the next weekly snapshot."
      : "Weekly snapshots begin with the next metrics refresh.", "note"));
    return;
  }
  const results = element("div");
  const label = element("label", "Snapshot comparison ");
  const select = element("select");
  for (const [i, week] of periods.entries()) {
    const option = element("option", day(week.from) + " → " + day(week.at));
    option.value = String(i);
    select.prepend(option);
  }
  select.value = String(periods.length - 1);
  label.append(select);
  host.append(label, results);
  const monday = stamp => {
    const date = new Date(stamp);
    return Date.UTC(date.getUTCFullYear(), date.getUTCMonth(), date.getUTCDate() - (date.getUTCDay() + 6) % 7);
  };
  function draw() {
    const index = Number(select.value);
    const week = periods[index];
    results.replaceChildren();
    const groups = element("div", undefined, "history-groups");
    groups.style.cssText = "display:flex;flex-wrap:wrap;gap:1rem;margin:.8rem 0;align-items:flex-start";
    let start = index + 1;
    while (start > 0 && monday(periods[start - 1].at) - monday(periods[start - 1].from) === 7 * 86400000) start--;
    const trend = periods.slice(start, index + 1);
    for (const [key, title, color] of series) {
      const rows = week[key];
      const group = element("div");
      group.style.cssText = "flex:1 1 12rem;min-width:0";
      if (trend.length >= 3) {
        const ns = "http://www.w3.org/2000/svg";
        const counts = trend.map(w => w[key].length);
        const max = Math.max(1, ...counts);
        const svg = document.createElementNS(ns, "svg");
        svg.setAttribute("viewBox", "0 0 120 32");
        svg.setAttribute("width", "120");
        svg.setAttribute("height", "32");
        svg.setAttribute("role", "img");
        svg.setAttribute("aria-label", title + " from " + day(trend[0].at) + " to " + day(week.at) + ": " + counts.join(", "));
        const line = document.createElementNS(ns, "polyline");
        line.setAttribute("points", counts.map((v, i) => (2 + i * 116 / (counts.length - 1)) + "," + (29 - v * 26 / max)).join(" "));
        line.setAttribute("fill", "none");
        line.setAttribute("stroke", color);
        line.setAttribute("stroke-width", "2.5");
        svg.append(line);
        group.append(svg);
      }
      const count = title + " (" + rows.length + ")";
      if (rows.length) {
        const details = element("details");
        const summary = element("summary", count);
        summary.style.cursor = "pointer";
        details.append(summary);
        const list = element("ul");
        list.style.cssText = "max-height:18rem;overflow:auto;padding-inline-start:1.3rem;overflow-wrap:anywhere";
        for (const repo of rows) {
          const item = element("li");
          const link = element("a", repo);
          link.href = "https://github.com/" + repo;
          item.append(link);
          list.append(item);
        }
        details.append(list);
        group.append(details);
      } else {
        group.append(element("span", count));
      }
      groups.append(group);
    }
    results.append(groups, element("p", "Active again counts projects returning from Recent, Slow or Stale to Active. Each project is counted once per period for its observed releases. Releases discovered on later refreshes are added to the period in which they were published.", "note"));
  }
  select.addEventListener("change", draw);
  draw();
})();
