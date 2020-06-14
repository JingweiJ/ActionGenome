# Action Genome
This repo contains README and snippets for using the Action Genome dataset v1.0.

## Prerequisite
To use the snippets in this repo, `python 3` and `ffmpeg` are required.

## Get started

### Download videos and annotations
Download Charades videos (scaled to 480p) from [here](https://prior.allenai.org/projects/charades) and extract (or softlink) them under `dataset/ag/videos`.

Download [Action Genome annotations](https://drive.google.com/drive/folders/1LGGPK_QgGbh9gH9SDFv_9LIhBliZbZys?usp=sharing) and place them under `dataset/ag/annotations`.

### Dump frames
We are not releasing the dumped frames from Charades videos. Instead, you can download the Charades videos from [here](https://prior.allenai.org/projects/charades) and dump the frames following the instruction below.

After preparing all 480p videos into your `dataset/ag/videos`, dump the frames into `dataset/ag/frames`:
```bash
python tools/dump_frames.py
```
The dumped frames are ~74GB. The dumping may take half a day to finish. Note that we have only annotated sampled frames (see the sampling strategy in our [paper](http://openaccess.thecvf.com/content_CVPR_2020/papers/Ji_Action_Genome_Actions_As_Compositions_of_Spatio-Temporal_Scene_Graphs_CVPR_2020_paper.pdf)) rather than all frames. If you prefer to dump all frames, run:
```bash
python tools/dump_frames.py --all_frames
```

### Annotations structure
The `object_bbox_and_relationship.pkl` contains a dictionary structured like:
```
{...
    'VIDEO_ID/FRAME_ID':
        [...
            {
                'class': 'book',
                'bbox': (x, y, w, h),
                'attention_relationship': ['looking_at'],
                'spatial_relationship': ['in_front_of'],
                'contacting_relationship': ['holding', 'touching'],
                'visible': True,
                'metadata': 
                    {
                        'tag': 'VIDEO_ID/FRAME_ID',
                        'set': 'train'
                    }
            }
        ...]
...}
```
Noticeably, 'visible' indicates if the interacted object is visible in the frame.

The `person_bbox.pkl` contains the person bounding boxes of each frame. Here we release the Faster-RCNN detected
person boxes as we've used in our paper. In our next version of the dataset, we'll release person boxes labeled 
manually.

The `frame_list.txt` contains all frames we've labeled.

The `object_classes.txt` contains all classes of objects.

The `relationship_classes.txt` contains all classes of human-object relationships. 
