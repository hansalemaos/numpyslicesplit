import numpy as np


def np_slice_split(a, splits, delete=True):
    r"""
    Splits a numpy array or a list based on the given indices or ranges and returns the split arrays.

    Parameters:
    a (numpy array/list): The input array/list to be split.
    splits (list): The indices or ranges to split the array on.
    delete (bool, optional): If True, removes the specified indices from the split arrays,
    if not it keeps them and deletes the others
    Defaults to True.

    Returns:
    list: A list of numpy arrays split based on the given indices or ranges.

    Example:
    from numpyslicesplit import np_slice_split
    a = np.arange(1000).reshape(100, 10)[..., 0]
    splits = [(3, 5), (9, 14), (24, 30), (41, 43)]
    s1 = np_slice_split(a, splits, delete=True)
    print(f"{s1=}")
    s2 = np_slice_split(a, splits, delete=False)
    print(f"{s2=}")

    splits = [3, 4, 5, 65, 7, 4, 6, 63, 2, 5, (0, 10)]
    s1 = np_slice_split(a.tolist(), splits, delete=True)
    print(f"{s1=}")
    s2 = np_slice_split(a.tolist(), splits, delete=False)
    print(f"{s2=}")


    # s1=[array([ 0, 10, 20]), array([50, 60, 70, 80]),
    #     array([140, 150, 160, 170, 180, 190, 200, 210, 220, 230]),
    #     array([300, 310, 320, 330, 340, 350, 360, 370, 380, 390, 400]),
    #     array([430, 440, 450, 460, 470, 480, 490, 500, 510, 520, 530, 540, 550,
    #        560, 570, 580, 590, 600, 610, 620, 630, 640, 650, 660, 670, 680,
    #        690, 700, 710, 720, 730, 740, 750, 760, 770, 780, 790, 800, 810,
    #        820, 830, 840, 850, 860, 870, 880, 890, 900, 910, 920, 930, 940,
    #        950, 960, 970, 980, 990])]


    # s1=[[100, 110, 120, 130, 140, 150, 160, 170, 180, 190, 200, 210, 220, 230,
    # 240, 250, 260, 270, 280, 290, 300, 310, 320, 330, 340, 350, 360, 370, 380
    # , 390, 400, 410, 420, 430, 440, 450, 460, 470, 480, 490, 500,
    # 510, 520, 530, 540, 550, 560, 570, 580, 590, 600, 610, 620],
    #  [640], [660, 670, 680, 690, 700, 710, 720, 730, 740, 750, 760,
    #  770, 780, 790, 800, 810, 820, 830, 840, 850, 860, 870, 880, 890,
    #  900, 910, 920, 930,
    # 940, 950, 960, 970, 980, 990]]
    # s2=[[0, 10, 20, 30, 40, 50, 60, 70, 80, 90], [630], [650]]

    """
    arraylen = np.arange(len(a))
    splitsindex = set()
    for x in splits:
        if hasattr(x, "__iter__") or hasattr(x, "__len__"):
            splitsindex.update(list(range(x[0], x[1])))
        else:
            splitsindex.add(x)
    if not delete:
        n = []
        for x in range(len(a)):
            if x not in splitsindex:
                n.append(x)
        splitsindex = set(n)
    indextokeep = np.sort(np.setdiff1d(arraylen, np.array(list(splitsindex))))
    sliceindex = [([indextokeep[0]])]
    for i in zip(indextokeep[1:], indextokeep[2:]):
        if i[1] - i[0] > 1:
            if i[0] + 1 < len(a):
                sliceindex[-1].append(i[0] + 1)
                sliceindex.append([i[1]])
    if sliceindex:
        if len(sliceindex[-1]) == 1:
            if delete:
                sliceindex[-1].append(len(a))
            else:
                sliceindex[-1].append(max(indextokeep))
                if sliceindex[-1][0] == sliceindex[-1][1]:
                    sliceindex[-1][1] = sliceindex[-1][1] + 1
    newarrays = []
    for x in sliceindex:
        newarrays.append(a[x[0] : x[1]])

    return newarrays



