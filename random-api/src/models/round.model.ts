import mongoose from "mongoose";
mongoose.pluralize(null);

const RoundSchema = new mongoose.Schema(
  {
    round: { type: Number },
    nft1: { type: Array },
    nft2: { type: Array },
    nft3: { type: Array },
    nft4: { type: Array },
    nft5: { type: Array },
    timecreate: { type: Date, default: new Date() },
    isactive: { type: Boolean },
    totalsold: { type: Number },
    reward: { type: Array },
    compelete: { type: Boolean },
  },
  { versionKey: false }
);

export default mongoose.model("round", RoundSchema);
