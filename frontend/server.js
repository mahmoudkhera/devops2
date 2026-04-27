const express = require('express');
const path = require('path');
require('dotenv').config();

const app = express();
app.use(express.static(__dirname));

const PORT = process.env.FRONTEND_PORT || 8000;
const HOST = process.env.FRONTEND_HOST || '0.0.0.0';
const API = process.env.API || 'http://localhost:3000'

// Runtime config — the browser fetches this before anything else
app.get('/config.js', (req, res) => {
  res.type('application/javascript');
  res.send(`window.APP_CONFIG = { API_URL: "${API}" };`);
});

app.listen(PORT, HOST, () => {
  console.log(`Frontend running on http://${HOST}:${PORT}`);
  console.log(`public api test     ${process.env.API}`);
  console.log(` trigger first commit `);
});