# This script can be used to prove the connectability of eGDB connections (.sde files) from ArcGIS Server
# The script can be run from the Python included with ArcGIS Server

# Run from anywhere:
# Usage Example #1: "C:\Program Files\ArcGIS\Server\framework\runtime\ArcGIS\bin\Python\Scripts\propy.bat" c:\path\proveSdeConnections.py "c:\path\myConnection1.sde,c:\path\myConnection2.sde"
# Run from the Python directory in ArcGIS Server:
# Usage Example #2: C:\Program Files\ArcGIS\Server\framework\runtime\ArcGIS\bin\Python\Scripts\>propy.bat c:\path\proveSdeConnections.py "c:\path\myConnection1.sde,c:\path\myConnection2.sde"

import arcpy
from arcpy import env
from pathlib import Path
import argparse
import logging
import sys 

def main(argv=None):
    
    # logging to the current working directory and stdout
    try:
        logging.basicConfig(filename="proveSdeConnections.log",encoding="utf-8",level=logging.DEBUG, format="%(asctime)s %(levelname)-8s %(message)s",datefmt="%Y-%m-%d %H:%M:%S")
    except:
        logging.basicConfig(filename="proveSdeConnections.log",level=logging.DEBUG, format="%(asctime)s %(levelname)-8s %(message)s",datefmt="%Y-%m-%d %H:%M:%S")
    logging.getLogger().addHandler(logging.StreamHandler(sys.stdout))
    print("")
    logging.info("*** PROVING .SDE CONNECTIONS ***")
    print("")
    parser = argparse.ArgumentParser()
    parser.add_argument('sdeFiles', help=('Comma delimited list of .sde files'))
    args = parser.parse_args()
    sdeFiles = args.sdeFiles
    logging.info("sdeFiles to be tested: " + sdeFiles)
    print("")
    
    sdeFileList = sdeFiles.split(",")
    for sdeFile in sdeFileList:
        file = Path(sdeFile)
        if (file.is_file()):
            try:
                desc = arcpy.Describe(sdeFile)
                if (desc.dataType == 'File'):
                    # When arcpy sees the describe data type as 'File', it means it could not connect to the workspace
                    # For reasons unknown to me, arcpy requires connection to the target to be able to report on the 
                    # contents of the .sde file
                    raise Exception('The target cannot be reached.  Check to see if the instance is down/inaccessible, drivers are missing, or contents of the .sde file are incorrect')		    
                reportConnectionProperties(sdeFile, desc)
                reportFeatureClassCount(sdeFile)
            except Exception as e:
                logging.error("CONNECTION FAILED TO: " + sdeFile)
                logging.error("  ERROR message: " + str(e))
                try:
                    # If we cannot connect for any reason, we try to report the text content of the .sde file ...
                    fileContent = returnSdeFileText(sdeFile)
                    logging.info('FILE CONTENT: ' + fileContent)
                except:
                    logging.error("UNABLE TO READ TEXT FROM FILE: " + sdeFile)
                    logging.error("  ERROR message: " + str(e))		    
            print("")
        else:
            logging.error("ERROR! File does not exist: " + sdeFile)
            print("")
    print("")
    logging.info("### PROVING .SDE CONNECTIONS COMPLETE ###")
 
def returnSdeFileText(fileName):
	chunkSize = 16
	accumulatedAsciiText = '' 
	with open (fileName,'rb') as theFile:
		while True:
			data = theFile.read(chunkSize)
			hexdata = data.hex()
			if len(hexdata) == 0:
				break #when we're out of data from the file, we exit the read loop
			try:            
				line = data.decode("utf-8") # if we cannot decode the data to utf-8  (i.e. it is not a bytestring, it is something else), we skip the chunk
				lineAsciiFiltered = ' '.join(i for i in line if (ord(i) > 31 and ord(i) < 126)) # replace goofy characters with a space
				if (len(lineAsciiFiltered) > 0):
					accumulatedAsciiText = accumulatedAsciiText + ' '  + lineAsciiFiltered # add any characters found to our eventual return value
			except: 
				line = '' # do nothing because we could decode to utf-8
	return accumulatedAsciiText

def reportFeatureClassCount(targetSdeName):
    env.overwriteOutput = True
    env.workspace = targetSdeName
    fcList = arcpy.ListFeatureClasses()
    logging.info("  NUMBER OF FEATURECLASSES FOUND on connection: " + str(len(fcList)))

def reportConnectionProperties(targetSdeName, desc):
    logging.info("FILE: " + targetSdeName + " properties:")
    connectionProperties = desc.connectionProperties
    try:
        logging.info("  Server: " + connectionProperties.server)
    except:
        logging.info("  - No server property")
    try:
        logging.info("  Instance: " + connectionProperties.instance)
    except:
        logging.info("  - No instance property")
    try:
        logging.info("  Database: " + connectionProperties.database)
    except:
        logging.info("  - No database property")
    try:
        logging.info("  User: " + connectionProperties.user)
    except:
        logging.info("  - No user property")
    try:
        logging.info("  Version: " + connectionProperties.version)
    except:
        logging.info("  - No version property")
    try:
        logging.info("  Authentication Mode: " + connectionProperties.authentication_mode)
    except:
        logging.info("  - No authentication mode property")        
    try:
        logging.info("  Historical Name: " + connectionProperties.historical_name)
    except:
        logging.info("  - No historical name property")        
    try:
        logging.info("  Historical Timestamp: " + connectionProperties.historical_timestamp)
    except:
        logging.info("  - No historical timestamp property")        
    try:
        logging.info("  Is Geodatabase: " + connectionProperties.is_geodatabase)
    except:
        logging.info("  - No is_geodatabase property")    
    try:
        logging.info("  Branch: " + connectionProperties.branch)
    except:
        logging.info("  - No branch property")   
    try:
        logging.info("  Geodatabase release: " +  desc.release)
    except:
        logging.info("  - No Geodatabase release property")   
       
if __name__ == "__main__":
	sys.exit(main(sys.argv))
    
