def imgDistance(points):
    h = 500 #高度
    convert(h,points)

# v 物距   雷达扫描 单位mm
def convert(v,points):
    unit  = 1.4 #1.4um  像素大小
    f = 3.6  # 3.6mm 焦距
    ratio = v/f
    realPoints  = []
    for point in points:
        realPoints.append((point[0]*unit*ratio/1000/10,point[1]*unit*ratio/1000/10)) 
    print ("实际距离，单位厘米:",realPoints)
    pass
