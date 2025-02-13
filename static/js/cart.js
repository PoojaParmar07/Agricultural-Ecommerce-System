document.addEventListener("DOMContentLoaded", function () {
        
    document.querySelectorAll(".quantity-selector").forEach((selector) => {
        const quantityInput = selector.querySelector("input");
        const decreaseBtn = selector.querySelector(".decrease");
        const increaseBtn = selector.querySelector(".increase");
        const variantDropdown = document.getElementById("variant");
        const priceDisplay = document.getElementById("price-display");

        function adjustQuantity(amount) {
            let quantity = parseInt(quantityInput.value) || 1;
            quantity = Math.min(5, Math.max(1, quantity + amount)); // Limit between 1 and 5
            quantityInput.value = quantity;
            updatePrice(selector, quantity, units);
        }

        decreaseBtn.addEventListener("click", function () {
            adjustQuantity(-1);
        });

        increaseBtn.addEventListener("click", function () {
            adjustQuantity(1);
        });

    });
    
    function updatePrice(selector, quantity) {
        const priceElement = selector.closest("tr").querySelector("#price-display");
        const basePrice = parseFloat(priceElement.getAttribute("data-base-price")) || 0;
        priceElement.textContent = (basePrice * quantity).toFixed(2);
    }


     // Handle Variant Change
    // document.querySelectorAll("select").forEach((select) => {
    //     select.addEventListener("change", function () {
    //         const row = select.closest("tr");
    //         const quantity = parseInt(row.querySelector("#variant").value) || 1;
    //         updatePrice(row.querySelector(".quantity-selector"), quantity);
    //     });
    // });

    document.querySelector(".variant").foreach((selector)=>{
        const variantDropdown = document.getElementById("variant");
        const priceDisplay = document.getElementById("price-display");
 
        // variantDropdown.addEventListener("change", function () {
        //     const selectedVariant = variantDropdown.value;
        //     const variantPrice = parseFloat(variantDropdown.getAttribute("data-price")) || 0;
        //     priceDisplay.textContent = (variantPrice).toFixed(2);
        //     });
        
    });


    

});