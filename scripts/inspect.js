const benchmarkFormat = new Intl.NumberFormat('en-US', { maximumFractionDigits: 1 });
const benchmarkMeasures = [
  ['stars', 'Stars'],
  ['contributors', 'Human contributors'],
  ['commits_90d', 'Commits in 90 days'],
];

function benchmarkData(peers, field, value) {
  const values = peers.map(p => p[field]).filter(Number.isFinite).sort((a, b) => a - b);
  const count = values.length;
  if (!count) return { count, median: null, percentile: null };
  const mid = Math.floor(count / 2);
  const median = count % 2 ? values[mid] : (values[mid - 1] + values[mid]) / 2;
  if (!Number.isFinite(value)) return { count, median, percentile: null };
  const lower = values.filter(n => n < value).length;
  const equal = values.filter(n => n === value).length;
  return { count, median, percentile: 100 * (lower + equal / 2) / count };
}

function measuredNumber(n) {
  return Number.isFinite(n) ? benchmarkFormat.format(n) : '—';
}

function percentileCell(rank) {
  const cell = node('td', measuredNumber(rank));
  if (rank === null) return cell;
  const scale = node('span');
  scale.className = 'percentile-scale';
  scale.setAttribute('aria-hidden', 'true');
  const marker = node('i');
  marker.style.left = rank + '%';
  scale.append(marker);
  cell.append(scale);
  return cell;
}

function inspectTable(columns) {
  const table = node('table');
  const head = table.createTHead().insertRow();
  for (const column of columns) {
    const th = node('th', column);
    th.scope = 'col';
    head.append(th);
  }
  return table;
}

function inspectProject(p) {
  const dialog = el('inspectDialog');
  const content = el('inspectContent');
  const title = node('h2', p.name);
  title.id = 'inspectTitle';
  const close = node('button', 'Close');
  close.type = 'button';
  close.onclick = () => dialog.close();
  const header = node('div');
  header.className = 'toolbar';
  header.append(title, close);
  const peers = projects.filter(other => other.category === p.category && other.repo !== p.repo);
  const category = catalog.categories[p.category] || p.category;
  const table = inspectTable(['Measure', 'Project', 'Peer median', 'Percentile', 'Measured peers']);
  const body = table.createTBody();
  for (const [field, label] of benchmarkMeasures) {
    const { count, median, percentile } = benchmarkData(peers, field, p[field]);
    const row = body.insertRow();
    const measure = node('th', label);
    measure.scope = 'row';
    row.append(measure, node('td', measuredNumber(p[field])), node('td', measuredNumber(median)),
      percentileCell(percentile), node('td', measuredNumber(count)));
  }
  const wrap = node('div');
  wrap.className = 'scroll';
  wrap.append(table);
  const note = node('p', 'Dots mark the project on a 0–100 percentile scale. The center tick marks 50. '
    + 'Percentile counts peers below the project and half of peers tied with it. Each measure uses peers with a recorded value.');
  note.className = 'note';
  const repository = link(p);
  repository.textContent = p.repo;
  content.replaceChildren(header, repository, node('h3', 'Category benchmarks'),
    node('p', category + ' · ' + peers.length + (peers.length === 1 ? ' other project' : ' other projects')), wrap, note);
  const issues = inspectTable(['Measure', 'Observation']);
  const issueBody = issues.createTBody();
  for (const [measure, value] of Object.entries(issueMeasures(p))) {
    const row = issueBody.insertRow();
    row.append(node('th', measure), node('td', value));
  }
  content.append(node('h3', 'Issue responsiveness'), issues, node('p',
    'The report sample takes up to six external reports aged 7–90 days from the 30 newest issues. Only human team replies count. The closure sample takes up to six recent closures. Timing medians require three observations.'));
  if (!dialog.open) dialog.showModal();
}

let maintenanceExpanded = false;

function drawMaintenance(hits) {
  const measured = hits.filter(p => Number.isFinite(p.top_author_share)).sort((a, b) =>
    b.top_author_share - a.top_author_share || (b.commits_all_time ?? -1) - (a.commits_all_time ?? -1)
      || a.repo.localeCompare(b.repo));
  const container = el('maintenanceContent');
  const note = node('p', measured.length + ' of ' + hits.length + ' matching projects have a measured top-author share. '
    + 'Share uses human contributions. Commit totals cover the entire default branch.');
  note.className = 'note';
  container.replaceChildren(note);
  if (!measured.length) return;
  const table = inspectTable(['Project', 'Top author share', 'Human contributors', 'Total commits']);
  const body = table.createTBody();
  for (const p of maintenanceExpanded ? measured : measured.slice(0, 8)) {
    const row = body.insertRow();
    const name = node('th');
    name.scope = 'row';
    name.append(link(p));
    row.append(name, node('td', measuredNumber(100 * p.top_author_share) + '%'),
      node('td', measuredNumber(p.contributors)), node('td', measuredNumber(p.commits_all_time)));
  }
  const wrap = node('div');
  wrap.className = 'scroll';
  wrap.append(table);
  container.append(wrap);
  if (measured.length > 8) {
    const more = node('button', maintenanceExpanded ? 'Show fewer' : 'Show all ' + measured.length + ' projects');
    more.type = 'button';
    more.setAttribute('aria-expanded', String(maintenanceExpanded));
    more.onclick = () => {
      maintenanceExpanded = !maintenanceExpanded;
      drawMaintenance(hits);
      container.querySelector('button')?.focus();
    };
    container.append(more);
  }
}

function issueMeasures(project) {
  const s = project.issues;
  const updated = project.fetched_at || '';
  function count(key, fallback) {
    if (s && s.date >= updated) return s[fallback];
    return project[key] ?? s?.[fallback] ?? '—';
  }
  const values = {
    'Open issues': count('open_issues', 'open'),
    'Closed issues': count('closed_issues', 'closed'),
    'Issue sample': s ? s.date : 'Awaiting sample',
    'External reports sampled (from up to 30 newest issues)': '—',
    'Maintainer reply within 7 days': '—',
    'Median first reply': '—',
    'Recent closures sampled': '—',
    'Median time to completed closure': '—'
  };
  if (!s) return values;
  if (!s.enabled) { values['Issue sample'] += ' · issues disabled'; return values; }
  values['External reports sampled (from up to 30 newest issues)'] = s.sampled
    ? s.sampled + ' sampled (max 6)'
    : '0 sampled · no eligible reports in this window';
  if (s.sampled) {
    values['Maintainer reply within 7 days'] =
      s.answered+' answered · '+s.unanswered+' unanswered · '+s.unknown+' unknown';
    const timingCount = s.timed_replies == null ? '' : ' (' + s.timed_replies + ' timed replies)';
    const replyMedian = s.reply_hours == null ? 'Fewer than 3 timed replies' : s.reply_hours + ' hours';
    values['Median first reply'] = replyMedian + timingCount;
  }
  const o=s.outcomes;
  values['Recent closures sampled'] = o.COMPLETED+' completed · '+o.NOT_PLANNED+' not planned · '+o.DUPLICATE+' duplicate · '+o.UNSPECIFIED+' unspecified';
  values['Median time to completed closure'] = s.completion_days == null
    ? 'Insufficient data (' + o.COMPLETED + ' completed, 3 required)'
    : s.completion_days + ' days (' + o.COMPLETED + ' completed)';
  return values;
}
