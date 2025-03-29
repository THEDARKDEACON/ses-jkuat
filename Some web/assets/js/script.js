document.getElementById('explore-btn').addEventListener('click', () => {
    alert('Explore the About page to learn more!');
});

document.getElementById('contact-form')?.addEventListener('submit', (e) => {
    e.preventDefault();
    alert('Thank you for your message!');
});

document.addEventListener('DOMContentLoaded', function() {
    // DOM Elements
    const scrollProgress = document.querySelector('.scroll-progress-bar');
    const hero = document.querySelector('.hero');
    const mainHeading = document.querySelector('.hero h1 span');
    const testimonials = document.querySelectorAll('.testimonial-card');
    const floatingElements = document.querySelectorAll('.feature-card, .team-card, .testimonial-card');
    const workCards = document.querySelectorAll('.work-card');

    // State variables
    let mouseX = 0;
    let mouseY = 0;
    let currentSlide = 0;
    let hue = 0;
    const totalSlides = testimonials.length;
    let isAnimating = false;

    // Mouse trail setup
    const trail = [];
    const trailLength = 20;
    for (let i = 0; i < trailLength; i++) {
        const dot = document.createElement('div');
        dot.className = 'mouse-trail';
        document.body.appendChild(dot);
        trail.push(dot);
    }

    // Mouse movement tracking
    window.addEventListener('mousemove', (e) => {
        mouseX = e.clientX;
        mouseY = e.clientY;
    });

    // Animation functions
    function updateTrail() {
        trail.forEach((dot, index) => {
            const scale = (trailLength - index) / trailLength;
            dot.style.left = `${mouseX}px`;
            dot.style.top = `${mouseY}px`;
            dot.style.transform = `scale(${scale})`;
            dot.style.opacity = scale * 0.5;
        });
        requestAnimationFrame(updateTrail);
    }

    function animateValue(element, start, end, duration) {
        const range = end - start;
        const increment = range / (duration / 16);
        let current = start;
        const timer = setInterval(() => {
            current += increment;
            if ((increment > 0 && current >= end) || (increment < 0 && current <= end)) {
                clearInterval(timer);
                current = end;
            }
            element.textContent = Math.round(current).toLocaleString();
        }, 16);
    }

    function showSlide(index) {
        if (isAnimating) return;
        isAnimating = true;

        testimonials.forEach((slide, i) => {
            slide.style.opacity = i === index ? '1' : '0';
            slide.style.transform = i === index ? 'translateX(0)' : 'translateX(100%)';
        });

        setTimeout(() => {
            isAnimating = false;
        }, 500);
    }

    function nextSlide() {
        currentSlide = (currentSlide + 1) % totalSlides;
        showSlide(currentSlide);
    }

    function prevSlide() {
        currentSlide = (currentSlide - 1 + totalSlides) % totalSlides;
        showSlide(currentSlide);
    }

    function isInViewport(element) {
        const rect = element.getBoundingClientRect();
        return (
            rect.top >= 0 &&
            rect.left >= 0 &&
            rect.bottom <= (window.innerHeight || document.documentElement.clientHeight) &&
            rect.right <= (window.innerWidth || document.documentElement.clientWidth)
        );
    }

    function handleScroll() {
        floatingElements.forEach(element => {
            if (isInViewport(element)) {
                element.style.transform = 'translateY(0)';
                element.style.opacity = '1';
            }
        });
    }

    function typeWriter(element, text, speed = 50) {
        let i = 0;
        element.textContent = '';
        function type() {
            if (i < text.length) {
                element.textContent += text.charAt(i);
                i++;
                setTimeout(type, speed);
            }
        }
        type();
    }

    function animateGradient() {
        hue = (hue + 1) % 360;
        hero.style.background = `linear-gradient(135deg, 
            hsl(${hue}, 50%, 95%) 0%, 
            hsl(${(hue + 60) % 360}, 50%, 90%) 100%)`;
        requestAnimationFrame(animateGradient);
    }

    // Enhanced work card hover effect
    workCards.forEach(card => {
        card.addEventListener('mousemove', (e) => {
            const rect = card.getBoundingClientRect();
            const x = e.clientX - rect.left;
            const y = e.clientY - rect.top;

            const centerX = rect.width / 2;
            const centerY = rect.height / 2;

            const angleX = (y - centerY) / 20;
            const angleY = (centerX - x) / 20;

            card.style.transform = `perspective(1000px) rotateX(${angleX}deg) rotateY(${angleY}deg) scale3d(1.02, 1.02, 1.02)`;
        });

        card.addEventListener('mouseleave', () => {
            card.style.transform = 'perspective(1000px) rotateX(0) rotateY(0) scale3d(1, 1, 1)';
        });
    });

    // Intersection Observer setup
    const observer = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                entry.target.classList.add('animate');
                const numberElement = entry.target.querySelector('.number');
                if (numberElement) {
                    const endValue = parseInt(numberElement.textContent.replace(/[^0-9]/g, ''));
                    animateValue(numberElement, 0, endValue, 2000);
                }
                observer.unobserve(entry.target);
            }
        });
    }, { threshold: 0.5 });

    // Event listeners
    window.addEventListener('scroll', () => {
        const scrollHeight = document.documentElement.scrollHeight - window.innerHeight;
        const scrolled = (window.scrollY / scrollHeight) * 100;
        scrollProgress.style.width = `${scrolled}%`;

        // Parallax effect for sections
        document.querySelectorAll('section').forEach(section => {
            const speed = section.dataset.parallax || 0.2;
            const yPos = -(window.scrollY * speed);
            section.style.backgroundPositionY = `${yPos}px`;
        });
    });

    // Smooth scrolling for anchor links
    document.querySelectorAll('a[href^="#"]').forEach(anchor => {
        anchor.addEventListener('click', function (e) {
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

    // Initialize animations and effects
    updateTrail();
    handleScroll();
    window.addEventListener('scroll', handleScroll);
    setInterval(nextSlide, 5000);

    // Add keyboard navigation for testimonials
    document.addEventListener('keydown', (e) => {
        if (e.key === 'ArrowLeft') prevSlide();
        if (e.key === 'ArrowRight') nextSlide();
    });

    // Observe elements for animation
    document.querySelectorAll('.feature-card, .team-card, .testimonial-card, .stat-item, .feature-stats').forEach(el => {
        observer.observe(el);
    });

    // Initialize typing effect
    if (mainHeading) {
        const originalText = mainHeading.textContent;
        typeWriter(mainHeading, originalText);
    }

    // Start background gradient animation
    animateGradient();

    // Intersection Observer for Fade-in Animations
    const observerOptions = {
        threshold: 0.1,
        rootMargin: '0px 0px -50px 0px'
    };

    const observerFadeIn = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                entry.target.classList.add('fade-in');
                observerFadeIn.unobserve(entry.target);
            }
        });
    }, observerOptions);

    // Add fade-in animation to elements
    document.querySelectorAll('.feature-card, .work-card, .team-card, .testimonial-card').forEach(el => {
        el.classList.add('animate-on-scroll');
        observerFadeIn.observe(el);
    });

    // Mobile Menu Toggle
    const menuBtn = document.querySelector('.menu-btn');
    const nav = document.querySelector('nav');

    if (menuBtn) {
        menuBtn.addEventListener('click', () => {
            nav.classList.toggle('active');
            menuBtn.classList.toggle('active');
        });
    }

    // Button Ripple Effect
    document.querySelectorAll('.btn').forEach(button => {
        button.addEventListener('click', function(e) {
            const x = e.clientX - e.target.offsetLeft;
            const y = e.clientY - e.target.offsetTop;

            const ripple = document.createElement('span');
            ripple.classList.add('ripple');
            ripple.style.left = `${x}px`;
            ripple.style.top = `${y}px`;

            this.appendChild(ripple);

            setTimeout(() => ripple.remove(), 600);
        });
    });

    // Floating Sidebar Visibility
    let lastScrollTop = 0;
    const floatingSidebar = document.querySelector('.floating-sidebar');

    window.addEventListener('scroll', () => {
        const scrollTop = window.pageYOffset || document.documentElement.scrollTop;
        
        if (scrollTop > lastScrollTop) {
            // Scrolling down
            floatingSidebar.style.transform = 'translateY(-50%) translateX(100%)';
        } else {
            // Scrolling up
            floatingSidebar.style.transform = 'translateY(-50%) translateX(0)';
        }
        
        lastScrollTop = scrollTop;
    });

    // Add hover effect to navigation links
    document.querySelectorAll('nav a').forEach(link => {
        link.addEventListener('mouseenter', function() {
            this.style.transform = 'translateY(-2px)';
        });
        
        link.addEventListener('mouseleave', function() {
            this.style.transform = 'translateY(0)';
        });
    });

    // Parallax effect for hero section
    window.addEventListener('scroll', () => {
        const scrolled = window.pageYOffset;
        hero.style.backgroundPositionY = `${scrolled * 0.5}px`;
    });

    // Add loading animation to buttons when clicked
    document.querySelectorAll('.btn').forEach(button => {
        button.addEventListener('click', function() {
            this.classList.add('loading');
            setTimeout(() => {
                this.classList.remove('loading');
            }, 2000);
        });
    });

    // Scroll Progress Bar
    const progressBar = document.createElement('div');
    progressBar.className = 'scroll-progress';
    document.body.appendChild(progressBar);

    window.addEventListener('scroll', () => {
        const winScroll = document.body.scrollTop || document.documentElement.scrollTop;
        const height = document.documentElement.scrollHeight - document.documentElement.clientHeight;
        const scrolled = (winScroll / height) * 100;
        progressBar.style.width = scrolled + '%';
    });

    // Smooth Scroll for Navigation Links
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

    // Intersection Observer for Scroll Animations
    const observerOptionsScroll = {
        root: null,
        rootMargin: '0px',
        threshold: 0.1
    };

    const observerScroll = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                entry.target.classList.add('fade-in');
                if (entry.target.classList.contains('animate-on-scroll')) {
                    observerScroll.unobserve(entry.target);
                }
            }
        });
    }, observerOptionsScroll);

    document.querySelectorAll('.animate-on-scroll').forEach(element => {
        observerScroll.observe(element);
    });

    // Testimonials Slider
    let currentSlideTestimonials = 0;
    const totalSlidesTestimonials = testimonials.length;

    function showSlideTestimonials(index) {
        testimonials.forEach((slide, i) => {
            slide.style.transform = `translateX(${100 * (i - index)}%)`;
        });
    }

    function nextSlideTestimonials() {
        currentSlideTestimonials = (currentSlideTestimonials + 1) % totalSlidesTestimonials;
        showSlideTestimonials(currentSlideTestimonials);
    }

    function prevSlideTestimonials() {
        currentSlideTestimonials = (currentSlideTestimonials - 1 + totalSlidesTestimonials) % totalSlidesTestimonials;
        showSlideTestimonials(currentSlideTestimonials);
    }

    // Auto advance slides
    setInterval(nextSlideTestimonials, 5000);
    showSlideTestimonials(0);

    // Mobile Menu Toggle
    const menuToggle = document.querySelector('.menu-toggle');
    const navTestimonials = document.querySelector('nav');

    if (menuToggle) {
        menuToggle.addEventListener('click', () => {
            navTestimonials.classList.toggle('active');
            menuToggle.classList.toggle('active');
        });
    }

    // Button Ripple Effect
    document.querySelectorAll('.btn, .cta-button').forEach(button => {
        button.addEventListener('click', function(e) {
            const ripple = document.createElement('span');
            ripple.className = 'ripple';
            this.appendChild(ripple);

            const rect = this.getBoundingClientRect();
            const size = Math.max(rect.width, rect.height);
            const x = e.clientX - rect.left - size / 2;
            const y = e.clientY - rect.top - size / 2;

            ripple.style.width = ripple.style.height = `${size}px`;
            ripple.style.left = `${x}px`;
            ripple.style.top = `${y}px`;

            setTimeout(() => ripple.remove(), 600);
        });
    });

    // Floating Sidebar
    let lastScrollTestimonials = 0;
    const floatingSidebarTestimonials = document.querySelector('.floating-sidebar');

    if (floatingSidebarTestimonials) {
        window.addEventListener('scroll', () => {
            const currentScrollTestimonials = window.pageYOffset;
            
            if (currentScrollTestimonials > lastScrollTestimonials && currentScrollTestimonials > 200) {
                floatingSidebarTestimonials.classList.add('hide');
            } else {
                floatingSidebarTestimonials.classList.remove('hide');
            }
            
            lastScrollTestimonials = currentScrollTestimonials;
        });
    }

    // Navigation Link Hover Effect
    document.querySelectorAll('nav a').forEach(link => {
        link.addEventListener('mouseenter', function() {
            this.classList.add('hover-scale');
        });
        
        link.addEventListener('mouseleave', function() {
            this.classList.remove('hover-scale');
        });
    });

    // Parallax Effect for Hero Section
    if (hero) {
        window.addEventListener('scroll', () => {
            const scrollTestimonials = window.pageYOffset;
            hero.style.backgroundPositionY = `${scrollTestimonials * 0.5}px`;
        });
    }

    // Loading Animation for Buttons
    document.querySelectorAll('.btn, .cta-button').forEach(button => {
        button.addEventListener('click', function() {
            if (!this.classList.contains('loading')) {
                const originalText = this.textContent;
                this.classList.add('loading');
                this.innerHTML = '<div class="loading-spinner"></div>';
                
                // Simulate loading (replace with actual loading if needed)
                setTimeout(() => {
                    this.classList.remove('loading');
                    this.textContent = originalText;
                }, 2000);
            }
        });
    });
});
