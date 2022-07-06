
v = 950
def imgDistance(points):
    h = 950 #高度 cm
    distance = convert(points)
    return distance

# v 物距   雷达扫描 单位mm
def convert(points):
    global v
    unit  = 1.4 #1.4um  像素大小
    f = 3.6  # 3.6mm 焦距
    ratio = v/f
    s= 4 #调整系数
    realPoints  = []
    for point in points:
        realPoints.append((point[0]*unit*ratio/1000/10*s,point[1]*unit*ratio/1000/10*s)) 
    # print ("实际距离，单位厘米:",realPoints)
    
    return realPoints

def getYDistance (points):
    global v
    center  = getCenter(points)
    pass


def getCenter(points):
    xCenter = (points[1][0] - points[0][0])/2
    yCenter = (points[2][1] - points[0][1])/2
    center = (xCenter,yCenter)
    # print ("center:",center)
    return center
