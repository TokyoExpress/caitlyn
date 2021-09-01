import os

for count, filename in enumerate(os.listdir("presivir/Games by Gameness/Not Game/")):
    dst = str(count).zfill(5) + ".jpg"
    src ='presivir/Games by Gameness/Not Game/'+ filename
    dst ='presivir/Games by Gameness/Not Game/NG_'+ dst
    os.rename(src, dst)