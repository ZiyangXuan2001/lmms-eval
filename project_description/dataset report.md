# Dataset Report

Generated on 2026-07-02 for the lmms-eval surgical video benchmark workspace.

This report summarizes the local datasets found under `<benchmark-root>`. It is based only on local files in the shared folder; no online lookup was used.

## Local Inventory

| Dataset | Local path pattern | Local state |
|---|---|---|
| GraSP | `<benchmark-root>/GraSP` | Code and README repository only; the full GraSP frame/annotation archives are not present locally. |
| CholecT50 | `<benchmark-root>/CholecT50` | Extracted frame folders, label JSON files, task manifests, and scripts. |
| Cholec80 | `<benchmark-root>/cholec80` | Extracted frames, phase annotations, tool annotations, generated task manifests, and scripts. |
| Cataract-1K | `<benchmark-root>/data/Cataract-1K` | Multiple cataract surgery subsets for phase recognition, segmentation, pupil reaction, and lens irregularity. |
| GynSurg | `<benchmark-root>/data/GynSurg` | Gynecologic surgery segmentation images and action/classification video clips. |
| Endoscapes2023 | `<benchmark-root>/data/Endoscapes2023/endoscapes.zip` | Single zip archive containing images, COCO annotations, segmentation masks, metadata, and split files. |

## Quick Comparison

| Dataset | Surgical domain | Main tasks | Typical input | Typical labels |
|---|---|---|---|---|
| GraSP | Robot-assisted radical prostatectomy | Phase recognition, step recognition, instrument segmentation, atomic action recognition | Endoscopic frames/video clips | Phase, step, instrument masks, action labels |
| CholecT50 | Laparoscopic cholecystectomy | Surgical action triplet recognition and phase/action consistency | Extracted frames at 1 fps | `<instrument, verb, target>` triplets and phase labels |
| Cholec80 | Laparoscopic cholecystectomy | Phase recognition and tool presence recognition | Extracted frames at 1 fps | 7 surgical phases and 7 binary tool-presence labels |
| Cataract-1K | Cataract surgery | Phase recognition, scene/instrument segmentation, pupil/lens related tasks | Cataract surgery videos and annotated frames | Surgical phase intervals, COCO/Supervisely masks, video-level subset membership |
| GynSurg | Gynecologic laparoscopy | Instrument/anatomy segmentation and short action classification | Images and short video clips | Instrument/anatomy masks, action folders, bleeding/smoke labels |
| Endoscapes2023 | Laparoscopic cholecystectomy CVS region | CVS assessment, object detection, semantic/instance segmentation | Laparoscopic frames | CVS criteria, boxes, segmentation masks for anatomy/tool classes |

## GraSP

### What It Is For

GraSP is described in the local README as the Holistic and Multi-Granular Surgical Scene Understanding of Prostatectomies dataset. It targets multi-level understanding of radical prostatectomy videos:

- Long-term tasks: surgical phase recognition and surgical step recognition.
- Short-term tasks: surgical instrument segmentation and atomic visual action detection.
- Associated model code: TAPIS, short for Transformers for Actions, Phases, Steps, and Instrument Segmentation.

### Local Contents

The local folder contains the repository and code, not the full dataset:

| Item | Local count |
|---|---:|
| Files outside `.git` | 187 |
| Python files | 126 |
| YAML config files | 29 |
| Shell scripts | 9 |
| Local image assets | 2 |

Important local files:

- `<benchmark-root>/GraSP/README.md`
- `<benchmark-root>/GraSP/TAPIS/README.md`
- `<benchmark-root>/GraSP/TAPIS/tapis/datasets/grasp.py`
- `<benchmark-root>/GraSP/TAPIS/run_files/grasp_actions.sh`
- `<benchmark-root>/GraSP/TAPIS/run_files/grasp_phases.sh`
- `<benchmark-root>/GraSP/TAPIS/run_files/grasp_steps.sh`
- `<benchmark-root>/GraSP/TAPIS/run_files/grasp_instruments.sh`

### Expected Dataset Structure

The README says the full dataset should include structures such as:

```text
GraSP_30fps/
  frames/
    CASE001/
      000000000.jpg
      000000001.jpg
  annotations/
    segmentations/
    grasp_long-term_train.json
    grasp_long-term_test.json
    grasp_short-term_train.json
    grasp_short-term_test.json
```

Those full frame and annotation folders were not found in the local shared folder.

### Example

An expected full-data example from the README would be:

```text
GraSP_30fps/frames/CASE001/000000000.jpg
GraSP_30fps/annotations/grasp_long-term_train.json
GraSP_30fps/annotations/segmentations/CASE001/000000068.png
```

Local caveat: these examples describe the expected GraSP data layout, but this workspace currently only has the repository/code version.

## CholecT50

### What It Is For

CholecT50 is an endoscopic laparoscopic cholecystectomy dataset. It is centered on surgical action triplets:

```text
<instrument, verb, target>
```

The local README describes support for:

- Surgical action triplet recognition.
- Surgical action triplet detection/localization.
- Surgical tool presence detection.
- Surgical action or verb recognition.
- Surgical target recognition.
- Surgical phase recognition.

### Local Contents

| Item | Local count |
|---|---:|
| Extracted frame folders under `videos` | 47 |
| Extracted frame images | 92,978 |
| Label JSON files under `labels` | 50 |
| Generated benchmark task folders | 4 |
| Generated benchmark samples | 14,649 |

Important local paths:

- `<benchmark-root>/CholecT50/README.md`
- `<benchmark-root>/CholecT50/label_mapping.txt`
- `<benchmark-root>/CholecT50/videos`
- `<benchmark-root>/CholecT50/labels`
- `<benchmark-root>/CholecT50/data/C2/manifest.jsonl`
- `<benchmark-root>/CholecT50/data/C3/manifest.jsonl`
- `<benchmark-root>/CholecT50/data/D1/manifest.jsonl`
- `<benchmark-root>/CholecT50/data/D2/manifest.jsonl`

### Labels

Example label metadata from `labels/VID01.json`:

| Field | Value |
|---|---|
| `fps` | 1 |
| `num_frames` | 1734 |
| `video` | 1 |

Core label categories include:

| Category | Example values |
|---|---|
| Instrument | `grasper`, `bipolar`, `hook`, `scissors`, `clipper`, `irrigator` |
| Verb | `grasp`, `retract`, `dissect`, `coagulate`, `clip`, `cut`, `aspirate`, `irrigate`, `pack`, `null_verb` |
| Target | `gallbladder`, `cystic_plate`, `cystic_duct`, `cystic_artery`, `cystic_pedicle`, `blood_vessel`, `fluid`, `abdominal_wall_cavity`, `liver`, `adhesion`, `omentum`, `peritoneum`, `gut`, `specimen_bag`, `null_target` |

Example triplets:

```text
triplet 7: grasper, grasp, gallbladder
triplet 23: bipolar, coagulate, blood_vessel
triplet 58: hook, dissect, cystic_duct
triplet 82: irrigator, aspirate, fluid
```

### Generated lmms-eval Tasks

| Task folder | Task name | Samples | Purpose |
|---|---|---:|---|
| C2 | `C2_action_state_consistency` | 3,980 | Check whether a claimed action is consistent with the procedural phase/state. |
| C3 | `C3_tool_action_target_consistency` | 1,911 | Check or classify tool-action-target triplets. |
| D1 | `D1_hierarchical_procedure_consistency` | 1,990 | Check lower-level action consistency with higher-level phase. |
| D2 | `D2_deviation_type_classification` | 6,768 | Mixed Cholec80 and CholecT50 deviation/error classification tasks. |

### Example

Frame example:

```text
<benchmark-root>/CholecT50/videos/VID01/000000.png
```

Label example from `VID01`:

```json
{
  "frame": 0,
  "triplet_id": 7,
  "instrument": "grasper",
  "verb": "grasp",
  "target": "gallbladder"
}
```

Generated benchmark example:

```text
Claimed action: grasper grasps gallbladder.
Is this action consistent with the procedural state shown in the clip?

Choices:
A. Yes
B. No

Answer: A
```

### Local Caveats

The local labels include 50 videos, but only 47 videos are extracted under `videos`. The missing extracted frame folders are:

```text
VID80
VID92
VID96
```

The local generated C2, C3, and D1 manifests reference the 47 extracted video folders.

## Cholec80

### What It Is For

Cholec80 is an endoscopic laparoscopic cholecystectomy dataset for:

- Surgical phase recognition.
- Surgical tool presence recognition.
- Temporal procedure-understanding tasks derived from phase/tool progress.

### Local Contents

| Item | Local count |
|---|---:|
| Video frame folders | 80 |
| Extracted frame images | 184,498 |
| Phase annotation text files | 80 |
| Tool annotation text files | 80 |
| Generated benchmark task folders | 8 |
| Generated benchmark samples | 4,979 |

Important local paths:

- `<benchmark-root>/cholec80/cholec80/frames`
- `<benchmark-root>/cholec80/cholec80/phase_annotations`
- `<benchmark-root>/cholec80/cholec80/tool_annotations`
- `<benchmark-root>/cholec80/TF-Cholec80/readme.md`
- `<benchmark-root>/cholec80/data/A1/manifest.jsonl`
- `<benchmark-root>/cholec80/data/A2/manifest.jsonl`
- `<benchmark-root>/cholec80/data/A3/manifest.jsonl`
- `<benchmark-root>/cholec80/data/B1/manifest.jsonl`
- `<benchmark-root>/cholec80/data/B2/manifest.jsonl`
- `<benchmark-root>/cholec80/data/B3/manifest.jsonl`
- `<benchmark-root>/cholec80/data/B4/manifest.jsonl`
- `<benchmark-root>/cholec80/data/C1/manifest.jsonl`

### Labels

The local TF-Cholec80 README lists 7 surgical phases:

```text
Preparation
CalotTriangleDissection
ClippingCutting
GallbladderDissection
GallbladderRetraction
CleaningCoagulation
GallbladderPackaging
```

It also lists 7 surgical instruments in this binary-label order:

```text
Grasper
Bipolar
Hook
Scissors
Clipper
Irrigator
SpecimenBag
```

### Generated lmms-eval Tasks

| Task folder | Task name | Samples | Purpose |
|---|---|---:|---|
| A1 | `A1_step_recognition` | 544 | Identify the procedural step shown in a clip. |
| A2 | `A2_order_understanding` | 378 | Reorder clips into correct procedural order. |
| A3 | `A3_transition_validity` | 836 | Judge whether a phase transition is valid. |
| B1 | `B1_milestone_awareness` | 544 | Identify latest procedural milestone. |
| B2 | `B2_missing_milestone_diagnosis` | 378 | Identify missing procedural milestone. |
| B3 | `B3_prerequisite_satisfaction` | 544 | Judge whether prerequisites are satisfied. |
| B4 | `B4_premature_progression_detection` | 756 | Detect premature procedural progression. |
| C1 | `C1_procedure_state_tracking` | 999 | Classify transition/procedure-state changes. |

### Example

Frame example:

```text
<benchmark-root>/cholec80/cholec80/frames/video01/video01_000007.png
```

Phase annotation example from `video01-phase.txt`:

```text
Frame  Phase
0      Preparation
1      Preparation
2      Preparation
```

Tool annotation example from `video01-tool.txt`:

```text
Frame  Grasper  Bipolar  Hook  Scissors  Clipper  Irrigator  SpecimenBag
0      1        0        0     0         0        0          0
475    1        0        1     0         0        0          0
```

Generated benchmark example:

```text
What procedural step is shown in this clip?

Choices:
A. Gallbladder dissection
B. Clipping and cutting
C. Gallbladder packaging
D. Preparation

Answer: D
```

## Cataract-1K

### What It Is For

Cataract-1K is a cataract surgery dataset with several local subsets:

- Phase recognition.
- Segmentation.
- Pupil reaction.
- Lens irregularity.

### Local Contents

| Subset | MP4 files | CSV files | JSON files | PNG files | Purpose |
|---|---:|---:|---:|---:|---|
| `Phase_recognition_dataset` | 56 | 171 | 0 | 0 | Phase interval annotations over surgery videos. |
| `Segmentation_dataset` | 30 | 155 | 2,287 | 2,256 | COCO and Supervisely style segmentation annotations. |
| `Pupil_reaction` | 38 | 1 | 0 | 0 | Pupil reaction videos. |
| `Lens_irregularity` | 10 | 1 | 0 | 0 | Lens irregularity videos. |

Important local paths:

- `<benchmark-root>/data/Cataract-1K/Phase_recognition_dataset`
- `<benchmark-root>/data/Cataract-1K/Segmentation_dataset`
- `<benchmark-root>/data/Cataract-1K/Pupil_reaction`
- `<benchmark-root>/data/Cataract-1K/Lens_irregularity`

### Labels

Phase annotation example from:

```text
<benchmark-root>/data/Cataract-1K/Phase_recognition_dataset/annotations/case_5013/case_5013_annotations_phases.csv
```

Example rows:

| caseId | phase/comment | frame | endFrame | sec | endSec |
|---|---|---:|---:|---:|---:|
| 5013 | `Incision` | 240 | 408 | 4.004 | 6.807 |
| 5013 | `Viscoelastic` | 1043 | 1519 | 17.401 | 25.342 |
| 5013 | `Capsulorhexis` | 1647 | 4358 | 27.477 | 72.706 |

Segmentation COCO example from:

```text
<benchmark-root>/data/Cataract-1K/Segmentation_dataset/Annotations/Coco-Annotations/case_5013/annotations/instances.json
```

For `case_5013`, the COCO file has:

| Item | Count |
|---|---:|
| Images | 69 |
| Annotations | 242 |
| Categories | 15 |

Example segmentation categories:

```text
Lens
Phacoemulsification Tip
Pupil
Cornea
Slit Knife
Gauge
Lens Injector
Incision Knife
Katena Forceps
Capsulorhexis Forceps
```

### Example

Video example:

```text
<benchmark-root>/data/Cataract-1K/Phase_recognition_dataset/videos/case_5013.mp4
```

Segmentation frame/annotation example:

```text
<benchmark-root>/data/Cataract-1K/Segmentation_dataset/Annotations/Images-and-Supervisely-Annotations/case_5051/img/case5051_01.png
<benchmark-root>/data/Cataract-1K/Segmentation_dataset/Annotations/Images-and-Supervisely-Annotations/case_5051/ann/case5051_01.png.json
```

## GynSurg

### What It Is For

GynSurg is a gynecologic laparoscopic surgery dataset collection. The local copy supports:

- Instrument segmentation.
- Anatomy segmentation.
- Instrument/anatomy joint annotations.
- Action recognition from short clips.
- Bleeding and smoke related classification tasks.

### Local Contents

| Subset | Files | MP4 files | PNG files | JSON files |
|---|---:|---:|---:|---:|
| `GynSurg_Action_3sec` | 7,518 | 7,518 | 0 | 0 |
| `GynSurg_Action_Segments` | 1,901 | 1,901 | 0 | 0 |
| `GynSurg_Anatomy_Dataset` | 1,450 | 0 | 1,450 | 0 |
| `GynSurg_Auxiliary_Tool_Dataset` | 3,158 | 0 | 3,158 | 0 |
| `GynSurg_Instrument_Dataset` | 9,984 | 0 | 9,984 | 0 |
| `Instrument_Anatomy_Original_Dataset` | 23,372 | 0 | 23,244 | 48 |

Important local paths:

- `<benchmark-root>/data/GynSurg/GynSurg_Action_3sec`
- `<benchmark-root>/data/GynSurg/GynSurg_Action_Segments`
- `<benchmark-root>/data/GynSurg/GynSurg_Instrument_Dataset`
- `<benchmark-root>/data/GynSurg/GynSurg_Anatomy_Dataset`
- `<benchmark-root>/data/GynSurg/Instrument_Anatomy_Original_Dataset/instruments.json`
- `<benchmark-root>/data/GynSurg/Instrument_Anatomy_Original_Dataset/anatomy.json`

### Action Clip Classes

`GynSurg_Action_Segments` contains:

| Class folder | MP4 clips |
|---|---:|
| `Bleeding` | 114 |
| `Coagulation` | 321 |
| `Irrigation` | 59 |
| `NeedlePassing` | 510 |
| `Non-bleeding` | 304 |
| `Non-smoke` | 593 |

`GynSurg_Action_3sec` contains:

| Class folder | MP4 clips |
|---|---:|
| `GynSurg_action_dataset/Coagulation` | 1,068 |
| `GynSurg_action_dataset/NeedlePassing` | 1,206 |
| `GynSurg_action_dataset/Rest` | 1,100 |
| `GynSurg_action_dataset/SuctionIrrigation` | 212 |
| `GynSurg_action_dataset/Transection` | 354 |
| `GynSurg_bleeding_dataset/Bleeding` | 977 |
| `GynSurg_bleeding_dataset/Non_bleeding` | 1,064 |
| `GynSurg_smoke_dataset/Non_smoke` | 1,537 |

### Segmentation Categories

The local instrument COCO-style JSON has:

| Item | Count |
|---|---:|
| Images | 5,774 |
| Annotations | 14,913 |
| Categories | 23 |

Example instrument categories:

```text
instrument
grasper
irrigator
morcellator
bipolar-forceps
needle
sealer-divider
trocar
thread
scissors
hook
needle-holder
knot-pusher
clip-applier
```

The local anatomy COCO-style JSON has:

| Item | Count |
|---|---:|
| Images | 818 |
| Annotations | 1,165 |
| Categories | 8 |

Anatomy categories:

```text
organ
uterus
liver
tube
ovary
ligamentum-rotundum
colon
small-intestine
```

### Example

Action clip example:

```text
<benchmark-root>/data/GynSurg/GynSurg_Action_Segments/Irrigation/case_458_Irigation_0%3A03%3A09.366667-0%3A03%3A12.86666730fps.mp4
```

Instrument image example from local COCO metadata:

```text
Instrument_Anatomy_Original_Dataset/insseg/INSSEG_01/3.mp4_/3_014423_08-00-23.png
```

## Endoscapes2023

### What It Is For

Endoscapes2023 is a laparoscopic cholecystectomy dataset focused on the critical view of safety region. The local zip README describes three related sub-datasets:

- `Endoscapes-CVS201`: CVS assessment from 201 videos.
- `Endoscapes-BBox201`: bounding boxes for anatomy/tool classes.
- `Endoscapes-Seg50`: semantic and instance segmentation masks for a 50-video subset.

### Local Contents

The local data is stored as one zip file:

```text
<benchmark-root>/data/Endoscapes2023/endoscapes.zip
```

Zip inventory:

| Item | Count |
|---|---:|
| Zip entries | 160,001 |
| JPG files | 158,457 |
| PNG files | 495 |
| CSV files | 494 |
| NPY files | 493 |
| JSON files | 30 |
| TXT files | 13 |
| README files | 1 |

Top-level directories/files inside the zip include:

```text
endoscapes/train
endoscapes/val
endoscapes/test
endoscapes/val_seg
endoscapes/test_seg
endoscapes/insseg
endoscapes/semseg
endoscapes/12_5
endoscapes/25
endoscapes/all_metadata.csv
endoscapes/seg_label_map.txt
```

### Labels

The segmentation label map in the zip is:

```text
background
cystic_plate
calot_triangle
cystic_artery
cystic_duct
gallbladder
tool
```

COCO object-detection categories use IDs 1-6:

```text
cystic_plate
calot_triangle
cystic_artery
cystic_duct
gallbladder
tool
```

Example annotation counts from the zip:

| Split annotation | Images | Annotations | Categories |
|---|---:|---:|---:|
| `endoscapes/train/annotation_coco.json` | 1,212 | 5,566 | 6 |
| `endoscapes/val/annotation_coco.json` | 409 | 1,733 | 6 |
| `endoscapes/test/annotation_coco.json` | 312 | 1,485 | 6 |
| `endoscapes/val_seg/annotation_coco.json` | 76 | 363 | 6 |
| `endoscapes/test_seg/annotation_coco.json` | 74 | 270 | 6 |

`all_metadata.csv` contains CVS-related columns:

```text
vid
frame
avg_cvs
C1
C2
C3
is_ds_keyframe
cvs_annotator_1
cvs_annotator_2
cvs_annotator_3
mask_path
label_path
```

### Example

Image example inside the zip:

```text
endoscapes/train/8_14775.jpg
```

COCO image record example:

```json
{
  "file_name": "8_14775.jpg",
  "height": 480,
  "width": 854,
  "id": 8014775,
  "is_det_keyframe": true,
  "ds": [0.3333333333333333, 0.3333333333333333, 0.0],
  "video_id": 8,
  "is_ds_keyframe": true
}
```

COCO annotation example:

```json
{
  "category_id": 2,
  "bbox": [453.0, 208.0, 124.0, 55.0],
  "area": 3399,
  "image_id": 8014775
}
```

### Local Caveat

The README describes a `train_seg` split, but in this local zip the `endoscapes/train_seg` entry appears as a directory marker only. Segmentation assets are present under `insseg`, `semseg`, `val_seg`, and `test_seg`, while training segmentation images appear to be represented through other split folders and annotation files.

## Cross-Dataset Notes

### Best Fit by Task

| Research need | Best local dataset candidates |
|---|---|
| Surgical phase recognition | Cholec80, CholecT50, Cataract-1K, GraSP if full data is downloaded |
| Tool presence recognition | Cholec80 |
| Action triplet recognition | CholecT50 |
| Procedure-order or milestone reasoning | Generated Cholec80 manifests in `<benchmark-root>/cholec80/data` |
| Cross-level action/phase consistency | Generated CholecT50 manifests in `<benchmark-root>/CholecT50/data` |
| Cataract phase/segmentation work | Cataract-1K |
| Gynecologic instrument/anatomy segmentation | GynSurg |
| CVS assessment and cholecystectomy anatomy/tool detection | Endoscapes2023 |
| Holistic prostatectomy scene understanding | GraSP, after downloading the actual data archives |

### Known Local Gaps

| Dataset | Gap |
|---|---|
| GraSP | Full frames and annotation archives are not present locally. |
| CholecT50 | `VID80`, `VID92`, and `VID96` labels exist, but extracted frame folders are missing. |
| Endoscapes2023 | Dataset is zipped; some workflows may need extraction or zip-aware loaders. |
| Cataract-1K | Several `.DS_Store` files and Synapse manifests are present; loaders should filter non-data files. |
| GynSurg | Contains many zip archives plus extracted folders; avoid double-counting if both are used. |

## Practical Examples for lmms-eval

### Cholec80 Step Recognition

Use:

```text
<benchmark-root>/cholec80/data/A1/manifest.jsonl
```

Example task shape:

```json
{
  "task": "A1_step_recognition",
  "dataset": "Cholec80",
  "question": "What procedural step is shown in this clip?",
  "choices": [
    {"label": "A", "text": "Gallbladder dissection"},
    {"label": "B", "text": "Clipping and cutting"},
    {"label": "C", "text": "Gallbladder packaging"},
    {"label": "D", "text": "Preparation"}
  ],
  "answer_label": "D"
}
```

### CholecT50 Action-State Consistency

Use:

```text
<benchmark-root>/CholecT50/data/C2/manifest.jsonl
```

Example task shape:

```json
{
  "task": "C2_action_state_consistency",
  "dataset": "CholecT50",
  "question": "Claimed action: grasper grasps gallbladder.\nIs this action consistent with the procedural state shown in the clip?",
  "choices": [
    {"label": "A", "text": "Yes"},
    {"label": "B", "text": "No"}
  ],
  "answer_label": "A"
}
```

### Cataract-1K Phase Recognition

Use:

```text
<benchmark-root>/data/Cataract-1K/Phase_recognition_dataset/videos/case_5013.mp4
<benchmark-root>/data/Cataract-1K/Phase_recognition_dataset/annotations/case_5013/case_5013_annotations_phases.csv
```

Example annotation:

```text
caseId=5013, phase=Capsulorhexis, frame=1647, endFrame=4358, sec=27.477, endSec=72.706
```

### GynSurg Action Classification

Use class-folder supervision such as:

```text
<benchmark-root>/data/GynSurg/GynSurg_Action_3sec/GynSurg_action_dataset/NeedlePassing/*.mp4
<benchmark-root>/data/GynSurg/GynSurg_Action_3sec/GynSurg_action_dataset/Coagulation/*.mp4
```

The folder name is the class label.

### Endoscapes2023 Detection/Segmentation

Use zip-aware loading or extract:

```text
<benchmark-root>/data/Endoscapes2023/endoscapes.zip
```

Inside the zip:

```text
endoscapes/train/annotation_coco.json
endoscapes/val/annotation_coco.json
endoscapes/test/annotation_coco.json
endoscapes/val_seg/annotation_coco.json
endoscapes/test_seg/annotation_coco.json
```

## Recommendation

For immediate lmms-eval style multimodal QA, the most ready-to-use local sources are:

1. Cholec80 generated manifests under `<benchmark-root>/cholec80/data`.
2. CholecT50 generated manifests under `<benchmark-root>/CholecT50/data`.

For future task expansion:

1. Add Cataract-1K phase and segmentation tasks for ophthalmic surgery coverage.
2. Add GynSurg action and segmentation tasks for gynecologic surgery coverage.
3. Add Endoscapes2023 CVS/detection tasks, preferably with a zip-aware loader or a controlled extraction step.
4. Download the full GraSP data archives before treating GraSP as available training/evaluation data.
