import os
import xml.etree.ElementTree as ET
import json
import shutil
from PIL import Image

def convert_tiff_to_jpg_if_needed(imagePath):
    if imagePath.endswith("tiff") or imagePath.endswith("tif"):
        name, ext = os.path.splitext(imagePath)
        image = Image.open(imagePath)
        target_path = name + ".jpg"
        image.save(target_path)
        print("Convert tiff to jpg: "+target_path)
        os.remove(imagePath)

def append_barcode(results, barcode):
    result = {}
    result["attrib"] = barcode.attrib
    if barcode.attrib["Type"] == "PDF417":
        Values = get_elements(barcode, "Value")
        Polygon  = get_elements(barcode, "Polygon")[0]
        Points = get_elements(Polygon,"Points")[0]
        for Value in Values:
            result["text"] = Value.text
            if result["text"] == "^":
                print("empty text. Skip")
                return False
            #result["text"] = ""
            result["value_attrib"] = Value.attrib
        index = 0
        print(Points[0])
        for point in Points:
            index = index + 1
            result["x"+str(index)] = point.attrib["X"]
            result["y"+str(index)] = point.attrib["Y"]
        results.append(result)
        return True
    else:
        return False
                            
def get_elements(root, name):
    children = []
    for child in root:
        if child.tag == name:
            children.append(child)
    return children

def get_image_name(root, name):
    ext_list = ["jpeg","jpg","png","bmp","tiff","tif","JPEG","JPG","PNG","BMP","TIFF","TIF"]
    for ext in ext_list:
        if os.path.exists(os.path.join(root,name + "." +ext)):
            return name + "." +ext
    return "null"
    

for filename in os.listdir("./Markup"):
    if filename.endswith(".xml") == False:
        continue
    tree = ET.parse(os.path.join("./Markup",filename))
    root = tree.getroot()
    pages = root[0]
    results = []
    for page in pages:
        has_PDF417 = False
        BarcodesRoot = get_elements(page, "Barcodes")[0]
        Barcodes = get_elements(BarcodesRoot, "Barcode")
        for barcode in Barcodes:
            if append_barcode(results, barcode):
                has_PDF417 = True
    if has_PDF417:
        name, ext = os.path.splitext(filename)
        image_name = get_image_name("./Image",name)
        image_path = os.path.join("./Image", image_name)
        target_path = os.path.join("./PDF417", image_name)
        if os.path.exists(image_path):
            shutil.copyfile(image_path, target_path)
        else:
            print("Image not exist: " + filename)
        convert_tiff_to_jpg_if_needed(target_path)
        txt_path = os.path.join("./PDF417",name+".txt")
        f = open (txt_path,"w")
        f.write(json.dumps(results))
        f.close()
        
     
        

    