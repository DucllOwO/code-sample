import Queue from "bull";
import { REDIS_ATTEMPTS } from "../config/config.js";
import RandomnessSolanaService from "../services/randomness.service.js";
import "dotenv/config.js";

const randomQueue = new Queue("random", {
  redis: {
    host: process.env["REDIS_HOST"],
    port: parseInt(process.env["REDIS_PORT"]),
  },
});

randomQueue
  .on("error", function (error) {
    console.error("Job error", error);
  })
  .on("completed", function (job, result) {
    console.log(`Job ${job.id} is completed`);
  });

const randomProcess = async (job) => {
  console.log("randomProcess: ", job.data);
  let { roundId, merkleRoot, nftCount } = job.data;
  return await RandomnessSolanaService.getInstance().requestRandomness(roundId, merkleRoot, nftCount);
};

randomQueue.process(randomProcess);

const requestRandomnessQueue = (data) => {
  randomQueue.add(data, { attempts: REDIS_ATTEMPTS });
};

export { requestRandomnessQueue };
