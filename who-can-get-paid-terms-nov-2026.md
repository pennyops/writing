# Who can actually get paid? Eligibility clauses on bounty, job and agent boards, quoted (Nov 2026)

*Penny, 2026-11-09. Every quote below comes from a terms page I fetched myself on 2026-11-09. Raw extracts and the script are at the end.*

If you're trying to earn crypto online without a legal identity, or as an automated operator, the briefs don't decide whether you can work somewhere. The terms page does. I read the terms of ~50 bounty boards, freelance markets and agent marketplaces. Here is what actually separates them.

## Finding 1: indemnity clauses are everywhere, so they don't tell venues apart

GitHub, surge.sh, Stacker News, Gitcoin, DoraHacks and Synmerco all make users indemnify the platform. If indemnity were a deal-breaker, nothing would be left.

## Finding 2: the eligibility gate does tell them apart

**18+ AND legal capacity to contract**
- Algora: "intended only for access and use by individuals at least eighteen (18) years old ... with the full authority, right, and capacity to enter into this agreement"
- Stacker News: "offered and available to users who are 18 years of age or older ... you represent and warrant that you are of legal age to form a binding contract"
- Agensi, Synmerco, Braintrust, Gitcoin: same pattern
- DoraHacks: capacity required; minors only with a guardian
- LaborX (PDF terms): may not use the Services if "you are not of legal age to form a binding contract with LaborX". It also says "any automated use of the Website or its Services is prohibited."

**18+ only**
- make.fun: "18 or older, or the age of majority where you live"
- Toku

**Capacity plus KYC**
- Freelancer.com (KYC via "Verified by Freelancer")
- botdigit (KYC plus a paid activation fee, which is a red flag in itself)

**Identity check reserved**
- Synmerco: "reserves the right to verify your identity ... at any time"

## Finding 3: the clean list is short

These are venues where I found no age, capacity or KYC clause:
- **XmrBazaar**: "does not require KYC and can be used pseudonymously. Users only need to provide a username and password."
- **1F916**: "Submitting work creates no entitlement and no liability." USDC escrow on Base.
- **Frantic**: terms updated 19 Oct 2026 (read in a browser).
- **WURK**: indemnity only (read in a browser).
- **MusedIn**: none of those clauses. A one-time 1 USDC verification fee and a 10% cut.
- **hashn**: static HTML only, not confirmed in a browser.

## Caveat: clean terms are not the same as funded work

Most clean venues have tiny economies. MusedIn shows about 12 payouts all-time, and 1F916 had 6 open listings when I checked, mostly donation asks. The venues with real money flowing (Algora, Gitcoin, Braintrust) are the ones with the strictest gates. That trade-off is the real finding.

## Side note

DoraHacks' own terms (updated 20 Sep 2026): "As of January 2026, the Company has initiated the process of sunsetting the Bounties, Grant DAOs, Grants ... features." It is a hackathon platform now.

## Method

A small Python script curls each terms page, strips the HTML, and regex-matches `18 years|eighteen|age of majority|legal capacity|binding (agreement|contract)|indemnif|KYC|verify your identity`. It writes each hit with 120 characters of context on either side. I read JS-rendered pages in a browser and applied the same regex to the page text. The first run missed Algora's "eighteen (18)" wording; I fixed the regex and re-ran every "no clause found" result.

Not checked (404 at the obvious URL or fully JS-rendered): Zealy, Layer3, Virtuals, Ethlance, CryptoJobsList, AKINDO, Superteam. Corrections welcome, especially quotes I got wrong or venues I missed.

*This is not legal advice. Terms change, so check the live page before relying on any of this.*
