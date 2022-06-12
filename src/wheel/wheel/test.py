import os
b = "1.txt"
a = os.path.exists(b)
print(a)
if(a==False):
    f = open(b,'w')
    f.close()
# os.remove(b)  

# try:
#     f = open("1.txt",'r')
#     f.close()
# except IOError:
#     f = open("1.txt",'w')