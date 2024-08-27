document.addEventListener('DOMContentLoaded', function () {
    const formSteps = document.querySelectorAll('.form-step');
    const nextBtns = document.querySelectorAll('.next-step');
    const prevBtns = document.querySelectorAll('.prev-step');
    let currentStep = 0;

    nextBtns.forEach((button) => {
        button.addEventListener('click', () => {
            formSteps[currentStep].classList.remove('active');
            currentStep++;
            formSteps[currentStep].classList.add('active');
        });
    });

    prevBtns.forEach((button) => {
        button.addEventListener('click', () => {
            formSteps[currentStep].classList.remove('active');
            currentStep--;
            formSteps[currentStep].classList.add('active');
        });
    });

    // Form submission handling can be added here if needed
    const form = document.getElementById('contactForm');
    form.addEventListener('submit', function (event) {
        event.preventDefault();
        // Add your form submission logic here (e.g., AJAX request)
        alert('Form submitted!');
    });
});