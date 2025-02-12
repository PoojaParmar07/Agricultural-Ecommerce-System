document.addEventListener("DOMContentLoaded", function () {
    const variantDropdown = document.getElementById("variant");
    const priceDisplay = document.getElementById("price-display");
    const quantityInput = document.getElementById("quantity");
    const decreaseBtn = document.querySelector(".decrease");
    const increaseBtn = document.querySelector(".increase");
    const starRatingContainer = document.getElementById("star-rating");
    const ratingInput = document.getElementById("rating-input");

    let variantPrices = {};

    try {
        let rawData = document.getElementById("variant-data")?.textContent || "{}";
        variantPrices = JSON.parse(rawData.trim());
        if (typeof variantPrices === "string") {
            variantPrices = JSON.parse(variantPrices);
        }
    } catch (error) {
        console.error("Error parsing variant prices:", error.message);
    }

    function updatePrice() {
        if (!variantDropdown) return;

        const selectedVariant = (variantDropdown.value.trim()).toString();
        const quantity = parseInt(quantityInput?.value || 1, 10);

        if (!Object.prototype.hasOwnProperty.call(variantPrices, selectedVariant)) {
            priceDisplay.textContent = "Select a variant";
            return;
        }

        const selectedPrice = parseFloat(variantPrices[selectedVariant]);
        priceDisplay.textContent = (selectedPrice * quantity).toFixed(2);
    }

    function adjustQuantity(amount) {
        if (!quantityInput) return;
        let quantity = parseInt(quantityInput.value, 10) || 1;
        quantity = Math.max(1, quantity + amount);
        quantityInput.value = quantity;
        updatePrice();
    }

    variantDropdown?.addEventListener("change", updatePrice);
    decreaseBtn?.addEventListener("click", () => adjustQuantity(-1));
    increaseBtn?.addEventListener("click", () => adjustQuantity(1));

    if (variantDropdown?.value) {
        updatePrice();
    }

    if (starRatingContainer && ratingInput) {
        starRatingContainer.addEventListener("click", function (event) {
            if (event.target.tagName === "SPAN" && event.target.dataset.value) {
                const selectedValue = parseInt(event.target.dataset.value, 10);
                [...starRatingContainer.children].forEach((star, index) => {
                    star.classList.toggle("selected", index < selectedValue);
                });
                ratingInput.value = selectedValue;
            }
        });
    }
});
