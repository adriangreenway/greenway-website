# Proposal Email Templates

Adrian-supplied, locked wording. Source: Adrian in chat, 2026-07-14 (first used for the
turner draft). Use with the create-proposal skill's draft step. Drafts only, never send.

## GOTCHA: update_draft can silently destroy the draft (2026-07-29)

On the Ken-Ran pass email, `update_draft` was called four times to revise
wording. Every call returned success with the draft ID. The draft was then
**absent from Gmail entirely** — Adrian couldn't find it and had to ask for it
again. Recreating with `create_draft` worked fine.

Rules:
- After ANY `update_draft`, call `list_drafts` to confirm the draft still
  exists. Never report "the draft is updated" on the tool's return value alone.
- For more than a one-word tweak, prefer deleting the approach entirely and
  calling `create_draft` fresh.
- `create_draft` needs `subject` AND `replyToMessageId` to land on the right
  thread. `update_draft` calls that omit `subject` are a suspected contributor
  to the loss.

## Voice for ad-hoc replies (2026-07-29, Ken-Ran pass draft correction)

Template 4.1 covers new inquiries only. Every OTHER client email (negotiation,
clarification, passing on a gig) is written in Adrian's own sent style, which
is much barer than composed prose. A relationship-managing 3-paragraph pass
draft got rejected flat: "this sounds nothing like my voice."

Model on his real sent emails, verbatim examples from the Ken-Ran and
Juneteenth threads:
- "Hi, our corporate rate for a 4pc band is $5000. This includes lights and
  sound. Please let me know if you have any questions or concerns. We'd love
  to work with you!"
- "We can go as low as $4000 for the 4pc since it's a Monday. Is that closer
  to your budget?"
- "No problem. What is your max budget for something like this?"

The pattern: 2 to 4 short sentences, states the fact or number plainly, one
warm closer at most ("We'd love to work with you!"), then done. No "I'm going
to be straight with you," no advice about what the buyer should do instead,
no relationship speeches. Numbers stated bare ($5000, not "five thousand").
Sign-off "Best," + "Adrian" for drafts he'll send from adrian@.

# Template 4.1 — New Inquiry Response (The Greenway Band)
First touch email for a new wedding inquiry that includes a date and venue. Working version with embedded links. Both links live inside anchor text. No raw URLs visible, no colon before a link.

## Placeholders
| Placeholder | Meaning | Example |
|---|---|---|
| {{first_name}} | Client first name | Caroline |
| {{date_full}} | Full date with year, subject line only | October 9, 2027 |
| {{date_short}} | Month and day, no year, body only | October 9 |
| {{venue}} | Venue name | Sandlewood Manor |
| {{proposal_url}} | Hosted proposal page | https://proposals.greenwayband.com/hergenrether/ |
| {{scheduling_url}} | 17hats scheduler, static, never changes | https://greenwayband.17hats.com/p#/scheduling/tttktcfskcdfwcxbvprcvkhxzxsfxvht |

## Subject
```
The Greenway Band — {{date_full}}
```

## Body (canonical HTML send format)
```html
<p>Hi, {{first_name}}! Thank you for reaching out and congratulations on your engagement! We're available on {{date_short}} and would love to come play at {{venue}}.</p>
<p>I've put together a <a href="{{proposal_url}}">proposal</a> with everything you need to know about the band, what your night looks like, and pricing. Take a look whenever you get a chance.</p>
<p>If you'd like, I'm happy to hop on a quick call to walk through the proposal and hear more about what you have in mind. You can schedule a time <a href="{{scheduling_url}}">here</a>.</p>
<p>Looking forward to hearing from you!</p>
<p>Best,<br>Adrian</p>
```

## Rules (do not deviate)
1. "proposal" and "here" are the only hyperlink anchor words. Never change the anchor words. Never add more links.
2. No raw URLs anywhere in the body. No colon leading into a link.
3. Greeting is exactly "Hi, {{first_name}}!" with the comma.
4. Sign off is exactly "Best," with "Adrian" on the next line.
5. Body date drops the year ({{date_short}}). Subject keeps the year ({{date_full}}).
6. Proposal URL pattern is https://proposals.greenwayband.com/{client-slug}/ with a trailing slash.
7. Optional personalization: if the inquiry mentioned a specific detail (venue feel, guest energy, piece count, song tastes), weave ONE natural sentence into paragraph 2 after the first sentence. Never list their details back. Approved examples: "It sounds like the music is going to be a big part of your night." / "I included both the 10 piece and the 6 piece so you can compare."
8. Keep the exclamation points exactly as written. Do not add more.
9. Voice constraints for any generated sentence: contractions throughout, no hyphens used as dashes, no em dashes, no semicolons. Banned words: bespoke, elevated, premier, world class, unforgettable, one of a kind, curated, seamless, exceptional, rest assured.

## Claude usage notes (from the turner draft, 2026-07-14)
- The template asserts availability ("We're available on {{date_short}}"). Adrian must
  confirm the calendar before sending. The proposal page itself never claims availability.
- Create via Gmail create_draft with htmlBody only. Never send; sending is Adrian's.
- New inquiry = fresh email to the client's address, not a reply to the 17hats
  notification thread.
- **KNOWN GOTCHA — Google "Redirect Notice" (Adrian, 2026-07-14, turner send):** the
  17hats scheduler URL has a `#` mid-path. Clicking it from inside Gmail can bounce
  through a google.com "Redirect Notice" interstitial on an API-created draft, even
  when the stored href is the correct raw URL. Adrian fixed the turner draft by
  re-inserting the link in Gmail compose before sending (select the anchor word,
  Cmd+K, paste the URL). Rule for next time: hrefs must be the exact raw URLs (never
  a google.com/url or any tracking wrapper). The sent turner email was verified clean
  in Sent (direct hrefs on both anchors).
- **UPDATE (2026-07-21, hinojosa draft — supersedes the turner theory): Gmail wraps
  the hrefs ITSELF when a draft is created through the connector API.** Proven by the
  compose-view "Go to link" chip showing `google.com/url?...&ust=...` on a freshly
  created, never-edited test draft. Passing clean HTML does not help; recreating the
  draft does not help. The turner email only sent clean because Adrian manually
  re-inserted both links in compose first. **Standing procedure for every API-created
  draft:** Adrian must re-link both anchor words before sending (click the anchor →
  "Change" in the link chip → paste the raw URL), pasting the raw URLs from Claude's
  status card, NEVER from anything Google renders (the Redirect Notice page, the
  chip, or the rendered draft — those give the wrapper). The status card must always
  include both raw URLs in copyable form. After sending, Claude verifies the Sent
  copy's hrefs via the API (the turner sent copy verified clean this way).
