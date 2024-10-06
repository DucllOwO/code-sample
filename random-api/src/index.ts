import express from "express";
import bodyParser from "body-parser";
import RandomnessSolanaService from "./services/randomness.service.js";
import { requestRandomnessQueue } from "./queues/random.queue.js";
import database from "./config/database.js";
import morgan from "morgan";
import "dotenv/config.js";
import { web3 } from "@coral-xyz/anchor";

const app = express();
app.use(bodyParser.json());

const port = 3000;

morgan.token("id", (req) => {
  return req.id.split("-")[0];
});

app.use(morgan("[:date[iso]] API :method :url :status :response-time ms"));

app.get("/health-check", (req, res) => {
  res.status(200).send("Hello World!");
});

app.post("/randomness", async (req, res) => {
  const data = req.body;

  requestRandomnessQueue(data);

  // await RandomnessSolanaService.getInstance().requestRandomness(data.roundId, data.merkleRoot, data.nftCount);

  res.send({ status: "ok" });
});

const server = app.listen(port, "0.0.0.0", async () => {
  console.log("Initializing dependencies...")
  await database.connectToDatabase();

  await RandomnessSolanaService.getInstance().setup(process.env["PAYER"], process.env["COMMITMENT"] as web3.Commitment, process.env["PROVIDER"], parseInt(process.env["MAX_PRIZE_DRAW_PER_TRANSACTION"]));

  console.log("Initializing dependencies successfully...")
});

async function shutdown() {
  await database.closeDatabaseConnection();

  server.close(() => {
    process.exit(0);
  });
}

process.on("SIGTERM", shutdown);
process.on("SIGINT", shutdown);
