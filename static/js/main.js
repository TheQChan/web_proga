document.addEventListener('DOMContentLoaded', function() {
    // Анимация появления элементов при скролле
    const animateOnScroll = () => {
        const elements = document.querySelectorAll('.animate__animated:not(.animate__fadeIn)');
        elements.forEach(element => {
            const elementTop = element.getBoundingClientRect().top;
            const elementBottom = element.getBoundingClientRect().bottom;
            
            if (elementTop < window.innerHeight && elementBottom > 0) {
                element.classList.add('animate__fadeIn');
            }
        });
    };

    window.addEventListener('scroll', animateOnScroll);
    animateOnScroll();

    // Плавный скролл для якорных ссылок
    document.querySelectorAll('a[href^="#"]').forEach(anchor => {
        anchor.addEventListener('click', function(e) {
            e.preventDefault();
            const target = document.querySelector(this.getAttribute('href'));
            if (target) {
                target.scrollIntoView({
                    behavior: 'smooth',
                    block: 'start'
                });
            }
        });
    });

    // Анимация карточек фильмов при наведении
    const movieCards = document.querySelectorAll('.movie-card');
    movieCards.forEach(card => {
        card.addEventListener('mouseenter', function() {
            this.style.transform = 'translateY(-10px)';
            this.style.transition = 'transform 0.3s ease';
        });

        card.addEventListener('mouseleave', function() {
            this.style.transform = 'translateY(0)';
        });
    });

    // Горизонтальный скролл для популярных фильмов
    const moviesSlider = document.querySelector('.movies-slider');
    if (moviesSlider) {
        let isDown = false;
        let startX;
        let scrollLeft;

        moviesSlider.addEventListener('mousedown', (e) => {
            isDown = true;
            startX = e.pageX - moviesSlider.offsetLeft;
            scrollLeft = moviesSlider.scrollLeft;
        });

        moviesSlider.addEventListener('mouseleave', () => {
            isDown = false;
        });

        moviesSlider.addEventListener('mouseup', () => {
            isDown = false;
        });

        moviesSlider.addEventListener('mousemove', (e) => {
            if (!isDown) return;
            e.preventDefault();
            const x = e.pageX - moviesSlider.offsetLeft;
            const walk = (x - startX) * 2;
            moviesSlider.scrollLeft = scrollLeft - walk;
        });
    }

    // Валидация форм
    const forms = document.querySelectorAll('form');
    forms.forEach(form => {
        form.addEventListener('submit', function(e) {
            const requiredFields = form.querySelectorAll('[required]');
            let isValid = true;

            requiredFields.forEach(field => {
                if (!field.value.trim()) {
                    isValid = false;
                    field.classList.add('is-invalid');
                } else {
                    field.classList.remove('is-invalid');
                }
            });

            if (!isValid) {
                e.preventDefault();
            }
        });
    });
}); 