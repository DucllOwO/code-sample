import mongoose from "mongoose";
mongoose.pluralize(null);

const RewardSchema = new mongoose.Schema(
  {
    round: { type: Number },
    timecreate: { type: Number },
    prizes: { type: Array },
  },
  { versionKey: false }
);

export default mongoose.model("reward", RewardSchema);
