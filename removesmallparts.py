import arcpy

def RemoveSmallParts_management(in_fc, threshold):
    """
    The function removes shapes and parts smaller than the threshold from a polygon feature class.
    in_fc is a polygon feature class.
    threshold is numeric.
    """
    desc = arcpy.Describe(in_fc)
    if desc.dataType !="FeatureClass" and desc.dataType != "ShapeFile":
        print("Invalid data type. The input is supposed to be a Polygon FeatureClass or Shapefile.")
        return
    else:
        if desc.shapeType != "Polygon":
            print("The input is supposed to be a Polygon FeatureClass or Shapefile.")
            return

    with arcpy.da.UpdateCursor(in_fc, ["SHAPE@"]) as updateCursor:
        for updateRow in updateCursor:
            shape = updateRow[0]
            new_shape = arcpy.Array()
            for part in shape:
                new_part = arcpy.Array()
  
                #find None point in shape part
                #in arcpy module, a None point is used to separate exterior and interior vertices
                #Build a list of indexes for the start of each interior ring
                null_point_index = []
                for i in range(len(part)):
                    if part[i] == None:
                        null_point_index.append(i)

                #if interior vertices exist, create polygons and compare polygon shape area to given threshold
                #if larger, keep vertices, else, dismiss them
                if len(null_point_index) > 0:

                    #build the new exterior ring part
                    for k in range(0, null_point_index[0]):
                        new_part.add(part[k])

                    #for each interior ring
                    for i in range(len(null_point_index)):
                        pointArray = arcpy.Array()
                        
                        if i+1 < len(null_point_index): #if the None point is not the last one
                            for j in range(null_point_index[i] + 1, null_point_index[i+1]):
                                pointArray.add(part[j])
                        else: #if the None point is the last one
                            for j in range(null_point_index[i] + 1, len(part)):
                                pointArray.add(part[j])
                        #create a polygon to check shape area against the given threshold
                        inner_poly = arcpy.Polygon(pointArray)
                        #if larger than threshold, then add to the new part Array
                        if inner_poly.area > threshold:
                            if i+1 < len(null_point_index): #if the None point is not the last one
                                for k in range(null_point_index[i], null_point_index[i+1]):
                                    new_part.add(part[k])
                            else: #if the None point is the last one
                                for k in range(null_point_index[i], len(part)):
                                    new_part.add(part[k])
                    new_shape.add(new_part)
                #if interior does not exist, add the whole part
                else:
                    new_shape.add(part)
                
            if len(new_shape) > 0:
                new_poly = arcpy.Polygon(new_shape)
                updateRow[0] = new_poly
                updateCursor.updateRow(updateRow)


RemoveSmallParts_management("C:\\Temp\\Export_Output.shp",300)