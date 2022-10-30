def xywh_to_tlbr(coord):
    return [coord[1], coord[0]+coord[2], coord[1]+coord[3], coord[0]]

def tlbr_to_xywh(coord):
    return [coord[3], coord[0], coord[1]-coord[3], coord[2]-coord[0]]