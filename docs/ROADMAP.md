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

## Phase 2: browser-harness Douyin player adapter
- [ ] Inspect <video> elements and accessible UI elements only; handle SPA navigation.
- [ ] Start recorder BEFORE playback; confirm transition to playing.
- [ ] Poll paused/currentTime/ended; distinguish end, buffering, live video and timeouts.
- [ ] Stop recorder AFTER verified end, never upon unrelated navigation.
- [ ] Operator override and consent, rate limits, login/denial handling.
- [ ] Batch queue with no concurrent tabs on shared local Chrome daemon.

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
