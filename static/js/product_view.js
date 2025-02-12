document.addEventListener("DOMContentLoaded", function () {
    const variantDropdown = document.getElementById("variant");
    const priceDisplay = document.getElementById("price-display");
    const quantityInput = document.getElementById("quantity");
    const decreaseBtn = document.querySelector(".decrease");
    const increaseBtn = document.querySelector(".increase");
    const starRatingContainer = document.getElementById("star-rating");
    const ratingInput = document.getElementById("rating-input");

    // ✅ Parse variant prices safely
    let variantPrices = {};

    try {
        let rawData = '{{ variant_prices|safe }}';  // Safe JSON output
        console.log("Raw Data from Django:", rawData);

        if (rawData && rawData.trim() !== "" && rawData.trim() !== "null" && rawData !== "{}") {
            variantPrices = JSON.parse(rawData);
        } else {
            console.warn("No variant prices found.");
        }
    } catch (error) {
        console.error("Error parsing variant prices:", error);
        variantPrices = {};
    }

    let selectedPrice = 0;

    // ✅ Function to update price display
    function updatePrice() {
        const quantity = parseInt(quantityInput.value) || 1;
        if (!isNaN(selectedPrice) && selectedPrice > 0) {
            priceDisplay.textContent = (selectedPrice * quantity).toFixed(2);
        } else {
            priceDisplay.textContent = "Select a variant";
        }
    }

    // ✅ Handle variant selection
    if (variantDropdown) {
        variantDropdown.addEventListener("change", function () {
            const selectedVariant = variantDropdown.value;
            console.log("Selected Variant:", selectedVariant);

            selectedPrice = variantPrices[selectedVariant.toString()] 
                ? parseFloat(variantPrices[selectedVariant.toString()]) 
                : 0;

            console.log("Selected Price:", selectedPrice);
            updatePrice();
        });

        // ✅ Set initial price if there's a preselected variant
        if (variantDropdown.value) {
            selectedPrice = variantPrices[variantDropdown.value.toString()] || 0;
            updatePrice();
        }
    }

    // ✅ Handle quantity changes
    function adjustQuantity(amount) {
        let quantity = parseInt(quantityInput.value) || 1;
        quantity = Math.max(1, quantity + amount);
        quantityInput.value = quantity;
        updatePrice();
    }

    if (decreaseBtn && increaseBtn && quantityInput) {
        decreaseBtn.addEventListener("click", function () {
            adjustQuantity(-1);
        });

        increaseBtn.addEventListener("click", function () {
            adjustQuantity(1);
        });
    }

    // ✅ Star rating system for review submission
    if (starRatingContainer && ratingInput) {
        starRatingContainer.addEventListener("click", function (event) {
            if (event.target.tagName === "SPAN" && event.target.dataset.value) {
                const stars = Array.from(starRatingContainer.children);
                const selectedValue = parseInt(event.target.dataset.value);

                stars.forEach((star, index) => {
                    star.classList.toggle("selected", index < selectedValue);
                });

                ratingInput.value = selectedValue;
            }
        });
    }
});
