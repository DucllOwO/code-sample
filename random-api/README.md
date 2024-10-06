# Random API - ExpressJS

This repository is used to trigger internally to draw random numbers and handle related signatures.

## Run Locally

To run this project locally, follow these steps:

1. Create a `.env` file with the following content:

   ```bash
   RANDOM_PROGRAM_ID=<random-program-id>
   SWITCHBOARD_PROGRAM_ID=<switchboard-program-id>
   PAYER=<solana-private-key>
   PROVIDER=<solana-rpc-provider>
   MONGO_URI=<your-database-connection-string>
   REDIS_HOST=<host-of-your-redis>
   REDIS_PORT=<port-of-your-redis>
   BACKEND_URL=<backend-url>
   ```

   - Notes:
     - `RANDOM_PROGRAM_ID`: Random program id when deploying smart contract in repo `RandomSmartContract`
     - `PAYER`: The private key of the Solana wallet used to pay for the transaction fee to draw a random number
     - `PROVIDER`: The RPC provider of Solana. For example, Devnet: `https://api.devnet.solana.com`, Mainnet: `https://api.mainnet-beta.solana.com`
     - `BACKEND_URL`: The URL of your deployed `brc20-backend-api` repo

2. Install dependencies:

   ```bash
   npm install
   ```

3. Run the server:

```bash
npm run dev
```

To avoid unexpected errors, please use Node.js version v20.10.0.

## Documentation

### Internal API

1. Draw random number

- Method: POST
- Endpoint: `/randomness`
