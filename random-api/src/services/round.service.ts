import Round from "../models/round.model.js";
import database from "../config/database.js";

async function getPrizeInfoByRound(roundId) {
  try {
    let result = await Round.findOne({ round: roundId });
    console.log("result", result, roundId)

    return result
      ? {
          reward: result.reward[0],
          prizeCount: sumAllPrize(result.reward[0]),
          isactive: result.isactive,
          compelete: result.compelete,
        }
      : null;
  } catch (error) {
    console.error(error)
    return null;
  }
}

function sumAllPrize(reward) {
  return (
    reward.special +
    reward.top1 +
    reward.top2 +
    reward.top3 +
    reward.consolation
  );
}

export default { getPrizeInfoByRound };
