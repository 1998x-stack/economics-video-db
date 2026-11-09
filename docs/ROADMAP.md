# Incremental implementation roadmap

Each phase should be a separate reviewed PR with tests and a demonstrated artifact.

## Phase 0: skeleton [scaffold]
- [x] Python package, CLI, documentation, schemas, gitignored data directories, placeholders.
- [x] Douyin URL validation and an operator-assisted capture-one flow.
- [ ] Run one authorized test video in the user's Chrome + local loopback environment.

## Phase 1: reliable single-video capture
- [ ] Verify macOS/Linux/Windows audio routing and Chrome permission.
- [ ] Add audio RMS/silence checks, clipping/length QC, trim silence.
- [ ] Persistent job ledger with restart, duplicate detection and failure states.
- [ ] Test one accessible, authorized Douyin clip from page to verified WAV.

## Phase 2: Pi-agent homepage discovery + serial capture (Douyin first, then Xigua)
- [ ] Build persistent jobs table: platform, creator ID, video ID, URL, discovery checkpoint, status, retries and provenance.
- [ ] Expose noninteractive local recorder start/status/stop commands for Pi. Current capture-one is NOT suitable for unattended agents.
- [ ] Implement homepage visible-works enumeration and creator identity verification for Douyin.
- [ ] Build a separate Xigua author/profile discovery adapter without sharing unverified selectors or IDs.
- [ ] Model one-video-at-a-time lease, restart, failed attempts and audio quality flags.
- [ ] Pilot 3 authorized videos with failure and crash recovery. Read docs/AGENT_WORKFLOW.md before writing automation.

## Phase 2A: browser-harness video player adapter
- [ ] Inspect <video> elements and accessible UI elements only; handle SPA navigation.
- [ ] Start recorder BEFORE playback; confirm transition to playing.
- [ ] Poll paused/currentTime/ended; distinguish end, buffering, live video and timeouts.
- [ ] Stop recorder AFTER verified end, never upon unrelated navigation.
- [ ] Operator override and consent, rate limits, login/denial handling.
- [ ] Serial queue with no concurrent tabs or recorders in shared local Chrome; prevent recommended autoplay contamination.

## Phase 3: ASR and corpus
- [ ] Test faster-whisper and FunASR on 20 manually reviewed samples.
- [ ] Store raw timestamped segments and review versions; flag numbers/proper nouns.
- [ ] Media/video duplication detection; transcript CER quality report.

## Phase 4: structured LLM analysis
- [ ] JSON-schema validated claim/forecast extraction.
- [ ] Source segment evidence verifier, dates/units/conditions and citation links.
- [ ] Human review queue and prompt/model provenance.

## Phase 5: database, search, evaluation
- [ ] PostgreSQL + pgvector + hybrid retrieval.
- [ ] FRED/NBS data snapshots, release/revision metadata.
- [ ] Forecast outcome evaluation with explicit metric/horizon/conditions.
- [ ] Search UI, topic timeline, incremental updates and reproducibility tests.

Release gate: only claim complete historical coverage when catalog sources and missing/inaccessible works are documented, not simply when every discovered accessible file is processed.
