# CholecT50 Data Report

Generated on 2026-06-30 for the lmms-eval CholecT50 task redesign.

## Source Paths

Primary generated task data:

`/data/shared/benchmark/CholecT50/data`

Related media and annotation roots:

| Content | Path | Size |
|---|---|---:|
| Generated task manifests | `/data/shared/benchmark/CholecT50/data` | 49M |
| Extracted frame images | `/data/shared/benchmark/CholecT50/videos` | 49G |
| Frame-wise labels | `/data/shared/benchmark/CholecT50/labels` | 13M |
| Build scripts | `/data/shared/benchmark/CholecT50/scripts` | 312K |
| Build scripts v2 | `/data/shared/benchmark/CholecT50/scriptsv2` | 312K |
| Label mapping | `/data/shared/benchmark/CholecT50/label_mapping.txt` | 4.0K |

Local directory inventory:

| Item | Count |
|---|---:|
| Task manifest folders in `data` | 4 |
| Label JSON files | 50 |
| Extracted video/frame folders | 47 |
| Label mapping rows including header | 101 |

The local extracted video folders are missing `VID80`, `VID92`, and `VID96`, although label JSON files for those videos are present. The generated C2, C3, and D1 manifests only reference the 47 extracted video folders.

## Dataset Notes

The source README describes CholecT50 as 50 endoscopic videos from laparoscopic cholecystectomy surgeries at the University Hospital of Strasbourg. The dataset is annotated frame-wise with surgical action triplets in the form `<instrument, verb, target>` and also includes phase labels. The current local release notes list binary presence labels for triplets, instruments, verbs/actions, targets/anatomies, and phases.

License in the local README:

`CC BY-NC-SA 4.0`, released for non-commercial scientific research purposes.

The README also warns that CholecT50 overlaps with other CAMMA cholecystectomy datasets such as Cholec80, Cholec120, and M2CAI16. That overlap matters for train/test leakage and for D2, which intentionally mixes Cholec80 and CholecT50-derived examples.

## Dataset Scale

The generated data contains 4 task-family manifests and 14,649 JSONL records.

| Task folder | Manifest | Samples |
|---|---|---:|
| C2 | `/data/shared/benchmark/CholecT50/data/C2/manifest.jsonl` | 3,980 |
| C3 | `/data/shared/benchmark/CholecT50/data/C3/manifest.jsonl` | 1,911 |
| D1 | `/data/shared/benchmark/CholecT50/data/D1/manifest.jsonl` | 1,990 |
| D2 | `/data/shared/benchmark/CholecT50/data/D2/manifest.jsonl` | 6,768 |
| Total |  | 14,649 |

Task-level media references:

| Task folder | Unique `video_id` values | Clip container fields | Unique `frames` paths | Total `frames` refs |
|---|---:|---|---:|---:|
| C2 | 47 | `current_clip` | 7,960 | 31,840 |
| C3 | 47 | `current_clip` | 5,096 | 15,288 |
| D1 | 47 | `current_clip` | 7,960 | 15,920 |
| D2 | 127 | `clips`, `current_clip` | 9,136 | 99,264 |

C2, C3, and D1 records store both relative `frames` paths and absolute `source_frames` paths. D2 also stores both fields, but its Cholec80-derived records currently need path normalization.

## Answer Target Schemas

There is 1 machine target schema across the generated CholecT50 manifests.

| Target schema | Samples | Task folders | Expected model output |
|---|---:|---|---|
| `single_choice_label` | 14,649 | C2, C3, D1, D2 | `{"answer_label":"A"}` |

Every record has `choices`, `answer`, and `answer_label`. There are no free-text generation or clip-order-sequence answers in the generated CholecT50 manifests.

## Semantic Answer Types

There are 8 question templates. Semantically, they fall into 5 broad answer families: binary consistency verification, 4-way action-state classification, 4-way tool-action-target triplet classification, binary hierarchy verification, and 6-way deviation classification.

| Task folder | Task name | Question type | Semantic answer type | Choice count |
|---|---|---|---|---:|
| C2 | `C2_action_state_consistency` | `phase_action_consistency` | Yes/no phase-action consistency | 2 |
| C2 | `C2_action_state_consistency` | `state_action_mismatch_detection` | Consistent/mismatched action-state classification | 4 |
| C3 | `C3_tool_action_target_consistency` | `triplet_consistency_verification` | Yes/no tool-action-target consistency | 2 |
| C3 | `C3_tool_action_target_consistency` | `tool_action_target_mcq` | Tool-action-target triplet classification | 4 |
| D1 | `D1_hierarchical_procedure_consistency` | `cross_level_consistency_verification` | Consistent/inconsistent cross-level hierarchy verification | 2 |
| D2 | `D2_deviation_type_classification` | `deviation_type_classification` | Deviation type classification | 6 |
| D2 | `D2_deviation_type_classification` | `procedural_error_diagnosis` | Procedural error diagnosis | 6 |
| D2 | `D2_deviation_type_classification` | `counterfactual_audit_qa` | Counterfactual audit classification | 6 |

## Question Type Distribution

| Task folder | Question type | Samples |
|---|---|---:|
| C2 | `phase_action_consistency` | 1,990 |
| C2 | `state_action_mismatch_detection` | 1,990 |
| C3 | `triplet_consistency_verification` | 1,274 |
| C3 | `tool_action_target_mcq` | 637 |
| D1 | `cross_level_consistency_verification` | 1,990 |
| D2 | `deviation_type_classification` | 2,256 |
| D2 | `procedural_error_diagnosis` | 2,256 |
| D2 | `counterfactual_audit_qa` | 2,256 |

## Answer Distribution

### C2: Action State Consistency

Target schema: `single_choice_label`

Answer labels:

| Label | Count |
|---|---:|
| A | 1,990 |
| B | 1,990 |

Answer text:

| Answer | Count |
|---|---:|
| Yes | 995 |
| No | 995 |
| The claimed action is consistent with the procedure state shown. | 995 |
| The claimed action belongs to a different procedure state than the one shown. | 995 |

Choice counts:

| Choices per question | Samples |
|---:|---:|
| 2 | 1,990 |
| 4 | 1,990 |

### C3: Tool Action Target Consistency

Target schema: `single_choice_label`

Answer labels:

| Label | Count |
|---|---:|
| A | 799 |
| B | 796 |
| C | 149 |
| D | 167 |

Choice counts:

| Choices per question | Samples |
|---:|---:|
| 2 | 1,274 |
| 4 | 637 |

Most common answer text:

| Answer | Count |
|---|---:|
| Yes | 637 |
| No | 637 |
| grasper retracts gallbladder | 47 |
| hook dissects gallbladder | 46 |
| grasper retracts liver | 46 |
| grasper grasps specimen bag | 46 |
| grasper grasps gallbladder | 43 |
| hook dissects cystic duct | 38 |
| irrigator aspirates fluid | 29 |
| grasper retracts omentum | 21 |
| clipper clips cystic duct | 21 |
| bipolar coagulates liver | 18 |
| hook dissects cystic artery | 17 |
| scissors cuts cystic duct | 16 |
| hook dissects omentum | 14 |
| clipper clips cystic artery | 14 |
| grasper retracts gut | 12 |
| grasper grasps cystic duct | 12 |
| bipolar coagulates abdominal wall cavity | 12 |
| hook dissects cystic plate | 11 |

### D1: Hierarchical Procedure Consistency

Target schema: `single_choice_label`

Answer labels:

| Label | Count |
|---|---:|
| A | 995 |
| B | 995 |

Answer text:

| Answer | Count |
|---|---:|
| Consistent | 995 |
| Inconsistent | 995 |

Choice counts:

| Choices per question | Samples |
|---:|---:|
| 2 | 1,990 |

### D2: Deviation Type Classification

Target schema: `single_choice_label`

Answer labels:

| Label | Count |
|---|---:|
| A | 1,143 |
| B | 1,103 |
| C | 1,116 |
| D | 1,091 |
| E | 1,158 |
| F | 1,157 |

Answer text:

| Answer | Count |
|---|---:|
| Invalid transition | 752 |
| Out-of-order step | 752 |
| Phase-action mismatch | 752 |
| Premature progression | 752 |
| Skipped milestone | 752 |
| Tool-action-target mismatch | 752 |
| Invalid transition: the shown clips jump through a transition that is not locally valid. | 376 |
| Out-of-order step: the clips are arranged in an incorrect procedural order. | 376 |
| Phase-action mismatch: the claimed action does not fit the procedural phase shown in the clip. | 376 |
| Premature progression: the later clip enters a phase before the required prerequisite is shown. | 376 |
| Skipped milestone: a required intermediate phase or milestone is missing between the shown clips. | 376 |
| Tool-action-target mismatch: the claimed tool-action-target triplet does not match the visual micro-action. | 376 |

Source dataset mix:

| Source dataset | Samples |
|---|---:|
| Cholec80 | 4,512 |
| CholecT50 | 2,256 |

Source task mix:

| Source task | Samples |
|---|---:|
| `A2_order_understanding` | 1,128 |
| `A3_transition_validity` | 1,128 |
| `B2_missing_milestone_diagnosis` | 1,128 |
| `B4_premature_progression_detection` | 1,128 |
| `C2_action_state_consistency` | 1,128 |
| `C3_tool_action_target_consistency` | 1,128 |

Deviation type balance:

| Deviation type | Samples |
|---|---:|
| `invalid_transition` | 1,128 |
| `out_of_order_step` | 1,128 |
| `phase_action_mismatch` | 1,128 |
| `premature_progression` | 1,128 |
| `skipped_milestone` | 1,128 |
| `tool_action_target_mismatch` | 1,128 |

Choice counts:

| Choices per question | Samples |
|---:|---:|
| 6 | 6,768 |

## Record Structure Notes

Common top-level fields:

| Field | Meaning |
|---|---|
| `id` | Unique generated sample id |
| `task` | Task-family name |
| `question_type` | Specific question template family |
| `dataset` | Source dataset label, or `Cholec80+CholecT50` for D2 |
| `video_id` | Video identifier used by the source dataset |
| `question` | Natural language prompt |
| `choices` | Multiple-choice options with labels |
| `answer` | Gold answer text |
| `answer_label` | Gold multiple-choice label |

Task-specific fields include `claimed_action`, `claimed_triplet_id`, `correct_triplet`, `distractor_triplet_ids`, `source_dataset`, `source_task`, `deviation_type`, and `source_details`.

Clip/media fields:

| Field | Usage |
|---|---|
| `current_clip` | Single clip evidence for C2, C3, D1, and CholecT50-derived D2 records |
| `clips` | Multi-clip evidence for Cholec80-derived D2 records |
| `frames` | Paths intended for task loading |
| `source_frames` | Original absolute source frame paths |
| `source_frame_ids` / `source_png_indices` | Frame ids from source annotation or extracted PNG sequence |
| `storage` | Usually `paths` |

## Path Health

C2, C3, and D1 path references resolve in the local copy:

| Task folder | `frames` refs | Unique `frames` paths | Invalid `frames` refs |
|---|---:|---:|---:|
| C2 | 31,840 | 7,960 | 0 |
| C3 | 15,288 | 5,096 | 0 |
| D1 | 15,920 | 7,960 | 0 |

D2 has a path portability issue:

| Field | Total refs | Invalid refs | Invalid refs fixed by replacing `/home/andrew/data/shared/` with `/data/shared/` |
|---|---:|---:|---:|
| `frames` | 99,264 | 81,216 | 81,216 |
| `source_frames` | 99,264 | 81,216 | 81,216 |

The invalid references are Cholec80-derived examples with paths like:

`/home/andrew/data/shared/benchmark/cholec80/cholec80/frames/video01/video01_000007.png`

The equivalent local path exists after prefix normalization:

`/data/shared/benchmark/cholec80/cholec80/frames/video01/video01_000007.png`

## Redesign Recommendations

1. Implement CholecT50 as single-choice tasks first. The machine target schema is uniform, so the evaluator can parse and score `answer_label` for all four task folders.
2. Keep semantic answer types explicit in task metadata. C2 and C3 mix binary verification with 4-way classification; D2 uses 6-way classification across three prompt styles.
3. Normalize frame paths at load time. A robust loader should support relative paths against the manifest folder and rewrite the D2 Cholec80 prefix from `/home/andrew/data/shared/` to `/data/shared/`.
4. Treat D2 as a mixed-dataset benchmark. Its `source_dataset`, `source_task`, and `deviation_type` fields should be preserved for stratified evaluation.
5. Do not put the full media folders in GitHub. The generated manifests are 49M and the extracted frames are 49G; only small smoke fixtures should be committed.
