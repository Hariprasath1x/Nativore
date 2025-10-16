async function getTrends() {
  const location = document.getElementById("location").value;
  const res = await fetch(`http://localhost:5000/trends/${location}`);
  const data = await res.json();

  const resultsDiv = document.getElementById("results");
  resultsDiv.innerHTML = "";

  if (data.length === 0) {
    resultsDiv.innerHTML = "<p>No data available for this location.</p>";
    return;
  }

  data.forEach(item => {
    const div = document.createElement("div");
    div.className = "trend-item";
    div.innerHTML = `<h3>${item.name}</h3>
                     <p>Trend: ${item.trend}</p>
                     <p>Average Spend: ${item.avgSpend}</p>`;
    resultsDiv.appendChild(div);
  });
}
