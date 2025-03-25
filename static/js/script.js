// Wait for the DOM to be fully loaded
document.addEventListener('DOMContentLoaded', function() {
    // Initialize Bootstrap tooltips
    var tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'));
    var tooltipList = tooltipTriggerList.map(function (tooltipTriggerEl) {
        return new bootstrap.Tooltip(tooltipTriggerEl);
    });

    // Handle quantity inputs in cart
    setupQuantityInputs();

    // Rating input handling
    setupRatingInputs();
});

// Handle quantity inputs in cart
function setupQuantityInputs() {
    const quantityInputs = document.querySelectorAll('.cart-quantity-input');
    
    if (quantityInputs.length) {
        quantityInputs.forEach(input => {
            input.addEventListener('change', function() {
                const form = this.closest('form');
                if (form) {
                    form.submit();
                }
            });
        });
    }
}

// Rating input handling for reviews
function setupRatingInputs() {
    const ratingInput = document.getElementById('rating-input');
    const stars = document.querySelectorAll('.rating-select .star');
    
    if (ratingInput && stars.length) {
        stars.forEach(star => {
            star.addEventListener('click', function() {
                const value = parseInt(this.dataset.value);
                ratingInput.value = value;
                
                // Update visual state
                stars.forEach(s => {
                    if (parseInt(s.dataset.value) <= value) {
                        s.classList.add('selected');
                    } else {
                        s.classList.remove('selected');
                    }
                });
            });
            
            // Hover effects
            star.addEventListener('mouseenter', function() {
                const value = parseInt(this.dataset.value);
                stars.forEach(s => {
                    if (parseInt(s.dataset.value) <= value) {
                        s.classList.add('hover');
                    } else {
                        s.classList.remove('hover');
                    }
                });
            });
        });
        
        // Remove hover effects when leaving the container
        document.querySelector('.rating-select').addEventListener('mouseleave', function() {
            stars.forEach(s => s.classList.remove('hover'));
        });
    }
}

// Format currency
function formatCurrency(amount) {
    return '$' + parseFloat(amount).toFixed(2);
}

// Get CSRF token from cookies - needed for AJAX POST requests
function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
} 