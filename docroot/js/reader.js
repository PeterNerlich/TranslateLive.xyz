
const socketURL = `${location.protocol.replace('http','ws')}//${location.search.substr(1).split("&").includes('debug') ? location.hostname+':8765' : location.host+'/socket'}`;

const html = document.body.parentElement;
const connectionQuality = document.getElementById("connection-quality");
const history = document.getElementById("history");
const recognition = document.getElementById("recognition");

function updateLine(line) {
  let p = history.querySelector(`p[tid="${line.tid}"]`);
  if (p === null) {
    p = document.createElement('p');
    p.setAttribute("tid", line.tid);
    p.setAttribute("original", line.text);
    history.appendChild(p);
    p.innerText = line.text;

  } else {
    const original = p.getAttribute("original") || p.innerText;
    p.innerHTML = new Diff(original, line.text).html((x, tag) => {
      if (['insert', 'replace'].includes(tag)) {
        return x.replaceAll('\n', '⏎<br>');
      } else if (tag == 'delete') {
        return `<i>${x.replaceAll('\n', '⏎')}</i>`;
      } else {
        return x.replaceAll('\n', '<br>');
      }
    });
    p.querySelectorAll('.delete i').forEach(i => {
      i.parentElement.style.width = `calc(${.5 * i.scrollWidth}px - .1em)`;
    });
    p.setAttribute("tid", line.tid);
    p.classList.add("changed");
  }
  return p;
}
function sortLines(lines) {
  lines.forEach(line => {
    const p = history.querySelector(`p[tid="${line.tid}"]`);
    history.appendChild(p);
  });
}
const {calculateShouldScroll, scrollToBottom} = setupStickyScroll(document.body.parentElement);

const reader = new WebsocketReader(socketURL, "default", "uk");
const transcript = new Transcript(null, "uk");

logAll(reader, "reader", ["pong"]);

reader.subscribe("existing", msg => {
  const lines = JSON.parse(msg.lines);
  lines.forEach(transcript.addOrUpdateLine.bind(transcript));
  sortLines(transcript.linesSorted());
  scrollToBottom(html);
});
reader.subscribe(["new", "changed"], msg => {
  transcript.addOrUpdateLine(msg.line);
});

transcript.subscribe("new", line => {
  calculateShouldScroll();
  updateLine(line);
  //sortLines(transcript.linesSorted());
  scrollToBottom(html);
});
transcript.subscribe("changed", line => {
  calculateShouldScroll();
  updateLine(line);
  sortLines(transcript.linesSorted());
  scrollToBottom(html);
});

reader.connect();

reader.subscribe(["pong", "becomesUnhealthy"], () => {
  const ping = isNaN(reader.connectionCondition.pingAvg) ? "?" : Math.round(reader.connectionCondition.pingAvg);
  const classes = ["fast", "medium", "slow", "extremely-slow", "disconnected"];
  let current;
  if (reader.isHealthy()) {
    if (ping < 500) current = "fast";
    else if (ping < 1500) current = "medium";
    else if (ping < 3000) current = "slow";
    else current = "extremely-slow";
  } else {
    current = "disconnected";
  }
  connectionQuality.classList.add(current);
  connectionQuality.classList.remove.apply(connectionQuality.classList, classes.filter(c => c !== current));
  connectionQuality.querySelector('span').innerText = `${ping} ms`;
});

connectionQuality.addEventListener("click", e => {
  reader.connect();
});
