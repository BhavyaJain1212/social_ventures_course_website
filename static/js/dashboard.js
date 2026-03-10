/**
 * Artisan Dashboard — Frontend JavaScript
 *
 * Handles:
 *   - Trend recommendation fetching and rendering
 *   - Design concept generation
 *   - Cascading dropdown loading (crafts → products → audiences)
 *   - Profile editing
 *   - Loading states and toast notifications
 */

// ─── Trend Recommendations ──────────────────────────────────────────────────

/**
 * Load product categories when a craft type is selected.
 */
async function loadProducts(craftKey) {
    const productSelect = document.getElementById("trendProduct");
    const audienceSelect = document.getElementById("trendAudience");

    // Reset downstream dropdowns
    productSelect.innerHTML = '<option value="">Loading...</option>';
    audienceSelect.innerHTML = '<option value="">Any audience</option>';

    if (!craftKey) {
        productSelect.innerHTML = '<option value="">Select product...</option>';
        return;
    }

    try {
        const response = await fetch(`/api/products/${craftKey}`);
        const data = await response.json();

        productSelect.innerHTML = '<option value="">Select product...</option>';
        if (data.success && data.products) {
            data.products.forEach((p) => {
                const option = document.createElement("option");
                option.value = p.key;
                option.textContent = p.label;
                productSelect.appendChild(option);
            });
        }
    } catch (err) {
        productSelect.innerHTML = '<option value="">Error loading products</option>';
        console.error("Failed to load products:", err);
    }
}

/**
 * Load target audiences when a product category is selected.
 */
async function loadAudiences() {
    const craftKey = document.getElementById("trendCraft").value;
    const productKey = document.getElementById("trendProduct").value;
    const audienceSelect = document.getElementById("trendAudience");

    audienceSelect.innerHTML = '<option value="">Any audience</option>';

    if (!craftKey || !productKey) return;

    try {
        const response = await fetch(`/api/audiences/${craftKey}/${productKey}`);
        const data = await response.json();

        if (data.success && data.audiences) {
            data.audiences.forEach((a) => {
                const option = document.createElement("option");
                option.value = a.key;
                option.textContent = a.label;
                audienceSelect.appendChild(option);
            });
        }
    } catch (err) {
        console.error("Failed to load audiences:", err);
    }
}

/**
 * Fetch trend recommendations from the API and render results.
 */
async function fetchTrends(event) {
    event.preventDefault();

    const form = document.getElementById("trendForm");
    const btn = document.getElementById("trendBtn");
    const resultsDiv = document.getElementById("trendResults");

    // Collect form data
    const formData = new FormData(form);
    const payload = {
        craft_type: formData.get("craft_type"),
        product_category: formData.get("product_category"),
        target_customer: formData.get("target_customer") || "",
        style_preference: formData.get("style_preference") || "",
    };

    // Show loading state
    btn.disabled = true;
    btn.innerHTML =
        '<span class="spinner-border spinner-border-sm me-2"></span>Exploring...';
    resultsDiv.style.display = "block";
    resultsDiv.innerHTML = `
        <div class="loading-overlay flex-column">
            <div class="spinner-artisan"></div>
            <div class="loading-text">Analyzing trends for your craft...</div>
        </div>
    `;

    try {
        const response = await fetch("/api/recommend-trends", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify(payload),
        });

        const data = await response.json();

        if (data.success) {
            renderTrendResults(data.recommendations);
        } else {
            resultsDiv.innerHTML = `
                <div class="alert alert-danger">
                    <i class="bi bi-exclamation-triangle me-2"></i>
                    ${data.error || "Failed to load recommendations."}
                </div>
            `;
        }
    } catch (err) {
        resultsDiv.innerHTML = `
            <div class="alert alert-danger">
                <i class="bi bi-wifi-off me-2"></i>
                Network error. Please check your connection and try again.
            </div>
        `;
        console.error("Trend fetch error:", err);
    } finally {
        btn.disabled = false;
        btn.innerHTML = '<i class="bi bi-search me-2"></i>Explore Trends';
    }
}

/**
 * Render trend recommendation results into the DOM.
 */
function renderTrendResults(rec) {
    const resultsDiv = document.getElementById("trendResults");

    // Build color swatches HTML
    const colorSwatches = (rec.trending_colors || [])
        .map(
            (c) => `
            <div class="color-swatch">
                <div class="swatch-circle" style="background-color: ${c.hex};"></div>
                <span class="swatch-name">${c.name}</span>
            </div>
        `
        )
        .join("");

    // Build motif list
    const motifList = (rec.trending_motifs || [])
        .map((m) => `<li>${m}</li>`)
        .join("");

    // Build product suggestions
    const productList = (rec.product_suggestions || [])
        .map((p) => `<li>${p}</li>`)
        .join("");

    // Build styling insights
    const insightList = (rec.styling_insights || [])
        .map((s) => `<li>${s}</li>`)
        .join("");

    // Style note (if present)
    const styleNote = rec.style_note
        ? `<div class="style-note"><i class="bi bi-palette2"></i>${rec.style_note}</div>`
        : "";

    resultsDiv.innerHTML = `
        <div class="trend-results-card">
            <div class="trend-header">
                <h5><i class="bi bi-graph-up-arrow me-2"></i>Trend Insights: ${rec.craft_type} — ${rec.product_category}</h5>
                <small class="text-muted">Target: ${rec.target_audience} · Source: ${rec.data_source}</small>
            </div>
            <div class="trend-body">
                <div class="trend-section-title">Trending Color Palette</div>
                <div class="color-swatches">${colorSwatches}</div>

                <div class="trend-section-title">Trending Motifs & Patterns</div>
                <ul class="trend-list">${motifList}</ul>

                <div class="trend-section-title">Product Format Suggestions</div>
                <ul class="trend-list">${productList}</ul>

                <div class="trend-section-title">Styling Insights</div>
                <ul class="trend-list">${insightList}</ul>

                ${rec.rationale ? `
                <div class="rationale-box">
                    <div class="trend-section-title" style="margin-top:0;">
                        <i class="bi bi-lightbulb me-1"></i>Why This Is Recommended
                    </div>
                    <p>${rec.rationale}</p>
                </div>
                ` : ""}

                ${styleNote}
            </div>
        </div>
    `;
}

// ─── Design Concept Generation ──────────────────────────────────────────────

/**
 * Generate a design concept from form inputs.
 */
async function generateDesign(event) {
    event.preventDefault();

    const form = document.getElementById("generateForm");
    const btn = document.getElementById("generateBtn");
    const resultsDiv = document.getElementById("generateResult");

    // Collect form data
    const formData = new FormData(form);
    const payload = {
        craft_type: formData.get("craft_type"),
        product_type: formData.get("product_type"),
        style: formData.get("style") || "contemporary",
        color_palette: formData.get("color_palette") || "",
        motif_direction: formData.get("motif_direction") || "",
        target_audience: formData.get("target_audience") || "",
    };

    // Show loading state
    btn.disabled = true;
    btn.innerHTML =
        '<span class="spinner-border spinner-border-sm me-2"></span>Generating...';
    resultsDiv.style.display = "block";
    resultsDiv.innerHTML = `
        <div class="loading-overlay flex-column">
            <div class="spinner-artisan"></div>
            <div class="loading-text">Crafting your design concept...</div>
        </div>
    `;

    try {
        const response = await fetch("/api/generate-design", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify(payload),
        });

        const data = await response.json();

        if (data.success) {
            renderDesignResult(data.concept);
            updateConceptCount();
        } else {
            resultsDiv.innerHTML = `
                <div class="alert alert-danger">
                    <i class="bi bi-exclamation-triangle me-2"></i>
                    ${data.error || "Failed to generate concept."}
                </div>
            `;
        }
    } catch (err) {
        resultsDiv.innerHTML = `
            <div class="alert alert-danger">
                <i class="bi bi-wifi-off me-2"></i>
                Network error. Please check your connection and try again.
            </div>
        `;
        console.error("Generate design error:", err);
    } finally {
        btn.disabled = false;
        btn.innerHTML = '<i class="bi bi-stars me-2"></i>Generate Concept';
    }
}

/**
 * Render the generated design concept into the DOM.
 */
function renderDesignResult(concept) {
    const resultsDiv = document.getElementById("generateResult");

    resultsDiv.innerHTML = `
        <div class="generate-result-card">
            <div class="generate-header">
                <h5><i class="bi bi-stars me-2"></i>${concept.title}</h5>
                <small class="text-muted">${concept.craft_type} · ${concept.product_type} · ${concept.style}</small>
            </div>

            <div class="concept-image-wrap">
                <img src="${concept.image_url}" alt="${concept.title}"
                     style="max-width: 400px;">
                <p class="text-muted mt-2 small">
                    <i class="bi bi-info-circle me-1"></i>
                    Mock concept preview — Connect a real image API for AI-generated visuals
                </p>
            </div>

            <div class="trend-body">
                <div class="trend-section-title">Concept Summary</div>
                <p class="text-muted">${concept.summary}</p>

                <div class="trend-section-title">Generated Prompt</div>
                <div class="prompt-display">${concept.prompt}</div>

                <div class="mt-3 d-flex gap-2">
                    <a href="/saved-concepts" class="btn btn-outline-warm btn-sm">
                        <i class="bi bi-bookmark-heart me-1"></i>View in Saved Ideas
                    </a>
                    <button class="btn btn-outline-warm btn-sm" onclick="copyPrompt('${encodeURIComponent(concept.prompt)}')">
                        <i class="bi bi-clipboard me-1"></i>Copy Prompt
                    </button>
                </div>
            </div>
        </div>
    `;
}

/**
 * Copy the generated prompt to clipboard.
 */
function copyPrompt(encodedPrompt) {
    const prompt = decodeURIComponent(encodedPrompt);
    navigator.clipboard
        .writeText(prompt)
        .then(() => showToast("Prompt copied to clipboard!", "success"))
        .catch(() => showToast("Failed to copy. Please select and copy manually.", "danger"));
}

// ─── Profile Editing ────────────────────────────────────────────────────────

/**
 * Toggle between profile view and edit modes.
 */
function toggleProfileEdit() {
    const view = document.getElementById("profileView");
    const edit = document.getElementById("profileEdit");
    const btn = document.getElementById("editProfileBtn");

    if (edit.style.display === "none") {
        view.style.display = "none";
        edit.style.display = "block";
        btn.innerHTML = '<i class="bi bi-x-lg me-1"></i>Cancel';
    } else {
        view.style.display = "block";
        edit.style.display = "none";
        btn.innerHTML = '<i class="bi bi-pencil me-1"></i>Edit';
    }
}

/**
 * Save the artisan profile (stretch feature).
 */
async function saveProfile(event) {
    event.preventDefault();

    const form = document.getElementById("profileForm");
    const formData = new FormData(form);
    const payload = Object.fromEntries(formData.entries());

    try {
        const response = await fetch("/api/profile", {
            method: "PUT",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify(payload),
        });

        const data = await response.json();

        if (data.success) {
            // Update the view mode with new values
            document.getElementById("profileName").textContent =
                payload.name || "";
            document.getElementById("profileCraft").textContent =
                payload.craft_type || "";
            document.getElementById("profileRegion").textContent =
                payload.region || "";
            document.getElementById("profileMaterials").textContent =
                payload.materials || "";
            document.getElementById("profileExperience").textContent =
                payload.experience || "";

            // Update welcome card
            const welcomeTitle = document.querySelector(".welcome-title .text-accent");
            if (welcomeTitle) welcomeTitle.textContent = payload.name || "Artisan";

            toggleProfileEdit();
            showToast("Profile updated successfully!", "success");
        } else {
            showToast(data.error || "Failed to update profile.", "danger");
        }
    } catch (err) {
        showToast("Network error. Please try again.", "danger");
        console.error("Profile save error:", err);
    }
}

// ─── Utility Functions ──────────────────────────────────────────────────────

/**
 * Update the concept count badge in the sidebar.
 */
function updateConceptCount() {
    const counter = document.getElementById("conceptCount");
    if (counter) {
        const current = parseInt(counter.textContent, 10) || 0;
        counter.textContent = current + 1;
    }
}

/**
 * Show a toast notification at the top of the page.
 */
function showToast(message, type = "info") {
    // Remove any existing toasts first
    document.querySelectorAll(".toast-notification").forEach((t) => t.remove());

    const toast = document.createElement("div");
    toast.className = `alert alert-${type} alert-dismissible fade show toast-notification`;
    toast.style.cssText =
        "position: fixed; top: 80px; right: 20px; z-index: 9999; " +
        "min-width: 300px; max-width: 450px; animation: fadeUp 0.3s ease;";
    toast.innerHTML = `
        ${message}
        <button type="button" class="btn-close" data-bs-dismiss="alert"></button>
    `;

    document.body.appendChild(toast);
    setTimeout(() => {
        toast.style.opacity = "0";
        toast.style.transition = "opacity 0.3s ease";
        setTimeout(() => toast.remove(), 300);
    }, 4000);
}

// ─── Sidebar Navigation Highlighting ────────────────────────────────────────

document.addEventListener("DOMContentLoaded", function () {
    // Smooth scroll for sidebar navigation links
    const sidebarLinks = document.querySelectorAll(".sidebar-link, .mobile-nav-pill");

    sidebarLinks.forEach((link) => {
        link.addEventListener("click", function (e) {
            const href = this.getAttribute("href");
            if (href && href.startsWith("#")) {
                e.preventDefault();
                const target = document.querySelector(href);
                if (target) {
                    target.scrollIntoView({ behavior: "smooth", block: "start" });

                    // Update active states
                    sidebarLinks.forEach((l) => l.classList.remove("active"));
                    // Activate matching links in both sidebar and mobile nav
                    document
                        .querySelectorAll(`[href="${href}"]`)
                        .forEach((l) => l.classList.add("active"));
                }
            }
        });
    });

    // Intersection Observer for auto-highlighting sidebar on scroll
    const sections = document.querySelectorAll(".dashboard-section");
    if (sections.length > 0) {
        const observer = new IntersectionObserver(
            (entries) => {
                entries.forEach((entry) => {
                    if (entry.isIntersecting) {
                        const id = entry.target.id;
                        sidebarLinks.forEach((link) => {
                            link.classList.toggle(
                                "active",
                                link.getAttribute("href") === `#${id}`
                            );
                        });
                    }
                });
            },
            { threshold: 0.3, rootMargin: "-80px 0px 0px 0px" }
        );

        sections.forEach((section) => observer.observe(section));
    }
});
