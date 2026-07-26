"""
IoU（Intersection over Union）

计算两个矩形区域的 IoU（交并比）。

公式：IoU = |A ∩ B| / |A ∪ B|

应用：
- 目标检测评估指标
- 计算机视觉中的区域相似度
- 物体追踪

时间复杂度：O(1)
"""

def IoU(box1, box2) -> float:
    """
    IOU, Intersection over Union
 
    :param box1: list, 第一个框的两个坐标点位置 box1[x1, y1, x2, y2]
    :param box2: list, 第二个框的两个坐标点位置 box2[x1, y1, x2, y2]
    :return: float, 交并比
    """
    if box2[0] > box2[2]:
        box2[0], box2[2] = box2[2], box2[0]
    if box2[1] > box2[3]:
        box2[1], box2[3] = box2[3], box2[1]
     
    weight = max(min(box1[2], box2[2]) - max(box1[0], box2[0]), 0)
    height = max(min(box1[3], box2[3]) - max(box1[1], box2[1]), 0)
    s_inter = weight * height
    s_box1 = (box1[2] - box1[0]) * (box1[3] - box1[1])
    s_box2 = (box2[2] - box2[0]) * (box2[3] - box2[1])
    s_union = s_box1 + s_box2 - s_inter
    return s_inter / s_union