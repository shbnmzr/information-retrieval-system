const $ = (s) => document.querySelector(s);
const $$ = (s) => document.querySelectorAll(s);

let currentSearchMethod = "boolean";
const allowedSearchMethods = ["boolean", "ranked", "positional"];
let lastQuerySumitted = null;

$$(".option").forEach((a) =>
  a.addEventListener("click", (e) => {
    $(".option.active")?.classList.remove("active");
    a.classList.add("active");
    currentSearchMethod = e.target.closest(".option").dataset.option;
  })
);

const resultsModal = document.getElementsByTagName("dialog")[0];

function countWords(str) {
  return str.split(" ").length;
}
async function doSearch(query) {
  const queryWordCount = countWords(query);
  if (!query) {
    return notify("Query cannot be empty");
  }

  if (["positional", "biword"].includes(currentSearchMethod)) {
    if (queryWordCount == 1) {
      return notify("Positional and Biword need at least two words!");
    }
  }

  url = "http://localhost:5000/" + currentSearchMethod;
  const rawResponse = await fetch(url, {
    method: "POST",
    headers: {
      Accept: "application/json",
      "Content-Type": "application/json",
    },
    body: JSON.stringify({ query }),
  });
  const content = await rawResponse.json();
  console.log(content);
  if (content.length == 0) {
    return notify("No results found!");
  }
  lastQuerySumitted = query;
  showResults(content);
}

function showResults(results) {
  while ($("#results").firstChild)
    $("#results").removeChild($("#results").firstChild);
  if (currentSearchMethod == "ranked") {
    showRankedResults(results);
  }
  if (["biword", "positional", "boolean"].includes(currentSearchMethod)) {
    showPositionalResults(results);
  }
}
function showPositionalResults(results) {
  const docs = results[0];
  const texts = results[1];
  const fragment = document.createDocumentFragment();
  docs.forEach((result) => {
    const resultEl = document.createElement("div");
    resultEl.classList.add("result");
    const heading = document.createElement("h1");
    const text = document.createElement("p");
    text.classList.add("text");
    text.innerHTML = highlightQuery(texts[result]);
    heading.innerText = `Document ID: ${result}`;
    resultEl.appendChild(heading);
    resultEl.appendChild(text);
    fragment.appendChild(resultEl);
  });
  $("#results").appendChild(fragment);
  resultsModal.showModal();
}
function showRankedResults(results) {
  const fragment = document.createDocumentFragment();
  results.forEach((result) => {
    const resultEl = document.createElement("div");
    resultEl.classList.add("result");
    const heading = document.createElement("h1");
    const text = document.createElement("p");
    text.classList.add("text");
    text.innerHTML = highlightQuery(result[2]);
    heading.innerText = `Document ID: ${result[0]}`;
    resultEl.appendChild(heading);
    resultEl.appendChild(text);
    fragment.appendChild(resultEl);
  });
  $("#results").appendChild(fragment);
  resultsModal.showModal();
}

function highlightQuery(phrase) {
  let result = phrase;
  lastQuerySumitted.split(" ").forEach((word) => {
    result = result.replace(` ${word} `, `<span class="hl">$&</span>`);
  });
  return result;
}

function changeSearchMethod(to = "boolean") {
  if (allowedSearchMethods.includes(to)) currentSearchMethod = to;
}
function closeModal(event) {
  const rect = resultsModal.getBoundingClientRect();
  const isInDialog =
    rect.top <= event.clientY &&
    event.clientY <= rect.top + rect.height &&
    rect.left <= event.clientX &&
    event.clientX <= rect.left + rect.width;
  if (!isInDialog) {
    results.close();
  }
}

function notify(message, color = "crimson") {
  const el = document.createElement("div");
  el.classList.add("alert");
  el.innerText = message;
  el.style.cssText = `
    background: ${color};
    position: fixed;
    left: 0;
    top: 0;
    width: 100%;
    height: 100%;
    font-size: 2rem;
    color: #fff;
    opacity: 0;
    display: grid;
    place-content: center
  `;
  document.body.appendChild(el);
  el.animate({ opacity: [0, 1] }, { duration: 300, fill: "forwards" });
  setTimeout(() => {
    el.animate({ opacity: [1, 0] }, { duration: 300, fill: "forwards" });
  }, 1500);
  setTimeout(() => {
    el.remove();
  }, 3000);
}

// Event Listeners
$("input").addEventListener("keydown", (e) => {
  if (e.code == "Enter") {
    doSearch(e.target.value);
  }
});
resultsModal.addEventListener("click", closeModal);
addEventListener("keydown", (e) => {
  if (e.code == "Escape") closeModal(e);
});
