# Space Base strategy

Space Base is a race to 40 VP where you build a 12-sector dice engine: on your turn you take blue (station) rewards, and on everyone else’s turn you take red (deployed) rewards. Player count and Light Speed both change which of those two sides actually wins games.

The rest of this is a table guide: shared engine math first, then four complete playbooks.

## The rules of the engine (all modes)

**Allocation.** Two d6s. You pick both singles or the sum.

- **Doubles** (both dice the same 1–6): that sector fires twice. Double 6s pay 6 twice. Double 4s pay 4 twice. Same rule for every low sector.
- **Two different 1–6 numbers:** taking singles pays both sectors. A 2 and a 5 is two rewards. A 6 and a 3 is also two rewards — 6 double-hits this way too.
- **Sum:** one reward on 2–12.

Every 1–6 can double-hit. Sector 6 just does it most often: most faces, leftover sum-to-6s, and the same two-payout singles/doubles as 1–5.

Rough hit rates (singles or sum, no dice fixing; doubles count as two hits on that sector):

| Sector | Hits / 36 | Chance |
| ------ | --------- | ------ |
| 6      | 17        | 47%    |
| 5      | 16        | 44%    |
| 4      | 15        | 42%    |
| 3      | 14        | 39%    |
| 2      | 13        | 36%    |
| 1      | 12        | 33%    |
| 7      | 6         | 17%    |
| 8      | 5         | 14%    |
| 9      | 4         | 11%    |
| 10     | 3         | 8%     |
| 11     | 2         | 6%     |
| 12     | 1         | 3%     |

So 1–6 fire constantly and pay small. 7–12 fire rarely and pay huge. Cards are priced around that, but not perfectly: a 6 is noticeably better than a 3 with the same text; an 11 is almost always better than a 12 with similar text. Prefer 6 given equal text because it hits more — not because it is the only sector that can pay twice.

Buying a ship in a sector deploys whatever was there. That is how red engines get built. Sometimes the right buy is a mediocre new ship whose whole job is to flip a strong red.

**Income is a floor, not a salary.** After you buy, if credits are below income, you refill up to income. Gold from the roll can be spent the same turn. Extra gold above income only exists if you stop buying. That is why “buy every turn” is correct with high income, and “save” is for a colony or a level 3 that costs more than one refill.

**Colonies** are 3 gold → 1 VP, immediate, and they permanently lock that sector (no more stationing there; deployed ships in that sector still fire on red). They are the standard way games actually end.

### What actually decides games

- Player count (red vs blue frequency, and how many of your turns you get).
- Whether you overspend (top players leak far less gold than average).
- Whether you notice the opponent’s arrow chain / You Win setup in time to hate-draft it.
- When you stop building and start converting gold into colonies.

### The one table that should change how you draft

|                                | 2p   | 3p   | 4p   | 5p   |
| ------------------------------ | ---- | ---- | ---- | ---- |
| Red chances / round            | 1    | 2    | 3    | 4    |
| Blue chances / round           | 1    | 1    | 1    | 1    |
| Typical rounds                 | ~21  | ~18  | ~15  | ~12  |
| Red hits / game                | ~21  | ~36  | ~45  | ~48  |
| Blue hits / game               | ~21  | ~18  | ~15  | ~12  |

**2p is a blue/income engine game.** Red is a bonus. **3p is the pivot count.** Red is already twice as common as blue. Income still matters, but “flip it to red” and “score on other people’s dice” start beating long blue snowballs.

## 1. Two-player, normal start

**Shape of the game:** ~20 of your turns. You roll every other turn. Income compounds for a long time. Arrow chains on blue 7–11 are the most broken thing in the matchup. Gordon (the −VP ship) is only okay. You Win is real if you build support; it is a trap if you don’t.

### Opening (turns 1–6)

Standard start is 5 gold and one random level 1 (you pay its cost). Second player gets +1 gold. That opening card is luck; your job is to not let a mediocre one dictate the whole game.

Buy priority, in order:

1. **Income on 5–8.** Even +1 income in the first few rounds can win 2p by itself. A 7 or 8 that is “2 gold + 1 income” is often the best card on the table for a long stretch.
2. **Arrows on 7–11.** These are your combo skeleton. A right-arrow on 7 into a point/income 8 is already a plan.
3. **2-gold cargo on 4–6.** Frequency plus cash. Prefer 6 over 5 over 4 given equal text.
4. **Dice plus / reroll / set-a-die.** Not first, but get two manipulators over the game. They turn a 12-sector from a lottery into a job.

Usually skip early: 1 VP on 1–6, green “add to the sum” with no target yet, expensive 12s, Gordon, You Win, sector-swap cards.

**Buy vs save:** Early, buy almost every turn if the card is efficient. If you have 6 gold and every level 1 is 3, pass. Waiting one turn for a level 2 is how you stop leaking gold. That leak is one of the few stats that actually separates strong players from average ones.

### Midgame (turns 7–14)

You want one of these engines. Mix them; don’t worship one.

**A. Income snowball (default 2p plan)**

- Stack income on 7/8, and on 5/6 if the card is good.
- Spend down every turn so the floor refill actually works.
- Once income is 5–8, you can afford level 2s and cheap colonies without ever going broke.
- Finish with colonies on dead or weak sectors (often 1, 2, 11, 12).

**B. Blue arrow chain (highest ceiling)**

- Right-arrows on 7 and 8 into a fat 9, or 8–9–10 into a 10/11 VP pile.
- Add “increase the sum” so a 4+ total still reaches the chain.
- A 7+8 arrow into a 7-VP 9 is already ~42% to score that 7 VP on your turn.
- Opponent’s job is to take the next arrow. Your job is to take it first even if it is slightly off-role.

**C. Swap line (2p-only, slow, real)**

- The 9 that swaps with one charge: swap onto 6, then swap a 11/12 onto 6. Now your best blue lives on the most common number.
- Only do this in 2p. 3p usually ends before the second swap pays.

**D. You Win**

- Do not buy it unless you already have “put a cube on any card” and/or “place then move a cube,” plus dice fixing.
- Late-game You Win with no support is a wasted 12 and a gift to the opponent.

**Deploying:** In 2p you deploy because you needed a better blue in that sector, not because red is your main plan. Exception: a red rocket on 5/6 is still excellent because your opponent rolls ~21 times too.

### Closing (turns 15+)

Race math, not engine math.

- Colonies are 3 gold per VP. A shiny level 3 that might fire twice is often worse than 8 VP in colonies now.
- If income is high (6+), not buying is expensive; take the colony that fits.
- If income is low, saving for the 8–10 VP colony can be right.
- Watch their gold + income + face-up colonies. If they can hit 40 next turn, you buy the colony they need or you burst yourself over. Deny the 3-gold-per-VP they were counting on.
- Do not colony-lock a sector that is still your blue engine (a 7-income, an arrow keystone, a charged green). Colony the sectors you already outgrew.

### 2p hate-draft list

Take these away even if they are only okay for you:

- The arrow that completes their 7–10 chain
- The cube-placement card if they took You Win
- The last cheap colony they can afford this turn
- A 5/6 income if they are on the income plan and you can still use it

Gordon is not a panic buy in 2p. Score in bursts with colonies so −3 VP does not keep you under the line.

## 2. Three-player, normal start

**Shape of the game:** ~18 rounds, but only ~18 of your turns vs ~36 red opportunities. Red is now the main scoring channel. Games end sooner, so long blue-only engines get sniped by someone who scored on other people’s dice.

**Turn-order patch:** P2 +1 gold, P3 +2 gold. P3 should spend that extra gold on an actual engine piece, not a vanity 12.

### How 3p is not “2p plus one”

| 2p | 3p |
| -- | -- |
| Income on blue is king | Income is still good; red income / red rockets are better |
| Arrow chains on blue 7–11 | Arrow chains on red, and “buy to flip” |
| 20 turns to assemble a combo | You get maybe 12–14 meaningful buys. Combos must be short |
| Swap / You Win / slow dice-fix are playable | Those are usually too slow unless they come together for free |
| Gordon is fine | Gordon is actually scary (hits two people) |
| Colony later | Colony earlier |

### Opening

Same first-card lottery, less time to recover.

Buy priority:

1. **Anything that will be strong after it flips** — red rockets on 4–6, red income, red arrows into a loaded sector.
2. **Blue income on 5–8** if you can’t get a flip plan. You still have ~18 income ticks; that is not nothing.
3. **Low-sector (1–6) cargo that you intend to cover.** In 3p, buying a better 6 in order to deploy a 2-rocket 6 is a standard winning line.
4. **Arrows on 8–11** that will sit on red after the next buy.

**Rush line (very strong at 3p):** live on 1–6, get rockets onto red as soon as you can, start taking 4–8 VP colonies around 10–20 VP instead of waiting for a beautiful board. The person still “building” loses to the person who converted.

**Income line:** only if you can flip income to red or the income is on a 7/8 you will keep as blue and you are buying rockets elsewhere. Pure blue income with no red plan is how you come third.

### Midgame

Build a red stack on one or two numbers, then feed it.

- **Best stack numbers:** 5 and 6 (frequency), then 7 and 8 (power). Stacking 12 without arrows or plus-dice is a hobby, not a strategy.
- **Red arrows are a double dip:** you get the arrow sector and the target. A deployed arrow on 9 into a loaded 10 is why 3p games suddenly end.
- **Dice-plus cards** are for aiming at that stack, not for a general “high numbers” identity.
- **Buy to deploy is the 3p skill.** Ask every turn: “If I overlay this sector, is the red I just created worth more than the blue I lost?” At 3p the answer is yes much more often.
- **Gordon:** respect it. Counter is not a specific card. Counter is burst scoring — colonies, a 6-rocket 7, anything that jumps you 8–12 VP in a window so −3/−4 cannot keep you pinned. Do not sit at 37 hoping they miss.

### Closing (starts earlier than you think)

In 3p, “a few more engine turns” is how you watch someone else buy two colonies and end it.

- Start looking at colonies when anyone is in the mid-20s, or when you have 12+ gold and no card that is clearly worth more than 4 guaranteed VP.
- Lock sectors that are already deployed-out and not part of your red stack.
- Two opponents means two finish lines. Track both gold piles. Hate-draft the colony that lets the leader close; the other player’s slightly better ship can wait.
- If two people are on arrow races, take the connecting arrow even if it does nothing for you. 3p combos are fragile; one stolen card ends them.

### 3p opening traps

- Saving for a slow 12-swap.
- Buying You Win on turn 4 with no cube movers.
- Taking 1-VP 1–6s while someone else is flipping 2-rocket 6s.
- Ignoring red because “the blue side is bigger.” Bigger per hit, half as many hits.

## 3. Light Speed: what the variant actually changes

Official setup:

- Start with 15 gold and 1 income (not 5 gold).
- Draw four level 1s and two level 2s.
- Buy as many as you can afford. Leftover gold is kept.
- Unbought cards go under their decks.
- Most leftover gold goes first. Tie: highest sector purchased, then a roll.
- Seat bonuses are the same as normal (2p: P2 +1 gold; 3p: P2 +1, P3 +2).

This is not a different game. It is turns 1–5 played as a draft, then a shorter remaining race. Variance is similar to a normal game that has already reached turn 4; skill goes up because you choose the start instead of eating a random level 1.

**The market is part of the opening.** Look at the face-up shipyard (especially juicy level 2/3s and the cheap colonies) before you spend your 15. Leftover gold is both tempo and first player.

### How to spend the 15 (all Light Speed games)

Rank the six cards, then pick a **package**, not six independent greeds.

**Spend a lot (down to 0–4) when:**

- Two cards stack the same sector (especially 5/6 or 7/8).
- You can start with income already on a good number and a second ship that will flip it.
- You get a real arrow into a real payoff (not an arrow into a starter 2-gold).
- The two level 2s actually synergize (arrow + payload, cargo + income, plus-dice + high slot).

**Keep 8–12 gold when:**

- The six cards are scattered junk.
- The board has a 5/6 income, a key arrow, or a level 3 you can buy on turn 1.
- You want first player in a 2p race (first player with 10 gold and 1 income often beats the person who spent to 0 on two uncoordinated 3-cost ships).

**Keep ~15 and buy nothing when:**

- The six are actively bad and a face-up level 3 is the game (classic: save, take a 3-cost-on-red-rockets 1–6, or a buy-extra-cards 2, on turn 1). This is more of a 3p/4p play. In 2p you usually want some engine because you will have more turns.

**Never auto-buy.** People lose Light Speed in the draft by spending 14 on a 12-arrow and a 1-VP 3.

**First player vs extra stuff:** in 2p LS, leftover gold → first is real. In 3p LS, a live red engine in front of two opponents is often worth going second.

## 4. Two-player Light Speed

Shorter 2p: still a blue/income game, but you skip the awkward poverty turns. Income 1 is already on. The winner is usually whoever leaves the draft with a plan plus enough gold to execute it on turn 1–2.

### Draft goals (2p LS)

- Income on 5–8, or a pair that will become that after one overlay.
- Blue arrows 7–10 if they chain. Two arrows that point at nothing are not a chain.
- Keep gold for a board income/arrow if your six don’t provide it.
- A 4–6 cargo plus a 7–8 payoff is a perfectly good “fair” start.

### Sample packages

- **Income first:** buy the 7-income, keep 8–11 gold, take first, buy the face-up 5/6 cargo or the missing arrow on turn 1.
- **Chain first:** 7-right + 8-right, keep a little gold, hunt the 9/10 payload in the market. This is the “you might just win” start; the opponent must steal the next arrow.
- **Reject the pack:** keep 12–15, go first, buy the actual good card in the shipyard. Correct more often than it feels.

### Play after the draft

Same 2p midgame, compressed:

- You already have income 1. Getting to 3–4 income still wins, but you need it in the first handful of turns, not by turn 10.
- Arrow chains still break the game. Hate-draft immediately; there are fewer turns to recover.
- Swap / You Win need the support to be in the opening six or the first two buys. Otherwise they are too slow for LS.
- Colony pivot is earlier than normal 2p. When anyone hits the mid-20s, start converting. Level 3s that need three charges often do not finish.
- Overspending hurts more because there are fewer refills left.

**2p LS win condition in one line:** leave setup with either (income + cash) or (arrow chain + a way to hit it), then take colonies before the opponent’s chain completes.

## 5. Three-player Light Speed

This is the sharpest of the four. Red engines can be live before turn 1. A 6 with rockets already deployed, or income already flipped, can look unbeatable. It is beatable if you convert faster, but you cannot “out-engine” it over 15 leisurely turns.

### Draft goals (3p LS)

- A sector that will score on red immediately. Two cards on 6, or a 5/6 you will overlay on turn 1, is the dream.
- Red arrows into a loaded number.
- Rockets on 1–6 more than pretty blue 11s.
- Enough leftover gold to buy the flip on turn 1 if you only got one half of a stack.

If someone else drafts a stacked 6 with red rockets, you are already in a rush game. Do not answer with a slow 12. Answer with your own 4–6 rockets and the first colonies.

### After the draft

- **Rush is the default.** 1–6, red rockets, colonies from the midgame, force 40 before fancy boards come online.
- Income is for buying the next rocket/colony every turn, not for a 2p-style 20-turn snowball.
- Gordon is live and hits two people. If it is in the opening six or on the board, respect it; don’t worship it. Burst still beats it.
- You Win is almost always a trap in 3p LS unless the cube movers came in the same draft.
- Hate-draft connecting arrows and the cheap colony the leader can afford. With two opponents, deny the leader, not the prettiest card.
- **Seat:** going first with 10 gold is nice. Going second with a deployed 2-rocket 6 and 4 gold is often better. Spend for the red stack; don’t hoard for first unless the six cards are bad.

**3p LS win condition in one line:** get red points on 5/6 (or a short red arrow) from the draft or turn 1, then buy colonies the moment you can close, because someone else is on the same clock.

## Shared tactics that win across all four

**Don’t overspend.** If the buy wastes 3+ gold, pass unless the card is a keystone (completing arrow, flip that creates red rockets, denial).

**One or two sectors, not twelve.** Feed a 6 and a 7, or a 8–10 chain. Wallpapering every slot with “okay” cards is how you never roll your payoff.

**Arrows are multiplicative.** Count the new hit rate. Arrow on 9 into 10 takes 10 from 3/36 to 7/36; plus-dice can take it to ~12/36. That is why arrows get stolen.

**Green dice control is support, not a strategy.** Two pieces of manipulation around a real target. Zero is too swingy in 2p; four with no payload is how you lose 3p.

**Colonies are the finish, not the engine.** Convert when:

- your next ship is unlikely to fire enough times to beat 3 gold/VP,
- someone can end it next round,
- income is high and saving would just refill anyway.

Never colony-lock your last working blue keystone in 2p, or your red stack number in 3p, unless that colony is the win.

**Watch the other board.** Every turn: their gold, income, VP, open arrows, You Win cubes, and which colony they can afford. Space Base feels like multiplayer solitaire until one stolen 3-cost arrow ends a 15-turn plan.

### “You Win” and Gordon

- **You Win:** only with cube placement/movement and time. Great in long 2p, rare in 3p, almost never in 3p LS.
- **Gordon:** weak in 2p, real in 3p. Beat it with burst VP, not with sitting at 38.

## Quick reference

| Mode | What you maximize | When you colony | What you steal |
| ---- | ----------------- | --------------- | -------------- |
| 2p normal | Blue income, blue arrows 7–11, dice fix | Late; after income 5+ | Their next arrow, cube movers, finishing colony |
| 3p normal | Red rockets 4–6, red arrows, short combos | Mid; when anyone is ~25 | Leader’s arrow/colony, flip-enablers |
| 2p Light Speed | Draft a plan + keep gold for turn 1 | Earlier than 2p normal | Same as 2p, faster |
| 3p Light Speed | Immediate red on 5/6 from the 15-gold draft | Early; this is a sprint | Leader’s close, stacked-sector follow-ups |

If you only remember four sentences:

1. 2p = income and blue chains; 3p = red stacks and earlier colonies.
2. Light Speed is an opening draft plus a shorter game — leftover gold is first player and your first buy.
3. Stop leaking gold; pass rather than buy a 3-cost with 6.
4. The opponent’s board is part of the market.
