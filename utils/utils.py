import pytesseract
from PIL import Image

def translate_hp_sp_from_Image(img):
    pytesseract.pytesseract.tesseract_cmd ='C:/Program Files/Tesseract-OCR/tesseract.exe' 

    result = pytesseract.image_to_string(img) 
    
    result = result.split("%")
    try:
        hp = int(result[0])
        sp = int(result[1])
    
    except:
        return {
        "hp" : 50,
        "sp" : 100
    }
    
    health_status = {
        "hp" : hp,
        "sp" : sp
    }
    
    return health_status

def spiral(width, height,dx):
    
    list_spiral_loop = []
    
    """
    w of img , h of img , dx = spacing
    """
    NORTH, S, W, E = (0, -dx), (0, dx), (-dx, 0), (dx, 0) # directions
    turn_right = {NORTH: E, E: S, S: W, W: NORTH} # old -> new direction
    
    if width < 1 or height < 1:
        raise ValueError
    x, y = width // 2, height // 2 # start near the center
    dx, dy = NORTH # initial direction
    matrix = [[None] * width for _ in range(height)]
    count = 0
    while True:
        count += 1
        matrix[y][x] = count # visit
        # try to turn right
        new_dx, new_dy = turn_right[dx,dy]
        new_x, new_y = x + new_dx, y + new_dy
        if (0 <= new_x < width and 0 <= new_y < height and
            matrix[new_y][new_x] is None): # can turn right
            x, y = new_x, new_y
            dx, dy = new_dx, new_dy
            list_spiral_loop.append([x,y])
        else: # try to move straight
            x, y = x + dx, y + dy
            if not (0 <= x < width and 0 <= y < height):
                return list_spiral_loop # nowhere to go
            list_spiral_loop.append([x,y])
            

def tranform_spiral(spiral,top_left_location):
    
    tf_list = []
    
    for x,y in spiral:
        x = x + top_left_location[0]
        y = y + top_left_location[1]
        tf_list.append([x,y])
    
    return tf_list
    
            
        
# if __name__ == "__main__":
#     # spiral(768,1024)
#     # for x,y in spiral(30,50):
#         # print(x,"   ",y)
#     a = spiral(1000,700,50)
#     print(a)