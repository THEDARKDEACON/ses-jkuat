// API Configuration
const API_BASE_URL = 'http://localhost:5000/api';

// API Client Class
class ApiClient {
    constructor() {
        this.token = localStorage.getItem('token');
    }

    // Set authentication token
    setToken(token) {
        this.token = token;
        localStorage.setItem('token', token);
    }

    // Clear authentication token
    clearToken() {
        this.token = null;
        localStorage.removeItem('token');
    }

    // Get headers for API requests
    getHeaders() {
        const headers = {
            'Content-Type': 'application/json'
        };
        if (this.token) {
            headers['Authorization'] = `Bearer ${this.token}`;
        }
        return headers;
    }

    // Authentication methods
    async login(username, password) {
        try {
            const response = await fetch(`${API_BASE_URL}/auth/login`, {
                method: 'POST',
                headers: this.getHeaders(),
                body: JSON.stringify({ username, password })
            });
            const data = await response.json();
            if (response.ok) {
                this.setToken(data.access_token);
                return data;
            }
            throw new Error(data.error);
        } catch (error) {
            throw error;
        }
    }

    async register(userData) {
        try {
            const response = await fetch(`${API_BASE_URL}/auth/register`, {
                method: 'POST',
                headers: this.getHeaders(),
                body: JSON.stringify(userData)
            });
            const data = await response.json();
            if (response.ok) {
                return data;
            }
            throw new Error(data.error);
        } catch (error) {
            throw error;
        }
    }

    // Post methods
    async getPosts() {
        try {
            const response = await fetch(`${API_BASE_URL}/posts`, {
                headers: this.getHeaders()
            });
            const data = await response.json();
            if (response.ok) {
                return data;
            }
            throw new Error(data.error);
        } catch (error) {
            throw error;
        }
    }

    async createPost(postData) {
        try {
            const formData = new FormData();
            Object.keys(postData).forEach(key => {
                if (key === 'image' && postData[key]) {
                    formData.append('image', postData[key]);
                } else {
                    formData.append(key, postData[key]);
                }
            });

            const response = await fetch(`${API_BASE_URL}/posts`, {
                method: 'POST',
                headers: {
                    'Authorization': `Bearer ${this.token}`
                },
                body: formData
            });
            const data = await response.json();
            if (response.ok) {
                return data;
            }
            throw new Error(data.error);
        } catch (error) {
            throw error;
        }
    }

    async updatePost(postId, postData) {
        try {
            const formData = new FormData();
            Object.keys(postData).forEach(key => {
                if (key === 'image' && postData[key]) {
                    formData.append('image', postData[key]);
                } else {
                    formData.append(key, postData[key]);
                }
            });

            const response = await fetch(`${API_BASE_URL}/posts/${postId}`, {
                method: 'PUT',
                headers: {
                    'Authorization': `Bearer ${this.token}`
                },
                body: formData
            });
            const data = await response.json();
            if (response.ok) {
                return data;
            }
            throw new Error(data.error);
        } catch (error) {
            throw error;
        }
    }

    async deletePost(postId) {
        try {
            const response = await fetch(`${API_BASE_URL}/posts/${postId}`, {
                method: 'DELETE',
                headers: this.getHeaders()
            });
            const data = await response.json();
            if (response.ok) {
                return data;
            }
            throw new Error(data.error);
        } catch (error) {
            throw error;
        }
    }

    // Event methods
    async getEvents() {
        try {
            const response = await fetch(`${API_BASE_URL}/events`, {
                headers: this.getHeaders()
            });
            const data = await response.json();
            if (response.ok) {
                return data;
            }
            throw new Error(data.error);
        } catch (error) {
            throw error;
        }
    }

    async createEvent(eventData) {
        try {
            const response = await fetch(`${API_BASE_URL}/events`, {
                method: 'POST',
                headers: this.getHeaders(),
                body: JSON.stringify(eventData)
            });
            const data = await response.json();
            if (response.ok) {
                return data;
            }
            throw new Error(data.error);
        } catch (error) {
            throw error;
        }
    }

    async updateEvent(eventId, eventData) {
        try {
            const response = await fetch(`${API_BASE_URL}/events/${eventId}`, {
                method: 'PUT',
                headers: this.getHeaders(),
                body: JSON.stringify(eventData)
            });
            const data = await response.json();
            if (response.ok) {
                return data;
            }
            throw new Error(data.error);
        } catch (error) {
            throw error;
        }
    }

    async deleteEvent(eventId) {
        try {
            const response = await fetch(`${API_BASE_URL}/events/${eventId}`, {
                method: 'DELETE',
                headers: this.getHeaders()
            });
            const data = await response.json();
            if (response.ok) {
                return data;
            }
            throw new Error(data.error);
        } catch (error) {
            throw error;
        }
    }

    // Stats methods
    async getStats() {
        try {
            const response = await fetch(`${API_BASE_URL}/stats`, {
                headers: this.getHeaders()
            });
            const data = await response.json();
            if (response.ok) {
                return data;
            }
            throw new Error(data.error);
        } catch (error) {
            throw error;
        }
    }
}

// Create and export API client instance
const api = new ApiClient();
export default api; 