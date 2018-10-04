from wand.image import Image
from wand.display import display

for i in range(1,935):
   with Image(filename="./origin/%03d.jpg"%i) as img:
       print(img.size)
       for r in 1, 2, 3:
           try:
               with img.clone() as tmp :
                   #tmp.liquid_rescale(int(40), int(60))
                   tmp.resize(int(40),int(60))
                   #print("1")
                   tmp.rotate(90 * r)
                   #print("1")
                   tmp.type = 'grayscale';
                   tmp.save(filename="./after/rotate{0}/{1}.jpg".format(r,i))
                   print("succ")
           except:
               print("error")
               pass
