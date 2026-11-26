# The World on Wednesday — 25 November 2026

[![news-image-20261125](https://make.fun/badge/news-image-20261125.svg)](https://make.fun/bounty/news-image-20261125)
[![Rank](https://make.fun/badge/news-image-20261125/marwankickup/news-image-20261125-entry/rank.svg)](https://make.fun/bounty/news-image-20261125)
[![Reward](https://make.fun/badge/news-image-20261125/marwankickup/news-image-20261125-entry/reward.svg)](https://make.fun/bounty/news-image-20261125)

Entry for [news-image-20261125](https://make.fun/bounty/news-image-20261125): a program
that draws one newspaper front page summing up the world news of
Wednesday 25 November 2026.

Run it with Node 22:

```sh
node main.ts   # writes /output/entry.png (or $MAKEFUN_OUTPUT_DIR/entry.png)
```

`main.ts` runs `draw_image.py` (Pillow) to draw the page, then validates the
PNG bytes itself — magic bytes, IHDR size/CRC, bit depth and colour type,
and the IEND trailer — before writing `/output/entry.png`.

Six stories, verified against wire reports for 25 November 2026:

1. **US tariffs** — the US proposed new tariffs on 14 trading partners,
   highest for China (+20% on Chinese goods).
2. **Hormuz** — oil tankers hit naval mines in the Strait of Hormuz and
   caught fire on an unofficial route, Iran says.
3. **Shenzhou 24** — China launched Shenzhou 24 to Tiangong; Pakistani
   payload specialist Muhammad Zeeshan Ali is the first foreigner aboard.
4. **Canary Islands** — a record 2,100+ migrants reached the Canary Islands
   in 24 hours on crowded boats.
5. **US inflation** — Thanksgiving dinner costs about 6% more than last
   year as US prices stayed high in October.
6. **Abrego Garcia** — Kilmar Abrego Garcia, wrongfully deported, left the
   US voluntarily for Spain.

The image is deterministic: two runs produce byte-identical PNGs.

## License

MIT — see LICENSE.
