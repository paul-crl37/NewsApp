const API_BASE_URL = "http://127.0.0.1:8000";
const form = document.getElementById("newsForm");
const container = document.getElementById("results");
const dateStartInput = document.getElementById("dateStart");
const dateEndInput = document.getElementById("dateEnd");
const maxArticlesInput = document.getElementById("maxArticles");
const typesSelect = document.getElementById("typesSelect");
const sourcesSelect = document.getElementById("sourcesSelect");
const quickFigaroPolitique = document.getElementById("quickFigaroPolitique");
const quickReset = document.getElementById("quickReset");

const renderLoading = () => {
    container.innerHTML = "<div class=\"loading\">Chargement des articles en cours...</div>";
};

const renderError = (message) => {
    container.innerHTML = `<p class=\"error\">${message}</p>`;
};

const buildParams = () => {
    const params = new URLSearchParams();
    const dateStart = dateStartInput.value;
    const dateEnd = dateEndInput.value;
    const maxArticles = maxArticlesInput.value;

    if (dateStart) params.set("date_start", dateStart);
    if (dateEnd) params.set("date_end", dateEnd);
    if (maxArticles) params.set("max_articles", maxArticles);

    const types = Array.from(typesSelect.selectedOptions).map((opt) => opt.value);
    const sources = Array.from(sourcesSelect.selectedOptions).map((opt) => opt.value);
    types.forEach((type) => params.append("types", type));
    sources.forEach((source) => params.append("sources", source));
    return params;
};

const loadArticles = async () => {
    const params = buildParams();
    const url = `${API_BASE_URL}/news/?${params.toString()}`;

    renderLoading();
    try {
        const res = await fetch(url);
        if (!res.ok) {
            throw new Error(`Erreur API: ${res.status}`);
        }
        const data = await res.json();

        if (!data.length) {
            renderError("Aucun article trouvé pour ces filtres.");
            return;
        }

        container.innerHTML = "";
        data.forEach((article) => {
            const div = document.createElement("div");
            div.className = "article";
            div.innerHTML = `
                <div class="article-header">
                    <h2>${article.title}</h2>
                    <span class="badge">${article.type}</span>
                </div>
                <p>${article.summary}</p>
                <p class="meta"><strong>Source :</strong> ${article.source} | <strong>Date :</strong> ${new Date(article.date).toLocaleDateString()}</p>
                <a href="${article.url}" target="_blank" rel="noopener noreferrer">Lire l'article</a>
            `;
            container.appendChild(div);
        });
    } catch (error) {
        renderError("Impossible de récupérer les articles. Réessayez plus tard.");
        console.error(error);
    }
};

form.addEventListener("submit", async (e) => {
    e.preventDefault();
    await loadArticles();
});

document.getElementById("checkFeeds").addEventListener("click", async () => {
    const statusContainer = document.getElementById("feedsStatus");
    statusContainer.innerHTML = "<p>Vérification en cours...</p>";
    try {
        const res = await fetch(`${API_BASE_URL}/news/feeds/status`);
        if (!res.ok) {
            throw new Error(`Erreur API: ${res.status}`);
        }
        const data = await res.json();
        const feedsHtml = data.feeds.map((feed) => {
            const statusLabel = feed.ok ? "OK" : `Erreur - ${feed.error}`;
            return `
            <li class="${feed.ok ? "ok" : "error"}">
                <strong>${feed.source_name}</strong> (${feed.type}) :
                ${statusLabel}
                <a href="${feed.url}" target="_blank" rel="noopener noreferrer">Flux</a>
            </li>
        `;
        }).join("");
        const categoriesHtml = Object.entries(data.categories).map(([type, info]) => `
            <li class="${info.ok ? "ok" : "error"}">
                <strong>${type}</strong> : ${info.ok ? "OK" : "KO"}
            </li>
        `).join("");
        statusContainer.innerHTML = `
            <h2>Statut des catégories</h2>
            <ul>${categoriesHtml}</ul>
            <h2>Statut des flux</h2>
            <ul>${feedsHtml}</ul>
        `;
    } catch (error) {
        statusContainer.innerHTML = "<p class=\"error\">Impossible de vérifier les flux.</p>";
        console.error(error);
    }
});

quickFigaroPolitique.addEventListener("click", async () => {
    Array.from(typesSelect.options).forEach((option) => {
        option.selected = option.value === "politique";
    });
    Array.from(sourcesSelect.options).forEach((option) => {
        option.selected = option.value === "Le Figaro";
    });
    maxArticlesInput.value = "20";
    await loadArticles();
});

quickReset.addEventListener("click", () => {
    form.reset();
    Array.from(typesSelect.options).forEach((option) => {
        option.selected = false;
    });
    Array.from(sourcesSelect.options).forEach((option) => {
        option.selected = false;
    });
    container.innerHTML = "";
});
