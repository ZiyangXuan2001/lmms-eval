# Cholec80 Data Report

Generated on 2026-06-30 for the lmms-eval Cholec80 task redesign.

## Source Paths

Primary generated task data:

`/data/shared/benchmark/cholec80/data`

Related media and annotation roots:

| Content | Path | Size |
|---|---|---:|
| Generated task manifests | `/data/shared/benchmark/cholec80/data` | 21M |
| Extracted frame images | `/data/shared/benchmark/cholec80/cholec80/frames` | 97G |
| Phase annotations | `/data/shared/benchmark/cholec80/cholec80/phase_annotations` | 122M |
| Tool annotations | `/data/shared/benchmark/cholec80/cholec80/tool_annotations` | 3.7M |

GitHub smoke fixture:

`/data/home/ziyang/shared/benchmark/lmms-eval/smoke_data/cholec80`

## Dataset Scale

The generated data contains 8 task-family manifests and 4,979 JSONL records.

| Task folder | Manifest | Samples |
|---|---|---:|
| A1 | `/data/shared/benchmark/cholec80/data/A1/manifest.jsonl` | 544 |
| A2 | `/data/shared/benchmark/cholec80/data/A2/manifest.jsonl` | 378 |
| A3 | `/data/shared/benchmark/cholec80/data/A3/manifest.jsonl` | 836 |
| B1 | `/data/shared/benchmark/cholec80/data/B1/manifest.jsonl` | 544 |
| B2 | `/data/shared/benchmark/cholec80/data/B2/manifest.jsonl` | 378 |
| B3 | `/data/shared/benchmark/cholec80/data/B3/manifest.jsonl` | 544 |
| B4 | `/data/shared/benchmark/cholec80/data/B4/manifest.jsonl` | 756 |
| C1 | `/data/shared/benchmark/cholec80/data/C1/manifest.jsonl` | 999 |
| Total |  | 4,979 |

The manifests reference 80 videos, 12,915 unique frame image paths, and 69,632 total frame references.

Example frame path:

`/data/shared/benchmark/cholec80/cholec80/frames/video01/video01_000007.png`

## Answer Target Schemas

There are 2 target schema types.

| Target schema | Samples | Task folders | Expected model output |
|---|---:|---|---|
| `single_choice_label` | 4,601 | A1, A3, B1, B2, B3, B4, C1 | `{"answer_label":"A"}` |
| `clip_order_sequence` | 378 | A2 | `{"answer":"A,C,B"}` |

`single_choice_label` records contain `answer_label` and usually `choices`.

`clip_order_sequence` records contain `answer_format: "clip_order"`, `answer`, `answer_sequence`, and `legal_clip_ids`.

## Semantic Answer Types

| Task folder | Task name | Question type | Semantic answer type | Choice count |
|---|---|---|---|---:|
| A1 | `A1_step_recognition` | `A1_step_recognition` | Procedural step classification | 4 |
| A2 | `A2_order_understanding` | `out_of_order_step_correction` | Clip order sequence | 3 clip IDs |
| A3 | `A3_transition_validity` | `invalid_transition_detection` | Yes/no transition validity | 2 |
| B1 | `B1_milestone_awareness` | `progress_milestone_check` | Latest milestone/procedural step classification | 4 |
| B2 | `B2_missing_milestone_diagnosis` | `missing_milestone_identification` | Missing milestone classification | 4 |
| B3 | `B3_prerequisite_satisfaction` | `prerequisite_satisfaction_verification` | Yes/no prerequisite satisfaction | 2 |
| B4 | `B4_premature_progression_detection` | `premature_progression_detection` | Yes/no premature progression | 2 |
| C1 | `C1_procedure_state_tracking` | `transition_type_classification` | Phase/tool transition type classification | 4 |

## Answer Distribution

### A1: Step Recognition

Target schema: `single_choice_label`

Answer labels:

| Label | Count |
|---|---:|
| A | 128 |
| B | 148 |
| C | 130 |
| D | 138 |

Answer text:

| Answer | Count |
|---|---:|
| Calot triangle dissection | 80 |
| Clipping and cutting | 80 |
| Gallbladder dissection | 80 |
| Gallbladder packaging | 80 |
| Gallbladder retraction | 79 |
| Cleaning/coagulation | 74 |
| Preparation | 71 |

### A2: Order Understanding

Target schema: `clip_order_sequence`

Answer strings:

| Answer | Count |
|---|---:|
| B,A,C | 85 |
| C,B,A | 79 |
| B,C,A | 74 |
| C,A,B | 71 |
| A,C,B | 69 |

### A3: Transition Validity

Target schema: `single_choice_label`

| Answer | Count |
|---|---:|
| Yes | 458 |
| No | 378 |

Answer labels:

| Label | Count |
|---|---:|
| A | 458 |
| B | 378 |

### B1: Milestone Awareness

Target schema: `single_choice_label`

Answer labels:

| Label | Count |
|---|---:|
| A | 141 |
| B | 130 |
| C | 129 |
| D | 144 |

Answer text:

| Answer | Count |
|---|---:|
| Calot triangle dissection | 80 |
| Clipping and cutting | 80 |
| Gallbladder dissection | 80 |
| Gallbladder packaging | 80 |
| Gallbladder retraction | 79 |
| Cleaning/coagulation | 74 |
| Preparation | 71 |

### B2: Missing Milestone Diagnosis

Target schema: `single_choice_label`

Answer labels:

| Label | Count |
|---|---:|
| A | 91 |
| B | 93 |
| C | 94 |
| D | 100 |

Answer text:

| Answer | Count |
|---|---:|
| Clipping and cutting | 80 |
| Gallbladder dissection | 80 |
| Gallbladder packaging | 74 |
| Cleaning/coagulation | 73 |
| Calot triangle dissection | 71 |

### B3: Prerequisite Satisfaction

Target schema: `single_choice_label`

| Answer | Count |
|---|---:|
| No | 277 |
| Yes | 267 |

Answer labels:

| Label | Count |
|---|---:|
| A | 267 |
| B | 277 |

### B4: Premature Progression Detection

Target schema: `single_choice_label`

| Answer | Count |
|---|---:|
| Yes | 378 |
| No | 378 |

Answer labels:

| Label | Count |
|---|---:|
| A | 378 |
| B | 378 |

### C1: Procedure State Tracking

Target schema: `single_choice_label`

Answer labels:

| Label | Count |
|---|---:|
| A | 244 |
| B | 265 |
| C | 234 |
| D | 256 |

Answer text:

| Answer | Count |
|---|---:|
| Both the procedural phase and tracked tool presence changed | 397 |
| Only tracked tool presence changed | 383 |
| No tracked phase/tool state changed | 152 |
| Only the procedural phase changed | 67 |

## Common Record Fields

All records include task identity and question text. Most records include visual evidence as nested `frames` lists.

Important target fields:

| Field | Meaning |
|---|---|
| `answer` | Human-readable answer text, or clip-order string for A2 |
| `answer_label` | Multiple-choice target label for A1, A3, B1, B2, B3, B4, C1 |
| `answer_sequence` | Ordered clip IDs for A2 |
| `answer_format` | Present in A2 as `clip_order` |
| `choices` | Multiple-choice options for label-based tasks |
| `legal_clip_ids` | Legal output clip IDs for A2 |

Important visual fields:

| Field | Meaning |
|---|---|
| `frames` | Ordered frame paths for a single clip |
| `clips` | Multi-clip inputs, each usually containing its own `frames` |
| `source_png_indices` | PNG frame indices under the extracted frame root |
| `source_original_frames` | Original video frame indices |
| `video_id` | Cholec80 video identifier, such as `video01` |

## Redesign Notes

1. The task suite should support two scoring adapters: label accuracy for `answer_label`, and exact ordered-sequence matching for A2 `answer`.
2. A unified lmms-eval task wrapper can load each manifest with `dataset_path: json` and `dataset_kwargs.data_files.test`.
3. Chat models should use `doc_to_messages`, placing chronological frame images before the text prompt. Existing manifest prompts already contain `{images}` placeholders, so the redesign should either remove that placeholder or replace it with a concise visual marker.
4. Because the full frame root is 97G, GitHub should only carry smoke fixtures. Full evaluation should point to `/data/shared/benchmark/cholec80/data` and `/data/shared/benchmark/cholec80/cholec80/frames`.
5. For reporting, task-level metrics should remain separate by semantic type. A single aggregate can hide major differences between step classification, temporal ordering, prerequisite reasoning, and phase/tool state tracking.
