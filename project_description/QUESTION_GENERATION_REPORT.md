# Cholec80 + CholecT50 Question Generation Report

This is the single Markdown report for revising the generated surgical-video questions.

Important location note:

- Current repo/folder: `/data/shared/benchmark/cholec80`
- CholecT50 sibling folder: `/data/shared/benchmark/CholecT50`
- CholecT50 exists one level up from this folder as `../CholecT50`, not inside `cholec80`.

## High-Level Inventory

| Dataset folder | Generated sets | Total generated questions | Main source |
|---|---:|---:|---|
| `cholec80/data` | A1, A2, A3, B1, B2, B3, B4, C1 | 4,979 | Cholec80 phase/tool annotations |
| `../CholecT50/data` | C2, C3, D1, D2 | 14,649 | CholecT50 triplet + phase annotations, plus Cholec80 manifests for D2 |

Cholec80 mainly tests phase/order/milestone/progression reasoning.
CholecT50 mainly tests phase-action and tool-action-target consistency.
D2 is a combined Cholec80 + CholecT50 deviation classification layer.

## Shared Surgical Phase Vocabulary

Both datasets use laparoscopic cholecystectomy phase concepts. Cholec80 calls the final phase `Gallbladder retraction`; CholecT50 uses `gallbladder-extraction`.

Common Cholec80 phase order:

1. Preparation
2. Calot triangle dissection
3. Clipping and cutting
4. Gallbladder dissection
5. Gallbladder packaging
6. Cleaning/coagulation
7. Gallbladder retraction

CholecT50 phase labels from JSON categories:

1. preparation
2. carlot-triangle-dissection / calot-triangle-dissection
3. clipping-and-cutting
4. gallbladder-dissection
5. gallbladder-packaging
6. cleaning-and-coagulation
7. gallbladder-extraction

## Critical Revision Issues

1. CholecT50 D2 is stale relative to current Cholec80 A2/A3 schemas.
   - Current Cholec80 A2 uses `question_type = out_of_order_step_correction`.
   - Current Cholec80 A3 uses `question_type = invalid_transition_detection`.
   - CholecT50 `scripts/build_d2_deviation_type_classification.py` still looks for older Cholec80 question types such as `valid_invalid_progression` and `local_progression_verification`.
   - Existing `../CholecT50/data/D2/manifest.jsonl` contains source IDs like `a3_video01_00_local_claim_false_gallbladderretraction`, which are not present in the current Cholec80 `data/A3/manifest.jsonl`.
   - If D2 is regenerated now without updating the D2 builder, the Cholec80 out-of-order and invalid-transition sources may not be rebuilt correctly.

2. B1 wording is ambiguous.
   - Question says: "What is the latest milestone that has occurred before the current clip?"
   - Code answers with the last phase label before the sampled clip start.
   - That answer can be the same phase as the current clip, because the sampled clip may begin after the phase has already started.
   - If intended answer is "previous completed phase," B1 generation logic should change.

3. A3, B2, and B4 overlap strongly.
   - All are mostly built from one skipped intermediate phase.
   - A3 asks if the transition is valid.
   - B2 asks which milestone is missing.
   - B4 asks if Clip B is premature.
   - These are useful variants, but they may not be independent reasoning categories.

4. B3 is not clinical prerequisite logic.
   - It answers "Yes" iff the queried phase is earlier in the canonical phase order.
   - It does not encode expert-defined prerequisite relationships.

5. CholecT50 C2 and D1 both test phase-action consistency.
   - C2 has yes/no and mismatch-description variants.
   - D1 has a "hierarchical consistency" framing.
   - They are related and should be revised together to avoid duplicate concepts.

6. D2 choices mix macro-order errors and micro-action errors.
   - Macro Cholec80 categories: skipped milestone, out-of-order step, invalid transition, premature progression.
   - Micro CholecT50 categories: phase-action mismatch, tool-action-target mismatch.
   - This is a good unified audit task, but only if source generation is schema-aligned.

## Cholec80: Common Construction

Files:

- Frames: `cholec80/frames/videoXX/*.png`
- Phase annotations: `cholec80/phase_annotations/videoXX-phase.txt`
- Tool annotations: `cholec80/tool_annotations/videoXX-tool.txt`
- Generated manifests: `data/{A1,A2,A3,B1,B2,B3,B4,C1}/manifest.jsonl`
- Build scripts: `scripts/build_*.py`

Most Cholec80 tasks use a shared meta-prompt:

- Give phase definitions.
- Insert visual evidence at `{images}`.
- Tell the model frames in a clip are chronological.
- Ask one multiple-choice or order question.
- Require JSON-only output.

Most clips use 8 PNG frames. PNG frame index `n` maps back to original annotation frame `(n - 1) * 25`.

### Cholec80 Summary

| Set | Task | Count | Source |
|---|---|---:|---|
| A1 | Step recognition | 544 | raw frames + phase annotations |
| A2 | Order understanding | 378 | A1 clips |
| A3 | Transition validity | 836 | A1 clips |
| B1 | Milestone awareness | 544 | A1 clips + phase annotations |
| B2 | Missing milestone diagnosis | 378 | A1 clips |
| B3 | Prerequisite satisfaction | 544 | A1 clips |
| B4 | Premature progression detection | 756 | A1 clips |
| C1 | Procedure state tracking | 999 | raw frames + phase/tool annotations |

## Cholec80 A1: Step Recognition

Builder: `scripts/build_a1_step_recognition.py`

How it is made:

- Reads Cholec80 PNG frames and phase annotation rows.
- Groups consecutive same-phase frames.
- Samples one 8-frame clip per phase per video when possible.
- Builds 4-choice phase MCQ: correct phase + 3 random distractors.

Example:

```text
ID: a1_video01_preparation_0000_00_0006
Question: What procedural step is shown in this clip?

Choices:
A. Gallbladder dissection
B. Clipping and cutting
C. Gallbladder packaging
D. Preparation

Answer: D, Preparation
```

Revision notes:

- A1 has no `question_type` field.
- Phase counts are uneven because not every video has every long-enough phase run.
- Frame paths are absolute with default `storage=paths`.

## Cholec80 A2: Order Understanding

Builder: `scripts/build_a2_order_understanding.py`

How it is made:

- Reuses A1 clips.
- Takes 3 consecutive phases in canonical order.
- Shuffles the three clips with `random_permutation`.
- Asks for the correct clip order.
- Answer is a comma-separated order string, such as `A,C,B`.

Example:

```text
ID: a2_video01_00_correction_00_random_permutation_021
Observed clip phases: Preparation, Clipping and cutting, Calot triangle dissection
Question: What is the correct procedural order for these clips?

Answer: A,C,B
Reference order: Preparation -> Calot triangle dissection -> Clipping and cutting
```

Revision notes:

- Every A2 sample is out-of-order; there are no already-correct examples.
- Answer format is `{"answer":"A,C,B"}`, unlike most other tasks that use `answer_label`.
- D2 builder currently expects an older A2 question type, so update D2 before regenerating.

## Cholec80 A3: Transition Validity

Builder: `scripts/build_a3_transition_validity.py`

How it is made:

- Reuses A1 clips.
- Builds valid adjacent transitions, such as `Preparation -> Calot triangle dissection`.
- Builds invalid transitions by skipping one intermediate phase, such as `Preparation -> Clipping and cutting`.
- Asks whether the transition is valid.

Example:

```text
ID: a3_video01_00_skip_calottriangledissection
Transition: Preparation -> Clipping and cutting
Missing phase: Calot triangle dissection
Question: Is this transition between the two clips valid?
Choices: A. Yes, B. No
Answer: B, No
```

Revision notes:

- Invalid cases are only skip-one-phase cases.
- No reversed transitions, repeated phase errors, or multi-phase skips are generated.
- D2 builder currently expects an older A3 question type, so update D2 before regenerating.

## Cholec80 B1: Milestone Awareness

Builder: `scripts/build_b1_milestone_awareness.py`

How it is made:

- Reuses each A1 clip as the current clip.
- Reads the full phase annotation for the video.
- Finds the last valid phase annotation before the current clip start frame.
- Uses that as the "latest prior milestone."
- Builds a 4-choice phase/milestone MCQ.

Example:

```text
ID: b1_progress_video01_calottriangledissection_0000_00_0322
Current clip phase: Calot triangle dissection
Question: What is the latest milestone that has occurred before the current clip?

Choices:
A. Preparation
B. Gallbladder packaging
C. Calot triangle dissection
D. Gallbladder retraction

Answer: C, Calot triangle dissection
```

Revision notes:

- The answer can equal the current phase.
- If that is not intended, change the logic to previous completed phase.

## Cholec80 B2: Missing Milestone Diagnosis

Builder: `scripts/build_b2_missing_milestone.py`

How it is made:

- Reuses A1 clips.
- Creates canonical triples `[before, missing, after]`.
- Shows only before and after clips.
- Asks which middle milestone is missing.

Example:

```text
ID: b2_video01_00_missing_identification
Shown transition: Preparation -> Clipping and cutting
Question: What key milestone is missing between these two clips?

Choices:
A. Calot triangle dissection
B. Gallbladder dissection
C. Clipping and cutting
D. Gallbladder packaging

Answer: A, Calot triangle dissection
```

Revision notes:

- Only the middle phases of 3-phase windows can be answers.
- `Preparation` and final `Gallbladder retraction` are never missing milestones.

## Cholec80 B3: Prerequisite Satisfaction

Builder: `scripts/build_b3_prerequisite_satisfaction.py`

How it is made:

- Reuses A1 current clips.
- Randomly chooses one queried prerequisite phase from all phases except final `Gallbladder retraction`.
- Answers "Yes" iff queried prerequisite phase occurs earlier than current phase in canonical order.

Example:

```text
ID: b3_prereq_video01_calottriangledissection_0000_00_0322_gallbladderpackaging_before_current_phase
Current phase: Calot triangle dissection
Queried prerequisite: Gallbladder packaging
Question: At the current point in the procedure, should Gallbladder packaging have already been completed as a prerequisite for the current phase?

Choices:
A. Yes
B. No

Answer: B, No
```

Revision notes:

- This tests phase-order relation, not expert surgical prerequisites.
- Some questions sound odd because they ask whether a later phase should be complete before an earlier phase.

## Cholec80 B4: Premature Progression Detection

Builder: `scripts/build_b4_premature_progression.py`

How it is made:

- Reuses A1 clips.
- For each canonical triple `[early, prerequisite, target]`, creates:
  - Premature example: `[early, target]`
  - Not-premature example: `[prerequisite, target]`
- Asks whether Clip B is premature.

Example:

```text
ID: b4_video01_00_premature_yes
Transition: Preparation -> Clipping and cutting
Required prerequisite: Calot triangle dissection
Question: Is Clip B a premature progression?
Choices: A. Yes, B. No
Answer: A, Yes
```

Revision notes:

- This is very close to A3 and B2 because it also uses skipped intermediate phases.

## Cholec80 C1: Procedure State Tracking

Builder: `scripts/build_c1_procedure_state_tracking.py`

How it is made:

- Reads phase annotations and tool annotations directly.
- Samples up to 2 clips per phase per video.
- Aggregates tool presence over each 8-frame clip.
- Pairs consecutive sampled clips by time.
- Classifies transition type:
  - `phase_change`
  - `tool_change`
  - `phase_and_tool_change`
  - `no_change`

Example:

```text
ID: c1_c1_video01_preparation_01_00_0009__to__c1_video01_calottriangledissection_00_00_0004_transition_type
Before phase/tools: Preparation, Grasper
After phase/tools: Calot triangle dissection, Grasper + Hook
Question: What type of tracked state transition occurs between these two clips?

Choices:
A. Only tracked tool presence changed
B. Only the procedural phase changed
C. No tracked phase/tool state changed
D. Both the procedural phase and tracked tool presence changed

Answer: D, Both the procedural phase and tracked tool presence changed
```

Revision notes:

- This tests state change, not strict procedural validity.
- Tool presence is coarse: a tool is present if it appears in any sampled frame.

## CholecT50: Common Construction

Files:

- Labels: `../CholecT50/labels/VID*.json`
- Frames: `../CholecT50/videos/VID*/NNNNNN.png`
- Triplet mapping: `../CholecT50/label_mapping.txt`
- Generated manifests: `../CholecT50/data/{C2,C3,D1,D2}/manifest.jsonl`
- Build scripts: `../CholecT50/scripts/build_*.py`

CholecT50 contains 50 label files. Local frame folders exist for 47 videos; `VID80`, `VID92`, and `VID96` are skipped because their frame directories are missing.

Raw annotation interpretation:

- Each frame has a list of annotation arrays.
- `item[0]` is the triplet ID.
- `item[14]` is the phase ID.
- `label_mapping.txt` maps triplet ID to instrument, verb, and target IDs.
- Triplets with `verb_id == 9` or `target_id == 14` are treated as null and excluded from action examples.

Common clip selection for C2, C3, and D1:

- Read label JSON and matching PNG frames.
- Keep frames with exactly one valid phase.
- Count non-null triplets per frame.
- Split frames into same-phase consecutive runs.
- Slide 8-frame windows with stride 8.
- Keep windows with at least 4 frames containing action/triplet evidence.
- Require dominant triplet count of at least 3.
- Keep one clip per group by default to reduce duplicates.

### CholecT50 Summary

| Set | Task | Count | Source |
|---|---|---:|---|
| C2 | Action-state consistency | 3,980 | raw CholecT50 phase + triplet labels |
| C3 | Tool-action-target consistency | 1,911 | raw CholecT50 triplet labels |
| D1 | Hierarchical procedure consistency | 1,990 | raw CholecT50 phase + triplet labels |
| D2 | Deviation type classification | 6,768 | Cholec80 A2/A3/B2/B4 + CholecT50 C2/C3 source manifests |

## CholecT50 C2: Action-State Consistency

Builder: `../CholecT50/scripts/build_c2_action_state_consistency.py`

Question types:

- `phase_action_consistency`: yes/no action fits shown phase/state.
- `state_action_mismatch_detection`: choose whether action fits or belongs to another state.

How it is made:

- Builds 8-frame same-phase clips with dominant non-null triplet/action.
- Positive claim uses observed dominant triplet.
- Negative claim uses a weighted mismatched triplet that is not in the clip and usually belongs to another phase.
- Creates balanced positive/negative questions for both C2 question types.

Counts:

- `phase_action_consistency`: 1,990
- `state_action_mismatch_detection`: 1,990
- Yes/No are balanced 995/995 in `phase_action_consistency`.

Example positive:

```text
ID: c2_VID01_preparation_t007_00_000000_phase_action_consistent
Current phase: Preparation
Claimed action: grasper grasps gallbladder
Question: Is this action consistent with the procedural state shown in the clip?
Choices: A. Yes, B. No
Answer: A, Yes
```

Example mismatch:

```text
ID: c2_VID01_preparation_t007_00_000000_state_action_mismatch
Current phase: Preparation
Claimed action: grasper grasps specimen bag
Mismatch source phase: Gallbladder packaging
Question: What best describes this claimed action relative to the procedural state shown in the clip?
Answer: B, The claimed action belongs to a different procedure state than the one shown.
```

Revision notes:

- Two distractor choices in `state_action_mismatch_detection` are never correct in current generated data:
  - "No relevant surgical action is visible in the clip."
  - "The clip does not show an endoscopic surgical scene."
- If those options remain, add examples where they are actually correct or remove them.

## CholecT50 C3: Tool-Action-Target Consistency

Builder: `../CholecT50/scripts/build_c3_tool_action_target_consistency.py`

Question types:

- `tool_action_target_mcq`: choose matching instrument-verb-target triplet.
- `triplet_consistency_verification`: yes/no claimed triplet matches clip.

How it is made:

- Builds 8-frame windows and chooses dominant triplet by:
  - highest frame count,
  - then highest annotation count,
  - then smaller triplet ID.
- MCQ uses the correct triplet plus distractors selected to share instrument, verb, or target when possible.
- Verification creates one consistent claim and one inconsistent claim per retained clip.

Counts:

- `tool_action_target_mcq`: 637
- `triplet_consistency_verification`: 1,274

Example MCQ:

```text
ID: c3_VID01_t007_00_000000_tat_mcq
Current phase: Preparation
Question: Which tool-action-target statement matches the clip?

Choices:
A. grasper grasps specimen bag
B. grasper grasps gallbladder
C. grasper dissects gallbladder
D. grasper retracts gallbladder

Answer: B, grasper grasps gallbladder
```

Example verification:

```text
ID: c3_VID01_t007_00_000000_triplet_inconsistent
Dominant triplet: grasper grasps gallbladder
Claimed triplet: grasper retracts gallbladder
Question: Does this tool-action-target triplet match the clip?
Choices: A. Yes, B. No
Answer: B, No
```

Revision notes:

- C3 focuses on micro-action recognition, not procedural phase order.
- Some clips contain multiple triplets; answer is based on the dominant triplet, which may be visually debatable if multiple actions are visible.

## CholecT50 D1: Hierarchical Procedure Consistency

Builder: `../CholecT50/scripts/build_d1_hierarchical_consistency.py`

Question type:

- `cross_level_consistency_verification`

How it is made:

- Builds clips like C2 using same-phase runs and dominant triplets.
- Positive claim uses the clip's observed dominant triplet/action.
- Negative claim uses a cross-phase triplet/action not observed in the clip and not typical of the current phase.
- Asks if the lower-level action is hierarchically consistent with the shown phase.

Counts:

- 1,990 total questions.
- 995 consistent and 995 inconsistent.

Example positive:

```text
ID: d1_VID01_preparation_t007_00_000000_cross_level_consistent
Current phase: Preparation
Claimed lower-level action: grasper grasps gallbladder
Question: Is this action hierarchically consistent with the procedural phase shown in the clip?
Choices: A. Consistent, B. Inconsistent
Answer: A, Consistent
```

Example negative:

```text
ID: d1_VID01_preparation_t007_00_000000_cross_level_inconsistent
Current phase: Preparation
Claimed lower-level action: hook dissects cystic duct
Mismatch source phase: Calot triangle dissection
Question: Is this action hierarchically consistent with the procedural phase shown in the clip?
Choices: A. Consistent, B. Inconsistent
Answer: B, Inconsistent
```

Revision notes:

- D1 is conceptually close to C2's phase-action consistency.
- Consider merging, renaming, or making the distinction explicit.

## CholecT50 D2: Deviation Type Classification

Builder: `../CholecT50/scripts/build_d2_deviation_type_classification.py`

Question types:

- `deviation_type_classification`
- `procedural_error_diagnosis`
- `counterfactual_audit_qa`

How it is made:

- Reads already-built source manifests.
- Converts negative/counterfactual cases into unified six-way deviation labels.
- Does not build new clips; it rewrites frame paths from source visual fields.
- Uses three question phrasings per source event.

Deviation categories:

- `skipped_milestone`
- `out_of_order_step`
- `invalid_transition`
- `premature_progression`
- `phase_action_mismatch`
- `tool_action_target_mismatch`

Counts:

- 6,768 total questions.
- 2,256 per D2 question type.
- 1,128 per deviation category.
- Source task counts:
  - Cholec80 A2: 1,128
  - Cholec80 A3: 1,128
  - Cholec80 B2: 1,128
  - Cholec80 B4: 1,128
  - CholecT50 C2: 1,128
  - CholecT50 C3: 1,128

Example from Cholec80-style source:

```text
ID: d2_cholec80_a3_video01_00_local_claim_false_gallbladderretraction_deviation_type_classification
Source: Cholec80 A3
Claimed local transition: Gallbladder retraction -> Calot triangle dissection
Question: What type of procedural deviation is present in the shown evidence?

Choices:
A. Premature progression
B. Out-of-order step
C. Invalid transition
D. Skipped milestone
E. Phase-action mismatch
F. Tool-action-target mismatch

Answer: C, Invalid transition
```

Example from CholecT50-style source:

```text
ID: d2_cholect50_c3_VID01_t012_00_001479_triplet_inconsistent_procedural_error_diagnosis
Source: CholecT50 C3
Claimed triplet: grasper retracts gallbladder
Dominant triplet: grasper grasps specimen bag
Question: Which diagnosis best explains the procedural error in the shown evidence?

Answer: D, Tool-action-target mismatch
```

Revision notes:

- D2 is valuable because it unifies high-level and low-level deviation categories.
- But the current D2 builder is not aligned with current Cholec80 A2/A3 manifest schemas.
- Before regenerating D2, update:
  - A2 event extraction to use `out_of_order_step_correction`.
  - A3 event extraction to use `invalid_transition_detection`.
  - The D2 source detail fields to match current A2/A3 row fields.

## Recommended Revision Plan

1. Decide taxonomy boundaries.
   - Keep Cholec80 A/B/C as macro-procedure questions.
   - Keep CholecT50 C2/C3/D1 as micro-action/hierarchy questions.
   - Keep D2 only if it is intended as a combined audit-diagnosis task.

2. Fix stale D2 source extraction first.
   - This is the most urgent technical issue.
   - Existing D2 manifest was built from older Cholec80 source rows.

3. Revise B1 wording or logic.
   - Use "most recently observed phase before this clip begins" if keeping current logic.
   - Use previous completed phase if you want milestone completion.

4. Reduce overlap among A3/B2/B4.
   - Add new negative types or make each task's reasoning target more distinct.

5. Make B3 either clinical or rename it.
   - If clinical: create explicit prerequisite rules.
   - If not clinical: rename to "phase order prerequisite check" or similar.

6. Reconsider C2/D1 duplication.
   - If both stay, define C2 as direct action-state consistency and D1 as hierarchy-level consistency with stricter cross-phase mismatch rules.

7. Add examples where currently unused distractor labels are correct.
   - Especially C2's "no relevant surgical action" and "non-surgical scene" options.

8. Normalize answer formats.
   - Most tasks use `answer_label`.
   - A2 uses `answer`.
   - Consistent schemas will make evaluation and D2 extraction easier.

9. Prefer relative frame paths if manifests need to move across machines.
   - Cholec80 currently stores many absolute frame paths.
   - CholecT50 stores relative `frames` plus absolute `source_frames`, which is more portable.

## Bottom Line

Cholec50 is present as `../CholecT50`. It contributes C2, C3, D1, and D2, not A1/A2/B1-style tasks. The strongest issue to fix before revising or regenerating is D2 schema drift: CholecT50 D2 was built against older Cholec80 A2/A3 question types and source IDs.
