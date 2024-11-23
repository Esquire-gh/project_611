document.addEventListener("DOMContentLoaded", function() {
    const form = document.querySelector(".input-form");
    const loadingOverlay = document.querySelector(".loading-overlay");

    form.addEventListener("submit", function(event) {
        event.preventDefault();
        loadingOverlay.style.display = "flex";

        form.submit();
    });

    const accordionHeaders = document.querySelectorAll('.accordion-header');

    accordionHeaders.forEach(header => {
        header.addEventListener('click', function() {
            // Get the clicked accordion's content
            const clickedContent = this.closest('.accordion-item').querySelector('.accordion-content');
            const clickedIcon = this.querySelector('.accordion-icon');
            
            // First, close all other accordions
            accordionHeaders.forEach(otherHeader => {
                if (otherHeader !== this) {
                    const otherContent = otherHeader.closest('.accordion-item').querySelector('.accordion-content');
                    const otherIcon = otherHeader.querySelector('.accordion-icon');
                    
                    // Hide other accordion contents
                    otherContent.classList.add('hidden');
                    // Reset other icons rotation
                    otherIcon.style.transform = 'rotate(0deg)';
                }
            });
            
            // Toggle the clicked accordion
            clickedContent.classList.toggle('hidden');
            
            // Rotate the clicked accordion's icon
            if (clickedContent.classList.contains('hidden')) {
                clickedIcon.style.transform = 'rotate(0deg)';
            } else {
                clickedIcon.style.transform = 'rotate(180deg)';
            }
        });
    });
});