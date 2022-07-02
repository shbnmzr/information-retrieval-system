let currentSearchMethod = "boolean";
const allowedSearchMethods = ["boolean", "ranked", "positional"];

async function doSearch(query) {
  url = "http://localhost:5000/boolean";
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
}

function changeSearchMethod(to = "boolean") {
  if (allowedSearchMethods.includes(to)) currentSearchMethod = to;
}
