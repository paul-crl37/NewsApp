document.getElementById("newsForm").addEventListener("submit", async (e) => {
    e.preventDefault();
    const dateStart = document.getElementById("dateStart").value;
    const dateEnd = document.getElementById("dateEnd").value;
    const maxArticles = document.getElementById("maxArticles").value;

    const url = `http://127.0.0.1:8000/news/?date_start=${dateStart}&date_end=${dateEnd}&max_articles=${maxArticles}`;

    const res = await fetch(url);
    const data = await res.json();

    const container = document.getElementById("results");
    container.innerHTML = "";

    data.forEach(article => {
        const div = document.createElement("div");
        div.className = "article";
        div.innerHTML = `
            <h2>${article.title}</h2>
            <p>${article.summary}</p>
            <p><strong>Source :</strong> ${article.source} | <strong>Date :</strong> ${new Date(article.date).toLocaleDateString()}</p>
            <a href="${article.url}" target="_blank">Lire l'article</a>
        `;
        container.appendChild(div);
    });
});
