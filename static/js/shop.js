/**
 * Artisan Shop — Mock preorder browsing experience.
 *
 * Loads product data from /api/products and renders responsive product cards.
 * Preorder actions only record mock interest with a visible notification.
 */

document.addEventListener("DOMContentLoaded", () => {
    loadShopProducts();
});

async function loadShopProducts() {
    const grid = document.getElementById("productGrid");
    const countPill = document.getElementById("shopProductCount");

    try {
        const response = await fetch("/api/products");
        const data = await response.json();

        if (!data.success || !Array.isArray(data.products)) {
            throw new Error(data.error || "Invalid product response");
        }

        renderProducts(data.products);
        if (countPill) {
            countPill.textContent = `${data.products.length} preorder products`;
        }
    } catch (err) {
        console.error("Failed to load shop products:", err);
        if (countPill) {
            countPill.textContent = "Catalog unavailable";
        }
        grid.innerHTML = `
            <div class="col-12">
                <div class="alert alert-danger">
                    <i class="bi bi-exclamation-triangle me-2"></i>
                    Could not load shop products. Please try again.
                </div>
            </div>
        `;
    }
}

function renderProducts(products) {
    const grid = document.getElementById("productGrid");

    grid.innerHTML = products.map((product) => `
        <div class="col-md-6 col-xl-3">
            <article class="card shop-product-card h-100">
                <div class="shop-product-image-wrap">
                    <img src="${escapeAttribute(product.image_url)}"
                         class="shop-product-image"
                         alt="${escapeAttribute(product.name)}">
                    <span class="shop-availability-badge ${availabilityClass(product.availability_status)}">
                        ${escapeHtml(product.availability_status)}
                    </span>
                </div>
                <div class="card-body d-flex flex-column">
                    <div class="shop-product-kicker">
                        <i class="bi bi-geo-alt me-1"></i>${escapeHtml(product.region)}
                    </div>
                    <h5 class="shop-product-title">${escapeHtml(product.name)}</h5>
                    <p class="shop-artisan-line">
                        by <strong>${escapeHtml(product.artisan_name)}</strong>
                    </p>
                    <div class="shop-craft-line">
                        <i class="bi bi-palette2 me-1"></i>${escapeHtml(product.craft_type)}
                    </div>
                    <p class="shop-product-description">${escapeHtml(product.short_description)}</p>
                    <div class="shop-tags">
                        ${(product.tags || []).map((tag) => `
                            <span>${escapeHtml(tag)}</span>
                        `).join("")}
                    </div>
                    <div class="shop-card-footer mt-auto">
                        <div>
                            <div class="shop-price">${formatPrice(product.price, product.currency)}</div>
                            <div class="shop-delivery">${escapeHtml(product.estimated_delivery)}</div>
                        </div>
                        <div class="shop-actions">
                            <button type="button"
                                    class="btn btn-accent btn-sm"
                                    onclick="recordPreorderInterest('${escapeAttribute(product.id)}')">
                                <i class="bi bi-bag-plus me-1"></i>Preorder
                            </button>
                            <button type="button"
                                    class="btn btn-outline-warm btn-sm"
                                    onclick="showProductDetails('${escapeAttribute(product.id)}')">
                                Details
                            </button>
                        </div>
                    </div>
                </div>
            </article>
        </div>
    `).join("");

    window.shopProductsById = Object.fromEntries(
        products.map((product) => [product.id, product])
    );
}

function recordPreorderInterest(productId) {
    const product = window.shopProductsById?.[productId];
    if (!product) return;

    showShopNotice(
        `Preorder interest recorded for ${escapeHtml(product.name)}. We'll notify you when checkout is available.`,
        "success"
    );
}

function showProductDetails(productId) {
    const product = window.shopProductsById?.[productId];
    if (!product) return;

    showShopNotice(
        `${escapeHtml(product.name)} is a mock listing for MVP browsing. Full product details will be available later.`,
        "info"
    );
}

function showShopNotice(message, type = "info") {
    const region = document.getElementById("shopAlertRegion");
    if (!region) return;

    region.innerHTML = `
        <div class="alert alert-${type} alert-dismissible fade show shop-alert" role="alert">
            ${message}
            <button type="button" class="btn-close" data-bs-dismiss="alert" aria-label="Close"></button>
        </div>
    `;
}

function availabilityClass(status = "") {
    const normalized = status.toLowerCase();
    if (normalized.includes("limited")) return "limited";
    if (normalized.includes("soon")) return "soon";
    return "open";
}

function formatPrice(price, currency) {
    try {
        return new Intl.NumberFormat("en-IN", {
            style: "currency",
            currency: currency || "INR",
            maximumFractionDigits: 0,
        }).format(price);
    } catch (err) {
        return `${escapeHtml(currency || "INR")} ${escapeHtml(String(price))}`;
    }
}

function escapeHtml(value = "") {
    return String(value)
        .replace(/&/g, "&amp;")
        .replace(/</g, "&lt;")
        .replace(/>/g, "&gt;")
        .replace(/"/g, "&quot;")
        .replace(/'/g, "&#039;");
}

function escapeAttribute(value = "") {
    return escapeHtml(value).replace(/`/g, "&#096;");
}
