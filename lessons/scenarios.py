"""Pre-built teaching scenarios and quiz questions for Poker4U."""

from typing import List, Dict
from engine.cards import Card, Suit


def _c(s: str) -> Card:
    """Shorthand to create a card from string like 'As', 'Th'."""
    return Card.from_str(s)


# --- Quiz Questions for Each Lesson ---

LESSON_QUIZZES = {
    1: [  # Hand Rankings
        {
            "question": "Which hand wins?",
            "hand_a": [_c("As"), _c("Ks"), _c("Qs"), _c("Js"), _c("Ts")],
            "hand_a_name": "A\u2660 K\u2660 Q\u2660 J\u2660 T\u2660 (Royal Flush)",
            "hand_b": [_c("Ac"), _c("Ad"), _c("Ah"), _c("Kc"), _c("Kd")],
            "hand_b_name": "A\u2663 A\u2666 A\u2665 K\u2663 K\u2666 (Full House)",
            "correct": "a",
            "explanation": "A Royal Flush is the strongest possible hand. It beats everything, including a Full House.",
        },
        {
            "question": "Which hand wins?",
            "hand_a": [_c("8h"), _c("8d"), _c("3c"), _c("3s"), _c("Kh")],
            "hand_a_name": "8\u2665 8\u2666 3\u2663 3\u2660 K\u2665 (Two Pair: 8s and 3s)",
            "hand_b": [_c("Jc"), _c("Jd"), _c("Jh"), _c("4s"), _c("7c")],
            "hand_b_name": "J\u2663 J\u2666 J\u2665 4\u2660 7\u2663 (Three of a Kind: Jacks)",
            "correct": "b",
            "explanation": "Three of a Kind beats Two Pair. The rank names can be deceiving — 'three' beats 'two pair'.",
        },
        {
            "question": "Which hand wins?",
            "hand_a": [_c("5h"), _c("6h"), _c("7h"), _c("8h"), _c("9h")],
            "hand_a_name": "5\u2665 6\u2665 7\u2665 8\u2665 9\u2665 (Straight Flush)",
            "hand_b": [_c("Ac"), _c("Ad"), _c("Ah"), _c("As"), _c("Kc")],
            "hand_b_name": "A\u2663 A\u2666 A\u2665 A\u2660 K\u2663 (Four of a Kind: Aces)",
            "correct": "a",
            "explanation": "A Straight Flush beats Four of a Kind. Even four Aces can't beat it!",
        },
        {
            "question": "Which hand wins?",
            "hand_a": [_c("Ah"), _c("Kc"), _c("Qd"), _c("Js"), _c("9h")],
            "hand_a_name": "A\u2665 K\u2663 Q\u2666 J\u2660 9\u2665 (High Card: Ace)",
            "hand_b": [_c("2c"), _c("2d"), _c("5h"), _c("8s"), _c("Tc")],
            "hand_b_name": "2\u2663 2\u2666 5\u2665 8\u2660 T\u2663 (One Pair: 2s)",
            "correct": "b",
            "explanation": "Any pair beats any high card hand. Even a lowly pair of 2s beats Ace-high.",
        },
        {
            "question": "Which hand is rarer (and therefore stronger)?",
            "hand_a": [_c("Kh"), _c("Kd"), _c("Kc"), _c("7s"), _c("7h")],
            "hand_a_name": "K\u2665 K\u2666 K\u2663 7\u2660 7\u2665 (Full House)",
            "hand_b": [_c("2s"), _c("5s"), _c("7s"), _c("9s"), _c("Js")],
            "hand_b_name": "2\u2660 5\u2660 7\u2660 9\u2660 J\u2660 (Flush)",
            "correct": "a",
            "explanation": "A Full House is rarer than a Flush (0.14% vs 0.20%), so it ranks higher.",
        },
    ],
    2: [  # Expected Value
        {
            "type": "ev_calculation",
            "question": "You have top pair. Pot is 100 chips. Opponent bets 50 chips. You estimate 60% equity. What's the EV of calling?",
            "pot": 100,
            "bet": 50,
            "equity": 0.60,
            "correct_ev": 70.0,
            "options": ["+70 chips", "+30 chips", "-10 chips", "+20 chips"],
            "correct": "+70 chips",
            "explanation": "EV = (0.60 x 150) - (0.40 x 50) = 90 - 20 = +70 chips. Calling is very profitable!",
        },
        {
            "type": "ev_calculation",
            "question": "Coin flip bet: Heads you win 30 chips, tails you lose 20 chips. What's the EV?",
            "correct_ev": 5.0,
            "options": ["+5 chips", "+10 chips", "0 chips", "-5 chips"],
            "correct": "+5 chips",
            "explanation": "EV = (0.5 x 30) - (0.5 x 20) = 15 - 10 = +5 chips. A good bet!",
        },
        {
            "type": "ev_calculation",
            "question": "You have a weak draw. Pot is 60 chips. Opponent bets 60 chips. You estimate 20% equity. EV of calling?",
            "pot": 60,
            "bet": 60,
            "equity": 0.20,
            "correct_ev": -24.0,
            "options": ["-24 chips", "+24 chips", "-12 chips", "0 chips"],
            "correct": "-24 chips",
            "explanation": "EV = (0.20 x 120) - (0.80 x 60) = 24 - 48 = -24 chips. Fold!",
        },
        {
            "type": "ev_decision",
            "question": "Pot is 200 chips. Opponent bets 100 chips. You estimate 40% equity. Should you call?",
            "options": ["Call (+EV)", "Fold (-EV)"],
            "correct": "Call (+EV)",
            "explanation": "Pot odds = 100/300 = 33%. Your equity (40%) > pot odds (33%). EV = (0.40 x 300) - (0.60 x 100) = 120 - 60 = +60 chips. Call!",
        },
        {
            "type": "ev_decision",
            "question": "Pot is 50 chips. Opponent bets 100 chips. You estimate 25% equity. Should you call?",
            "options": ["Call (+EV)", "Fold (-EV)"],
            "correct": "Fold (-EV)",
            "explanation": "Pot odds = 100/150 = 67%. Your equity (25%) < pot odds (67%). EV = (0.25 x 150) - (0.75 x 100) = 37.5 - 75 = -37.5 chips. Fold!",
        },
    ],
    3: [  # Pot Odds
        {
            "type": "pot_odds",
            "question": "Pot is 120 chips. Opponent bets 40 chips. What are your pot odds?",
            "options": ["25%", "33%", "40%", "50%"],
            "correct": "25%",
            "explanation": "Pot odds = 40 / (120 + 40) = 40/160 = 25%. You need at least 25% equity to call.",
        },
        {
            "type": "pot_odds",
            "question": "Pot is 200 chips. Opponent bets 200 chips. What are your pot odds?",
            "options": ["25%", "33%", "50%", "67%"],
            "correct": "50%",
            "explanation": "Pot odds = 200 / (200 + 200) = 200/400 = 50%. You need a coin flip or better to call.",
        },
        {
            "type": "outs",
            "question": "You have a flush draw on the flop (9 outs). Using the Rule of 4, what's your approximate chance of hitting by the river?",
            "options": ["18%", "27%", "36%", "45%"],
            "correct": "36%",
            "explanation": "Rule of 4: 9 outs x 4 = 36%. You'll hit your flush about 1 in 3 times by the river.",
        },
        {
            "type": "decision",
            "question": "You have a flush draw (36% equity). Pot is 100. Opponent bets 50. Do you call?",
            "options": ["Call (odds are good)", "Fold (too expensive)"],
            "correct": "Call (odds are good)",
            "explanation": "Pot odds = 50/150 = 33%. Your equity (36%) > pot odds (33%). Profitable call!",
        },
        {
            "type": "decision",
            "question": "You have a gutshot draw (4 outs, ~16% equity). Pot is 60. Opponent bets 60. Do you call?",
            "options": ["Call", "Fold"],
            "correct": "Fold",
            "explanation": "Pot odds = 60/120 = 50%. Your equity (~16%) is way below 50%. Clear fold.",
        },
    ],
    4: [  # Position
        {
            "type": "position",
            "question": "You have K-J offsuit. You're first to act (Under the Gun) with 5 players behind. What should you do?",
            "options": ["Raise", "Call", "Fold"],
            "correct": "Fold",
            "explanation": "In early position with many players behind, K-Jo is too weak. Someone likely has a better hand. Position disadvantage makes this a fold.",
        },
        {
            "type": "position",
            "question": "You have K-J offsuit. You're on the Button (last to act) and everyone has folded to you. What should you do?",
            "options": ["Raise", "Call", "Fold"],
            "correct": "Raise",
            "explanation": "On the Button with only the blinds left, K-Jo is a strong hand! You have position advantage and can raise to steal the blinds.",
        },
        {
            "type": "concept",
            "question": "Why is acting last an advantage?",
            "options": [
                "You get to see all opponents' actions first",
                "Your cards are dealt last so they're better",
                "The dealer gives you extra cards",
            ],
            "correct": "You get to see all opponents' actions first",
            "explanation": "Acting last means you have maximum information. You see checks (weakness), bets (strength), and raises (big strength) before you decide.",
        },
        {
            "type": "concept",
            "question": "In a negotiation, who has the advantage?",
            "options": [
                "The person who speaks first and sets the anchor",
                "The person who listens first and responds with more information",
                "Neither — position doesn't matter",
            ],
            "correct": "The person who listens first and responds with more information",
            "explanation": "Just like in poker, gathering information before acting gives you an edge. Let others reveal their positions first.",
        },
    ],
    5: [  # Ranges
        {
            "type": "range",
            "question": "An opponent raises from early position. Which range best describes their likely hands?",
            "options": [
                "Top 10%: AA, KK, QQ, JJ, AK, AQ",
                "Top 30%: Any pair, any Ace, KJ+",
                "Top 50%: Most hands with face cards",
                "Any two cards",
            ],
            "correct": "Top 10%: AA, KK, QQ, JJ, AK, AQ",
            "explanation": "Early position raises indicate strong hands. The range is tight — mostly big pairs and big aces.",
        },
        {
            "type": "range",
            "question": "Opponent raises preflop, then bets the flop (K-7-2), then bets the turn (3). They likely have:",
            "options": [
                "Strong hand (AK, KQ, KK) or a bluff",
                "A medium pair like 88 or 99",
                "A drawing hand like a flush draw",
            ],
            "correct": "Strong hand (AK, KQ, KK) or a bluff",
            "explanation": "Betting multiple streets narrows the range. Medium hands usually check somewhere. The range polarizes to strong hands and bluffs.",
        },
        {
            "type": "concept",
            "question": "What is Bayesian updating?",
            "options": [
                "Revising your beliefs based on new evidence",
                "Always sticking with your first impression",
                "Ignoring evidence that contradicts your belief",
            ],
            "correct": "Revising your beliefs based on new evidence",
            "explanation": "Bayesian updating means adjusting probabilities as new evidence arrives. Each opponent action is evidence that should update your estimate of their range.",
        },
    ],
    6: [  # Nash Equilibrium
        {
            "type": "nash",
            "question": "You have 5 big blinds and A-7 suited. Nash equilibrium says you should:",
            "options": ["Push all-in", "Fold", "Limp"],
            "correct": "Push all-in",
            "explanation": "With 5BB, A-7 suited is well within the Nash push range. At this stack depth, it's push or fold — no other plays are correct.",
        },
        {
            "type": "nash",
            "question": "You have 15 big blinds and 9-8 offsuit. Nash equilibrium says you should:",
            "options": ["Push all-in", "Fold", "Min-raise"],
            "correct": "Fold",
            "explanation": "With 15BB, the Nash push range is tight. 9-8o doesn't make the cut — you need premium hands at this stack depth.",
        },
        {
            "type": "concept",
            "question": "What does 'Game Theory Optimal' (GTO) mean?",
            "options": [
                "A strategy that cannot be exploited by any opponent",
                "The strategy that wins the most chips",
                "Always bluffing to keep opponents guessing",
            ],
            "correct": "A strategy that cannot be exploited by any opponent",
            "explanation": "GTO play minimizes your maximum loss. It may not maximize profit against weak players, but it guarantees you can't be beaten in the long run.",
        },
        {
            "type": "concept",
            "question": "Two gas stations across the street price fuel similarly because of:",
            "options": [
                "Nash Equilibrium — neither can gain by changing alone",
                "They're owned by the same company",
                "Government regulation",
            ],
            "correct": "Nash Equilibrium — neither can gain by changing alone",
            "explanation": "If one raises prices, they lose all customers. If one lowers prices, they lose profit margin. The equilibrium is matching prices — classic Nash!",
        },
    ],
}


# --- Scenario Challenges ---

SCENARIO_CHALLENGES = [
    {
        "id": "coin_flip",
        "title": "The Coin Flip",
        "description": "AK vs QQ — Understanding 50/50 variance",
        "concept": "Variance",
        "setup": "You hold A\u2660K\u2660 and go all-in preflop. Your opponent calls with Q\u2665Q\u2663.",
        "hole_cards": [_c("As"), _c("Ks")],
        "opponent_cards": [_c("Qh"), _c("Qc")],
        "community": [_c("7d"), _c("3h"), _c("Jc"), _c("2s"), _c("9d")],
        "question": "You lost this hand. Was going all-in a mistake?",
        "options": ["Yes, I lost so it was wrong", "No, it was the right play despite losing"],
        "correct": "No, it was the right play despite losing",
        "explanation": (
            "AK vs QQ is roughly a coin flip (~43% vs ~57%). Going all-in with AK preflop "
            "is NOT a mistake — it's a standard, correct play. The result of ONE hand "
            "doesn't determine if the decision was right.\n\n"
            "This is the key lesson about VARIANCE: correct decisions can have bad outcomes "
            "in the short run. Judge decisions by their process, not their results."
        ),
        "real_life": (
            "A startup with a solid business plan can still fail. "
            "That doesn't mean starting it was wrong — variance is real in life too."
        ),
    },
    {
        "id": "drawing_dead",
        "title": "The Drawing Dead",
        "description": "When math says fold even with a good hand",
        "concept": "Expected Value",
        "setup": (
            "You hold J\u2665T\u2665 on a board of A\u2665K\u2665Q\u2663 2\u2660. "
            "You have a flush draw AND an open-ended straight draw! "
            "Opponent goes all-in for 300 chips into a pot of 100 chips."
        ),
        "hole_cards": [_c("Jh"), _c("Th")],
        "opponent_cards": [_c("Ac"), _c("Kd")],
        "community": [_c("Ah"), _c("Kh"), _c("Qc"), _c("2s")],
        "question": "You have a big draw (15 outs!). The opponent shoves 300 into 100. Should you call?",
        "options": ["Call — I have so many outs!", "Fold — the price is too high"],
        "correct": "Fold — the price is too high",
        "explanation": (
            "You have ~15 outs (~30% equity). But the pot odds are terrible:\n"
            "300 / (100 + 300) = 75% equity needed!\n\n"
            "EV of calling = (0.30 x 400) - (0.70 x 300) = 120 - 210 = -90 chips\n\n"
            "Even with a massive draw, when the bet is too big relative to the pot, "
            "you must fold. Don't let excitement override math."
        ),
        "real_life": (
            "A 'can't miss' opportunity with terrible terms is still a bad deal. "
            "Even promising investments are bad if the price is too high."
        ),
    },
    {
        "id": "bluff_catcher",
        "title": "The Bluff Catcher",
        "description": "Use pot odds to decide",
        "concept": "Pot Odds",
        "setup": (
            "River card is dealt. Board: K\u2660 8\u2666 3\u2663 J\u2665 5\u2660\n"
            "You hold A\u2663K\u2663 (top pair, top kicker). Pot is 150 chips.\n"
            "Opponent bets 50 chips. They could have you beat or be bluffing."
        ),
        "hole_cards": [_c("Ac"), _c("Kc")],
        "opponent_cards": [_c("Qh"), _c("Td")],
        "community": [_c("Ks"), _c("8d"), _c("3c"), _c("Jh"), _c("5s")],
        "question": "Pot is 150, opponent bets 50. You need 25% equity. Is top pair good enough to call?",
        "options": ["Call — pot odds are good", "Fold — they might have better"],
        "correct": "Call — pot odds are good",
        "explanation": (
            "Pot odds: 50 / 200 = 25%. You only need to win 1 in 4 times!\n\n"
            "Top pair + top kicker is very likely to beat a range that includes "
            "bluffs and weaker hands. You probably win well over 50% of the time.\n\n"
            "When getting good pot odds, you don't need to be sure you're ahead. "
            "You just need to be right more than the pot odds require."
        ),
        "real_life": (
            "Sometimes you don't need to be certain. If the cost of checking is low "
            "and the potential payoff is high, it's worth investigating even uncertain leads."
        ),
    },
    {
        "id": "squeeze_play",
        "title": "The Squeeze Play",
        "description": "Position and aggression",
        "concept": "Position",
        "setup": (
            "Preflop: Player A raises to 6 chips. Player B calls 6 chips.\n"
            "You're on the Button with A\u2665Q\u2665. Pot is 15 chips.\n"
            "You can call 6, raise big, or fold."
        ),
        "hole_cards": [_c("Ah"), _c("Qh")],
        "opponent_cards": [_c("Kd"), _c("Js")],
        "community": [],
        "question": "Two players already in. You have AQs on the Button. What's the best play?",
        "options": ["Call 6 chips", "Raise to 20 chips (squeeze)", "Fold"],
        "correct": "Raise to 20 chips (squeeze)",
        "explanation": (
            "This is the 'squeeze play' — a powerful positional weapon.\n\n"
            "Why it works:\n"
            "1. You have a strong hand (AQs)\n"
            "2. You have position (Button)\n"
            "3. The caller (Player B) likely has a mediocre hand — they would have "
            "re-raised with a premium hand\n"
            "4. Your big raise puts maximum pressure on BOTH players\n\n"
            "The combination of a good hand, position, and fold equity makes this "
            "a high-EV play."
        ),
        "real_life": (
            "In a group negotiation, waiting to see others' positions before making "
            "a bold move is a 'squeeze play' in real life. You use their revealed "
            "information to strengthen your own position."
        ),
    },
    {
        "id": "laydown",
        "title": "The Laydown",
        "description": "Discipline over ego",
        "concept": "Sunk Cost",
        "setup": (
            "You raised preflop with K\u2660K\u2663. Board: A\u2665 A\u2660 T\u2663 7\u2666 2\u2665\n"
            "You've bet every street and put 150 chips in.\n"
            "Opponent now raises all-in for 200 more chips on the river.\n"
            "They've been passive all hand until now."
        ),
        "hole_cards": [_c("Ks"), _c("Kc")],
        "opponent_cards": [_c("Ad"), _c("Jh")],
        "community": [_c("Ah"), _c("As"), _c("Tc"), _c("7d"), _c("2h")],
        "question": "You have Kings but there are two Aces on the board. Opponent raises big on the river. What do you do?",
        "options": ["Call — I've invested too much to fold", "Fold — they likely have an Ace"],
        "correct": "Fold — they likely have an Ace",
        "explanation": (
            "The 150 chips you've already invested are SUNK COSTS — they're gone "
            "regardless of your decision. Only consider future EV.\n\n"
            "A passive player suddenly raising all-in on the river with two Aces "
            "on the board almost always has an Ace. Your Kings are likely beaten.\n\n"
            "The hardest skill in poker (and life) is letting go of past investments "
            "when the math says to move on."
        ),
        "real_life": (
            "'I've already invested 3 years in this project...' is sunk cost thinking. "
            "If the project is failing, the time already spent shouldn't influence your "
            "decision to continue. Only future costs and benefits matter."
        ),
    },
    {
        "id": "job_offer",
        "title": "Real Life: The Job Offer",
        "description": "Apply EV thinking to career choices",
        "concept": "Expected Value",
        "setup": (
            "You have two job offers:\n\n"
            "Job A: Large stable company\n"
            "  - Salary: $90K/year\n"
            "  - Growth potential: Modest (2-5% raises)\n"
            "  - Job satisfaction: High (85% chance)\n"
            "  - Job security: Very high (95%)\n\n"
            "Job B: Fast-growing startup\n"
            "  - Salary: $75K/year + equity worth $200K if IPO\n"
            "  - IPO probability: 15%\n"
            "  - Job satisfaction: Medium (60% chance)\n"
            "  - Job security: Moderate (70%)"
        ),
        "hole_cards": [],
        "opponent_cards": [],
        "community": [],
        "question": "Which job has higher Expected Value over 3 years?",
        "options": [
            "Job A: Stable company ($90K)",
            "Job B: Startup ($75K + equity)",
        ],
        "correct": "Job A: Stable company ($90K)",
        "explanation": (
            "Let's calculate 3-year EV:\n\n"
            "Job A: $90K x 3 x 0.95 (security) = $256.5K guaranteed\n"
            "  + High satisfaction value\n\n"
            "Job B: $75K x 3 x 0.70 (security) = $157.5K base\n"
            "  + $200K x 0.15 (IPO) = $30K expected equity\n"
            "  = $187.5K total EV\n\n"
            "Job A has higher EV AND higher satisfaction probability.\n"
            "Job B only wins if you dramatically increase IPO odds or equity value.\n\n"
            "This is poker thinking: don't be seduced by the 'big pot' (IPO) "
            "when the odds are heavily against you."
        ),
        "real_life": (
            "Apply EV to every major decision. Multiply each outcome by its "
            "probability. The highest EV option isn't always the flashiest one."
        ),
    },
    {
        "id": "startup_pivot",
        "title": "Real Life: The Startup Pivot",
        "description": "Use pot odds logic for business decisions",
        "concept": "Pot Odds",
        "setup": (
            "You've invested $50K in a mobile app startup (6 months of work).\n"
            "Current metrics are disappointing — only 200 users.\n\n"
            "Option A: Pivot to a new market (costs $20K more)\n"
            "  - 30% chance of reaching $300K revenue\n"
            "  - 70% chance of total failure\n\n"
            "Option B: Shut down and start fresh\n"
            "  - Save the $20K\n"
            "  - Apply lessons learned to a new venture"
        ),
        "hole_cards": [],
        "opponent_cards": [],
        "community": [],
        "question": "Should you invest $20K more to pivot the startup?",
        "options": [
            "Pivot (invest $20K more)",
            "Shut down and start fresh",
        ],
        "correct": "Pivot (invest $20K more)",
        "explanation": (
            "This is a pot odds problem!\n\n"
            "The $50K already spent is a SUNK COST — ignore it.\n"
            "Only consider: Should I invest $20K for 30% chance at $300K?\n\n"
            "EV = (0.30 x $300K) - (0.70 x $20K) = $90K - $14K = +$76K\n\n"
            "The pot odds are excellent! $20K to potentially win $300K "
            "only needs ~7% chance to break even (20/300 = 6.7%).\n"
            "You have 30% — way above the threshold.\n\n"
            "Key: Don't let the sunk $50K cloud your thinking. "
            "Evaluate the REMAINING decision on its own merits."
        ),
        "real_life": (
            "Always separate sunk costs from future decisions. "
            "The question isn't 'Can I recover my investment?' but "
            "'Is this NEXT investment +EV?'"
        ),
    },
    {
        "id": "negotiation",
        "title": "Real Life: The Negotiation",
        "description": "Position advantage in salary negotiation",
        "concept": "Position & Information",
        "setup": (
            "You're negotiating a salary for a new role.\n"
            "You've researched: market rate is $95K-$120K.\n"
            "You'd accept $100K. Your ideal is $115K.\n\n"
            "The hiring manager asks: 'What salary are you looking for?'\n\n"
            "You have two strategies:\n"
            "Strategy A: Name your price first ($115K)\n"
            "Strategy B: Ask them what the budgeted range is"
        ),
        "hole_cards": [],
        "opponent_cards": [],
        "community": [],
        "question": "Which negotiation strategy gives you better 'position'?",
        "options": [
            "Name your price first ($115K)",
            "Ask for their range first",
        ],
        "correct": "Ask for their range first",
        "explanation": (
            "This is the poker concept of POSITION applied to real life!\n\n"
            "By asking their range first, you:\n"
            "1. Gather information before committing (like acting last)\n"
            "2. Avoid anchoring too low (what if their budget was $130K?)\n"
            "3. Can calibrate your ask based on their response\n\n"
            "If they say '$100K-$130K', you now know you can ask for $120K+.\n"
            "If you'd named $115K first, you left money on the table!\n\n"
            "In poker and in life: information is power. Get it before giving it."
        ),
        "real_life": (
            "Always try to let the other side reveal information first. "
            "Whether it's salary, pricing, or any negotiation — "
            "position advantage is as real in life as it is in poker."
        ),
    },
]
