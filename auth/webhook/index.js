const express = require('express');
const app = express();

app.use(express.json());

app.post('/authorize', (req, res) => {
  const { headers } = req;
  const userId = headers['user-id'];

  let responseBody;
  let statusCode;

  console.log('Received request with headers:', headers);
  console.log('user-id:', userId);

  if (!userId) {
    responseBody = {
      "x-hasura-role": "anonymous"
    };
    statusCode = 401;
  } else {
    responseBody = {
      "x-hasura-role": "pguser",
      "x-hasura-user-id": userId	    
    };
    statusCode = 200;
  }

  console.log(`Sending response with status ${statusCode}:`, responseBody);
  return res.status(statusCode).json(responseBody);
});

const PORT = process.env.PORT || 3000;
app.listen(PORT, () => {
  console.log(`Auth webhook listening on port ${PORT}`);
});

