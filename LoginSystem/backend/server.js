require('dotenv').config();
const express = require('express');
const mysql = require('mysql2/promise');
const cors = require('cors');
const app = express();

app.use((req, res, next) => {
    console.log(`[${new Date().toISOString()}] ${req.method} ${req.url}`);
    next();
});

app.use(cors());
app.use(express.json());

const pool = mysql.createPool({
    host: process.env.DB_HOST || 'localhost',
    user: process.env.DB_USER || 'auth_user',
    password: process.env.DB_PASSWORD || 'Auth@1234',
    database: process.env.DB_NAME || 'auth_system'
});

app.post('/login', async (req, res) => {
    console.log('Login request body:', req.body);
    res.json({ success: true, message: 'Login successful' });
});

app.post('/register', async (req, res) => {
    console.log('Register request body:', req.body);
    res.status(201).json({ success: true });
});

const PORT = process.env.PORT || 3000;
app.listen(PORT, () => {
    console.log(`Server running on port ${PORT}`);
    pool.getConnection()
        .then(conn => {
            console.log(' MySQL connected');
            conn.release();
        })
        .catch(err => console.error('MySQL connection failed:', err));
});