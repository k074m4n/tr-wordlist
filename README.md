# 🔐 Password Self-Audit Toolkit · Turkish Combinator

![Platform](https://img.shields.io/badge/OS-Parrot%20Security-05C3DD?logo=parrotsecurity&logoColor=white)
![hashcat](https://img.shields.io/badge/tool-hashcat-EE0000)
![Python](https://img.shields.io/badge/python-3.x-3776AB?logo=python&logoColor=white)
![Seed](https://img.shields.io/badge/seed-1193%20words-success)
![Rules](https://img.shields.io/badge/rules-light%20%7C%20medium%20%7C%20strong-yellow)
![Scope](https://img.shields.io/badge/scope-own%20data%20only-important)

A small toolkit for testing the resilience of passwords you are authorized to audit against
**1/2/3-word combinations of Turkish words** and progressively stronger rule layers.
The steps below let you build and run your own wordlist even if you have never used
hashcat before.

> [!WARNING]
> These tools are intended only for passwords, hashes, and systems you are authorized
> to test. Unauthorized access may be illegal. You are responsible for how you use them.

---

## 📑 Table of Contents

1. [How it works](#-how-it-works)
2. [Prerequisites](#0️⃣-prerequisites)
3. [Download the repository](#1️⃣-download-the-repository-and-enter-it)
4. [Install the tools](#2️⃣-install-the-tools-and-check-the-gpu)
5. [Generate rules](#5️⃣-generate-rule-files)
6. [Prepare the seed](#6️⃣-prepare-the-seed-add-your-own-words)
7. [Combinations & size](#7️⃣-combinations-and-size)
8. [Rule layers](#8️⃣-rule-layers-light--medium--strong)
9. [Attack plan](#9️⃣-attack-plan-step-by-step)
10. [View the result](#-view-the-result-and-continue)
11. [Troubleshooting](#-troubleshooting)
12. [Quick summary](#-quick-summary-copy-and-run)

---

## 🧭 How it works

```
turkce_tohum.txt (1,193 Turkish words, ASCII)
        │
        │   + benim.txt (your words: name, city, year, etc.)
        ▼
   normalize.py  ──►  tam_tohum.txt
        │
        ▼
kombinasyon_uret.py ── 1/2/3-word ordered combinations ──►  hashcat
                                                          ▲
                            hafif.rule / orta.rule / sert.rule
```

People often build passwords by combining familiar words: `kahve`+`kitap`+`2026` =
`kahvekitap2026`. This toolkit tests that pattern using a Turkish-focused seed.

---

## 0️⃣ Prerequisites

| Required | Why |
|---------|-------|
| **Parrot OS** (or Kali / any Linux) | Environment where the tools run |
| **Python 3** | The scripts are written in Python 3 (`python3 --version`) |
| **hashcat** | Password-testing engine |
| **A GPU** | 3-word combinations create billions of candidates; CPUs can be very slow |

> [!NOTE]
> The scripts use only standard Python 3; **no additional pip packages are required**.

---

## 1️⃣ Download the repository and enter it

```bash
git clone https://github.com/k074m4n/tr-wordlist.git
cd tr-wordlist
```

Check that the files are present:

```bash
ls
# expected: README.md  tohum_uret.py  turkce_tohum.txt  normalize.py
#           kombinasyon_uret.py  kural_uret.py  hafif.rule  orta.rule  sert.rule
```

---

## 2️⃣ Install the tools and check the GPU

Check whether they are installed:

```bash
which hashcat python3
```

Install anything that is missing:

```bash
sudo apt update && sudo apt install -y hashcat
```

Verify that hashcat can see the GPU and check its speed:

```bash
hashcat -b
```

> [!TIP]
> Note the value on the **`Speed`** line (e.g. `450.5 kH/s`). Use this for
> time estimates: `time = candidate_count ÷ Speed`.
> If the GPU is not visible, verify that hashcat is working with `hashcat -I` and check the device list.

---

## 5️⃣ Generate rule files

Generate the three-tier rule set:

```bash
python3 kural_uret.py
```

Expected output:

```
hafif.rule : 32 rules
orta.rule  : 189 rules
sert.rule  : 732 rules
```

> The files are included in the repository; this command regenerates them if you changed them.

---

## 6️⃣ Prepare the seed (add your own words)

**a.** Generate the core seed (included in the repository; regenerate it if needed):

```bash
python3 tohum_uret.py
# output: Total unique (ASCII) words: 1193
```

**b.** Add your own specific words. For your authorized audit, put
your relevant words here — your name, surname, birth year, city, pet,
team, or old password fragments. Turkish characters are fine,
the next step normalizes them:

```bash
nano benim.txt
```

Example contents (one word per line):

```
Ahmet
İstanbul
1998
beşiktaş
mırmır
```

**c.** Combine the core seed with your own words → convert to ASCII → deduplicate:

```bash
cat turkce_tohum.txt benim.txt | python3 normalize.py > tam_tohum.txt
wc -l tam_tohum.txt        # shows how many words there are
```

> [!NOTE]
> `normalize.py` converts Turkish characters to ASCII (`İstanbul→istanbul`,
> `Aşkım→askim`), converts to lowercase, and removes duplicates. Because people
> often type passwords as they speak, without Turkish characters (`askim`, `bitanem`).

---

## 7️⃣ Combinations and size

`kombinasyon_uret.py` generates **ordered** combinations from the seed: `aliveliahmet`,
`aliveli` (no repeated word), `aliahmetveli`, `veliahmet`…
(order matters, and the same word is not used twice in one combination).

First **estimate the size** (it only counts; nothing is generated):

```bash
python3 kombinasyon_uret.py tam_tohum.txt --estimate
```

Expected size for the 1,193-word seed:

| Tier | Candidate count | If written to disk |
|--------|-------------|-----------------|
| 1 word | 1,193 | — |
| 2 words | ~1.42 million | small file |
| 3 words | **~1.70 billion** | ~25 GB ⚠️ |

> [!WARNING]
> Do **NOT write 3-word combinations to disk** (`-o` writes to a file). Pipe them directly to hashcat
> with `|` (pipe) — otherwise a file of roughly 25 GB is created. Writing 1- and 2-word combinations
> to a file is fine (they are small).

---

## 8️⃣ Rule layers (light · medium · strong)

Rules transform each candidate: capitalization, appending numbers/years, and leetspeak
(`a→@`, `o→0`, `e→3`). This means the single word `askim` can produce `Askim`, `askim123`,
`askim2024`, `4skim` and dozens of other variants can be generated.

| Tier | Rules | What it does | Where to use it |
|:------:|:-----:|----------|---------------|
| 🟢 **hafif** | **32** | Capitalize the first letter, append a single digit / `123` / recent years (2020–26), a few symbols, basic leetspeak (`o0 e3 i1`) | Speed first; first pass on the large (3-word) base |
| 🟡 **orta** | **189** | Light + `00–99` suffixes, `1980–2030` years, `uppercase+digit`, extended leetspeak, symbol+digit | balanced scan on 1–2-word bases |
| 🔴 **sert** | **732** | Medium + leading digits, `000–499` suffixes, multiple leetspeak combinations, duplicate/reverse, symbol×digit | deep scan on 1–2-word bases |

**Example transformations**:

```
hafif  ·  askim   ->  Askim   ASKIM   askim1   askim123   askim2024
orta   ·  efsane  ->  efsane1998   Efsane2024   3fsan3(e→3)   efs@ne(a→@)
sert   ·  anan    ->  anan2000   1anan   anan000   @n@n(multiple leetspeak)   Anan
```

> [!IMPORTANT]
> **Rules multiply the candidate count.** Choose the tier based on the base size:
 > - **1–2-word base** (~1.42M) → `sert` can still be used, producing ~1.04 billion candidates.
> - **3-word base** (~1.70 billion) is already enormous → use **no rules** or at most `hafif`.
>   `orta`/`sert` would produce about 320 billion candidates (1.70 billion × 189).

Rough multiplication (base × rule count = total candidates):

| Base | × hafif (32) | × orta (189) | × sert (732) |
|-------|:---:|:---:|:---:|
| 1+2 words (~1.42M) | ~45M | ~269M | ~1.04 billion |
| 3 words (~1.70 billion) | ~54 billion ❌ | ❌ | ❌ |

<details>
<summary>📖 Rule syntax (for reference)</summary>

```
:      do nothing (try the word as-is)
c      capitalize first letter      u  all uppercase      t  swap case
r      reverse          d  duplicate the word
$X     append X          ^X  prepend X    sXY  replace X with Y
```
Example: `c$1$2$3` → `askim` ⇒ `Askim123`  ·  `se3` → replaces `e` with `3`.
</details>

Parrot also includes ready-made rules: `ls /usr/share/hashcat/rules/`
(`best64.rule`, `rockyou-30000.rule`, `dive.rule`).

---

## 9️⃣ Attack plan (step by step)

Start with the cheaper stages. Move to the next stage only if the previous one does not find a match.

### 🟢 Stage A — 1+2 words + progressive rules (file-based)

2-word combinations are small enough to write to a file. With a file-based run, hashcat provides
**progress, ETA, and pause/resume** information.

```bash
# write 1+2-word combinations to a small file (~1.42M lines)
python3 kombinasyon_uret.py tam_tohum.txt --max 2 -o w12.txt
wc -l w12.txt

# light first; if no match, medium; if no match, strong:
hashcat target.hash w12.txt -r hafif.rule
hashcat target.hash w12.txt -r orta.rule
hashcat target.hash w12.txt -r sert.rule
```

In this command: `target.hash` = target · `w12.txt` = candidate list · `-r ...` = rule file.

### 🔵 Stage B — 3 words, no rules (pipe)

Three-word passwords such as `aliveliahmet` are tested here. The candidates are streamed directly
to hashcat without being written to disk:

```bash
python3 kombinasyon_uret.py tam_tohum.txt --min 3 --max 3 | hashcat target.hash
```

> [!TIP]
> When fed through `stdin` (pipe), hashcat does not know the total candidate count → **it does not show an ETA**;
> this is normal. Calculate the time yourself: e.g. 1.70 billion ÷ 450k H/s ≈ **63 minutes**.

### 🟠 Stage C — 3 words + light rule (optional, heavy)

Only use this if necessary and you have enough time (≈54 billion candidates → can take hours):

```bash
python3 kombinasyon_uret.py tam_tohum.txt --min 3 --max 3 | hashcat target.hash -r hafif.rule
```

---

## 🎉 View the result and continue

When a password is found, the screen shows `Status: Cracked`, and the password appears next to the hash.
To view it again later:

```bash
hashcat target.hash --show
```

- Found passwords are stored in `~/.local/share/hashcat/hashcat.potfile`.
- Stop Stage A with `q` and resume later: the same command with `--restore`
  (pipe/stdin stages cannot be resumed; only file-based stages can).
- To test the same hash from the beginning, ignore the potfile: `--potfile-disable`.

---

## 🛠 Troubleshooting

| Symptom | Cause / Solution |
|---------|---------------|
| `No hashes loaded` | `target.hash` is empty or the path is wrong; check it with `cat` |
| `No devices found/left` | No GPU driver; `hashcat -I` to view devices, install the driver; for testing, `--force` (slow) |
| Very slow | The CPU may be used instead of the GPU; select the GPU with `-D 2`; increase the workload with `-w 3` |
| Nothing found | Expand the seed (add your own words), then continue with Stages B/C; the password may not be in the list |
| `nano: command not found` | Use another editor: `vi benim.txt` or a desktop text editor |

---

## ⚡ Quick summary (copy and run)

```bash
# 0. enter the repository
cd YOUR_REPOSITORY

# 1. generate the rules
python3 kural_uret.py

# 2. seed + your own words
python3 tohum_uret.py
nano benim.txt          # enter your own words
cat turkce_tohum.txt benim.txt | python3 normalize.py > tam_tohum.txt

# 3. estimate the size
python3 kombinasyon_uret.py tam_tohum.txt --estimate

# 4. Stage A: 1+2 words, progressive rules
python3 kombinasyon_uret.py tam_tohum.txt --max 2 -o w12.txt
hashcat target.hash w12.txt -r hafif.rule
hashcat target.hash w12.txt -r orta.rule
hashcat target.hash w12.txt -r sert.rule

# 5. Stage B: 3 words (pipe, no rules)
python3 kombinasyon_uret.py tam_tohum.txt --min 3 --max 3 | hashcat target.hash

# 6. result
hashcat target.hash --show
```

---

## 🗂 Files

| File | Purpose |
|-------|-----|
| `tohum_uret.py` | Generates the Turkish core seed → `turkce_tohum.txt` (1,193 ASCII words) |
| `turkce_tohum.txt` | Ready-made core list (affection, slang, colloquial Turkish, English, keyboard patterns…) |
| `normalize.py` | Converts words to ASCII + lowercase and deduplicates them |
| `kombinasyon_uret.py` | Generates ordered 1/2/3-word combinations (streams to stdout) |
| `kural_uret.py` | Generates `hafif.rule` / `orta.rule` / `sert.rule` |
| `hafif/orta/sert.rule` | Progressive rule layers (32 / 189 / 732) |

> [!NOTE]
> `target.hash`, `benim.txt`, `tam_tohum.txt`, `w12.txt`
> such as **personal/large** files are excluded via `.gitignore` and are not committed to the repository.

---

## 🎯 Security lesson

Meaningful word combinations such as `sampiyonmehmet` may *look* strong but can be weak against targeted
Turkish combinator + rule attacks. For real resilience,
use a password-manager-generated, **random, high-entropy** (16+ characters,
non-word) password.
