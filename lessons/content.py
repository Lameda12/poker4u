"""All lesson text content for Poker4U."""

LESSONS = {
    1: {
        "title": "Hand Rankings & Probability",
        "subtitle": "Understanding base rates in decision making",
        "intro": (
            "Every great decision maker starts with understanding the basics: "
            "what outcomes are possible, and how likely is each one?\n\n"
            "In poker, this means knowing the hand rankings — which hands beat "
            "which — and the probability of being dealt each type of hand.\n\n"
            "In real life, this is called understanding **base rates**: the "
            "background probability of events before you have any other information."
        ),
        "sections": [
            {
                "title": "The Hand Rankings (Weakest to Strongest)",
                "content": (
                    "1. **High Card** (50.1%) — No pair, no draw. Just your highest card.\n"
                    "2. **One Pair** (42.3%) — Two cards of the same rank.\n"
                    "3. **Two Pair** (4.75%) — Two different pairs.\n"
                    "4. **Three of a Kind** (2.11%) — Three cards of the same rank.\n"
                    "5. **Straight** (0.39%) — Five consecutive cards of any suit.\n"
                    "6. **Flush** (0.20%) — Five cards of the same suit.\n"
                    "7. **Full House** (0.14%) — Three of a kind + a pair.\n"
                    "8. **Four of a Kind** (0.024%) — Four cards of the same rank.\n"
                    "9. **Straight Flush** (0.0014%) — Five consecutive cards of the same suit.\n"
                    "10. **Royal Flush** (0.00015%) — A-K-Q-J-T of the same suit."
                ),
            },
            {
                "title": "Key Insight: Rarity = Strength",
                "content": (
                    "Notice the pattern: the rarer a hand is, the stronger it ranks. "
                    "This isn't arbitrary — it's mathematical necessity.\n\n"
                    "A Royal Flush appears roughly once in 650,000 hands. "
                    "A pair appears in almost half of all hands.\n\n"
                    "This teaches us a fundamental lesson: **rare events carry more weight** "
                    "in decision making. A piece of evidence that occurs rarely is far more "
                    "informative than one that happens all the time."
                ),
            },
        ],
        "real_life_tip": (
            "When evaluating claims or evidence, always ask: \"How often does this "
            "happen normally?\" A positive medical test is only alarming if the "
            "disease is common (high base rate) or the test is very accurate. "
            "The same thinking applies to poker: a player raising doesn't "
            "necessarily mean they have a great hand — you need to know their "
            "base rate of raising."
        ),
        "quiz_intro": "Let's test your knowledge of hand rankings!",
    },
    2: {
        "title": "Expected Value (EV)",
        "subtitle": "The single most important concept in decision making",
        "intro": (
            "Expected Value is the average outcome of a decision if you could repeat "
            "it thousands of times. It's the mathematical foundation of rational "
            "decision making.\n\n"
            "**EV = (Probability of Winning × Amount Won) - (Probability of Losing × Amount Lost)**\n\n"
            "A positive EV (+EV) decision makes you chips over time. "
            "A negative EV (-EV) decision costs you chips over time. "
            "Great players consistently make +EV decisions."
        ),
        "sections": [
            {
                "title": "Simple Example: The Coin Flip",
                "content": (
                    "Someone offers you a bet: flip a coin.\n"
                    "Heads: you win $20. Tails: you lose $10.\n\n"
                    "EV = (0.5 × $20) - (0.5 × $10) = $10 - $5 = **+$5**\n\n"
                    "This is a +EV bet. You should take it every time, even though "
                    "you'll lose half the time. Over 100 flips, you'd expect to "
                    "profit about $500."
                ),
            },
            {
                "title": "Poker Example: The Big Decision",
                "content": (
                    "You have top pair. Pot is 100 chips. Opponent bets 50 chips.\n\n"
                    "You estimate you'll win 65% of the time.\n\n"
                    "EV of calling = (0.65 × 150) - (0.35 × 50)\n"
                    "EV = 97.5 - 17.5 = **+80 chips**\n\n"
                    "This is clearly +EV — call! Even though you'll lose 35% of the time, "
                    "the math strongly favors calling."
                ),
            },
            {
                "title": "The -EV Trap",
                "content": (
                    "You have a small draw. Pot is 40 chips. Opponent bets 40 chips.\n\n"
                    "You estimate you'll win only 20% of the time.\n\n"
                    "EV of calling = (0.20 × 80) - (0.80 × 40)\n"
                    "EV = 16 - 32 = **-16 chips**\n\n"
                    "This is -EV — fold! It feels like you're giving up, but "
                    "folding saves you 16 chips on average."
                ),
            },
        ],
        "real_life_tip": (
            "Apply EV thinking to big life decisions:\n\n"
            "Job offer A: $80K salary, 90% chance you'll enjoy it\n"
            "Job offer B: $120K salary, 40% chance you'll enjoy it\n\n"
            "If happiness matters equally to money:\n"
            "EV(A) = 80K × 0.9 = 72K 'happiness-adjusted dollars'\n"
            "EV(B) = 120K × 0.4 = 48K 'happiness-adjusted dollars'\n\n"
            "Job A has higher expected value despite the lower salary!"
        ),
        "quiz_intro": "Let's practice calculating Expected Value!",
    },
    3: {
        "title": "Pot Odds & Implied Odds",
        "subtitle": "Cost-benefit analysis for every decision",
        "intro": (
            "Pot odds tell you the price the pot is offering you to make a call. "
            "If the pot is giving you good enough odds compared to your chance of "
            "winning, calling is profitable.\n\n"
            "**Pot Odds = Cost to Call / (Pot + Cost to Call)**\n\n"
            "If your equity (chance of winning) exceeds the pot odds, calling is +EV."
        ),
        "sections": [
            {
                "title": "Calculating Pot Odds",
                "content": (
                    "Pot is 100 chips. Opponent bets 50 chips.\n\n"
                    "Pot odds = 50 / (100 + 50) = 50/150 = **33.3%**\n\n"
                    "You need at least 33.3% equity to profitably call.\n\n"
                    "Quick ratio: the pot is offering you 3:1 odds "
                    "(you risk 50 to win 150)."
                ),
            },
            {
                "title": "Counting Outs: The Rule of 2 and 4",
                "content": (
                    "An 'out' is a card that improves your hand to a likely winner.\n\n"
                    "Quick math:\n"
                    "- **Rule of 2**: Multiply outs × 2 for chance on next card\n"
                    "- **Rule of 4**: Multiply outs × 4 for chance by river (from flop)\n\n"
                    "Example: You have a flush draw (9 outs)\n"
                    "- Next card: 9 × 2 = ~18%\n"
                    "- By river: 9 × 4 = ~36%\n\n"
                    "Common outs:\n"
                    "- Flush draw: 9 outs (~36% by river)\n"
                    "- Open-ended straight draw: 8 outs (~32%)\n"
                    "- Gutshot straight draw: 4 outs (~16%)\n"
                    "- Two overcards: 6 outs (~24%)"
                ),
            },
            {
                "title": "Putting It Together",
                "content": (
                    "You have a flush draw on the flop. Pot is 80 chips. "
                    "Opponent bets 20 chips.\n\n"
                    "Pot odds = 20/100 = **20%**\n"
                    "Your equity = 9 outs × 4 = **~36%**\n\n"
                    "36% > 20% → **Easy call!** The pot is offering great odds.\n\n"
                    "But what if opponent bets 80 chips?\n"
                    "Pot odds = 80/160 = **50%**\n"
                    "Your equity = ~36%\n\n"
                    "36% < 50% → **Fold.** The price is too high."
                ),
            },
        ],
        "real_life_tip": (
            "Pot odds = ROI analysis.\n\n"
            "Startup decision: Invest $50K for a 20% chance at $500K return.\n"
            "EV = 0.20 × $500K - 0.80 × $50K = $100K - $40K = **+$60K**\n\n"
            "The 'pot odds' are favorable! But also consider implied odds — "
            "what happens AFTER the investment? Maybe success leads to a $5M "
            "company. That's like implied odds in poker: future payoffs that "
            "aren't in the current pot."
        ),
        "quiz_intro": "Let's practice pot odds calculations!",
    },
    4: {
        "title": "Position & Information Advantage",
        "subtitle": "Why acting last is a superpower",
        "intro": (
            "In poker, position means where you sit relative to the dealer. "
            "The player who acts LAST has a massive advantage — they get to see "
            "what everyone else does before making their decision.\n\n"
            "This is **information advantage**: the more you know before deciding, "
            "the better your decisions will be."
        ),
        "sections": [
            {
                "title": "Early Position vs Late Position",
                "content": (
                    "**Early Position (EP)**: Acts first. Must play tight because "
                    "many players behind you could have strong hands.\n\n"
                    "**Middle Position (MP)**: Some information. Can play a few "
                    "more hands.\n\n"
                    "**Late Position (LP/Button)**: Acts last. Can play the widest "
                    "range because you see all other actions first.\n\n"
                    "The same hand (e.g., K-J offsuit) might be:\n"
                    "- A fold in early position\n"
                    "- A call in middle position\n"
                    "- A raise in late position\n\n"
                    "Information changes everything."
                ),
            },
            {
                "title": "The Power of Acting Last",
                "content": (
                    "When you act last, you can:\n\n"
                    "1. **Steal pots** when others show weakness (check)\n"
                    "2. **Control pot size** — check for free or bet for value\n"
                    "3. **Make more accurate decisions** with full information\n"
                    "4. **Bluff more effectively** — you know who's scared\n\n"
                    "Professional players estimate position is worth 2-3 big blinds "
                    "per hand on average. That's HUGE over thousands of hands."
                ),
            },
        ],
        "real_life_tip": (
            "In negotiations, the person who reveals their number first "
            "is at a disadvantage — just like being out of position.\n\n"
            "Job salary negotiation: If they ask 'What's your expected salary?', "
            "deflect with 'What's the range for this role?' "
            "Let THEM reveal information first.\n\n"
            "In business deals, the side with more information always has leverage. "
            "This is why due diligence exists — you're gathering information to "
            "improve your 'position' before making a decision."
        ),
        "quiz_intro": "Let's see how position changes decisions!",
    },
    5: {
        "title": "Reading & Ranges",
        "subtitle": "Bayesian thinking: updating beliefs with evidence",
        "intro": (
            "Beginners try to guess the exact hand their opponent has. "
            "Experts think in **ranges** — the set of all hands an opponent "
            "could have based on their actions.\n\n"
            "Each action narrows the range. A raise preflop eliminates weak hands. "
            "A big bet on the river eliminates mediocre hands. "
            "This is **Bayesian updating** — revising beliefs with new evidence."
        ),
        "sections": [
            {
                "title": "Thinking in Ranges",
                "content": (
                    "Instead of: 'He has Ace-King'\n"
                    "Think: 'He raised preflop, so his range is top 15% of hands: "
                    "pairs 77+, AJ+, KQ'\n\n"
                    "Then on the flop (K-7-2):\n"
                    "He bets big → narrows to: KK, 77, AK, KQ, and some bluffs\n"
                    "He checks → narrows to: AJ, QQ, JJ, and some weak kings\n\n"
                    "Each action provides evidence that updates the range."
                ),
            },
            {
                "title": "Updating with Evidence",
                "content": (
                    "Preflop raise → Range: ~15% of hands\n"
                    "Continuation bet on flop → Range: ~60% of preflop range\n"
                    "Double barrel on turn → Range: ~40% of flop range\n"
                    "Triple barrel on river → Range: ~25% of turn range\n\n"
                    "By the river, a player who bets every street likely has either:\n"
                    "- A very strong hand (value), OR\n"
                    "- A complete bluff (air)\n\n"
                    "The medium-strength hands check somewhere along the way. "
                    "This is called **polarization** — the range splits into "
                    "strong and weak, with little in between."
                ),
            },
        ],
        "real_life_tip": (
            "Bayesian thinking applies everywhere:\n\n"
            "A resume says 'Led team of 50 at top tech company.'\n"
            "Prior: Maybe true, maybe exaggerated (50/50).\n\n"
            "New evidence: They can discuss specific team challenges in detail.\n"
            "Updated belief: Much more likely true (85/15).\n\n"
            "New evidence: Their LinkedIn shows 2 years at a startup.\n"
            "Updated belief: Probably exaggerated (30/70).\n\n"
            "Each piece of evidence shifts the probability. Don't anchor on "
            "your first impression — keep updating as new information arrives."
        ),
        "quiz_intro": "Let's practice range reading!",
    },
    6: {
        "title": "Nash Equilibrium & GTO Basics",
        "subtitle": "Finding unexploitable strategies",
        "intro": (
            "A **Nash Equilibrium** is a strategy profile where no player can "
            "improve their outcome by changing their strategy alone. In poker, "
            "this means playing in a way that **cannot be exploited** — even if "
            "your opponent knows your exact strategy.\n\n"
            "This is called **Game Theory Optimal (GTO)** play. It's the "
            "foundation of modern poker strategy."
        ),
        "sections": [
            {
                "title": "The Push/Fold Game",
                "content": (
                    "The simplest GTO scenario: short-stacked poker.\n\n"
                    "With a short stack (under 10 big blinds), your only "
                    "options are push all-in or fold. No calling, no raising.\n\n"
                    "Nash equilibrium tells us EXACTLY which hands to push:\n"
                    "- With 5BB: Push wide (~50% of hands)\n"
                    "- With 10BB: Push tighter (~25% of hands)\n"
                    "- With 15BB: Push tight (~15% of hands)\n\n"
                    "If you follow these ranges, your opponent CANNOT gain an "
                    "edge against you, no matter what they do."
                ),
            },
            {
                "title": "GTO vs Exploitative Play",
                "content": (
                    "**GTO**: Play the mathematically optimal strategy. "
                    "Cannot be exploited, but doesn't maximally exploit others.\n\n"
                    "**Exploitative**: Deviate from GTO to take advantage of "
                    "opponents' mistakes. Higher profit potential, but you become "
                    "exploitable yourself.\n\n"
                    "The best approach:\n"
                    "1. Learn GTO as your baseline strategy\n"
                    "2. Deviate from GTO when you spot clear opponent mistakes\n"
                    "3. Return to GTO when unsure\n\n"
                    "Think of GTO as your 'safe harbor' — you can always retreat "
                    "to it when you're uncertain."
                ),
            },
        ],
        "real_life_tip": (
            "Nash Equilibrium applies to competitive strategy:\n\n"
            "Two coffee shops on the same street. If both price at $4, "
            "they split customers 50/50. If one drops to $3.50, they steal "
            "customers but make less per cup.\n\n"
            "Nash Equilibrium: both price at the level where neither benefits "
            "from changing. This is why gas stations across the street from "
            "each other always have similar prices!\n\n"
            "In your career: your 'GTO strategy' is being reliably good at "
            "your job. Your 'exploitative strategy' is finding specific "
            "opportunities where you can create outsized value. Start with "
            "the fundamentals, then look for edges."
        ),
        "quiz_intro": "Let's test your Nash equilibrium knowledge!",
    },
}
