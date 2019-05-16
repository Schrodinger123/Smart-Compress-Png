#coding:utf-8
import os
import os.path
import sys
import ConfigParser
import string

thisFilePath = sys.path[0]

#project res path
resPath = "Your res Path Here!"

#keep original path
keepOrgPath = thisFilePath+"/keepOrg.txt" 

#already compressed path (auto)
compressedFile = thisFilePath+"/compressedFile.txt"

compressedAllSize = 0

#create if not exists
if not os.path.exists(thisFilePath+"/compressedFile.txt"):
	os.system("touch "+thisFilePath+"/compressedFile.txt")

if not os.path.exists(thisFilePath+"/keepOrg.txt"):
	os.system("touch "+thisFilePath+"/keepOrg.txt")

def formatSize(bytes):
    try:
        bytes = float(bytes)
        kb = bytes / 1024
    except:
        return "Error"

    if kb >= 1024:
        M = kb / 1024
        if M >= 1024:
            G = M / 1024
            return "%fG" % (G)
        else:
            return "%fM" % (M)
    else:
        return "%fkb" % (kb)

for rt,dirs,files in os.walk(resPath):
	for file in files:
		if os.path.splitext(rt+"/"+file)[1] == ".png":
			filePath = rt+"/"+file

			compressFlag = True

			orgFileHandler = open(keepOrgPath)
			line = orgFileHandler.readline()
			line = line.strip('\n')

			while line:
				if resPath+"/"+line == filePath:
					compressFlag = False
					orgFileHandler.close()
					break
				line = orgFileHandler.readline()
				line = line.strip('\n')
				
			orgFileHandler.close()

			compressedHandler = open(compressedFile)
			line = compressedHandler.readline()
			line = line.strip('\n')
			while line:
				if resPath+"/"+line == filePath:
					compressFlag = False
					compressedHandler.close()
					break
				line = compressedHandler.readline()
				line = line.strip('\n')

			compressedHandler.close()

			if compressFlag == True:
				oriSize = os.path.getsize(filePath)
				os.system("./pngquant/pngquant "+filePath+" -o "+thisFilePath+"/"+"temp.png")
				comSize = os.path.getsize(thisFilePath+"/temp.png")
				size = formatSize(oriSize-comSize)
				if oriSize-comSize > 0:
					os.system("rm "+filePath)
					os.system("mv "+thisFilePath+"/temp.png"+" "+filePath)
					compressedAllSize += oriSize-comSize
					print "M "+filePath+"  "+size
				else:
					os.system("rm "+thisFilePath+"/temp.png")

				fileHandler = open(compressedFile,"a")
				fileHandler.write(str(filePath[len(resPath)+1:])+'\n')
				fileHandler.close()

print "total compressed: "+formatSize(compressedAllSize)
