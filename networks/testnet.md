# FLOP Testnet

These values identify FLOP Testnet. Compare them with what your wallet, node or explorer shows.

| Field | Value |
|---|---|
| Chain ID | `flop_testnet` |
| Genesis block hash | `0x918abd58fb16306b30ef3886514cfaebffecb4de43e82b6f8ec4795c43cfd800` |
| Runtime spec name | `flop-testnet` |
| Public RPC | `wss://testnet.flop.network` |
| Token | FLOP, 18 decimals |
| SS58 prefix | 42 |

## Offline wallets (Polkadot Vault)

Polkadot Vault adds FLOP Testnet from two signed QR codes: one with the network specs and one
with the runtime metadata. Both are signed by the FLOP Testnet metadata verifier below. This
page is the independent reference for that key. The QR codes themselves are on the
[FLOPScan offline wallet page](https://testnet.flopscan.io/offline-wallet), and the
[Testnet docs](https://docs.flop.network/networks/testnet) repeat the key.

| Field | Value |
|---|---|
| Verifier type | Custom network verifier, Ed25519 |
| Public key | `0x1c6baa92c3133d5734697f34fd34df6a7dab42b987bcc99f9ea8fd600b5ea311` |
| SHA-256 of the raw 32-byte key | `2f3e0ec577ce34104c156ed97c2b8b0334c5214e5dd30f679f09def033e36207` |

Before you scan:

1. Check that this page, FLOPScan and the docs show the same genesis hash and public key. Open
   at least one of them on a different device or connection.
2. When Vault adds the network, check that it shows this key as the network's custom verifier.
   Stop if Vault asks to add or replace its General Verifier.
3. After the import, select FLOP Testnet in Vault and check the genesis hash it shows.

Each runtime upgrade needs a new metadata QR, signed by the same key. FLOPScan shows the metadata
QR only for the runtime version the chain runs at its finalized head.

| Runtime spec version | Metadata QR SHA-256 |
|---|---|
| 1014035 | `5ebe220625805f67023eac297cdcec9aa61f8297954bbbcbe3f26ba0afbf4e75` |

The network-specs QR has SHA-256
`2e161e60205ef0ce88f0aaf1543334a6913f54106c86edb42bc9878fcf0b50d4`.

If this key is ever replaced or revoked, this page will say so first. Remove FLOP Testnet from
Vault and import it again with the new key.
