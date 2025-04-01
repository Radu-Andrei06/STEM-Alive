const API_BASE_URL = 'http://localhost:3000';

async function login() {
    console.log('Login initiated');
    try {
        const response = await fetch(`${API_BASE_URL}/login`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({
                username: 'testuser',
                password: 'Test@1234'
            })
        });
        console.log('Login response:', await response.json());
    } catch (error) {
        console.error('Login error:', error);
    }
}

async function register() {
    console.log('Register initiated');
    // Similar fetch call for registration
}

document.addEventListener('DOMContentLoaded', () => {
    document.getElementById('login-btn').addEventListener('click', login);
    document.getElementById('register-btn').addEventListener('click', register);
    console.log('Event listeners added');
});