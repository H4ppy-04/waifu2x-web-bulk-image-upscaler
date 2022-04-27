import os
import sys
import glob
import time
import shutil
import selenium
from os import listdir
from pathlib import Path
from asyncore import loop
from selenium import webdriver
from os.path import isfile, join
from datetime import datetime, timedelta
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys

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
if os.path.exists(outputDir) and os.path.isdir(outputDir):
     print("Output folder already exists, skipping creation of folder")
else:
     os.mkdir(outputDir)
os.mkdir(bufferDir)
print("Input is " + input + ", output folder is set to " + output + ", using server " + server)

chromeOptions = webdriver.ChromeOptions()
prefs = {"download.default_directory" : bufferDir}
chromeOptions.add_experimental_option("prefs",prefs)
driver = webdriver.Chrome(options=chromeOptions)
driver.get(server)

for filename in os.listdir(inputDir):

     # Compare number of files in input and output folder, and show percentage of completion in console
     inputFiles = len(os.listdir(inputDir))
     outputFiles = len(os.listdir(outputDir))
     percentage = (outputFiles / inputFiles) * 100
     
     # Show percentage of completion in console as progress bar
     sys.stdout.write("\r")
     sys.stdout.write("[%-20s] %d%%" % ('='*int(percentage/5), percentage) + ": ")
     sys.stdout.flush()

     # Check if file is a jpg, jpeg or png
     if filename.endswith(".jpg") or filename.endswith(".jpeg") or filename.endswith(".png"): 
          filePath = inputDir + "/" + filename
         
          # Check if any files have been placed in output folder, if so, skip them
          if os.path.exists(outputDir + "/" + filename):
               print(filename + " already exists, skipping")
               continue
         
          # Upload file to site, and choose options         
          driver.find_element(By.ID, 'file').send_keys(filePath)
          driver.find_element(By.XPATH, "//input[@name='style' and @value='photo']").click()
          driver.find_element(By.XPATH, "//input[@name='noise' and @value='-1']").click()
          driver.find_element(By.XPATH, "//input[@name='scale' and @value='2']").click()
          driver.find_element(By.XPATH, "//input[@class='button' and @value='Download']").click()

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