# Campus Relay 3D — Technical report

## Problem and objective

A campus lab needs a replacement relay. A courier can use a short corridor with an unreliable gate sensor or take a longer clear route. The objective is to demonstrate how sensor evidence changes both route planning and the immediate driving decision. The application is a turn-based educational simulation. All probabilities and rewards are assumed.

## Environment

The course map is a 5 × 5 grid. Coordinates use (x, y) from the top left. The depot is (0, 2), the lab is (4, 2), the gate is (1, 2), and the walls are (2, 1) and (3, 3). Each legal move changes one coordinate by one. Additional districts introduce blocked cells, slow terrain and timed crossings.

## 1. Bayesian inference

Only the gate is uncertain in the course map. Prior blockage probability is 0.30. A blocked gate gives an alert with probability 0.80. A clear gate gives a false alert with probability 0.20.

For ALERT, the numerator is 0.8 × 0.3 = 0.24. Total evidence is 0.24 + 0.2 × 0.7 = 0.38. Posterior blockage risk is 0.24 / 0.38 = 0.6316. For CLEAR, it is 0.06 / (0.06 + 0.56) = 0.0968. Bayes accounts for false alarms and the starting risk together.

## 2. A* search

A* prioritizes f = g + h. The accumulated cost g includes each step, any slow-terrain delay and a gate-entry penalty of four times the posterior probability. The heuristic h is Manhattan distance to the lab. It is a lower bound because movement uses four directions and each step costs at least one. Parent pointers reconstruct the selected route.

After ALERT, the four-step direct route costs 4 + 4 × 0.6316 = 6.53. A six-step detour costs 6.00, so A* selects it. With CLEAR, the direct route costs only 4.39. A weighted planning cost is expressed in model units; actual delivery turns are counted separately.

## 3. One-step MDP

The hidden gate states are CLEAR and BLOCKED. For a chosen next tile with blockage probability p, MOVE earns +3 if clear and −5 if blocked. WAIT earns −1 in either state. Expected move reward is 3(1 − p) − 5p = 3 − 8p. Compare this with −1 and select the greater value. Future rewards have zero weight in this exercise.

Under ALERT on the direct corridor, MOVE scores −2.05 and WAIT scores −1. On the detour the next tile has zero blockage probability, so MOVE scores +3. This shows why the same observation can produce different actions on different routes.

## Integration and implementation

The browser computes one posterior, uses it in A* edge costs, then evaluates the next tile of the selected path. Waiting spends one turn and requests another observation. After the opening signal, rescans return CLEAR by design. Each posterior becomes the next prior under an assumed fixed gate state and conditionally independent observations. Slow cells consume two turns. Rail signals are checked when entering the crossing. The Python reference reproduces the two opening signals on the course grid.

## Test cases and results

| Case | Observed result | Check |
| --- | --- | --- |
| Courtyard, CLEAR, planner | 4 steps, 4.39 weighted cost, MOVE | Compare with the direct path |
| Courtyard, ALERT, planner | 6 steps, 6.00 weighted cost, MOVE | Bypass the gate |
| Courtyard, ALERT, direct | WAIT followed by four moves, 5 turns total | Repeatable CLEAR rescan |
| Four districts, both signals, both route strategies | Deliveries reach their lab | Exercise suggested steps and manual drive separately |
| Steel grate / shallow water | Entering costs two turns | Inspect the turn counter |
| Deep water / wall | Movement is blocked | Confirm the tile and turn counter stay unchanged |
| Red rail crossing | Wait one turn, then cross | Check position and wait count |

The automated game checks exercise JavaScript logic with a simulated interface. Visual clarity, layout and GPU compatibility require a run in the intended presentation browser.

## Limitations and future work

The gate penalty and rewards are illustrative. The scripted rescan makes demonstrations repeatable but does not measure reliability in a real campus. Future experiments could estimate sensor likelihoods from recorded deliveries, vary rescan outcomes and compare success rate and average travel time across repeated trials.

