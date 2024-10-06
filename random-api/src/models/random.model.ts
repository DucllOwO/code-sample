import mongoose from "mongoose";
mongoose.pluralize(null);

const RandomSchema = new mongoose.Schema(
  {
    indexes: { type: Object },
    created_time: { type: Date, default: new Date() },
    round_id: { type: String },
    merkle_root: { type: String },
    round_state: { type: String },
    request_tx: { type: String },
    random_txs: { type: Array },
  },
  { versionKey: false }
);

export default mongoose.model("random", RandomSchema);
