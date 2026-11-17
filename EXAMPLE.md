# A worked example

**Question:** *Which teams have open-sourced their sentry navigation, and where is it?*

This is the first step the kit's research skill takes: search the official RoboMaster forum in Chinese. The run below is real, made on 2026-11-17.

```bash
PY 4-for-your-AI/tools/rm_public_research.py bbs-search "哨兵导航" --page-size 8
```

The forum returned 268 posts. The top eight by relevance, with titles translated:

| Posted | Team | What they released | Views | Post |
|---|---|---|---|---|
| 2026-09-09 | Northeastern University (China), TDT | Sentry navigation front end and back end, for 2D grid maps | 9,536 | [1969284](https://bbs.robomaster.com/article/1969284) |
| 2026-08-23 | China University of Petroleum (East China), RPS | Navigation for a swerve-drive sentry, built on ROS 2 Nav2 | 4,773 | [1942060](https://bbs.robomaster.com/article/1942060) |
| 2026-08-07 | Zhejiang University, Hello World | Navigation for a wheel-legged sentry, 2026 season | 5,050 | [1938205](https://bbs.robomaster.com/article/1938205) |
| 2025-09-06 | Harbin Institute of Technology, I Hiter | Sentry navigation code and simulation, 2024 version | 7,241 | [810080](https://bbs.robomaster.com/article/810080) |
| 2025-08-25 | University of Science and Technology of China, RoboWalker | RM2025 technical report written around sentry navigation | 8,019 | [803740](https://bbs.robomaster.com/article/803740) |
| 2025-04-19 | Dongguan University of Technology, ACE | RM2025 sentry navigation | 5,494 | [714451](https://bbs.robomaster.com/article/714451) |
| 2025-01-08 | Xidian University, IRobot | RMUC 2024 sentry navigation, using Faster-LIO and FAR Planner | 5,223 | [374512](https://bbs.robomaster.com/article/374512) |
| 2024-06-09 | Shenzhen MSU-BIT University, Polar Bear | RM2024 sentry navigation on ROS 2 | 15,339 | [9662](https://bbs.robomaster.com/article/9662) |

The descriptions come from each post's own opening lines, so check the post before relying on a detail.

## What the kit does next

Following the research skill, your AI then:

1. **Reads the posts that matter** with `fetch <url>`, including the repository links inside them.
2. **Checks each repository** with `github <owner/repo>`: licence, last commit, whether it is still maintained.
3. **Answers in English with a link for every claim,** and says which season and rulebook each design was built for.
4. **Saves a short note** in `3-club-research/`, so the next question on the topic starts from it.

A search in English finds almost none of these posts. That gap is what the kit is for.
