# EPK media manifest

Sources live in `~/Desktop/EPK` (never committed; repo is public). Rights: Adrian
confirmed 2026-07-24 that all listed footage/photos are his own gigs and cleared
for public use (testimonial couple, Big Spring Ranch name, pro photos, both films).

## Source videos (8) and their roles

| File | Length / format | Role |
|---|---|---|
| `Neon_Moon.mp4` | 0:31, 1080x1920 vertical | Primary solo proof (page embed + reel 0:09-0:19) |
| `suavemente_v1 (720p).mp4` | 0:13, 720x1280 vertical | Reel 0:05-0:09 (crowd interaction) |
| `Greenway_Band_9pc_Promo.mp4` | 1:13, 1920x1080 | Page embed + reel 0:26-0:30 (Adrian at 25.6-27.4, horns 30.3-33.4) |
| `big_spring_ranch_wedding_v1 (2160p).mp4` | 1:36, 4K | Page embed + reel opener 0:00-0:05 (Adrian + drum head) and payoff 0:36-0:43 |
| `crazy_in_love_v1 (540p).mp4` | 0:19, 480x852 vertical | Reel 0:19-0:26 + closing lift |
| `play_that_funky_music_v1 (540p).mp4` | 0:11, 480x852 vertical, mono | Reel 0:30-0:37 (packed floor) |
| `yeah!_v1 (540p).mp4` | 0:14, 480x852 vertical | NOT USED in v1 (too dark/distant; cut per Phase 0) |
| `november_12,_2022_testimonial_v1 (720p).mp4` | 0:11, 720x1280 vertical | Testimonial embed (quote transcription pending) |

## Photos used (from the 10 supplied)

- `04_captures_band_members_performing_on_stage_2.jpg` → `hero-solo-*` (solo hero, email card)
- `04_a_strong.JPEG` → `hero-vocalist-*` (vocalist + root hero)

## Generated page assets (`dist/adrian/assets/img/`)

`hero-solo` 1280x1920 (src-limited) + 800w · `hero-vocalist` 1600x2000 + 800w ·
`poster-reel` / `poster-film` / `poster-promo` 1600x900 + 800w ·
`poster-neon` / `poster-testimonial` 720x1280. All JPEG (q85) + WebP (q82).
Poster frames: big_spring t=2 (reel), t=40 (film), promo t=26, Neon Moon t=13,
testimonial t=3.

## Email cards (`dist/adrian/assets/email/`)

`card-solo.jpg`, `card-vocalist.jpg` — 1200x675 JPEG, ~100-111KB.

## Second batch of sources (added by Adrian 2026-07-24, full-song phone videos)

| File | Length / format | Notes |
|---|---|---|
| `uptown-funk-2026a.mp4` | 4:19, 1280x720 horizontal | Locked wide shot, full band; Adrian window 2:30-2:43 |
| `My Girl.MOV` | 1:23, 1530x2720 vertical, 25fps | Adrian close-up, guitar, Market Street dusk; window 0:40-0:50 |
| `You Make My Dreams.MOV` | 1:28, 1530x2720 vertical | Adrian in sequin tux, guitar, ballroom; window 0:18-0:32 |
| `Locked Out Of Heaven Neal Hamil.MOV` | 1:14, 1530x2720 vertical | Adrian + co-vocalist, drum head visible; window 0:05-0:15 |
| `Mr. Brightside Market Street.MOV` | 3:24, 1530x2720 vertical | Adrian fronting outdoor public gig; window 1:31-1:45 |
| `24k Magic San Marcos Wedding.MOV` | 0:18, 720x1280 vertical HEVC | Stage POV, packed tent, Adrian to camera; window 0:02-0:15 |
| `Friends In Low Places Neal Hamil.MOV` | 2:10, 1530x2720 vertical | Window 0:36-0:44; reserve, not in v3 |
| `24k Magic Neal Hamil.MOV` | 4:51, 1530x2720 vertical | EXCLUDED by Adrian |

All windows above are Adrian's own timestamp pass (2026-07-24), and v4 uses
every one of them at the full length he gave ("let's just keep the timestamps
that I gave you"). His exclusions: 9pc promo everywhere (it showcases another
vocalist) and `24k Magic Neal Hamil`.

## Reel draft v4 (NOT in repo) — all of Adrian's windows, full length

`~/Desktop/EPK/renders/adrian_michael_vocalist_reel_v4_draft.mp4` — 2:21
(141.1s), 1920x1080, 30fps, H.264 CRF19 + AAC 192k, 129MB. Running order
(his in-point → length), sequenced as an energy arc; windows untouched:
big_spring 0:00 (5s) → suavemente 0:00 (13s) → My Girl 0:40 (10s) →
You Make My Dreams 0:18 (14s) → Neon Moon 0:12 (18s) → Mr. Brightside 1:31
(14s) → uptown-funk 2:30 (13s) → crazy_in_love 0:00 (10s) → Locked Out Of
Heaven 0:05 (10s) → Friends In Low Places 0:36 (8s) → play_that_funky 0:01
(6s) → yeah! 0:00 (8s) → 24k Magic San Marcos 0:02 (13s) → end card 5.5s.
Verticals pillarboxed over a blurred fill; audio per-clip live sound,
loudnorm I=-16, 0.5s crossfades. End card: `renders/endcard.png`.
Encoded `-g 30` (keyframe every second) + faststart so scrubbing is exact.
v1/v2/v3 superseded.

## Page video encodes (self-hosted; live in `~/Desktop/EPK/renders/web/`)

`adrian-reel.mp4` (66MB, from the v4 master), `neon-moon.mp4` (13MB, full 31s),
`big-spring-wedding.mp4` (61MB, full 1:36 at 1080p), `testimonial-nov-2022.mp4`
(2MB). x264 CRF23-24, `-g 60` (2s keyframes), `+faststart`. Deploy destination:
`proposals.greenwayband.com/adrian/media/`. No Vimeo anywhere (Adrian's call,
2026-07-24, matching the proposal template's self-hosted pattern).

**Seeking:** Netlify serves HTTP Range correctly, so the deployed players
scrub normally. Python's stock `http.server` does NOT, which silently makes
local preview video unseekable — the `adrian-epk` launch entry therefore runs
`range_server.py` (session scratchpad) on port 8894, not `http.server`.
Verified: 206 Partial Content, forward and backward seeks land on all four
players.

## Not used

Remaining 8 supplied photos (alternates), `yeah!_v1`, `crazy_in_love_v1`,
`Friends In Low Places`, `24k Magic Neal Hamil` + `Greenway_Band_9pc_Promo`
(both excluded by Adrian), Desktop `Set List Full.pdf` (predates song-list
v4; page links the hosted list).
