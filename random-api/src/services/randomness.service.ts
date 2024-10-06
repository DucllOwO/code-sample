import web3, { ComputeBudgetProgram, Keypair, PublicKey, SystemProgram, Transaction, TransactionInstruction } from "@solana/web3.js";
import randomIDL from "../idl/random.json";
import { AnchorProvider, BN, Idl, Program, Wallet } from "@coral-xyz/anchor";
import base58 from "bs58";
import Random from "../models/random.model.js";
import RoundService from "./round.service.js";
import axios from "axios";
import "dotenv/config.js";
import * as sb from "@switchboard-xyz/on-demand";
import { delay } from "../utils/utils";
import SB_IDL from "../idl/switchboard_program.json"
import { Commitment } from "@solana/web3.js";

const txOpts = {
    commitment: "finalized" as Commitment,
    skipPreflight: false,
  };

class RandomnessSolanaService {
  static instance: RandomnessSolanaService
  payer: Keypair
  payerWallet: Wallet
  provider: AnchorProvider
  switchboardProgram: Program
  randomProgram: Program
  roundState: PublicKey
  randomnessAccount: sb.Randomness
  sbQueue: PublicKey
  configAccount: PublicKey
  // transaction config
  commit: web3.Commitment
  maxPrizePerTransaction: number

  // wrapped function: wrap with retry behavior when transaction send fail
  wrappedSetupRandomAccount = this.retryWrapper(
    this.setupRandomAccount,
    parseInt(process.env["NUMBER_OF_RETRIES"])
  );
  wrappedSendRequestRandomness = this.retryWrapper(this.sendRequestRandomness, parseInt(process.env["NUMBER_OF_RETRIES"]))
  wrappedSendConsumeRandomness = this.retryWrapper(this.sendConsumeRandomness, parseInt(process.env["NUMBER_OF_RETRIES"]))
  wrappedSendDrawRandomNumber = this.retryWrapper(this.sendDrawRandomNumber, parseInt(process.env["NUMBER_OF_RETRIES"]))

  constructor() {
    
  }

  public static getInstance(): RandomnessSolanaService {
        if (!RandomnessSolanaService.instance) {
            RandomnessSolanaService.instance = new RandomnessSolanaService();
        }

        return RandomnessSolanaService.instance;
    }

  async setup(payerSecretKey: string, commit: web3.Commitment, providerUrl: string, maxPrizeDrawPerTransaction: number) {
    this.commit = commit
    this.payer = web3.Keypair.fromSecretKey(base58.decode(payerSecretKey));
    this.payerWallet = new Wallet(this.payer);

    this.provider = new AnchorProvider(
      new web3.Connection(providerUrl),
      this.payerWallet,
      // @ts-ignore
      { commitment: this.commit }
    );

    this.randomProgram = new Program(
      randomIDL as Idl,
      this.provider
    );

    this.maxPrizePerTransaction = maxPrizeDrawPerTransaction
    this.sbQueue = await this.setupQueue(this.randomProgram);

    this.switchboardProgram = new Program(SB_IDL as Idl, this.provider);

    this.randomnessAccount = await this.wrappedSetupRandomAccount(this.switchboardProgram);

    const [configPDA, _] = web3.PublicKey.findProgramAddressSync(
      [
        Buffer.from("Config")
      ],
      this.randomProgram.programId
    )

    this.configAccount = configPDA

    console.log("Initialize important contract account completed")
  }
  
  async createPDA(roundId: number) {
    let roundIdBN = new BN(roundId);

    const [pda, _] = web3.PublicKey.findProgramAddressSync(
      [Buffer.from("Round"), roundIdBN.toArrayLike(Buffer, "le", 4)],
      this.randomProgram.programId
    );

    return pda
  }

  async setupRandomAccount(switchboardProgram: Program): Promise<sb.Randomness> {
    const rngKp = Keypair.generate();
    const [randomness, ix] = await sb.Randomness.create(switchboardProgram, rngKp, this.sbQueue);

    console.log("Randomness account", randomness.pubkey.toString());

    const createRandomnessTx = await sb.asV0Tx({
      connection: switchboardProgram.provider.connection,
      ixs: [ix],
      payer: this.payer.publicKey,
      signers: [this.payer, rngKp],
      computeUnitPrice: 75_000,
      computeUnitLimitMultiple: 1.3,
    });
    await this.provider.connection.simulateTransaction(createRandomnessTx, txOpts);
    const sig1 = await this.provider.connection.sendTransaction(createRandomnessTx, txOpts);
    await this.provider.connection.confirmTransaction(sig1, "finalized");
    console.log(
      "  Transaction Signature for randomness account creation: ",
      sig1
    );

    return randomness;
  }

  async setupQueue(program: Program): Promise<PublicKey> {
    const queueAccount = await sb.getDefaultQueue(
      program.provider.connection.rpcEndpoint
    );
    console.log("Queue account", queueAccount.pubkey.toString());
    try {
      await queueAccount.loadData();
    } catch (err) {
      console.error("Queue not found");
    }
    return queueAccount.pubkey;
  }

  async createRequestRandomnessInstruction(roundId: number, params: Object, roundState: PublicKey): Promise<TransactionInstruction> {
    return await this.randomProgram.methods.requestRandomness(
      roundId,
      params
    ).accounts({
      admin: this.payer.publicKey,
      systemProgram: SystemProgram.programId,
      randomnessAccountData: this.randomnessAccount.pubkey,
      roundState: roundState,
      configState: this.configAccount,
    }).signers([this.payer])
      .instruction();
  }

  async sendRequestRandomness(roundId: number, params: Object, roundState: PublicKey): Promise<string> {
    // Commit transaction
    let commitIx = await this.randomnessAccount.commitIx(this.sbQueue);

    let requestIx = await this.createRequestRandomnessInstruction(roundId, params, roundState)
    
    const commitTx = await sb.asV0Tx({
      connection: this.switchboardProgram.provider.connection,
      ixs: [commitIx, requestIx],
      payer: this.payer.publicKey,
      signers: [this.payer],
      computeUnitPrice: 75_000,
      computeUnitLimitMultiple: 2,
    });

    await this.provider.connection.simulateTransaction(commitTx, txOpts);
    const sig = await this.provider.connection.sendTransaction(commitTx, txOpts);
    await this.provider.connection.confirmTransaction(sig, "finalized");
    console.log("Transaction Signature commitTx", sig);
    return sig
  }

  async requestRandomness(roundId: number, merkleRoot, nftCount: number) {
    try {
      // check if round data is already existed
      let checkRound = await this.getRandomByRoundIdService(roundId);
      console.log("🚀 ~ RandomnessSolanaService ~ requestRandomness ~ checkRound:", checkRound)

      if (checkRound) {
        console.warn(`Round ${roundId} random result has already existed`);
        return;
      }

      let roundInfo = await RoundService.getPrizeInfoByRound(roundId);

      console.log("Round info:", roundInfo);

      if (!roundInfo) return;


      if (roundInfo.compelete == false || roundInfo.isactive == true) {
        console.warn("Round has not ended yet");
        return;
      }

      let roundState = await this.createPDA(roundId);
      console.log("🚀 ~ RandomnessSolanaService ~ requestRandomness ~ roundState:", roundState)

      let params = {
        nftCount: nftCount,
        merkleRoot: Buffer.from(merkleRoot),
        prizeCount: roundInfo.prizeCount,
      };

    console.log("\nCommit to randomness...");
      let requestSignature = await this.wrappedSendRequestRandomness(roundId, params, roundState)
    console.log("\nReveal the randomness...");
      await this.wrappedSendConsumeRandomness(roundState);

      // let reward = {
      //   special: 1,
      //   top1: 3,
      //   top2: 3,
      //   top3: 3,
      //   consolation: 140,
      // };

      let { winnerIndexes, randomSignatures } = await this.getRandomResults(
        roundState,
        roundInfo.reward
      );

      console.log(JSON.stringify(({
        indexes: winnerIndexes,
        round_id: roundId,
        merkle_root: merkleRoot,
        round_state: roundState,
        request_tx: requestSignature,
        random_txs: randomSignatures,
      })))

      // save random result into database
      await Random.create({
        indexes: winnerIndexes,
        round_id: roundId,
        merkle_root: merkleRoot,
        round_state: roundState,
        request_tx: requestSignature,
        random_txs: randomSignatures,
      });

      console.log("axios url:", process.env["BACKEND_URL"] + "/reward/process");
      // trigger handle random result from backend
      axios({
        method: "post",
        url: process.env["BACKEND_URL"] + "/reward/process",
        data: {
          ...winnerIndexes,
          round: roundId,
          random_txs: randomSignatures,
        },
      })
        .then(() => console.log(`TRIGGER SUCCESSFULLY FOR ROUND ${roundId}`))
        .catch((err) => {
          console.error(err?.code);
        });
    } catch (e) {
      console.error(e)
      throw e
    }
  }

  async sendConsumeRandomness(roundState: PublicKey): Promise<string> {
    const revealIx = await this.randomnessAccount.revealIx();
  
    const consumeIx = await this.randomProgram.methods.consumeRandomness().accounts({
      admin: this.payer.publicKey,
        systemProgram: SystemProgram.programId,
        randomnessAccountData: this.randomnessAccount.pubkey,
        roundState: roundState,
        configState: this.configAccount,
      }).signers([this.payer])
      .instruction();

    const revealTx = await sb.asV0Tx({
      connection: this.switchboardProgram.provider.connection,
      ixs: [revealIx, consumeIx],
      payer: this.payer.publicKey,
      signers: [this.payer],
      computeUnitPrice: 80_000,
      computeUnitLimitMultiple: 1.5,
    });

    await this.provider.connection.simulateTransaction(revealTx, txOpts);
    const sig = await this.provider.connection.sendTransaction(revealTx, txOpts);
    await this.provider.connection.confirmTransaction(sig, "finalized");
    console.log("Transaction Signature revealTx", sig);
    return sig
  }

  async getRandomResults(
    roundState: PublicKey,
    awardRule
  ) {
    let roundCurrentState;
    let randomSignatures = [];
    while (true) {
      let drawSignature = await this.wrappedSendDrawRandomNumber(roundState);

      randomSignatures.push(drawSignature);

      // @ts-expect-error error because the type
      roundCurrentState = await this.randomProgram.account.roundState.fetch(roundState);

      console.log("Current prize remaning prize: ", roundCurrentState.prizeRemaining);

      if (roundCurrentState.prizeRemaining <= 0) {
        break
      }
      await sb.sleep(1000)
    }

    // @ts-expect-error error because the type
    roundCurrentState = await this.randomProgram.account.roundState.fetch(
      roundState
    );
    return {
      winnerIndexes: this.sliceRandomResultToAwardFormat(
        roundCurrentState.winnerIndexes,
        awardRule
      ),
      randomSignatures,
    };
  }

  async sendDrawRandomNumber(roundState: PublicKey): Promise<string> {
    // get random number 
    
    let drawRandom = await this.randomProgram.methods.drawRandomNumber(this.maxPrizePerTransaction).accounts({ roundState: roundState, configState: this.configAccount }).signers([this.payer]).instruction()

    const modifyComputeUnits = ComputeBudgetProgram.setComputeUnitLimit({ 
      units: 2000000
    });

    const transaction = new Transaction().add(modifyComputeUnits, drawRandom);
    
    const sigDraw = await this.provider.sendAndConfirm(transaction, [this.payer], { commitment: "finalized"});
    console.log(`Draw random Transaction Signature: ${sigDraw}`);

    return sigDraw
  }

  sliceRandomResultToAwardFormat(array, awardRule) {
  return {
    special: array.slice(0, awardRule.special),
    top1: array.slice(awardRule.special, awardRule.top1 + awardRule.special),
    top2: array.slice(
      awardRule.top1 + awardRule.special,
      awardRule.top2 + awardRule.top1 + awardRule.special
    ),
    top3: array.slice(
      awardRule.top2 + awardRule.top1 + awardRule.special,
      awardRule.top3 + awardRule.top2 + awardRule.top1 + awardRule.special
    ),
    consolation: array.slice(
      awardRule.top3 + awardRule.top2 + awardRule.top1 + awardRule.special
    ),
  };
  }

  async getRandomByRoundIdService(roundId) {
    try {
      let result = await Random.findOne({ round_id: roundId });
      return result;
    } catch (error) {
      return null;
    }
  }

  retryWrapper(fn: Function, retries: number) {
    return async function (...args) {
      let attempts = 0;
      while (attempts < retries) {
        try {
          // Attempt to execute the transaction function
          return await fn.apply(this, args);
        } catch (error) {
          console.error("Execute fail. Retrying...");
          attempts++;
          if (attempts >= retries) {
            // If the number of retries has been exceeded, throw the error
            throw new Error(
              `Function failed after ${retries} retries: ${error.message}`
            );
          }
          // Optionally, add a delay between retries
          await delay(5000); // 5 second delay
        }
      }
    };
  }
}

export default RandomnessSolanaService;
