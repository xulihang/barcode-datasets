# barcode-datasets

Groud Truth for Several Barcode Datasets


## Annotation

There are two types of annotation:

1. Plain text including the barcode results.
2. A JSON containing the barcode format, localization and text: 

   ```json
   [{"attrib": {"Type": "QR"}, "text": "Text", "value_attrib": {}, "x1": "513.73134328358210000000", "y1": "89.85074626865672000000", "x2": "466.11940298507460000000", "y2": "295.22388059701490000000", "x3": "256.26865671641790000000", "y3": "273.58208955223880000000", "x4": "260.14925373134326000000", "y4": "77.76119402985074000000"}]
   ```