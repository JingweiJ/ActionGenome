import os
import argparse
import warnings
from tqdm import tqdm


def dump_frames(args):
    video_dir = args.video_dir
    frame_dir = args.frame_dir
    annotation_dir = args.annotation_dir
    all_frames = args.all_frames

    # Load the list of annotated frames
    frame_list = []
    with open(os.path.join(annotation_dir, 'frame_list.txt'), 'r') as f:
        for frame in f:
            frame_list.append(frame.rstrip('\n'))

    # Create video to frames mapping
    video2frames = {}
    for path in frame_list:
        video, frame = path.split('/')
        if video not in video2frames:
            video2frames[video] = []
        video2frames[video].append(frame)

    # For each video, dump frames.
    for v in tqdm(video2frames):
        curr_frame_dir = os.path.join(frame_dir, v)
        if not os.path.exists(curr_frame_dir):
            os.makedirs(curr_frame_dir)
            # Use ffmpeg to extract frames. Different versions of ffmpeg may generate slightly different frames.
            # We used ffmpeg 2.8.15 to dump our frames.
            # Note that the frames are extracted according to their original video FPS, which is not always 24.
            # Therefore, our frame indices are different from Charades extracted frames' indices.
            os.system('ffmpeg -loglevel panic -i %s/%s %s/%%06d.png' % (video_dir, v, curr_frame_dir))

            # if not keeping all frames, only keep the annotated frames included in frame_list.txt
            if not all_frames:
                keep_frames = video2frames[v]
                frames_to_delete = set(os.listdir(curr_frame_dir)) - set(keep_frames)
                for frame in frames_to_delete:
                    os.remove(os.path.join(curr_frame_dir, frame))
        else:
            warnings.warn('Frame directory %s already exists. Skipping dumping into this directory.' % curr_frame_dir,
                          RuntimeWarning)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Dump frames")
    parser.add_argument("--video_dir", default="dataset/ag/videos",
                        help="Folder containing Charades videos.")
    parser.add_argument("--frame_dir", default="dataset/ag/frames",
                        help="Root folder containing frames to be dumped.")
    parser.add_argument("--annotation_dir", default="dataset/ag/annotations",
                        help=("Folder containing annotation files, including object_bbox_and_relationship.pkl, "
                              "person_bbox.pkl and frame_list.txt."))
    parser.add_argument("--all_frames", action="store_true",
                        help="Set if you want to dump all frames, rather than the frames listed in frame_list.txt")
    args = parser.parse_args()
    dump_frames(args)
