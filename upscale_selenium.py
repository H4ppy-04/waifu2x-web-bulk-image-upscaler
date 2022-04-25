import os
import sys
import glob
import time
import shutil
import selenium
from os import listdir
from os.path import isfile, join
from asyncore import loop
from pathlib import Path
from selenium import webdriver
from datetime import datetime, timedelta

# Arguments passed from input
input = sys.argv[1]
output = sys.argv[2]
server = sys.argv[3]

# Directory variables
absDir = Path(__file__).parent.resolve()
inputDir = str(str(absDir) + "/" + input)
bufferDir = str(str(absDir) + "/buffer")
outputDir = str(str(absDir) + "/" + output)

# Init arguments
if os.path.exists(bufferDir) and os.path.isdir(bufferDir):
    shutil.rmtree(bufferDir)
os.mkdir(bufferDir)
os.mkdir(outputDir)
with open(bufferDir + 'buffer', 'w') as f:
    f.write('')
print("Input is " + input + ", output folder is set to " + output + ", using server " + server)

chromeOptions = webdriver.ChromeOptions()
prefs = {"download.default_directory" : bufferDir}
chromeOptions.add_experimental_option("prefs",prefs)
driver = webdriver.Chrome(chrome_options=chromeOptions)
driver.get(server)



for filename in os.listdir(inputDir):
     if filename.endswith(".jpg") or filename.endswith(".jpeg") or filename.endswith(".png"): 
          filePath = inputDir + "/" + filename
         
          # Check if any files have been placed in output folder, if so, skip them
          if os.path.exists(outputDir + "/" + filename):
               print(filename + " already exists, skipping")
               continue
         
          # Upload file to site, and choose options         
          choose_file = driver.find_element_by_id('file').send_keys(filePath)
          radio1 = driver.find_element_by_xpath("//input[@name='style' and @value='photo']").click()
          radio2 = driver.find_element_by_xpath("//input[@name='noise' and @value='-1']").click()
          radio3 = driver.find_element_by_xpath("//input[@name='scale' and @value='2']").click()
          downloadButton = driver.find_element_by_xpath("//input[@class='button' and @value='Download']").click()

          # While bufferDir empty, wait until file with random name is downloaded, and then rename it to filename and move to output folder
          while not os.listdir(bufferDir):
               time.sleep(1)
          for file in os.listdir(bufferDir):
               if file.endswith(".jpg") or file.endswith(".jpeg") or file.endswith(".png"):
                    os.rename(bufferDir + "/" + file, outputDir + "/" + filename)
                    print("Renamed " + file + " to " + filename)
                    break
         
          
          
          continue
     else:
          continue
# Close driver
driver.close()