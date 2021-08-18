import cv2

'''
Desenha os retangulos em uma imagem
'''
def draw(rectangles, image):
    for rect in rectangles:
        x, y, w, h = rect
        cv2.rectangle(image, (x, y), (x + w, y + h), (0, 255, 0), 2)

'''
Retorna o maior retangulo
'''
def getBiggest(rectangles):
    biggest = None
    biggestArea = 0
    for rect in rectangles:
        if (biggestArea == 0 or calculateArea(rect) > biggestArea):
            biggest = rect
            biggestArea = calculateArea(biggest)

    return biggest

def getBiggestImage(images):
    biggest = None
    biggestArea = 0
    for image in images:
        if (biggestArea == 0 or calculateImageArea(image) > biggestArea):
            biggest = image
            biggestArea = calculateImageArea(biggest)

    return biggest    


'''
Calcula a area do retangulo
'''
def calculateArea(rect):
    x, y, w, h = rect
    return w * h

'''
Calcula a area da imagem
'''
def calculateImageArea(img):
    w, h, _ = img.shape
    return w * h    

def expand(rect, pixels):
    newRect = [0,0,0,0]
    newRect[0] = max(0, rect[0] - pixels)
    newRect[1] = max(0, rect[1] - pixels)
    newRect[2] = rect[2] + pixels
    newRect[3] = rect[3] + pixels
    return newRect

'''
Retorna uma imagem a partir de um retangulo
'''
def getImage(rect, image):
    return image[rect[1]:rect[1] + rect[3], rect[0]:rect[0] + rect[2]]

'''
Busca os retângulos a partir dos contornos
'''
def getByContours(contours, minArea):
    detections = []
    for cnt in contours:
        x, y, w, h = cv2.boundingRect(cnt)
        detections.append([x, y, w, h])

    return filterByArea(detections, minArea)

'''
filtra os retangulos pela área mínima
'''
def filterByArea(rectangles, minArea):
    newRectangles = []
    for rect in rectangles:
        area = calculateArea(rect)
        if (area > minArea):
            newRectangles.append(rect)

    return newRectangles

'''
Realiza o merge de retangulos que ocupam o mesmo espaço
'''
def merge(rectangles, minArea):
    merges = []
    for rect in rectangles:
        matched = False
        for merge in merges:
            if (overlaps(rect, merge)):
                matched = True
                merge[0] = min(merge[0], rect[0])
                merge[1] = min(merge[1], rect[1])
                merge[2] = max(merge[2], rect[2])
                merge[3] = max(merge[3], rect[3])
        if (not matched):
            merges.append(rect)

    return filterByArea(merges, minArea)

'''
Retorna True quando um retangulo estiver sobreposto ao outro a partir das posições do eixo X e Y
'''
def rangeOverlaps(pos_min1, pos_max1, pos_min2, pos_max2):
    return (pos_min1 <= pos_max2) and (pos_min2 <= pos_max1)

'''
Retorna True quando um retangulo estiver sobreposto ao outro
'''
def overlaps(rect1, rect2):
    x1, y1, w1, h1 = rect1
    x2, y2, w2, h2 = rect2

    return (rangeOverlaps(x1, x1 + w1, x2, x2 + w2) and 
            rangeOverlaps(y1, y1 + h1, y2, y2 + h2))

def test():
    rectangle1 = [20, 10, 100, 200]
    rectangle2 = [30, 10, 90, 200]

    shouldOverlap = overlaps(rectangle1, rectangle2);
    if (not shouldOverlap):
        raise Exception("Rectangles do not overlap");

    rectangle2 = [40, 5, 300, 300]

    shouldOverlap = overlaps(rectangle1, rectangle2);
    if (not shouldOverlap):
        raise Exception("Rectangles do not overlap");    

    rectangle2 = [300, 300, 300, 300]

    shouldOverlap = overlaps(rectangle1, rectangle2);
    if (shouldOverlap):
        raise Exception("Rectangles should not overlap");              

    expandedRectangle = expand(rectangle1, 10)
    if (expandedRectangle[0] != 10 or
        expandedRectangle[1] != 0 or
        expandedRectangle[2] != 110 or
        expandedRectangle[3] != 210):
        raise Exception("Expanding rectangle failed");

    print("all testing passed")

if __name__ == "__main__":
    test()