---
Date: 2026-04-25 09:18
Tags: security, opinion, tech
---

# Passkeys are not enough

<!--
ASSISTANT NOTES — this is scaffolding for you to write against, not prose.

## Core thesis you outlined
- Passkeys are static secrets ("something you know", in the sense that they
  sit at rest in a vault and can be exfiltrated as a blob). They are great
  vs. phishing/credential stuffing but they don't add entropy at auth time.
- Real second-factor security needs something *dynamic*: a state revealed
  only at the moment of authentication (TOTP on a separate device, hardware
  key challenge-response). That's where entropy is preserved.
- Therefore: passkeys replace username+password well, but you still want a
  separate MFA factor on a separate device — e.g. Bitwarden + Aegis on the
  phone, never both in the same vault.

## Validating the Bitwarden CLI incident (April 22, 2026)
What actually happened (verified across multiple sources):
- The npm package `@bitwarden/cli@2026.4.0` was trojanized via a compromised
  GitHub Actions workflow, distributed for ~90 minutes (5:57pm–7:30pm ET).
- Part of the ongoing "Shai-Hulud: The Third Coming" / TeamPCP supply-chain
  campaign that previously hit Trivy, Checkmarx, LiteLLM.
- Payload (`bw1.js`) ran on install, harvested: GitHub/npm tokens, SSH keys,
  env vars, shell history, AWS/Azure/GCP creds, crypto wallet keys.
- Exfil method: AES-256-GCM encrypted blobs pushed to public GitHub repos
  under the victim's own account.

What did NOT happen — IMPORTANT for honesty in the article:
- Bitwarden's production servers and end-user vaults were NOT breached.
- No evidence (so far) that stored passkeys were exfiltrated from vaults.
- The CLI compromise affected developer machines that ran the bad version,
  not the vault itself.

So the framing needs care: this incident is a *cautionary signal*, not
direct proof that vault-stored passkeys were stolen. The argument is
"imagine if next time the compromise reached the desktop client or the
vault export path — your passkeys would be exfiltrable as static blobs,
unlike a TOTP seed living on a separate phone." You can sharpen the post
by making that hypothetical explicit rather than overclaiming.

Evidence of actual abuse: reports mention the exfil mechanism worked
(public repos appeared under victim accounts), so credential theft did
take place — but specifically dev secrets, not vault contents. Worth
saying plainly.

## "Passkeys ≈ static, TOTP ≈ dynamic" — the technical nuance
- Passkeys (FIDO2/WebAuthn) are actually *not* a shared secret transmitted
  on each login — they sign a server-issued challenge with a private key.
  In that sense they are dynamic at the protocol level.
- BUT the private key is stored at rest in the vault (or platform keystore),
  so if the storage layer is breached the key walks out the door. That's
  the static-at-rest problem you're pointing at.
- TOTP seeds are *also* static at rest — same problem. The real win of
  "Bitwarden + Aegis on a separate device" isn't dynamism per se, it's
  *factor separation*: an attacker has to compromise two independent
  devices/storage systems instead of one vault.
- Hardware keys (YubiKey) are the strongest case for your "dynamic" framing
  because the private key never leaves the device — it's not exportable
  even if the host is fully owned.
- Suggestion: reframe slightly from "static vs dynamic" to "single point of
  compromise vs. factor separation", with hardware keys as the pure form.

## Is Bitwarden + Aegis enough?
Threats it stops:
- Phishing (passkeys are origin-bound).
- Credential stuffing / password reuse.
- A breach of just the password manager (TOTP still on phone).
- A breach of just the phone (vault still requires master password).

Threats it does NOT stop:
- Malware on the device you're authenticating from (session token theft,
  AiTM proxies, browser-resident infostealers).
- Compromise of the master password via keylogger.
- Loss/theft of the phone with weak phone-level security.
- Supply-chain compromise of the apps themselves (the very lesson of the
  Bitwarden CLI incident).

Honest answer: nothing stops "all hacks". Goal is raising attacker cost
and shrinking blast radius, not hermetic safety.

## Aegis backup brittleness
Findings worth folding into the post:
- Aegis (open source, F-Droid) encrypts the vault with AES-256 keyed off
  the user's password; backups inherit that encryption.
- Built-in automatic backups only work to providers exposing Android's
  Storage Access Framework — Nextcloud is the canonical example. Most
  consumer clouds (Google Drive, Dropbox) don't, so users fall back to
  manual export.
- Brittle parts:
  * If you forget the vault password, the backup is unrecoverable. No
    escrow, no recovery codes for the vault itself.
  * Manual exports rot — people forget to do them.
  * If you only back up to the same phone you're protecting, a lost
    phone = lost 2FA.
  * Restoring on a new device after phone loss is the failure mode that
    pushes people to Authy in the first place.

## Authy alternative — tradeoffs
- Pros: real cloud sync, painless multi-device, easy recovery.
- Cons: closed source, Twilio-operated (and Twilio itself was breached in
  2022 — the irony writes itself), encryption tied to a backup password
  that Twilio could in principle weaken, desktop apps were sunset in 2024.
- Verdict to argue: convenience-vs-trust tradeoff. For a security-minded
  audience, Aegis + your own sync wins; for non-technical family members,
  Authy's ergonomics may genuinely be the safer real-world choice (a
  recovered backup beats a perfect one you lost).

## Open-source cloud backup for Android (your direct question)
Options that actually exist:
- Nextcloud — fully open source, server + Android client, integrates with
  Aegis via SAF. Self-hosted or hosted by a provider (Hetzner, etc.).
  Closest match to "open source cloud backup provider for Android".
- Syncthing — open source peer-to-peer sync. Note: the official Syncthing
  Android app was discontinued December 2024; community forks (syncthing-fork
  on F-Droid) are still maintained. Not "cloud" in the SaaS sense — needs
  another always-on node (NAS, home server, VPS).
- Seafile — open source self-hosted, Android client exists.
- rclone (with a script + Termux) — power-user route, can target any
  S3-compatible backend.
- Tertiary: any S3-compatible storage (Garage, MinIO self-hosted, Backblaze
  B2 with rclone) — open-source clients, not necessarily open-source
  service.

The honest answer: there is no "open-source SaaS cloud backup provider"
in the Dropbox sense. The open-source path is self-hosted (Nextcloud /
Seafile / Syncthing) or hosted-instance-of-open-source-software. Worth
calling that out plainly in the post — it's a gap in the ecosystem.

## Suggested article shape (you decide, this is just a sketch)
1. Hook: the Bitwarden CLI npm incident, what was/wasn't compromised.
2. Why it should still spook you even though vaults were untouched.
3. Passkeys: what they are, what they fix, what they don't.
4. The factor-separation argument (Bitwarden + Aegis + ideally a
   hardware key).
5. Is that enough? Honest list of remaining threats.
6. The backup problem: Aegis brittleness, Authy tradeoffs.
7. Open-source backup landscape for Android — the Nextcloud answer
   and the gap where a true OSS SaaS would sit.
8. Closing: there is no perfect setup; the goal is layered cost.

## Open questions for you to decide
- Do you want to name TeamPCP / Shai-Hulud explicitly or stay generic?
- Do you want to recommend a specific hardware key (YubiKey 5, Nitrokey,
  Token2)?
- Do you self-host Nextcloud? If so, anecdote material.
- Tone: technical deep-dive or opinionated rant? Recent posts lean rant.

## Sources to cite (pick what you want)
- The Hacker News: https://thehackernews.com/2026/04/bitwarden-cli-compromised-in-ongoing.html
- BleepingComputer: https://www.bleepingcomputer.com/news/security/bitwarden-cli-npm-package-compromised-to-steal-developer-credentials/
- Endor Labs writeup: https://www.endorlabs.com/learn/shai-hulud-the-third-coming----inside-the-bitwarden-cli-2026-4-0-supply-chain-attack
- Socket: https://socket.dev/blog/bitwarden-cli-compromised
- OX Security: https://www.ox.security/blog/shai-hulud-bitwarden-cli-supply-chain-attack/
- Bitwarden official statement: https://community.bitwarden.com/t/bitwarden-statement-on-checkmarx-supply-chain-incident/96127
- Aegis project: https://github.com/beemdevelopment/Aegis
- Aegis FAQ on backups: https://github.com/beemdevelopment/Aegis/blob/master/FAQ.md
- Aegis cloud-sync issue (SAF discussion): https://github.com/beemdevelopment/Aegis/issues/258
-->

