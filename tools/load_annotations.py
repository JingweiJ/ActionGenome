import os
import pickle


def load_annotations(annotation_dir):
    with open(os.path.join(annotation_dir, 'object_bbox_and_relationship.pkl'), 'rb') as f:
        object_anno = pickle.load(f)

    with open(os.path.join(annotation_dir, 'person_bbox.pkl'), 'rb') as f:
        person_anno = pickle.load(f)

    frame_list = []
    with open(os.path.join(annotation_dir, 'frame_list.txt'), 'r') as f:
        for frame in f:
            frame_list.append(frame.rstrip('\n'))

    return object_anno, person_anno, frame_list


if __name__ == "__main__":
    annotation_dir = 'dataset/ag/annotations'
    object_anno, person_anno, frame_list = load_annotations(annotation_dir)
    assert set(object_anno.keys()) == set(person_anno.keys())
    assert len(object_anno) == len(frame_list)
