"""Parse CVAT for images 1.1"""

import random
import xml.etree.ElementTree as ET
import itertools


DEFAULT_ANNOTATIONS_FILE='july_annotations_v2.xml'
BOX_AREA_THRESHOLD = 50*50

def parse(file_name=DEFAULT_ANNOTATIONS_FILE) -> list[tuple]:
    all_images = []
    tree = ET.parse(file_name)
    root = tree.getroot()

    # Return list [(file_name, usability, rotation), (file_name, usability), (file_name)]

    for child in root:
        if child.tag != 'image':
            continue
        entry = []
        file_name = child.attrib.get('name')
        entry.append(file_name)
        
        try:
            # Only parse images with tags
            next(child.iter('tag'))
        except StopIteration:
            all_images.append(tuple(entry))
            continue
        
        for tag in child.iter('tag'):
            if tag.attrib.get('label') == 'Usability':
                usability = next(tag.iter('attribute')).text
                if usability in ['usable', 'partially usable', 'unusable']:
                    entry.append(usability)
            elif tag.attrib.get('label') == 'Significant rotation':
                entry.append('Significant rotation')
        found_calving = False
        for box in child.iter('box'):
            if box.attrib.get('label') == 'Calving' and not found_calving:
                area = abs((float(box.attrib.get("xbr")) - float(box.attrib.get("xtl"))) * (float(box.attrib.get("ytl")) - float(box.attrib.get("ybr"))))
                if area < BOX_AREA_THRESHOLD:
                    # Enforce minimum calving size
                    continue
                entry.append('Calving')
                found_calving = True
        all_images.append(tuple(entry))
    return all_images

def get_labeled(file_name=DEFAULT_ANNOTATIONS_FILE) -> list[tuple]:
    parsed = parse(file_name)

    return [x for x in parsed if len(x) > 1]

def get_unlabeled(file_name=DEFAULT_ANNOTATIONS_FILE) -> list[tuple]:
    parsed = parse(file_name)

    return [x for x in parsed if len(x) == 1]

def get_with_label(label: str, file_name=DEFAULT_ANNOTATIONS_FILE) -> list[tuple]: 
    parsed = parse(file_name)

    return [x for x in parsed if label in x]

def get_calving(file_name=DEFAULT_ANNOTATIONS_FILE) -> list[tuple]:
    parsed = parse(file_name)
    return [x for x in parsed if 'Calving' in x]

def get_calving_pairs(file_name=DEFAULT_ANNOTATIONS_FILE, usable=True) -> list[tuple]:
    parsed = parse(file_name)
    # Get calving labels

    has_calving = []
    for x in parsed:
        if usable and (('unusable' in x) or ('partially usable' in x)):
            continue
        if len(x) == 1:
            has_calving.append((x[0], 'Unlabeled'))
        elif 'Calving' in x:
            has_calving.append((x[0], 'Calving'))
        else:
            has_calving.append((x[0], 'No calving'))

    # Create pairs of (before, after, calving) for all images
    pairs = []
    for i, x in enumerate(has_calving):
        if i == 0:
            continue
        pairs.append((has_calving[i-1][0], has_calving[i][0], has_calving[i][1]))
    return pairs

def _mix(pairs: list[tuple], label: str) -> list[tuple]:
    l = [pair[0] for pair in pairs]
    r = [pair[1] for pair in pairs]

    return [(l, r, label) for l, r in list(itertools.product(l, r, repeat=1))]



def get_calving_pairs_augmented(file_name=DEFAULT_ANNOTATIONS_FILE, usable=True) -> list[tuple]:
    pairs = get_calving_pairs(file_name=file_name, usable=usable)
    pairs = [pair for pair in pairs if 'Unlabeled' not in pair]
    non_calving_pairs = [pair for pair in pairs if 'No calving' in pair]
    calving_pairs = [pair for pair in pairs if 'Calving' in pair]


    # l_calvings = [pair[0] for pair in calving_pairs]
    # r_calvings = [pair[1] for pair in calving_pairs]

    # calving_pairs = [(l, r, 'Calving') for l, r in list(itertools.product(l_calvings, r_calvings, repeat=1))]
    #non_calving_pairs = _mix(non_calving_pairs, 'No calving')
    calving_pairs = _mix(calving_pairs, 'Calving')
    
    return non_calving_pairs + calving_pairs


def parse_with_size(file_name=DEFAULT_ANNOTATIONS_FILE) -> list[tuple]:
    all_images = []
    tree = ET.parse(file_name)
    root = tree.getroot()

    # Return list [(file_name, usability, rotation), (file_name, usability), (file_name)]

    for child in root:
        if child.tag != 'image':
            continue
        entry = []
        file_name = child.attrib.get('name')
        entry.append(file_name)
        
        try:
            # Only parse images with tags
            next(child.iter('tag'))
        except StopIteration:
            all_images.append(tuple(entry))
            continue
        
        for tag in child.iter('tag'):
            if tag.attrib.get('label') == 'Usability':
                usability = next(tag.iter('attribute')).text
                if usability in ['usable', 'partially usable', 'unusable']:
                    entry.append(usability)
            elif tag.attrib.get('label') == 'Significant rotation':
                entry.append('Significant rotation')
        found_calving = False
        for box in child.iter('box'):
            if box.attrib.get('label') == 'Calving' and not found_calving:
                area = abs((float(box.attrib.get("xbr")) - float(box.attrib.get("xtl"))) * (float(box.attrib.get("ytl")) - float(box.attrib.get("ybr"))))
                if area < BOX_AREA_THRESHOLD:
                    # Enforce minimum calving size
                    continue
                entry.append('Calving')
                entry.append(area)
                found_calving = True
        all_images.append(tuple(entry))
    return all_images

def get_calving_pairs_with_size(file_name=DEFAULT_ANNOTATIONS_FILE, usable=True) -> list[tuple]:
    parsed = parse_with_size(file_name)
    # Get calving labels

    has_calving = []
    for x in parsed:
        if usable and (('unusable' in x) or ('partially usable' in x)):
            continue
        if len(x) == 1:
            has_calving.append((x[0], 'Unlabeled'))
        elif 'Calving' in x:
            has_calving.append((x[0], 'Calving', x[3]))
        else:
            has_calving.append((x[0], 'No calving'))

    # Create pairs of (before, after, calving) for all images
    pairs = []
    for i, x in enumerate(has_calving):
        if i == 0:
            continue
        if has_calving[i][1] == 'Calving':
            pairs.append((has_calving[i-1][0], has_calving[i][0], has_calving[i][1], has_calving[i][2]))
        else:
            pairs.append((has_calving[i-1][0], has_calving[i][0], has_calving[i][1]))
    return pairs

def main():
    # print(len(parse()))
    # print(len(get_labeled()))
    # print(len(get_with_label('usable')))
    # print(len(get_calving()))
    # print(len([x for x in get_calving_pairs() if 'Unlabeled' not in x]))
    # print(len([x for x in get_calving_pairs(usable=True) if 'Unlabeled' not in x]))
    # print(len(get_calving_pairs("august_annotations.xml")))
    print(len(get_calving()))
    print(len([x for x in get_calving_pairs() if 'No calving' in x]))
    print(len(get_calving_pairs_augmented()))
    pairs_with_area = get_calving_pairs_with_size()
    random.seed(20)
    random.shuffle(pairs_with_area)
    random.seed()
    pairs_with_area = [x for x in pairs_with_area if x[2] != 'Unlabeled']
    test_pairs_with_area = pairs_with_area[int(0.8*len(pairs_with_area)):]

    test_calvings = [x[3] for x in test_pairs_with_area if 'Calving' in x]
    print(test_calvings)
    
    # print(get_calving_pairs_augmented())

if __name__ == '__main__':
    main()
