# revüe board review — VIP Lake Travis "Weekdays on the Water"

## Outcome

Reviewed the VIP Lake Travis landing concept (Figma, page 1E1E1E, three desktop frames) to decide
whether it is ready to send to the client.

## Mode

design-handoff · review board run

## Verdict

Verdict: caution  (face: flat mouth, amber badge)

Reason: Strong, near-ready desktop concept, but a required state is missing (no mobile/tablet frame),
the three frames disagree on the boat lineup so there is no single source-of-truth design, and the
testimonial copy is placeholder.

## Shared inputs (read by every panelist)

- Request: is the concept ready to send to the client as a design handoff?
- Stakeholder: the client / marina owner — must be able to react and decide without a walkthrough.
- Artifacts: native Figma file, page 1E1E1E, three desktop frames (one 3-boat, two 2-boat variants).
- Deliverable + proof: a Figma design; proof needed = exact format, editability, required states, one final frame.
- Constraints: navy/coral/aqua on lake imagery; "Save 15% on Weekday/Thursday" offer; premium-but-friendly.

Non-negotiable check: honesty rule flags the placeholder testimonials; exact-deliverable rule flags the missing mobile state. Rest clear.

## Board

Critique — Strengths to protect: single-promise hero ("Your Best Summer Day Is One Click Away"), a
legible funnel (value strip → boat picker with prices → social proof → FAQ → closing CTA), consistent
15% hook. Weaknesses by area: the hero rating card competes with the primary CTA; hierarchy is
even-weighted so nothing pulls the eye to "book"; the moat (why VIP over any rental) is never stated;
testimonials are filler; no mobile fold. Punch-list: name one final frame; make the reserve CTA the
single loudest hero element; add a one-line "why VIP" under the H1; replace filler testimonials; unify
the boat-card count and naming.

Aggressive — Sharper POV that still clears the bar: lead with loss aversion ("Summer is 12 weekends.
Don't spend one on the dock."), and promote the boat picker to the hero so the first scroll is
"pick your boat + see the price." Line held: no fabricated urgency counters or invented review counts —
the real 15% offer stays the only scarcity lever.

Conservative — Lowest-objection version a cautious owner couldn't reject: keep the calm structure, lead
with trust (local, well-maintained fleet, easy booking), plain pricing, keep the closing reservation
CTA. Close to Frame 1 today; risk is it stays generic unless the "why VIP" line and real proof land.

Proof — Exact format (Figma) present and editable → pass. Required states fail: three desktop frames,
no mobile/tablet. Cross-frame inconsistency: Frame 1 = Tritoon $435 / Pontoon $335 / Sea-Doo $330;
Frames 2–3 = Berkshire Tritoon $435 / Sea-Doo GTI 130 $330. No frame designated final. Testimonials unverified.

Stakeholder — Can the client decide without a walkthrough? Only partly. They can react to the desktop
look, but can't approve a build: no phone view, and it is unclear which of three frames and which boat
lineup is real. Ask them exactly two things: which lineup/pricing is correct, and whether mobile is in
scope this round.

Synthesis — Do first (ranked): 1) pick one canonical desktop frame; 2) confirm boat lineup + pricing
with the client; 3) design the matching mobile frame; 4) replace placeholder testimonials. Highest-
leverage single move: collapse to one final desktop frame — it unblocks mobile, copy, and sign-off at once.

## Evidence

- Verified (source): native Figma file, page 1E1E1E, three desktop frames — read from an on-screen
  screenshot (1512x785 capture) plus a zoomed preview of each frame this session.
- Verified (result): Frame 1 has 3 boat cards; Frames 2–3 have 2 boat cards, with the pricing above.
- Verified (result): no mobile or tablet frame exists on the reviewed page.
- Not verified (limitation): layer/component editability and client share-link permissions (inspected
  visually only); and whether the "Fresh VIP Figma" tab holds newer changes than this captured state.

## Scorecard

| Check | Status | Evidence |
| --- | --- | --- |
| Exact requested format | pass | Native, editable Figma file (not an export) |
| Source editability | partial | Visibly native; layer structure not opened |
| Desktop/mobile states | fail | Three desktop frames; no mobile/tablet |
| Preview fidelity | pass | All frames render cleanly at desktop dimensions |
| Brand fit | pass | Navy/coral/aqua on lake imagery; consistent 15% hook |
| Stakeholder access | partial | Open locally; client share link not verified |
| Developer clarity | partial | Two of three frames unnamed; no final designated |

## Stakeholder Summary

What is ready: a polished desktop landing-page concept with a clear offer, a boat picker with pricing,
social proof, FAQ, and a strong closing CTA. What to review: which boat lineup and pricing is correct.
What is not final: there is no phone version, testimonials are placeholder, and two of three layouts are
duplicates. Decision needed: pick the single final desktop version and confirm boats + prices so mobile
and real copy can be built on an approved base.

## Assumptions

- The client expects a client-facing page and mobile traffic matters for a lake-rental funnel.
- Frame 1 vs. Frames 2–3 is an iteration in progress, not three intentionally different pages.
- Pricing and the 15% Weekday/Thursday offer are real business terms.

## Risks / Blockers

- No mobile/tablet frame — cannot ship a desktop-only handoff as final.
- Cross-frame inconsistency — two boat lineups, no designated final frame.
- Placeholder testimonials — unsupported social proof on a booking page.
- Unnamed frames — hurts developer clarity.
- Share/permissions unverified.

## Decisions Needed

1. Which frame is canonical? 2. Two-boat or three-boat lineup, prices approved? 3. Is mobile in scope
this round? 4. Real testimonials available, or hold the section?

## Next Action

Collapse to one final desktop frame, confirm lineup/pricing with the client, build the matching mobile
frame, replace placeholder testimonials, then re-run revüe targeting `ship with changes`.
