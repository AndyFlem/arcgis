import removeholes
import arcpy

workspace="C:/temp/outlines.gdb"
inputNames=["D3_Q25","D3_R5","D3_R10"]

arcpy.env.overwriteOutput=True
arcpy.env.workspace=workspace


for inputName in inputNames:
    print("Processing: " + inputName)
    desc = arcpy.Describe(inputName)
    baseName=desc.baseName

    arcpy.MultipartToSinglepart_management(inputName, baseName + "_single")

    removeholes.RemovePolygonHoles_management(baseName + "_single", baseName + "_noholes", 300)

    arcpy.CopyFeatures_management(baseName + "_noholes", baseName + "_nosmalls")
    expression = arcpy.AddFieldDelimiters("tempLayer", "SHAPE_AREA") + " < 300"
    arcpy.MakeFeatureLayer_management(baseName + "_nosmalls", "tempLayer")
    arcpy.SelectLayerByAttribute_management("tempLayer", "NEW_SELECTION", expression)
    arcpy.DeleteFeatures_management("tempLayer")

    arcpy.SmoothPolygon_cartography(baseName + "_nosmalls", baseName + "_carto", "PAEK", 100)
