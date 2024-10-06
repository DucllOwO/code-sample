import mongoose from "mongoose";
import "dotenv/config.js";

const uri = process.env.MONGO_URI;

async function connectToDatabase() {
  try {
    await mongoose.connect(uri, { retryWrites: false });
    console.log("Connect to database success!");
  } catch (error) {
    console.error(error);
  }
}

async function closeDatabaseConnection() {
  try {
    await mongoose.disconnect();
    console.log("Database connection closed successfully!");
  } catch (error) {
    console.error("Error while closing database connection:", error);
  }
}

export default { connectToDatabase, closeDatabaseConnection };
