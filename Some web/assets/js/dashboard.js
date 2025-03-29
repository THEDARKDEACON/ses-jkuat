// Import API client
import api from './api.js';

// Dashboard JavaScript
document.addEventListener('DOMContentLoaded', function() {
    // Initialize Quill editor
    const quill = new Quill('#editor', {
        theme: 'snow',
        modules: {
            toolbar: [
                ['bold', 'italic', 'underline', 'strike'],
                ['blockquote', 'code-block'],
                [{ 'header': 1 }, { 'header': 2 }],
                [{ 'list': 'ordered'}, { 'list': 'bullet' }],
                [{ 'script': 'sub'}, { 'script': 'super' }],
                [{ 'indent': '-1'}, { 'indent': '+1' }],
                [{ 'direction': 'rtl' }],
                [{ 'size': ['small', false, 'large', 'huge'] }],
                [{ 'header': [1, 2, 3, 4, 5, 6, false] }],
                [{ 'color': [] }, { 'background': [] }],
                [{ 'font': [] }],
                [{ 'align': [] }],
                ['clean']
            ]
        }
    });

    // Sidebar toggle for mobile
    const menuToggle = document.querySelector('.menu-toggle');
    const sidebar = document.querySelector('.dashboard-sidebar');
    const mainContent = document.querySelector('.main-content');
    
    if (menuToggle) {
        menuToggle.addEventListener('click', () => {
            sidebar.classList.toggle('active');
            mainContent.classList.toggle('sidebar-active');
        });
    }

    // Close sidebar when clicking outside on mobile
    document.addEventListener('click', (e) => {
        if (window.innerWidth <= 768 && 
            !sidebar.contains(e.target) && 
            !menuToggle.contains(e.target)) {
            sidebar.classList.remove('active');
            mainContent.classList.remove('sidebar-active');
        }
    });

    // Dashboard section navigation
    const navLinks = document.querySelectorAll('.sidebar-nav a');
    const sections = document.querySelectorAll('.dashboard-section');

    navLinks.forEach(link => {
        link.addEventListener('click', (e) => {
            e.preventDefault();
            const target = link.getAttribute('href').substring(1);
            
            // Update active states
            navLinks.forEach(l => l.parentElement.classList.remove('active'));
            link.parentElement.classList.add('active');
            
            // Show target section
            sections.forEach(section => {
                section.classList.remove('active');
                if (section.id === target) {
                    section.classList.add('active');
                }
            });
        });
    });

    // Modal functionality
    const modal = document.querySelector('.modal');
    const closeModal = document.querySelector('.close-modal');
    const newPostBtn = document.querySelector('.new-post-btn');

    function openModal() {
        modal.classList.add('active');
        document.body.style.overflow = 'hidden';
    }

    function closeModalHandler() {
        modal.classList.remove('active');
        document.body.style.overflow = '';
    }

    if (newPostBtn) {
        newPostBtn.addEventListener('click', openModal);
    }

    if (closeModal) {
        closeModal.addEventListener('click', closeModalHandler);
    }

    // Close modal when clicking outside
    modal.addEventListener('click', (e) => {
        if (e.target === modal) {
            closeModalHandler();
        }
    });

    // Form submission
    const postForm = document.querySelector('#post-form');
    if (postForm) {
        postForm.addEventListener('submit', async (e) => {
            e.preventDefault();
            
            const formData = new FormData(postForm);
            formData.append('content', quill.root.innerHTML);
            
            try {
                const response = await api.createPost({
                    title: formData.get('title'),
                    category: formData.get('category'),
                    content: formData.get('content'),
                    image: formData.get('image')
                });
                
                // Add post to list
                addPostToList(response);
                
                // Close modal and reset form
                closeModalHandler();
                postForm.reset();
                quill.setContents([]);
            } catch (error) {
                alert('Error creating post: ' + error.message);
            }
        });
    }

    // Post list functionality
    const postList = document.querySelector('.post-list');

    async function loadPosts() {
        try {
            const posts = await api.getPosts();
            postList.innerHTML = '';
            posts.forEach(post => addPostToList(post));
        } catch (error) {
            console.error('Error loading posts:', error);
        }
    }

    function addPostToList(post) {
        const postElement = document.createElement('div');
        postElement.className = 'post-item';
        postElement.innerHTML = `
            <div class="post-image">
                <img src="${post.image_path || 'assets/images/placeholder.jpg'}" alt="${post.title}">
            </div>
            <div class="post-content">
                <h3>${post.title}</h3>
                <div class="post-meta">
                    <span class="category">${post.category}</span>
                    <span class="date">${new Date(post.created_at).toLocaleDateString()}</span>
                    <span class="author">${post.author}</span>
                </div>
                <div class="post-actions">
                    <button class="edit-post" data-id="${post.id}">
                        <i class="fas fa-edit"></i> Edit
                    </button>
                    <button class="delete-post" data-id="${post.id}">
                        <i class="fas fa-trash"></i> Delete
                    </button>
                </div>
            </div>
        `;
        
        postList.appendChild(postElement);
        
        // Add event listeners for edit and delete buttons
        const editBtn = postElement.querySelector('.edit-post');
        const deleteBtn = postElement.querySelector('.delete-post');
        
        editBtn.addEventListener('click', () => editPost(post.id));
        deleteBtn.addEventListener('click', () => deletePost(post.id));
    }

    async function editPost(postId) {
        try {
            const post = await api.getPost(postId);
            // Populate form with post data
            document.querySelector('#post-title').value = post.title;
            document.querySelector('#post-category').value = post.category;
            quill.root.innerHTML = post.content;
            
            // Update form to handle edit
            postForm.dataset.postId = postId;
            openModal();
        } catch (error) {
            alert('Error loading post: ' + error.message);
        }
    }

    async function deletePost(postId) {
        if (confirm('Are you sure you want to delete this post?')) {
            try {
                await api.deletePost(postId);
                const postElement = document.querySelector(`.post-item [data-id="${postId}"]`).closest('.post-item');
                postElement.remove();
            } catch (error) {
                alert('Error deleting post: ' + error.message);
            }
        }
    }

    // Search functionality
    const searchInput = document.querySelector('.search-box input');
    if (searchInput) {
        searchInput.addEventListener('input', (e) => {
            const searchTerm = e.target.value.toLowerCase();
            const posts = document.querySelectorAll('.post-item');
            
            posts.forEach(post => {
                const title = post.querySelector('h3').textContent.toLowerCase();
                const category = post.querySelector('.category').textContent.toLowerCase();
                const author = post.querySelector('.author').textContent.toLowerCase();
                
                if (title.includes(searchTerm) || category.includes(searchTerm) || author.includes(searchTerm)) {
                    post.style.display = 'flex';
                } else {
                    post.style.display = 'none';
                }
            });
        });
    }

    // Stats counter animation
    const stats = document.querySelectorAll('.stat-number');
    const observer = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                const target = entry.target;
                const value = parseInt(target.dataset.value);
                animateValue(target, 0, value, 2000);
                observer.unobserve(target);
            }
        });
    }, { threshold: 0.5 });

    stats.forEach(stat => observer.observe(stat));

    function animateValue(element, start, end, duration) {
        let startTimestamp = null;
        const step = (timestamp) => {
            if (!startTimestamp) startTimestamp = timestamp;
            const progress = Math.min((timestamp - startTimestamp) / duration, 1);
            element.textContent = Math.floor(progress * (end - start) + start);
            if (progress < 1) {
                window.requestAnimationFrame(step);
            }
        };
        window.requestAnimationFrame(step);
    }

    // Load initial data
    document.addEventListener('DOMContentLoaded', () => {
        loadPosts();
        loadStats();
    });

    // Load stats
    async function loadStats() {
        try {
            const stats = await api.getStats();
            document.querySelector('[data-stat="posts"]').dataset.value = stats.total_posts;
            document.querySelector('[data-stat="events"]').dataset.value = stats.total_events;
            document.querySelector('[data-stat="members"]').dataset.value = stats.total_users;
            document.querySelector('[data-stat="upcoming"]').dataset.value = stats.upcoming_events;
        } catch (error) {
            console.error('Error loading stats:', error);
        }
    }
}); 