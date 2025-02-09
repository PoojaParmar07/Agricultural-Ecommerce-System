// document.querySelectorAll('.add-to-cart').forEach(button => {
//     button.addEventListener('click', function () {
//         let batchId = this.dataset.batchId;
//         let variantId = this.dataset.variantId;
//         let quantity = 1;  // Default quantity

//         fetch('/add-to-cart/', {
//             method: 'POST',
//             headers: {
//                 'Content-Type': 'application/json',
//                 'X-CSRFToken': getCSRFToken(),
//             },
//             body: JSON.stringify({ 
//                 product_batch_id: batchId, 
//                 product_variant_id: variantId, 
//                 quantity: quantity 
//             })
//         })
//         .then(response => response.json())
//         .then(data => {
//             if (data.success) {
//                 // Redirect to cart page after adding to cart
//                 window.location.href = '/cart/';
//             } else {
//                 alert('❌ ' + data.message);
//             }
//         })
//         .catch(error => console.error('Error:', error));
//     });
// });

// // Function to get CSRF token
// function getCSRFToken() {
//     let cookieValue = document.cookie.split('; ').find(row => row.startsWith('csrftoken='));
//     return cookieValue ? cookieValue.split('=')[1] : '';
// }
