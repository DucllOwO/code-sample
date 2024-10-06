export type SbRandomness = {
  "address": "4vziut1PVQHX1dJihKuLpvGMSyVu8CXSPMuQvr2ig8tp",
  "metadata": {
    "name": "sbRandomness",
    "version": "0.1.0",
    "spec": "0.1.0",
    "description": "Created with Anchor"
  },
  "instructions": [
    {
      "name": "consumeRandomness",
      "docs": [
        "Notice: This instruction use to reveal the random data from randomness account and cast random data from array bytes to array u32",
        "Dev: Convert origin random data to array u32 to make sure the calculate result in range of total minted nft",
        "Function params:",
        "ctx: context store all the accounts need to request randomness",
        "user: payer account that sign and pay gas must be admin",
        "config: the configuration account had been initialized to store admin public key",
        "system_account: system account",
        "randomness_account_data: the randomness account had been created by switchboard to store randomness result",
        "round_state: the round state account store information about round randomness"
      ],
      "discriminator": [
        190,
        217,
        49,
        162,
        99,
        26,
        73,
        234
      ],
      "accounts": [
        {
          "name": "configState",
          "docs": [
            "config account to check admin state"
          ],
          "writable": true
        },
        {
          "name": "roundState",
          "docs": [
            "the round state account store information about round randomness"
          ],
          "writable": true
        },
        {
          "name": "randomnessAccountData"
        },
        {
          "name": "admin",
          "writable": true,
          "signer": true,
          "relations": [
            "configState"
          ]
        },
        {
          "name": "systemProgram",
          "address": "11111111111111111111111111111111"
        }
      ],
      "args": []
    },
    {
      "name": "drawRandomNumber",
      "docs": [
        "Notice: This instruction use to calculate all the prizes",
        "Dev: If the calculate result is duplicate, it will calculate until it's not duplicate anymore",
        "Function params:",
        "ctx: context store all the accounts need to request randomness",
        "user: payer account that sign and pay gas must be admin",
        "config: the configuration account had been initialized to store admin public key",
        "round_state: the round state account store information about round randomness"
      ],
      "discriminator": [
        223,
        242,
        102,
        191,
        226,
        117,
        234,
        218
      ],
      "accounts": [
        {
          "name": "admin",
          "writable": true,
          "signer": true,
          "relations": [
            "configState"
          ]
        },
        {
          "name": "configState",
          "docs": [
            "the configuration account had been initialized to store admin public key"
          ],
          "writable": true
        },
        {
          "name": "roundState",
          "docs": [
            "the round state account store information about round randomness"
          ],
          "writable": true
        }
      ],
      "args": [
        {
          "name": "numPrize",
          "type": "u16"
        }
      ]
    },
    {
      "name": "initConfig",
      "docs": [
        "Notice: This instruction use to initialize config account that store admin public key",
        "Function params:",
        "ctx: context store all the accounts need for initialize configuration",
        "payer: payer account that sign and pay gas",
        "config_account: the configuration account has been initialized in this instruction to store admin public key",
        "system_account: system account",
        "admin: Public key of admin who can call random instructions"
      ],
      "discriminator": [
        23,
        235,
        115,
        232,
        168,
        96,
        1,
        231
      ],
      "accounts": [
        {
          "name": "payer",
          "writable": true,
          "signer": true
        },
        {
          "name": "configAccount",
          "writable": true,
          "pda": {
            "seeds": [
              {
                "kind": "const",
                "value": [
                  67,
                  111,
                  110,
                  102,
                  105,
                  103
                ]
              }
            ]
          }
        },
        {
          "name": "systemProgram",
          "address": "11111111111111111111111111111111"
        }
      ],
      "args": [
        {
          "name": "admin",
          "type": "pubkey"
        }
      ]
    },
    {
      "name": "requestRandomness",
      "docs": [
        "Notice: This instruction to initialize round state account",
        "Function params:",
        "ctx: context store all the accounts need to request randomness",
        "user: payer account that sign and pay gas must be admin",
        "config: the configuration account had been initialized to store admin public key",
        "system_account: system account",
        "randomness_account_data: the randomness account had been created by switchboard to store randomness result",
        "round_state: the round state account store information about round randomness",
        "round_id: the id of round which admin request randomness result",
        "params:",
        "merkle_root: the merkle root generate from pair nft id and index. For example: [\"124,5\"]",
        "nft_count: total nft minted in this round_id",
        "prize_count: amount of prize has been awarded in this round_id"
      ],
      "discriminator": [
        213,
        5,
        173,
        166,
        37,
        236,
        31,
        18
      ],
      "accounts": [
        {
          "name": "configState",
          "docs": [
            "the configuration account had been initialized to store admin public key"
          ],
          "writable": true
        },
        {
          "name": "admin",
          "docs": [
            "PAYER ACCOUNTS sign and pay gas"
          ],
          "writable": true,
          "signer": true,
          "relations": [
            "configState"
          ]
        },
        {
          "name": "systemProgram",
          "docs": [
            "SYSTEM ACCOUNTS"
          ],
          "address": "11111111111111111111111111111111"
        },
        {
          "name": "randomnessAccountData"
        },
        {
          "name": "roundState",
          "docs": [
            "the round state account store information about round randomness"
          ],
          "writable": true,
          "pda": {
            "seeds": [
              {
                "kind": "const",
                "value": [
                  82,
                  111,
                  117,
                  110,
                  100
                ]
              },
              {
                "kind": "arg",
                "path": "roundId"
              }
            ]
          }
        }
      ],
      "args": [
        {
          "name": "roundId",
          "type": "u32"
        },
        {
          "name": "params",
          "type": {
            "defined": {
              "name": "requestRandomnessParams"
            }
          }
        }
      ]
    },
    {
      "name": "setAdmin",
      "docs": [
        "Notice: This instruction use to set admin account in config account",
        "Function params:",
        "ctx: context store all the accounts need for set admin",
        "///         payer: payer account that sign and pay gas",
        "config_account: the configuration account had been initialized to store admin public key",
        "admin: Public key of admin who can call random instructions"
      ],
      "discriminator": [
        251,
        163,
        0,
        52,
        91,
        194,
        187,
        92
      ],
      "accounts": [
        {
          "name": "configAccount",
          "writable": true
        },
        {
          "name": "admin",
          "writable": true,
          "signer": true,
          "relations": [
            "configAccount"
          ]
        }
      ],
      "args": [
        {
          "name": "admin",
          "type": "pubkey"
        }
      ]
    }
  ],
  "accounts": [
    {
      "name": "configState",
      "discriminator": [
        193,
        77,
        160,
        128,
        208,
        254,
        180,
        135
      ]
    },
    {
      "name": "roundState",
      "discriminator": [
        153,
        242,
        39,
        64,
        102,
        34,
        239,
        11
      ]
    }
  ],
  "errors": [
    {
      "code": 6000,
      "name": "randomnessNotResolved"
    }
  ],
  "types": [
    {
      "name": "configState",
      "type": {
        "kind": "struct",
        "fields": [
          {
            "name": "admin",
            "type": "pubkey"
          }
        ]
      }
    },
    {
      "name": "requestRandomnessParams",
      "type": {
        "kind": "struct",
        "fields": [
          {
            "name": "merkleRoot",
            "type": {
              "array": [
                "u8",
                32
              ]
            }
          },
          {
            "name": "nftCount",
            "type": "u32"
          },
          {
            "name": "prizeCount",
            "type": "u32"
          }
        ]
      }
    },
    {
      "name": "roundState",
      "type": {
        "kind": "struct",
        "fields": [
          {
            "name": "roundId",
            "type": "u32"
          },
          {
            "name": "merkleRoot",
            "type": {
              "array": [
                "u8",
                32
              ]
            }
          },
          {
            "name": "nftCount",
            "type": "u32"
          },
          {
            "name": "prizeCount",
            "type": "u32"
          },
          {
            "name": "prizeRemaining",
            "type": "u32"
          },
          {
            "name": "originResultBuffer",
            "type": {
              "array": [
                "u8",
                32
              ]
            }
          },
          {
            "name": "castedResultBuffer",
            "type": {
              "vec": "u32"
            }
          },
          {
            "name": "timestamp",
            "type": "i64"
          },
          {
            "name": "randomnessAccount",
            "type": "pubkey"
          },
          {
            "name": "winnerIndexes",
            "type": {
              "vec": "u32"
            }
          },
          {
            "name": "commitSlot",
            "type": "u64"
          }
        ]
      }
    }
  ]
};