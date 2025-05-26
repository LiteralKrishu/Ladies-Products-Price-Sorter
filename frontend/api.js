document.getElementById('searchForm').addEventListener('submit', async function (e) {
  e.preventDefault();

  const queryInput = document.getElementById('searchInput');
  const resultsDiv = document.getElementById('results');
  const query = queryInput.value.trim();
    
  if (!query) {
    resultsDiv.textContent = "Please enter a search term.";
    return;
  }

  resultsDiv.textContent = "Searching...";

  const apiUrl = `http://localhost:8000/search?query=${encodeURIComponent(query)}`;

  try {
    const response = await fetch(apiUrl);
    if (!response.ok) {
      throw new Error(`HTTP error! status: ${response.status}`);
    }

    const data = await response.json();

    if (!data || Object.keys(data).length === 0) {
      resultsDiv.textContent = "No results found.";
      return;
    }

    // Format and display result (assuming backend returns lowest price & platform & product_url)
    resultsDiv.innerHTML = `
      Lowest price for "<strong>${data.query}</strong>":<br>
      <span style="color: var(--primary); font-weight: 700;">
        ₹${data.lowest_price.replace(/[₹]/g, '')} on ${data.platform}
      </span><br>
      <a href="${data.product_url}" target="_blank" rel="noopener">View Product</a>
    `;
  } catch (error) {
    console.error("Fetch error:", error);
    resultsDiv.textContent = "Failed to fetch results. Please try again later.";
  }
});
