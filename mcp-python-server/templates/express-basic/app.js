const express = require('express');
const app = express();
const port = process.env.PORT || 3000;

app.get('/', (_req, res) => {
  res.json({ message: 'Hello from Express template' });
});

app.listen(port, () => {
  console.log(`Express server running on port ${port}`);
});
