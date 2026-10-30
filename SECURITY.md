# Security Policy

**Do not open a public issue for a vulnerability.**

This repository takes reports about a network people run. The findings that matter most are the
ones that must not be published first: a way to get unverified inference accepted, to avoid a slash
you earned, or to take funds out of an escrow, HTLC, or voucher flow. Filing one of those as an
issue publishes an exploit.

## How to report

1. **GitHub private vulnerability reporting** — [open a private
   advisory](https://github.com/flop-labs/network/security/advisories/new). Preferred: it keeps the
   report, the discussion, and the eventual disclosure in one place.
2. **Email** — `security@flop.finance`, if you would rather not use GitHub, or to send PGP.

Include the network (devnet or testnet), the release, commit or image digest you ran, and a
concrete attack: who deviates, what it costs them, and what they gain. A reproduction we can run —
a transaction, a request, a failing test — is usually the whole report. A rough report is better
than none.

## What counts

Report privately:

- **Verification bypass** — getting an inference accepted without doing the work, forging or
  replaying attestations, defeating TOPLOC or sampled re-execution, misreporting the model or
  hardware that served a request.
- **Slashing evasion** — avoiding a penalty you incurred, or causing an honest operator to be
  slashed.
- **Metering** — inflating effective FLOP or rewards, under-reporting work.
- **Escrow, HTLC, and voucher flows** — theft, double redemption, unfair settlement, refund races.
- **Consensus** — equivocation that goes unpunished, committee capture, finality stalls you can
  trigger on purpose.
- **Data availability** — withholding data without being slashed, evading audits.
- **Keys and accounts** — anything that exposes a signer, session key, or spending limit.

Open a public issue instead when the finding is "this does not work well" rather than "this can be
exploited": a crash with no attacker benefit, a bound you think is loose, an incentive you find
unconvincing. Disagreement with the specification itself goes to
[flop-labs/yellowpaper](https://github.com/flop-labs/yellowpaper). When it is unclear which one you
have, report privately and we will move it into the open together.

## What to expect

- **Acknowledgement within 3 business days.** If you do not hear back, please re-send — a missed
  report is our failure, not a rejection.
- **An assessment within 14 days**, saying whether we agree it is exploitable and what we intend to
  do about it.
- **Credit** in the advisory, unless you prefer to stay anonymous.
- **Coordinated disclosure.** We will agree a timeline with you rather than impose one.

## Scope and honesty about it

FLOP is **pre-mainnet**. Devnet and testnet tokens carry no value, and there is **no bug bounty
program at this time** — we will not pretend otherwise to attract reports. What we can offer is a
real technical response, public credit, and a record of what your finding changed.

Availability problems on devnet and testnet (a node that falls over under load) are welcome but
low severity unless they break safety or let someone profit.
