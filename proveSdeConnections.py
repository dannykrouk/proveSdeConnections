# This script can be used to prove the connectability of eGDB connections (.sde files) from ArcGIS Server
# The script can be run from the Python included with ArcGIS Server
# Usage Example: "C:\Program Files\ArcGIS\Server\framework\runtime\ArcGIS\bin\Python\Scripts\propy.bat" c:\path\proveSdeConnections.py "c:\path\myConnection1.sde,c:\path\myConnection2.sde"
import arcpy
from arcpy import env
from pathlib import Path
import argparse
import logging
import sys 

def main(argv=None):
    
    # logging to the current working directory and stdout
    logging.basicConfig(filename="proveSdeConnections.log",encoding="utf-8",level=logging.DEBUG, format="%(asctime)s %(levelname)-8s %(message)s",datefmt="%Y-%m-%d %H:%M:%S")
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
                reportConnectionProperties(sdeFile, desc)
                reportFeatureClassCount(sdeFile)
            except Exception as e:
                logging.error("CONNECTION FAILED TO: " + sdeFile)
                logging.error("  ERROR message: " + str(e))
            print("")
        else:
            logging.error("ERROR! File does not exist: " + sdeFile)
            print("")
    print("")
    logging.info("### PROVING .SDE CONNECTIONS COMPLETE ###")
 

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
    
