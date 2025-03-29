// Admin JavaScript

// Check if user is logged in
function checkAuth() {
    const isLoggedIn = localStorage.getItem('isLoggedIn');
    if (!isLoggedIn && !window.location.pathname.includes('login.html')) {
        window.location.href = 'login.html';
    }
}

// Handle login form submission
function handleLogin(e) {
    e.preventDefault();
    
    const username = document.getElementById('username').value;
    const password = document.getElementById('password').value;
    const remember = document.querySelector('input[name="remember"]').checked;

    // For demo purposes, using hardcoded credentials
    // In production, this should be handled securely with proper authentication
    if (username === 'admin' && password === 'admin123') {
        // Store login state
        localStorage.setItem('isLoggedIn', 'true');
        if (remember) {
            localStorage.setItem('rememberMe', 'true');
        }
        
        // Redirect to dashboard
        window.location.href = 'dashboard.html';
    } else {
        showError('Invalid username or password');
    }
}

// Handle logout
function handleLogout() {
    localStorage.removeItem('isLoggedIn');
    localStorage.removeItem('rememberMe');
    window.location.href = 'login.html';
}

// Show error message
function showError(message) {
    const errorDiv = document.createElement('div');
    errorDiv.className = 'error-message';
    errorDiv.textContent = message;
    
    const form = document.getElementById('loginForm');
    form.insertBefore(errorDiv, form.firstChild);
    
    setTimeout(() => {
        errorDiv.remove();
    }, 3000);
}

// Toggle mobile sidebar
function toggleSidebar() {
    const sidebar = document.querySelector('.admin-sidebar');
    sidebar.classList.toggle('active');
}

// Initialize dashboard
function initDashboard() {
    // Check authentication
    if (!localStorage.getItem('isLoggedIn')) {
        window.location.href = 'login.html';
        return;
    }

    // Initialize dashboard components
    const sidebar = document.querySelector('.sidebar');
    const mobileMenuBtn = document.querySelector('.mobile-menu-btn');
    
    if (mobileMenuBtn) {
        mobileMenuBtn.addEventListener('click', () => {
            sidebar.classList.toggle('active');
        });
    }

    // Handle logout
    const logoutBtn = document.querySelector('.logout-btn');
    if (logoutBtn) {
        logoutBtn.addEventListener('click', handleLogout);
    }

    // Initialize content management
    initContentManagement();
}

function initContentManagement() {
    // Add event listeners for content management actions
    const contentCards = document.querySelectorAll('.content-card');
    contentCards.forEach(card => {
        const editBtn = card.querySelector('.edit-btn');
        const deleteBtn = card.querySelector('.delete-btn');

        if (editBtn) {
            editBtn.addEventListener('click', () => handleEdit(card.dataset.id));
        }

        if (deleteBtn) {
            deleteBtn.addEventListener('click', () => handleDelete(card.dataset.id));
        }
    });
}

function handleEdit(contentId) {
    // Implement edit functionality
    console.log('Editing content:', contentId);
}

function handleDelete(contentId) {
    if (confirm('Are you sure you want to delete this item?')) {
        // Implement delete functionality
        console.log('Deleting content:', contentId);
    }
}

// Initialize based on current page
document.addEventListener('DOMContentLoaded', () => {
    // Check authentication on all admin pages except login
    if (!window.location.pathname.includes('login.html')) {
        checkAuth();
    }

    // Initialize login form if on login page
    const loginForm = document.getElementById('loginForm');
    if (loginForm) {
        loginForm.addEventListener('submit', handleLogin);
    }

    // Initialize dashboard if on dashboard page
    if (window.location.pathname.includes('dashboard.html')) {
        initDashboard();
    }

    // Add logout handler to logout link
    const logoutLink = document.querySelector('a[href="login.html"]');
    if (logoutLink) {
        logoutLink.addEventListener('click', (e) => {
            e.preventDefault();
            handleLogout();
        });
    }
}); 