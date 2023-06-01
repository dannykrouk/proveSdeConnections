# This script can be used to prove the connectability of eGDB connections (.sde files) from ArcGIS Server
# The script can be run from the Python included with ArcGIS Server
# Usage Example: "C:\Program Files\ArcGIS\Server\framework\runtime\ArcGIS\bin\Python\Scripts\propy.bat" c:\path\proveSdeConnections.py "c:\path\myConnection1.sde,c:\path\myConnection2.sde"
import arcpy
from arcpy import env
from pathlib import Path
import argparse

def main(argv=None):
    parser = argparse.ArgumentParser()
    parser.add_argument('sdeFiles', help=('Comma delimited list of .sde files'))
    args = parser.parse_args()
    sdeFiles = args.sdeFiles
    sdeFileList = sdeFiles.split(",")
    print("")
    print("Processing " + str(len(sdeFileList)) + " files ...")
    print("")
    for sdeFile in sdeFileList:
        file = Path(sdeFile)
        if (file.is_file()):
            try:
                desc = arcpy.Describe(sdeFile)
                reportConnectionProperties(sdeFile, desc)
                reportFeatureClassCount(sdeFile)
            except Exception as e:
                print ("ERROR processing: " + sdeFile + ": " + str(e))
            print("")
        else:
            print("ERROR! File does not exist: " + sdeFile)
            print("")
    print("")
    print("DONE!")
 

def reportFeatureClassCount(targetSdeName):
    env.overwriteOutput = True
    env.workspace = targetSdeName
    fcList = arcpy.ListFeatureClasses()
    print ("  NUMBER OF FEATURECLASSES FOUND on connection: " + str(len(fcList)))

def reportConnectionProperties(targetSdeName, desc):
    print ("FILE: " + targetSdeName + " properties:")
    connectionProperties = desc.connectionProperties
    try:
        print("%-12s %s" % ("  Server:", connectionProperties.server))
    except:
        print("  - No server property")
    try:
        print("%-12s %s" % ("  Instance:", connectionProperties.instance))
    except:
        print("  - No instance property")
    try:
        print("%-12s %s" % ("  Database:", connectionProperties.database))
    except:
        print("  - No database property")
    try:
        print("%-12s %s" % ("  User:", connectionProperties.user))
    except:
        print("  - No user property")
    try:
        print("%-12s %s" % ("  Version:", connectionProperties.version))
    except:
        print("  - No version property")
    try:
        print("%-12s %s" % ("  Authentication Mode:", connectionProperties.authentication_mode))
    except:
        print("  - No authentication mode property")        
    try:
        print("%-12s %s" % ("  Historical Name:", connectionProperties.historical_name))
    except:
        print("  - No historical name property")        
    try:
        print("%-12s %s" % ("  Historical Timestamp:", connectionProperties.historical_timestamp))
    except:
        print("  - No historical timestamp property")        
    try:
        print("%-12s %s" % ("  Is Geodatabase:", connectionProperties.is_geodatabase))
    except:
        print("  - No is_geodatabase property")    
    try:
        print("%-12s %s" % ("  Branch:", connectionProperties.branch))
    except:
        print("  - No branch property")   
    try:
        print("%-12s %s" % ("  Geodatabase release:", desc.release))
    except:
        print("  - No Geodatabase release property")   
       
if __name__ == "__main__":
	sys.exit(main(sys.argv))
    
