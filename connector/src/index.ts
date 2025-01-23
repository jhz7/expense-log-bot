import express from "express";
import webhookRoute from "./api/webhook.route.js"; // Import the route

const app = express();
app.use(express.json());

const PORT = process.env.PORT || 3000;

app.use("/webhook", webhookRoute);

app.listen(PORT, () => {
  console.log(`Server is running on port ${PORT}`);
});
