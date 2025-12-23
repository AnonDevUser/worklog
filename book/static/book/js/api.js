/**
 * Logbook API Client
 * 
 * Provides a clean interface for frontend components to interact with the backend API.
 */

const API_BASE_URL = '/api';

/**
 * Helper to get the CSRF token from cookies
 */
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

/**
 * UI Helpers for loader management
 */
const UI = {
    showLoader() {
        const loader = document.getElementById('global-loader');
        if (loader) loader.classList.add('active');
    },
    hideLoader() {
        const loader = document.getElementById('global-loader');
        if (loader) loader.classList.remove('active');
    }
};

/**
 * Generic request handler with error handling
 */
async function request(endpoint, options = {}) {
    const url = `${API_BASE_URL}${endpoint}`;
    const showLoader = options.showLoader !== false; // Default to true

    if (showLoader) UI.showLoader();

    const headers = {
        'Content-Type': 'application/json',
        'X-CSRFToken': getCookie('csrftoken'),
        ...options.headers,
    };

    try {
        const response = await fetch(url, { ...options, headers });
        const data = await response.json();

        if (!response.ok) {
            const error = new Error(data.message || 'API Request Failed');
            error.status = response.status;
            error.data = data;
            throw error;
        }

        return data;
    } catch (error) {
        console.error(`API Error [${endpoint}]:`, error);
        throw error;
    } finally {
        if (showLoader) UI.hideLoader();
    }
}

export const ApiClient = {
    /**
     * Get welcome message
     */
    async getMain() {
        return request('/main/');
    },

    /**
     * Fetch all tasks for the current user
     * @param {string} date - Partial date string to filter (YYYY-MM-DD)
     */
    async getTasks(date = '') {
        const query = date ? `?date=${date}` : '';
        return request(`/get-task/${query}`);
    },

    /**
     * Create a new task log
     * @param {Object} taskData - The task details
     */
    async createTask(taskData) {
        return request('/set-task/', {
            method: 'POST',
            body: JSON.stringify(taskData)
        });
    },

    /**
     * Update an existing task
     * @param {Object} updateData - Must include 'id' and fields to update
     */
    async updateTask(updateData) {
        return request('/edit-task/', {
            method: 'POST',
            body: JSON.stringify(updateData)
        });
    },

    /**
     * Get statistical summary
     */
    async getSummary() {
        return request('/summary/');
    },

    /**
     * Delete a task
     * @param {number} id - The task ID
     */
    async deleteTask(id) {
        return request('/delete-task/', {
            method: 'POST',
            body: JSON.stringify({ id })
        });
    }
};


export default ApiClient;
