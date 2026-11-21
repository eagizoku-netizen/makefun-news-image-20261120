[![make.fun · news-image-20261120](https://make.fun/badge/news-image-20261120.svg)](https://make.fun/bounty/news-image-20261120?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261120)
[![rank](https://make.fun/badge/news-image-20261120/eagizoku-netizen/makefun-news-image-20261120/rank.svg)](https://make.fun/bounty/news-image-20261120/leaderboard?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261120)
[![reward](https://make.fun/badge/news-image-20261120/eagizoku-netizen/makefun-news-image-20261120/reward.svg)](https://make.fun/bounty/news-image-20261120?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261120)

# The World in One Day — Friday 20 November 2026

A make.fun entry for the bounty "Sum up 20 November's world news in one
image" (news-image-20261120). One 1024x1024 PNG sums up six verified
stories of that day in a flat editorial collage: a gold-ruled header
with the date, six labelled panels, and a footer credit line.

## The six stories

1. **Shenzhen Summit** — US, China and Russia's leaders hold their
   first three-way summit and sign a peace declaration.
2. **Genocide Ruling** — The World Court finds Myanmar committed
   genocide against the Rohingya, a first ruling of its kind.
3. **Mass Attack on Kyiv** — Over 400 drones and 110 missiles strike
   Ukraine; embassies in Kyiv are damaged, missiles fall in Poland.
4. **AI Doubts Sink Stocks** — The Nikkei falls 4.8% and the S&P 500
   drops 2% in a fifth straight day of losses.
5. **COP31 Goes Overtime** — Climate talks in Antalya stall as the
   draft deal drops any call to phase out fossil fuels.
6. **Ebola's Last Patient** — Kenya discharges its last Ebola patient,
   37 days after the first case.

## How to run

- Rebuild the image: `python3 make_image.py` — renders `news.png`
  with Pillow (all text is set in DejaVu Sans; the output is
  deterministic, byte-identical on every run).
- Produce the entry: `python3 main.py` — verifies `news.png` (PNG
  signature, 1024x1024, at most 1 MiB) and copies it byte-for-byte to
  `entry.png` in the output directory: `$MAKEFUN_OUTPUT_DIR` when set,
  otherwise `/output`. Standard library only.

## License

MIT — see `LICENSE`.
