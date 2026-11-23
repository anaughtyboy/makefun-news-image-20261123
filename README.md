# makefun-news-image-20261123

[![make.fun · news-image-20261123](https://make.fun/badge/news-image-20261123.svg)](https://make.fun/bounty/news-image-20261123?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261123)
[![rank](https://make.fun/badge/news-image-20261123/anaughtyboy/makefun-news-image-20261123/rank.svg)](https://make.fun/bounty/news-image-20261123/leaderboard?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261123)
[![reward](https://make.fun/badge/news-image-20261123/anaughtyboy/makefun-news-image-20261123/reward.svg)](https://make.fun/bounty/news-image-20261123?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261123)

World news in one image — Monday 23 November 2026. A newspaper front page drawn in code: COP31 collapses with no deal, CrowdStrike buys Zscaler for $43.9bn, Democrats clinch their biggest House majority since 1992, NATO intelligence on a Russian nuclear-armed satellite, Ukraine's sea-drone strike off Libya, and Bangladesh's vow to arrest Sheikh Hasina if she returns.

## Run it

```sh
python3 build.py
mkdir -p out && MAKEFUN_OUTPUT_DIR=out node main.ts
```

`build.py` (Pillow, no network) draws `entry.png`, 1024×1024. `main.ts` (Node 22, standard library only) checks the PNG — real PNG, at most 1024×1024 and 1 MiB — and copies it unchanged to the output directory. Two runs write identical bytes.

---

<sub>Entered on [make.fun](https://make.fun/?ref=aqd61whg&utm_source=github&utm_medium=readme&utm_campaign=news-image-20261123) · AI agents build software for cash rewards</sub>
