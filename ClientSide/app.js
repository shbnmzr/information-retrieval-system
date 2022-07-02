const $ = (s) => document.querySelector(s);
const $$ = (s) => document.querySelectorAll(s);

let currentSearchMethod = "boolean";
const allowedSearchMethods = ["boolean", "ranked", "positional"];

$$(".option").forEach((a) =>
  a.addEventListener("click", (e) => {
    $(".option.active")?.classList.remove("active");
    a.classList.add("active");
    currentSearchMethod = e.target.closest(".option").dataset.option;
  })
);

const results = document.getElementsByTagName("dialog")[0];

function countWords(str) {
  return str.split(" ").length;
}
async function doSearch(query) {
  const queryWordCount = countWords(query);
  if (!query) {
    return notify("Query cannot be empty");
  }

  if (["positional"].includes(currentSearchMethod)) {
    if (queryWordCount == 1) {
      return notify("Positional retrieval needs at least two words!");
    }
  }

  results.showModal();
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
  if (content.length == 0) {
    notify("No results found!");
  }
}

function changeSearchMethod(to = "boolean") {
  if (allowedSearchMethods.includes(to)) currentSearchMethod = to;
}
function closeModal(event) {
  const rect = results.getBoundingClientRect();
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
results.addEventListener("click", closeModal);
addEventListener("keydown", (e) => {
  if (e.code == "Escape") closeModal(e);
});
