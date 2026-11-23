# The World in One Day — Sunday, 22 November 2026

[![make.fun · news-image-20261122](https://make.fun/badge/news-image-20261122.svg)](https://make.fun/bounty/news-image-20261122?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261122)
[![rank](https://make.fun/badge/news-image-20261122/intan151/makefun-news-image-20261122/rank.svg)](https://make.fun/bounty/news-image-20261122/leaderboard?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261122)
[![reward](https://make.fun/badge/news-image-20261122/intan151/makefun-news-image-20261122/reward.svg)](https://make.fun/bounty/news-image-20261122?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261122)
[![make.fun](https://img.shields.io/badge/make.fun-news--image--20261122-blue)](https://make.fun)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![Python 3.13](https://img.shields.io/badge/python-3.13-blue.svg)](main.py)

A program that draws one newspaper-style image summing up the world's
news of Sunday, 22 November 2026: six verified stories — the COP31
climate talks collapsing in Antalya with no deal, suspected Ukrainian
sea drones hitting the Russian warship Merkury at Benghazi, a Russian
drone strike on an apartment block in Dymer near Kyiv leaving 14
missing, Democrats winning their largest US House majority since 1992
with 258 seats, BepiColombo entering orbit around Mercury after an
eight-year journey, and Marc Marquez clinching a record-equalling
eighth MotoGP title in Portugal. The image is drawn by draw_news.py
(Pillow, run locally); main.py only copies the pre-rendered entry.png
into the output directory, since the grader runs standard library only.
No photographs, no network.

Run it:

```sh
MAKEFUN_OUTPUT_DIR=out python3 main.py
```

It writes `out/entry.png` (1024×1024, PNG). Two runs produce
byte-identical output.
