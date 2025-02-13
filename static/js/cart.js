document.addEventListener("DOMContentLoaded", function () {
    const variantElement = document.getElementById("variant-data");

    if (!variantElement) {
        console.error("Error: Variant data element not found.");
    } else {
        let jsonData = variantElement.textContent.trim();

        if (!jsonData) {
            console.error("Error: JSON data is empty.");
        } else {
            try {
                const variantData = JSON.parse(jsonData); // Parsed variant prices
                console.log("Parsed Variant Data:", variantData);

                const cartItems = document.querySelectorAll("tr[data-cart-item]");
                const grandTotalEl = document.getElementById("grand-total");

                function updateGrandTotal() {
                    let total = 0;
                    document.querySelectorAll(".price-display").forEach(priceEl => {
                        total += parseFloat(priceEl.textContent);
                    });
                    grandTotalEl.textContent = total.toFixed(2);
                }

                cartItems.forEach(row => {
                    const cartItemId = row.getAttribute("data-cart-item");
                    const variantDropdown = row.querySelector(".variant-dropdown");
                    const priceDisplay = row.querySelector(".price-display");
                    const quantityInput = row.querySelector(".quantity");
                    const decreaseBtn = row.querySelector(".decrease");
                    const increaseBtn = row.querySelector(".increase");

                    function updatePrice() {
                        const selectedVariantId = variantDropdown.value;
                        const newPrice = variantData[selectedVariantId] || 0;
                        priceDisplay.textContent = (newPrice * parseInt(quantityInput.value)).toFixed(2);
                        updateGrandTotal();
                    }

                    // Update price when variant changes
                    variantDropdown.addEventListener("change", updatePrice);

                    // Increase quantity
                    increaseBtn.addEventListener("click", function () {
                        let qty = parseInt(quantityInput.value);
                        qty++;
                        quantityInput.value = qty;
                        updatePrice();
                    });

                    // Decrease quantity
                    decreaseBtn.addEventListener("click", function () {
                        let qty = parseInt(quantityInput.value);
                        if (qty > 1) {
                            qty--;
                            quantityInput.value = qty;
                            updatePrice();
                        }
                    });

                    updatePrice(); // Initial price calculation for each row
                });

                updateGrandTotal(); // Initial grand total calculation

            } catch (error) {
                console.error("Error parsing JSON:", error, "Raw JSON:", jsonData);
            }
        }
    }
});
