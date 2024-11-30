const express = require("express");
const { exec } = require("child_process");
const path = require("path");

const app = express();
app.use(express.json());

app.post("/query", (req, res) => {
    const { errorCode, make } = req.body;

    exec(`python3 ai_agent.py ${errorCode} ${make}`, (error, stdout, stderr) => {
        if (error) {
            res.status(500).send({ error: error.message });
            return;
        }
        res.send({ solution: stdout });
    });
});

app.listen(3000, () => {
    console.log("Server is running on http://localhost:3000");
});

