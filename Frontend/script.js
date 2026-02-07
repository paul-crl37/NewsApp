document.getElementById("newsForm").addEventListener("submit", async (e) => {
    e.preventDefault();
    const dateStart = document.getElementById("dateStart").value;
    const dateEnd = document.getElementById("dateEnd").value;
    const maxArticles = document.getElementById("maxArticles").value;
    const typesSelect = document.getElementById("typesSelect");
    const sourcesSelect = document.getElementById("sourcesSelect");

    const params = new URLSearchParams();
    if (dateStart) params.set("date_start", dateStart);
    if (dateEnd) params.set("date_end", dateEnd);
    if (maxArticles) params.set("max_articles", maxArticles);

    const types = Array.from(typesSelect.selectedOptions).map((opt) => opt.value);
    const sources = Array.from(sourcesSelect.selectedOptions).map((opt) => opt.value);
    types.forEach((type) => params.append("types", type));
    sources.forEach((source) => params.append("sources", source));

    const url = `http://127.0.0.1:8000/news/?${params.toString()}`;

    const container = document.getElementById("results");
    container.innerHTML = "";
    try {
        const res = await fetch(url);
        if (!res.ok) {
            throw new Error(`Erreur API: ${res.status}`);
        }
        const data = await res.json();

        if (!data.length) {
            container.innerHTML = "<p class=\"error\">Aucun article trouvé pour ces filtres.</p>";
            return;
        }

        data.forEach((article) => {
            const div = document.createElement("div");
            div.className = "article";
            div.innerHTML = `
                <h2>${article.title}</h2>
                <p>${article.summary}</p>
                <p><strong>Source :</strong> ${article.source} | <strong>Date :</strong> ${new Date(article.date).toLocaleDateString()}</p>
                <a href="${article.url}" target="_blank" rel="noopener noreferrer">Lire l'article</a>
            `;
            container.appendChild(div);
        });
    } catch (error) {
        container.innerHTML = "<p class=\"error\">Impossible de récupérer les articles. Réessayez plus tard.</p>";
        console.error(error);
    }
});
