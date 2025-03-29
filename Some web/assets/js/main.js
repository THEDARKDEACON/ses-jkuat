// Utility Functions
const api = {
    async get(endpoint) {
        const response = await fetch(`/api/${endpoint}`);
        return response.json();
    },
    
    async post(endpoint, data) {
        const response = await fetch(`/api/${endpoint}`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(data)
        });
        return response.json();
    }
};

// Form handling
async function handleFormSubmit(event) {
    event.preventDefault();
    const form = event.target;
    const endpoint = form.dataset.endpoint;
    const redirectUrl = form.dataset.redirect;
    const submitButton = form.querySelector('.submit-button');
    
    try {
        // Show loading state
        submitButton.classList.add('loading');
        submitButton.disabled = true;
        
        // Collect form data
        const formData = new FormData(form);
        const data = Object.fromEntries(formData.entries());
        
        // Send request to backend
        const response = await fetch(`/api/${endpoint}`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify(data)
        });
        
        const result = await response.json();
        
        if (!response.ok) {
            throw new Error(result.message || 'An error occurred');
        }
        
        // Show success message
        showNotification('success', 'Success! Redirecting...');
        
        // Store auth token if provided
        if (result.token) {
            localStorage.setItem('authToken', result.token);
        }
        
        // Redirect after successful submission
        setTimeout(() => {
            window.location.href = redirectUrl;
        }, 1500);
        
    } catch (error) {
        showNotification('error', error.message);
        submitButton.classList.remove('loading');
        submitButton.disabled = false;
    }
}

// Notification system
function showNotification(type, message) {
    const notification = document.createElement('div');
    notification.className = `notification ${type}`;
    notification.textContent = message;
    
    document.body.appendChild(notification);
    
    // Trigger animation
    setTimeout(() => {
        notification.classList.add('show');
    }, 10);
    
    // Remove notification after delay
    setTimeout(() => {
        notification.classList.remove('show');
        setTimeout(() => {
            notification.remove();
        }, 300);
    }, 3000);
}

// Auth state management
function checkAuthState() {
    const authToken = localStorage.getItem('authToken');
    const protectedPages = ['/admin', '/dashboard'];
    const currentPath = window.location.pathname;
    
    if (protectedPages.some(page => currentPath.startsWith(page)) && !authToken) {
        window.location.href = '/login.html';
    }
}

// UI Components
const ui = {
    initializeNavigation() {
        const menuToggle = document.querySelector('.menu-toggle');
        const nav = document.querySelector('nav');
        
        if (menuToggle) {
            menuToggle.addEventListener('click', () => {
                nav.classList.toggle('active');
                menuToggle.classList.toggle('active');
            });
        }
    },
    
    initializeScrollProgress() {
        const progressBar = document.querySelector('.scroll-progress-bar');
        if (progressBar) {
            window.addEventListener('scroll', () => {
                const winScroll = document.body.scrollTop || document.documentElement.scrollTop;
                const height = document.documentElement.scrollHeight - document.documentElement.clientHeight;
                const scrolled = (winScroll / height) * 100;
                progressBar.style.width = scrolled + '%';
            });
        }
    },
    
    initializeAnimations() {
        const animatedElements = document.querySelectorAll('.animate-on-scroll');
        const observer = new IntersectionObserver((entries) => {
            entries.forEach(entry => {
                if (entry.isIntersecting) {
                    entry.target.classList.add('visible');
                }
            });
        });
        
        animatedElements.forEach(element => observer.observe(element));
    },
    
    initializeGallery() {
        const gallery = document.querySelector('.gallery-grid');
        if (gallery) {
            gallery.addEventListener('click', (e) => {
                const image = e.target.closest('.gallery-item');
                if (image) {
                    const modal = document.createElement('div');
                    modal.className = 'gallery-modal';
                    modal.innerHTML = `
                        <div class="modal-content">
                            <img src="${image.getAttribute('data-full')}" alt="${image.getAttribute('data-caption')}">
                            <p>${image.getAttribute('data-caption')}</p>
                        </div>
                    `;
                    document.body.appendChild(modal);
                    modal.addEventListener('click', () => modal.remove());
                }
            });
        }
    },
    
    initializeTestimonials() {
        const slider = document.querySelector('.testimonials-slider');
        if (slider) {
            let currentSlide = 0;
            const slides = slider.querySelectorAll('.testimonial');
            const totalSlides = slides.length;
            
            const showSlide = (index) => {
                slides.forEach((slide, i) => {
                    slide.style.transform = `translateX(${100 * (i - index)}%)`;
                });
            };
            
            setInterval(() => {
                currentSlide = (currentSlide + 1) % totalSlides;
                showSlide(currentSlide);
            }, 5000);
            
            showSlide(0);
        }
    }
};

// Event Handlers
const events = {
    async loadEvents() {
        try {
            const events = await api.get('events');
            const container = document.querySelector('.events-grid');
            if (container) {
                container.innerHTML = events.map(event => `
                    <div class="event-card animate-on-scroll">
                        <img src="${event.image_url}" alt="${event.title}">
                        <div class="event-content">
                            <h3>${event.title}</h3>
                            <p>${event.description}</p>
                            <time>${new Date(event.date).toLocaleDateString()}</time>
                        </div>
                    </div>
                `).join('');
            }
        } catch (error) {
            console.error('Error loading events:', error);
        }
    },
    
    async loadNews() {
        try {
            const news = await api.get('news');
            const container = document.querySelector('.news-grid');
            if (container) {
                container.innerHTML = news.map(post => `
                    <article class="news-card animate-on-scroll">
                        <img src="${post.image_url}" alt="${post.title}">
                        <div class="news-content">
                            <h3>${post.title}</h3>
                            <p>${post.content.substring(0, 150)}...</p>
                            <time>${new Date(post.created_at).toLocaleDateString()}</time>
                        </div>
                    </article>
                `).join('');
            }
        } catch (error) {
            console.error('Error loading news:', error);
        }
    }
};

// Initialize Everything
document.addEventListener('DOMContentLoaded', () => {
    // Initialize UI components
    ui.initializeNavigation();
    ui.initializeScrollProgress();
    ui.initializeAnimations();
    ui.initializeGallery();
    ui.initializeTestimonials();
    
    // Load dynamic content
    events.loadEvents();
    events.loadNews();
    
    // Initialize forms
    const forms = document.querySelectorAll('form[data-endpoint]');
    forms.forEach(form => {
        form.addEventListener('submit', handleFormSubmit);
    });
    
    // Check auth state
    checkAuthState();
    
    // Add input validation
    const inputs = document.querySelectorAll('input[required], select[required]');
    inputs.forEach(input => {
        input.addEventListener('blur', () => {
            if (input.value.trim() === '') {
                input.classList.add('invalid');
            } else {
                input.classList.remove('invalid');
            }
        });
    });
    
    // Initialize smooth scrolling
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

    // Gallery Filtering
    const filterButtons = document.querySelectorAll('.filter-btn');
    const galleryItems = document.querySelectorAll('.gallery-item');

    filterButtons.forEach(button => {
        button.addEventListener('click', () => {
            // Remove active class from all buttons
            filterButtons.forEach(btn => btn.classList.remove('active'));
            // Add active class to clicked button
            button.classList.add('active');

            const filterValue = button.getAttribute('data-filter');

            galleryItems.forEach(item => {
                if (filterValue === 'all' || item.getAttribute('data-category') === filterValue) {
                    item.style.display = 'block';
                    // Trigger animation
                    item.classList.add('visible');
                } else {
                    item.style.display = 'none';
                }
            });
        });
    });

    // Intersection Observer for gallery items
    const observerOptions = {
        threshold: 0.1,
        rootMargin: '0px 0px -50px 0px'
    };

    const observer = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                entry.target.classList.add('visible');
                observer.unobserve(entry.target);
            }
        });
    }, observerOptions);

    galleryItems.forEach(item => {
        observer.observe(item);
    });

    // Load More Functionality
    const loadMoreBtn = document.querySelector('.load-more button');
    if (loadMoreBtn) {
        loadMoreBtn.addEventListener('click', () => {
            // Simulate loading more items
            loadMoreBtn.classList.add('loading');
            setTimeout(() => {
                // Add more items here
                loadMoreBtn.classList.remove('loading');
            }, 1000);
        });
    }

    // Lazy Loading Images
    const lazyImages = document.querySelectorAll('img[data-src]');
    
    const imageObserver = new IntersectionObserver((entries, observer) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                const img = entry.target;
                img.src = img.dataset.src;
                img.classList.add('loaded');
                observer.unobserve(img);
            }
        });
    }, {
        rootMargin: '50px 0px',
        threshold: 0.1
    });

    lazyImages.forEach(img => {
        imageObserver.observe(img);
        // Add loading animation class
        img.classList.add('image-skeleton');
    });

    // Enhanced Animations
    const animateOnScroll = () => {
        const elements = document.querySelectorAll('.animate-on-scroll');
        
        const observer = new IntersectionObserver((entries) => {
            entries.forEach(entry => {
                if (entry.isIntersecting) {
                    entry.target.classList.add('animated');
                }
            });
        }, {
            threshold: 0.1
        });

        elements.forEach(element => {
            observer.observe(element);
        });
    };

    // Initialize animations
    animateOnScroll();

    // Smooth image transitions
    const enhanceImageTransitions = () => {
        const images = document.querySelectorAll('.gallery-image img, .team-image img, .activity-image img');
        
        images.forEach(img => {
            img.addEventListener('load', () => {
                img.classList.add('loaded');
            });
        });
    };

    enhanceImageTransitions();
});

// Logout functionality
function logout() {
    localStorage.removeItem('authToken');
    window.location.href = '/login.html';
}

// API utilities
async function fetchAPI(endpoint, options = {}) {
    const authToken = localStorage.getItem('authToken');
    
    const defaultOptions = {
        headers: {
            'Content-Type': 'application/json',
            ...(authToken ? { 'Authorization': `Bearer ${authToken}` } : {})
        }
    };
    
    try {
        const response = await fetch(`/api/${endpoint}`, {
            ...defaultOptions,
            ...options,
            headers: {
                ...defaultOptions.headers,
                ...options.headers
            }
        });
        
        const data = await response.json();
        
        if (!response.ok) {
            throw new Error(data.message || 'An error occurred');
        }
        
        return data;
    } catch (error) {
        showNotification('error', error.message);
        throw error;
    }
} 