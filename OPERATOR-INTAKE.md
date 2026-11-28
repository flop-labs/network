# Validator and RPC operator registration

Use the [operator registration form](https://github.com/flop-labs/network/issues/new?template=operator-application.yml) to register one team per network. Start with one keyless host and the [public Devnet RPC guide](https://gist.github.com/sv/7c8b93f3868bc15e3b6eabe0578057e3#run-a-flop-devnet-rpc-replica). Register while planning your host and add evidence as it becomes available. Link an existing introduction rather than repeating it. Testnet qualification stays pending until FLOP publishes the Testnet package and network inputs. Use a fresh Testnet database and collect Testnet evidence against that release.

The issue number is the public registration ID. Use it alongside the stable team ID and each node's peer ID in receipts and FLOP's private qualification registry. Coordinate dedicated RPC origin hostnames and fixed IPs, incident contacts and private routes with FLOP privately. Public P2P multiaddresses and peer IDs can go in the issue. Keep keys, enrollment material and unredacted logs private. Operators who already have a registration should keep that record; a maintainer can add the intake labels and request the missing form fields in the same thread.

## Collect sync and restart evidence

Once the network-specific package is published, use its `node qualify-rpc.mjs --profile public-devnet` or `node qualify-rpc.mjs --profile public-testnet` command as directed by the release guide. Choose the profile that matches the registration and add the public-safe receipt to **Sync and restart evidence**. If the selected profile is unpublished, leave qualification pending. Each profile requires its own release inputs and evidence.

Include a separate operator attestation that you restarted with the same Compose project and retained volume. Maintainers independently verify the network, release, public P2P reachability and sync evidence before recording qualification.

## Labels and review

The form automatically applies `type:registration`, `intake:operator`, `status:intake` and `area:node`. The [registration queue](https://github.com/flop-labs/network/issues?q=is%3Aissue+is%3Aopen+label%3Aintake%3Aoperator) is the shared register. Submitting the form records the team immediately. Node qualification and validator activation are tracked separately.

When organizing new registrations, a maintainer adds the selected `net:devnet` or `net:testnet` label and `role:validator`, `role:rpc`, or both. Keep `status:intake` while the operator is preparing a host or waiting for their cohort. Use `status:needs-info` only when asking the operator for specific missing information, then remove it when they reply. Operator registrations are exempt from the needs-info stale closer, so waiting for an invitation does not silently close them. The current shared triage action protects non-triage `status:` labels, including `status:intake`; retain that protection when updating the action.

Operations adds evidence labels only after independently verifying the corresponding facts:

| Label | Required evidence |
| --- | --- |
| `intake:sync-qualified` | Approved network/artifact identity, reachable P2P, matching common finalized hashes with advancement, and retained-volume restart with unchanged peer identity. |
| `intake:rpc-active` | Separate keyless origin, successful mTLS and refusal without the client certificate, archive and WebSocket checks, capacity review, and confirmed pool enablement. |
| `intake:validator-active` | Explicit signing invitation, approved release and DA routes, finalized registration and active authority membership, advancing finality and authored blocks, plus required DA qualification. |

Operators report their preparation stage. A label cannot promote an account, bypass sponsorship capacity, prove DA repair, or guarantee a seat or reward. Public signing qualification remains pending. RPC qualification does not establish validator qualification.

Record the verification date, release/genesis, public receipt summary and private registry reference when applying a qualification label. Recheck qualification after a host, peer, network or release change; remove labels whose evidence no longer applies. Remove the relevant active label after RPC withdrawal or validator exit and record the disposition. Keep active records open for updates. Close a withdrawn registration at the operator’s request. If a separate request for sponsorship or activation is declined, record its outcome and use `status:wontfix` for that request. Maintainers may close a duplicate after linking the retained registration. No automatic funding, promotion or historical relabeling is introduced by this form.

## Rollout and maintenance

Merge the template and label definitions, verify the label sync, then publish the direct form link in the explorer and guide. Labels are tracked in `.github/labels.yml`; do not invent a parallel private status vocabulary. The existing generic access form and miner sponsorship limits are unchanged.

Validate forms and label wiring with:

```sh
uv run --no-project --with pyyaml python -m unittest discover -s tests -v
```

Revert the form, documentation and workflow changes to undo this routing. Existing issues and labels remain; preserve their history. The label sync does not delete labels removed from its source file. Remove unused labels separately only after checking registrations that reference them.
