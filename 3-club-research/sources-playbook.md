# RoboMaster Technical Sources — Verified Access Playbook

> **2026-09-08 refresh:** the public ARTICLE feed returned **997 articles**; `rm_public_research.py bbs-index` builds a local index of them. New 2026 sources include NJUST Alliance auto-aim, HIT Weihai HERO sentry navigation, RPS partial auto-aim, SZU detector models/deployment, SCUT wheel-legged control and ZJU gimbal CAD. These dated findings supersede older ecosystem assumptions below; a 2026 `pushed_at` is not a 2026 algorithm change.
>
> **Access correction:** a BBS page may look empty while its public Nuxt `htmlContent` contains the complete article. A bounded local reader now recovers that content and its links without executing JavaScript. Current BBS `/search/` routes can also expose public metadata. Search snippets are discovery leads, not verified technical evidence. Current availability of SZU's `SZURPVision` organization replaces the older implication that its code cannot be found on GitHub.

> **2026-10-01 re-verification on two test machines.** Changes:
> - **CSDN is readable via Jina.** Use plain `curl -s https://r.jina.ai/<URL>` with curl's default user-agent. A browser user-agent trips Jina's Cloudflare challenge.
> - **WeChat articles are readable by direct curl.** WebFetch and Jina both hit a CAPTCHA.
> - **Bilibili's `view` API now returns HTTP 412.** Read the video page's `__INITIAL_STATE__` instead.
> - **Bilibili `space` pages are readable via Jina.**
> - **Gitee clone access and the unauthenticated API v5 are verified.**
> - **OSHWHub and GitCode are added (§7).** OSHWHub is DNS-blocked on some campus networks, so use Jina or another network.
> - **`gh search code` needs the GitHub CLI, logged in (`gh auth login`).**
> - **BBS on-site search now works**: `rm_public_research.py bbs-search` (§1).
> - **`yt-dlp` (with deno) and `bili` are installed on both hosts** (§5). YouTube subtitles work; Bilibili subtitles remain login-gated.
>
> Every route below was empirically tested from this environment on 2026-07-07 (6-agent recon; full evidence archived in the session task output `w8omrdd04.output`). Re-verify a route before declaring a source "broken" — sites change.

## Quick router

| Question type | Go to (in order) |
|---|---|
| Competition rules / referee system | **First determine which event governs**: RMUC/RMUL (China) → latest RMOC manual PDF (§2) → BBS rules hub `bbs.robomaster.com/wiki/20204847`; NA league (RMUL NA / RMNA, rebranded **ARC Robotics** from 2026 — rules may diverge from RMOC) → `arc-robotics.org` (verified fetchable, server-rendered). Protocol: `github.com/RoboMaster/referee_serial_port_protocol` (≤2020) |
| Embedded / 电控 (motors, CAN, power, boards) | `github.com/RoboMaster/Development-Board-C-Examples` → HNUYueLuRM/basic_framework → **taproot (English!)** → BBS 电控 column `wiki/4574` → cnblogs 电控入门 series |
| Vision / auto-aim / 自瞄 | Current research map → NJUST/SZU/RPS/Tongji releases and maintained rm_vision forks → BBS 算法 column → team docs |
| Sentry navigation / 哨兵导航 | Current research map → HERO 2026, PolarBear, ZJU/RPS/WUST/BIT release leads → BBS 算法 column; RoboRTS is historical reference |
| Mechanical / CAD | BBS 机械 column `wiki/4571` → BBS 硬件 column `wiki/4580` (boards/supercaps) |
| PCB / hardware designs (supercap, power, CAN boards) | BBS 硬件 column `wiki/4580` → OSHWHub (§7; via Jina where it is blocked) → GitHub/Gitee |
| "What did teams open-source this season?" | `bbs-search "<中文 topic> 开源" --sort createAt` → `bbs.robomaster.com/article` feed → `github.com/topics/robomaster` sorted by recency |
| Learning material for a new member | taproot wiki (EN) → robowalker_train, NeoZng/vision_tutorial → Bilibili 从零开始 series (BV1E24y1C7ER) → cnblogs |

**Cross-cutting rules**: search Chinese sources with **Chinese keywords** (glossary at bottom); answer in **English** with citations; for rules always state the manual **version + date** (version churn is high — V1.0.0→V1.1.0 within months); cache distilled answers as `3-club-research/<topic>.md`.

---

## 1. RoboMaster BBS — `bbs.robomaster.com` ✅

DJI's official community, rebranded "RoboMaster 社区" (article/Q&A/wiki platform; the old Discuz forum is gone).

- **Discover (on-site search, working since 2026-10-01)**: run `python 4-for-your-AI/tools/rm_public_research.py bbs-search "<中文关键词>"`. Add `--sort createAt` for newest first, or `--sort updateAt` for recently changed (verified 2026-10-16; this is how new rules manuals surface, §2); `--category ARTICLE|FAQ|WIKINODE|TEAMWIKINODE|WIKI|ALL` (default `ARTICLE FAQ`; the three wiki values verified 2026-10-16); `--page N --page-size ≤100`.
  - It returns title, URL, `created_at`, `updated_at`, tags and intro. No login is needed, and it works on both hosts. Articles and Q&A get `/article/{id}` or `/faq/{id}` (`access: fetch`). Rules-hub, team-wiki and wiki-root hits get their hub URL, `/wiki/{wikiId}/{id}` or `/wiki/{wikiId}`, marked `access: browser-only`: the reader sees only the hub's menu there (since 2026-10-16).
  - The server-rendered page `bbs.robomaster.com/search/<keyword>` also shows the top 15 to plain curl or a browser. The old `/search?keyword=` URL shape is wrong and always returns "暂无更多".
  - English keywords match almost nothing.
  - WebSearch `site:bbs.robomaster.com <中文关键词>` remains a fallback.
- **Fetch only these URL shapes**: `/article/{id}` (posts — full technical bodies load without login), `/faq/{id}` (Q&A; the reader recovers the body, verified 2026-10-01), `/wiki/{id}` (curated columns). Legacy `/thread-NNNNN-1-1.html` and `/forum.php?…` URLs return empty shells — if search surfaces one, re-search its exact title with `site:bbs.robomaster.com` to find the migrated `/article/{id}` (migration confirmed to exist, but not for every thread). `/faq/{id}` is unverified.
- **Curated open-source columns** (browse directly):
  - 电控 embedded: `https://bbs.robomaster.com/wiki/4574` (supercap boards, balanced infantry, PID-in-C, IMU attitude, power management)
  - 算法 algorithm/CV: `https://bbs.robomaster.com/wiki/4577` (auto-aim, Sim2Real navigation, radar)
  - 硬件 hardware: `https://bbs.robomaster.com/wiki/4580` (supercap + wireless charging, FOC drives)
  - 机械 mechanical: `https://bbs.robomaster.com/wiki/4571` (chassis, suspension CAD)
  - Rules/resources hub: `https://bbs.robomaster.com/wiki/20204847` (official rulebooks, bilingual)
  - Newest season feed: `https://bbs.robomaster.com/article`
- **Failure modes**: long posts truncate in a plain WebFetch, but `4-for-your-AI/tools/rm_public_research.py fetch` recovers the full body (article/803315: 9.6k chars, verified 2026-10-01). Jina returns only a short shell with no links, so use the reader for BBS. **Forum attachments are public (re-verified 2026-10-16):** PDF reports and CAD zips sit on `hz-rm-bbs-web-prod.oss-cn-hangzhou.aliyuncs.com`, and anonymous HEAD requests returned 200 with sizes for eight of them (PDFs 0.9–11 MiB, CAD zips 77–822 MiB). The reader lists them without downloading them; report the size and ask before pulling large CAD. **Read a PDF with `rm_public_research.py pdf-text "<url>"`** (2026-10-16): pypdf in memory, text only, `--find <词>` for the matching pages, then `--pages N-M`; 25 MiB default cap, `--max-mib` up to 200. On the Tongji 串联腿 chassis-control report (21 pages, 0.9 MiB, made by Chromium) the Chinese text extracts cleanly once radical-glyph substitutions such as ⾔ for 言 and ⻓ for 长 are repaired, which the tool does.
- **Search quirks (2026-10-16):** multi-word queries match inconsistently (`轮腿 过洞` returned 0 hits while `串联腿 过洞` returned 20), so try synonyms (轮腿 / 串联腿 / 平衡; 隧道 / 过洞 / 狗洞 / 越隧). Rules-hub wiki nodes come back as `WIKINODE` hits listed under their creation date; since 2026-10-16 each carries its browser-only hub URL and `updated_at` (see §2).
- **Offline index refresh (2026-10-16):** `rm_public_research.py bbs-index` rebuilds `2026-09-08-rm-bbs-source-index.json` (the name is kept so links work) from the public ARTICLE feed: at most 20 pages of 100, de-duplicated, the same title keyword tags, written atomically, with `checked_at` inside. The 2026-10-16 refresh holds 1068 articles; the 2026-09-07 snapshot had 997.

## 2. Official DJI/RM — GitHub org + CDN PDFs ✅

- **Code**: `github.com/RoboMaster`. Key repos: **Development-Board-C-Examples** (canonical Type C/STM32F407 reference: 20 graded examples incl. 9.remote_control_dma, 14.CAN, 17.chassis_task, 19.gimbal_task, 20.standard_robot; note `readme.md` lowercase — raw URLs are case-sensitive, default branch `master`), **referee_serial_port_protocol** (CN+EN protocol appendix PDFs + parsing code — stops at 2020 V1.1; current-season appendix ships with the season rules package, find via WebSearch), **DevelopmentBoard-Examples** (Type A), **RoboRTS / RoboRTS-Firmware / RoboRTS-Tutorial** (ROS stack; read Tutorial markdown via raw.githubusercontent.com — the rendered robomaster.github.io site is an empty shell).
- **Rules/spec PDFs**: never navigate `www.robomaster.com` (JS shell). WebSearch for direct CDN URLs: current season on `bbs-web-static.robomaster.com` (e.g. RM2026 联盟赛参赛手册), 2019–2022 era on `rm-static.djicdn.com`, 2017–2018 on `cdn-hz.robomaster.com`. BBS announcement articles (e.g. `/article/4856`) aggregate per-season manual links.
- **Rules hub navigation (verified 2026-10-09)**: `bbs.robomaster.com/wiki/20204847` renders only in a real browser (in-app browser works). Path: 比赛规则 Rulebooks → current season (RMUC 2027 had only the 2026-09-09 rule-change preview) → 历史资料 Archives → 2026 比赛规则 → RMUC 2026 page lists every rules/spec/participant manual version with direct `bbs-web-static.robomaster.com` links (read them from the page's `a[href]` via JS). Latest RMUC 2026 rules manual: V2.2.0 (2026-08-07, 21 MB; EN V2.1.0); local copy `inbox/rules/RMUC-2026-Rule-Manual-V2.2.0-20260807.pdf` (§4.1: field 28 m x 15 m; fig. 4-1 top-down, 4-2 oblique, 4-3 axonometric renders; §4.4 fig. 4-35, printed p. 60: tunnel sections 800 x 250 mm and 700 x 260 mm clear). Where pdftoppm is missing, its figures render with PyMuPDF (`fitz`).
- **Is a new manual or revision out? (added 2026-10-16):** only the hub node's own file list answers this. Open the hub page in a browser and read its file list. `bbs-search`, `bbs-feed` and page fetches cannot see hub files, so they never support a "no manual yet" answer. If the node list cannot be read, say "rules hub unchecked", never "no new manual". On 2026-10-15 a search-based check said "there is no 2027 manual" two hours after the RMUL V1.0.0 manual was uploaded (about 15:30 UTC+8).
- **2027 manuals published 2026-10-15 (found 2026-10-16):** RMUC 2027 Rules Manual V1.0.0 (22.46 MB, uploaded about 17:14 UTC+8), RMUL 2027 Rules Manual V1.0.0 (13.46 MB, about 15:30 UTC+8), the shared 2027 Robot Specification Manual V1.0.0 (18.24 MB) and both Participant Manuals, all Chinese only. They sit on hub nodes `wiki/20204847/1969149` (RMUC) and `wiki/20204847/1969150` (RMUL), which were created on 2026-09-04. `bbs-search` lists these nodes as `WIKINODE` hits under that old creation date, so **a newest-first search by creation date does not reveal a new manual.** Their `updateAt` moved to 2026-10-15 (UTC), so `bbs-search "2027 规则手册" --category ALL --sort updateAt` lists both nodes first (verified 2026-10-16), and since that date each hit carries its hub URL marked browser-only. `fetch https://bbs.robomaster.com/wiki/<node id>` returns HTTP 400, and fetching the hub URL returns only the menu: open the node in a browser and read its `a[href]` links. The upload time is the epoch-milliseconds folder name in each file URL.
- **PDF pipeline**: `rm_public_research.py pdf-text "<url>"` (2026-10-16) reads PDFs on the allowlisted hosts (forum attachments, `bbs-web-static.robomaster.com` manuals) with pypdf, Chinese included; see §1. Otherwise: WebFetch reports the PDF "unreadable" but saves the binary to a local path → run `pdftotext <saved.pdf> -` (`-f/-l` for page ranges). English PDFs extract cleanly; **Chinese PDFs drop CJK glyphs** (this machine's poppler lacks CJK CMaps) → prefer EN editions, or `pip install pypdf` as fallback. The Read tool's PDF rendering does not work here (pdftoppm missing).
- **api.github.com** works unauthenticated (~60 req/hr) for repo lists/trees; for heavy code reading, `git clone` (no auth needed) into the scratchpad.

## 3. GitHub team ecosystem ✅

- **Discover**: `github.com/topics/robomaster` (star-ranked snapshot); awesome-lists `robomaster-oss/awesome-robomaster` + OpenRoboMaster; anonymous repo search works incl. Chinese terms (`github.com/search?q=…&type=repositories`); `api.github.com/search/repositories` for JSON. **Code search (`type=code`) is login-walled anonymously**. With the GitHub CLI logged in, `gh search code "<terms>" --language c` works (verified 2026-10-01). Otherwise, shallow-clone (`git clone --depth 1`) and Grep locally.
- **Key repos by area**:
  - Vision: `chenjunnn/rm_vision` + `rm_auto_aim`, the community-standard ROS2 auto-aim. These are **frozen, not archived**: GitHub pushes 2024-11 and 2023-05, and the `gitlab.com/rm_vision` group's last activity was 2024-03-10 (checked 2026-10-01). They remain the canonical algorithm upstream, with current behaviour in forks (Ericsii/rm_vision, SCAU-RM-NAV, SMBU-PolarBear pb2025_rm_vision); TongjiSuperPower/sp_vision_25; SJTU: CVRM2021-sjtu, blog `sjtu-robomaster-team.github.io`
  - Embedded/EC: `HNUYueLuRM/basic_framework` (317★, bsp/module/app layers, best-documented Chinese starter; docs `hnuyuelurm.github.io/YueLu_EC_Guide`); `rm-controls/rm_control` + `rm_controllers` (ROS); XDU-IRobot (librm, irobotEC); xrobot-org/XRobot
  - **English-language**: `uw-advanced-robotics/taproot` — the de-facto EN RoboMaster embedded framework (GPL C++, DJI motors/CAN, DR16, referee UART, command/subsystem scheduler). **Use its GitHub wiki** (verified readable); its GitLab home's wiki renders empty via fetch; rendered docs at `aruw.gitlab.io/controls/taproot`. Natural onboarding path for an English-speaking team.
  - Sentry nav: `SMBU-PolarBear-Robotics-Team/pb2025_sentry_nav` (Mid360 + Point-LIO + small_gicp + Nav2; simulator `rmu_gazebo_simulator` on Ignition Fortress, robot in SDF xmacro), LihanChen2004/pb_rm_simulation (archived; Gazebo Classic 11 + planar_move).
  - Training: yssickjgd/robowalker_train (USTC EC course), NeoZng/vision_tutorial, PennState-RoboX/RobomasterControlHandbook (EN/CN)
  - Docs: `robomaster-dev.readthedocs.io/zh-cn/latest/`
- **Liveness (2026-10-01 sweep of 88 cited repos):**
  - 87 are alive.
  - `SZURPVision/26_YK_Network_Deployment_Lib` returns 404; use `SZURPVision/26_NNDeployment_Lib_and_Detection_Models`.
  - `PageChen04/radar_ros_ws` and `hkustenterprize/RM2023-SuperCapacitor` are archived.
  - `xrobot-org.github.io` now redirects to `xrobot.work`.
- **Gotchas**: default branch varies (master vs main) — check before building raw URLs; cosmetic "error while loading" widgets on org pages are ignorable; season repos rot — check last-commit dates; some famous teams have no GitHub org ("RobotPilots" on GitHub is an unrelated account — Shenzhen U publishes via BBS + Gitee; HITSZ via member accounts) — verify team identity in the README, and when a team is missing, WebSearch `<team name> bbs.robomaster.com 开源`.

## 4. Gitee — `gitee.com` ✅

- Repo pages, `/tree/`, `/blob/` all fetch without login. **Raw files are a 2-step dance**: `gitee.com/{o}/{r}/raw/{branch}/{path}` → 302 to a signed `raw.giteeusercontent.com` URL returned in the fetch output → fetch that URL immediately (it expires).
- **On-site search unusable** (`so.gitee.com` = JS shell; `/explore/*` = HTTP 405) → discover via WebSearch `gitee.com robomaster <中文关键词>`.
- Key: `gitee.com/hnuyuelurm/basic_framework` (mirror), `gitee.com/robomaster-edu/RoboMaster-SDK`, `gitee.com/willize/RoboRTS-Firmware` (mirror), `gitee.com/robomaster-oss/rmoss_core` (ROS2 ballistics/camera), curated collection `gitee.com/Derkai52/collections/288` (各大院校开源方案汇总).
- **API v5 works without a token** for repo metadata (`gitee.com/api/v5/repos/{o}/{r}`) and full file lists (`…/git/trees/{branch}?recursive=1`). Unauthenticated `api/v5/search/repositories` returns `[]`. Verified 2026-10-01.
- Mirrors can be stale, so prefer the GitHub canonical when freshness matters. The `hnuyuelurm/basic_framework` mirror was last pushed 2025-05-28, against GitHub 2026-09-07. `git clone` / `git ls-remote` from Gitee **works** (verified 2026-10-01 on both hosts).

## 5. Bilibili — finder, not reader ⚠️

Use it to **locate** videos and harvest description links; the video/audio itself is unreachable (subtitles login-gated: `need_login_subtitle:true`).

- **Search**: `rm_public_research.py bili-search "<中文>" [--page N]` (2026-10-16) reads the cookie-free `api.bilibili.com/x/web-interface/search/all/v2`: about 20 videos per page plus matching channels, no login. `search/type` now returns HTTP 412 without cookies, and `all/v2` ignores `order=`. In a browser, `https://search.bilibili.com/all?keyword=<URL-encoded 中文>` (+`&page=N`) shows the same ranking, and channels are at `/upuser?keyword=`; its embedded state is a JavaScript function, not JSON, so don't scrape it. WebSearch `site:bilibili.com` returned nothing on 2026-10-16.
- **Metadata**: `rm_public_research.py bili-video <BV id | URL>` (2026-10-16) does the following without running any script: title, uploader, date, description links, parts and collection episodes. By hand: fetch the video page `bilibili.com/video/BV…/` with `curl --compressed`, because the body is gzip even when not requested. The page embeds `window.__INITIAL_STATE__.videoData`: title, uploader, publish date, **description with links**, cid, subtitle list and episode list. **The JSON `x/web-interface/view?bvid=` API returns HTTP 412 for anonymous calls on both hosts (2026-10-01)**, so don't use it. Of the search APIs, only `x/web-interface/search/all/v2` still works without cookies (`search/type` returned 412 on 2026-10-16). Space out calls, because bursts trigger rate limiting.
- **Then follow the description links** (GitHub lesson code, kdocs outlines, forum posts) — that text is the answer material.
- **CLI tools (installed on both hosts 2026-10-01)**:
  - Without a login, `bili search "<中文>" --type video -n 10 --yaml`, `bili user-videos <uid> -n 20 --yaml` (channel listing), `bili user <uid>` and `bili hot` work.
  - `bili video` returns 412, the same block as the view API. Use the video page instead.
  - `yt-dlp` reads Bilibili metadata (`--print "%(title)s"`) and **downloads audio anonymously** (`-f <audio id>`; `-F` lists the formats).
  - **Subtitles stay login-gated**: `yt-dlp --list-subs` shows only `danmaku`. **Transcribe locally instead with `python 4-for-your-AI/tools/public_media_transcribe.py <BV id | Bilibili/YouTube URL> [--start S] [--end S] [--model medium]`** (2026-10-01, both hosts).
    - What it does: downloads the smallest audio stream with no login, then runs local faster-whisper with the RM glossary as `hotwords` and a short simplified-Chinese prompt, with `condition_on_previous_text=False`.
    - Output: JSON with timestamped segments and `quality_warnings`. Windows are 600 s per call (240 s for `medium`), with `next_start` to continue.
    - **Default `small`**: 9/12 RM jargon terms, 100% of speech kept, about 1× real time. Use it for noisy match or stream audio, and as the general default.
    - **`--model medium`**: 11/12 terms (CAN, C610 and 十安 correct) on clean single-speaker tutorials, at 3–7× real time. It **dropped up to 38% of speech on noisy audio**, so use it only for clean lecture-style videos.
    - Treat transcripts as good for search, summary and locating content; check exact wording before quoting. English matches YouTube captions at 97%.
  - Space Bilibili calls at least 5 s apart; back-to-back calls get rate-limited.
  - **On Windows, `bili` crashes with `UnicodeEncodeError` when its output is piped**: set `PYTHONUTF8=1` (verified 2026-10-16).
- **"Find the robot I saw" (2026-10-16):** the official account's 「机器人图鉴」 Robot Gallery season (id 1939428, 101 clips from 2023 to 2026, one notable robot each) is the best index. List all its clips from any episode page's `__INITIAL_STATE__.videoData.ugc_season`: `rm_public_research.py bili-video BV1CSG26BENT` does it. `bili search "串联腿 过洞"` found the ECUST tunnel-crossing balancer in one query; WebSearch `site:bilibili.com` returned no Bilibili results at all.
  - **Never run `bili` write commands** (`like`, `coin`, `triple`, `dynamic-post`, `unfollow`, `login`).
- **Whole courses → English study notes (2026-10-02):** run `python 4-for-your-AI/tools/lecture_series.py manifest <any BV of the course> --slug <name>`, then `transcribe`, then `notes`. The how-to is the `lecture-notes` skill (`4-for-your-AI/skills/lecture-notes/SKILL.md`).
  - The video page's `__INITIAL_STATE__.videoData.ugc_season` lists every episode of a 合集 with its duration and description: one fetch, no API. Multi-part videos come from `videoData.pages`.
  - Finished notes live in `2-courses/<slug>/`, and the catalog is `2-courses/README.md`.
- **Channel listing**: `space.bilibili.com/<uid>` is a shell when fetched directly, but **readable via Jina** (`curl -s https://r.jina.ai/https://space.bilibili.com/<uid>` lists the BV IDs; verified 2026-10-01).
- **Dead ends — don't try**: `/read/cv…` articles (CAPTCHA) and the space-videos API (412). `b23.tv` short links redirect to the video page.
- Key content: official 机甲大师 account (UID 20554233 — rules briefings, replays); **从零开始制作RoboMaster步兵机器人** (TIANBOT series, one BV per episode: LED→PWM→UART/DMA→DT7→IMU→CAN→FreeRTOS→PID→mecanum; `BV1E24y1C7ER` is ep. 21, RoboMaster Assistant and ESC firmware; enumerate the rest via search); 学长大人兼前辈 电控教程 (each lesson links its GitHub code); USTC RM 电控合集 (BV1HY411D7Ar).

## 6. Chinese blogs — mixed ⚠️

| Domain | Status | What to do |
|---|---|---|
| **cnblogs.com** | ✅ fully readable | First-choice blog source. Canonical series: sasasatori's RoboMaster电控入门 0–8 (env setup→GPIO→dbus/DT7→RM motor CAN→FreeRTOS), AZ_POLARIS 电控培训, 中南 supercap notes. Discover: WebSearch `site:cnblogs.com RoboMaster <中文>` |
| Team github.io wikis | ✅ fully readable | `hnuyuelurm.github.io/YueLu_EC_Guide` (USART/DMA/SPI/I2C/CAN/USB, IMU & 3D rotation, balanced infantry), `sjtu-robomaster-team.github.io` (motor/gimbal/chassis tasks, PID, calibration, YOLO deployment). Discover: WebSearch `<team> github.io 电控 OR 视觉` |
| blog.csdn.net | ✅ **via Jina** (2026-10-01) | Direct and WebFetch return HTTP 521. **`curl -s "https://r.jina.ai/<CSDN URL>"`** (default curl user-agent) returns the full article body on both hosts. It is the largest CN tutorial corpus, so treat it as a primary source again, while still preferring an original on GitHub/BBS when one exists |
| zhuanlan.zhihu.com | ❌ HTTP 403 | Direct, WebFetch and Jina all fail; Jina gets the "安全验证" CAPTCHA. Use snippet-mining. Classic articles (Kalman-in-gimbal, armour recognition) are often mirrored elsewhere |
| mp.weixin.qq.com | ✅ **direct curl** (2026-10-01) | WebFetch and Jina get the "环境异常" CAPTCHA. Plain `curl -s <URL>` returns the full article (verified on two machines, one article tested); strip the HTML locally. The club reader doesn't allow this host |
| guyuehome.com | ⚠️ discovery-only | The body is empty via direct, WebFetch and Jina (re-checked 2026-10-01). Snippets point to cnblogs originals and GitHub code |
| manuals.plus | ❌ 403 | Never route there for rules — use official CDN PDFs |

Members will paste CSDN/Zhihu/WeChat links constantly: don't say "can't open it" — identify the content from the URL + search snippets and route to a readable equivalent.

**Agent Reach routes ([Agent Reach](https://github.com/Panniantong/Agent-Reach), optional), tested 2026-10-01.**
- Jina Reader opens CSDN, Bilibili video and space pages, OSHWHub and GitLab READMEs. It does not open Zhihu, WeChat, guyuehome or Gitee.
- Call Jina with plain curl. A browser user-agent gets HTTP 403 from Cloudflare. Use public URLs only.
- `bili-cli`, `opencli` and `yt-dlp` are installed on neither host, so their Bilibili subtitle routes are still untested.

## 7. Other open-source spaces (added 2026-10-01)

| Space | What's there | Route |
|---|---|---|
| **OSHWHub** `oshwhub.com` (立创开源硬件平台) | RM PCB projects: supercap controllers (e.g. `ltyxh/psp-zhan-dui-duo-xiang-chao-dian`, Pacific Spirit RM24), CAN distribution boards, armour boards, often with a PDF technical report attached | **Blocked on some campus networks** (campus DNS returns NXDOMAIN; public DNS and DoH are reset). Off campus, use direct fetch or `rm_public_research.py fetch`. Where it is blocked, use Jina. Discover with WebSearch `site:oshwhub.com RoboMaster <中文>` |
| **GitCode / AtomGit** `gitcode.com` | `gh_mirrors/*` GitHub mirrors plus native CN team repos (e.g. `gcw_GtTHzau8/RM26_NUDT_navigation`, the NUDT 2026 sentry nav on ROS2 Humble) | Page HTML gives title and description only. Mirror pages and Jina return HTTP 418; the API needs a `private-token`. **Read via `git clone --depth 1`**, which works on both hosts. Discover with WebSearch `site:gitcode.com RoboMaster <中文>` |
| **GitLab** `gitlab.com` | `rm_vision` (frozen since 2024-03), `aruw` (taproot, aruw-mcb) | The unauthenticated API v4 works (`/api/v4/groups/<g>/projects`). Repo pages are an SPA, so use Jina for READMEs or clone |
| **arXiv** | RM-adjacent papers | `export.arxiv.org/api/query?search_query=all:robomaster` |
| **Hugging Face** | Nothing competition-grade yet: only S1/EP datasets and noise | `huggingface.co/api/models?search=` works; re-check before assuming a model is absent |

## Chinese keyword glossary

> RoboMaster has several circuits (RMUC and RMUL in China, RMUL/RMNA in North America). Always state which rulebook + version an answer cites.

电控 (embedded/elec control) · 视觉/自瞄 (vision/auto-aim) · 装甲板识别 (armor detection) · 云台 (gimbal) · 底盘 (chassis) · 功率控制/超功率 (power control) · 超级电容 (supercapacitor) · 裁判系统 (referee system) · 步兵 (infantry) · 平衡步兵 (balancing infantry) · 串联腿/轮腿/轮足 (serial leg / wheel-leg) · 隧道/过洞/狗洞/越隧 (tunnel / through the hole) · 英雄 (hero) · 工程 (engineer) · 哨兵 (sentry) · 无人机/空中 (aerial) · 飞镖 (dart) · 雷达 (radar) · 电机 (motor) · 拨弹/摩擦轮 (feeder/friction wheels) · 弹道 (ballistics) · 卡尔曼滤波 (Kalman filter) · 能量机关 (power rune) · 开源 (open source) · 规则 (rules)
