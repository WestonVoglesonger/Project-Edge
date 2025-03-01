// A simple script to serve a pre-built Angular app using a lightweight server
const { exec } = require("child_process");
const express = require("express");
const path = require("path");
const app = express();
const port = 1462;

console.log("Building Angular app in lightweight mode...");
exec("npm run build:minimal", (error, stdout, stderr) => {
  if (error) {
    console.error(`Error during build: ${error.message}`);
    return;
  }

  console.log(`Build output: ${stdout}`);

  if (stderr) {
    console.error(`Build stderr: ${stderr}`);
  }

  console.log("Build completed. Starting server...");

  // Serve static files from the dist directory
  app.use(express.static(path.join(__dirname, "../docs")));

  // For all GET requests, send back index.html
  app.get("/*", (req, res) => {
    res.sendFile(path.join(__dirname, "../docs/index.html"));
  });

  // Start the server
  app.listen(port, () => {
    console.log(`Server running on http://localhost:${port}`);
  });
});
