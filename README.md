# Geo-referenced Geometry Files

Classic geometry file formats as `.obj`, `.off`, `.ply`, `.stl` or `.dae` do not support the utilization of coordinate systems besides from a local system, that can not be defined more precisely.
This feature is a major requirement for global applications, exchanging geo-referenced models e.g. in the context of outdoor augmented reality applications.

For this reason, the present project evaluates different possibility of geo-referenced geometry files.

Next to wide-spread standards as `CityJSON`, `GeoJSON`, `GML` or `KML`, we introduce four geo-referenced extensions called `.geoobj`, `.geooff`, `.geoply` and `.geostl`.
While, the named standard formats allow defining objects with multiple additional features, they also come with an overhead according to the file size and an increased structural complexity with disadvantages to the read performance.
This overhead has to be minimized in many use cases and for this reason, some file formats are more suitable than others. For completeness: the overhead can be further reduced using binary representations (like binary `obj` or `stl`) instead of textual ones, but since not all named formats support a binary mode, this is ignored in favor of human-readability within this project.

In addition to the named formats there is also the `GeoVRML` format and its successor `X3D` with the geospatial extension. Both formats are currently not part of this comparison.

## Geo-referenced Extensions

In this chapter you can find multiple extensions of classic geometry file formats.
All of these extensions support two major features:

1. Defining the coordinate reference system (CRS) of the used vertices' coordinates
2. Defining an optional origin, which defines the model's center and allows to use relative local coordinates from this center.

### Geoobj

The `.geoobj` file format extends the classic `.obj` file format with two line-types:

1. The `crs` line type is used to define the coordinate system which is used within the file
2. The `o` line type is used to define the optional origin of the vertices

Example:
```
crs urn:ogc:def:crs:EPSG::4326
o 48.3028533074941 14.2842865755919 279.307006835938
```

#### Addons

Next to the geo-referencing features, the `.geoobj` extension also supports exchanging `scale`, `rotation`, as well as `translation` information in the `origin-based` variant using the following line prefixes:

1. `sc` for adding scale information (`s` is already defined in `.obj` for smoothing groups)
2. `t` for translation information
3. `r` for rotation angular information

Example:

```
sc 1.5 2 5
t 10 -5 4
r 90 45 10
```

### GeoOFF

The `.geooff` file format extends the classic `.off` file. 
For this we introduce a new file header using the `GeoOFF` prefix instead of `OFF`.
The next non-empty line after this header is used to define the crs as well as the origin in a whitespace-separated style.

Example:
```
GeoOFF
urn:ogc:def:crs:EPSG::4326 48.3028533074941 14.2842865755919 279.307006835938
```

### Geoply

The `.geoply` file format extends the classic `.ply` file format with two header-line-types:

1. The `crs` line type is used to define the coordinate system which is used within the file
2. The `origin` line type is used to define the optional origin of the vertices

In addition to those types it also changes the header from `ply` to `geoply`.

```
geoply
crs urn:ogc:def:crs:EPSG::4326
o 48.3028533074941 14.2842865755919 279.307006835938
...
end_header
```

#### Addons

Next to the geo-referencing features, the `.geply` extension also supports exchanging `scale`, `rotation`, as well as `translation` information using the following line prefixes:

1. `scale` for adding scale information
2. `translate` for translation information
3. `rotate` for rotation angular information

Example:

```
geoply
...
scale 1.5 2 5
translate 10 -5 4
rotate 90 45 10
...
end_header
```

### Geostl

The `.geostl` file format extends the classic `.stl` file using the `geosolid` root element.
Followed by the `geosolid` prefix of the file format a meta-data tuple is introduced.
This tuple consists of the crs at the first position, followed by the optional origin coordinates and finally the optional stl name.

``` 
geosolid urn:ogc:def:crs:OGC:2:84 48.3028533074941 14.2842865755919 279.307006835938 fileName
```

## File format comparison

The different named file formats come with a variable amount of features according to e.g. the supported CRS, multi-object support or also differ in the representation of vertices. To take up the last point, some formats use e.g. central vertex lists with referencing indices in the face definition and others re-define the vertices within every indiviudal face. Next to that there are many different other features (e.g. smoothing groups in `.obj`, `geographicalExtent` in `CityJSON` or exact property definitions in `.ply`), which vary between the file formats and lead to a diverse semantic expressiveness. 

| Format   | Baseformat | Coordinate Reference System | Multiple Objects | Vertex References | Origin Support | Transformation Information | Semantic Expressiveness |
|----------|------|-----------------------------|------------------|-------------------|----------------|----------------------------|-------------------------|
| [CityJSON](https://www.cityjson.org/) | [JSON](https://www.json.org/) | Any                         | Yes              | Yes               | No             | No                         | ++                      |
| [GeoJSON](https://geojson.org/)  | [JSON](https://www.json.org/) | WGS 84                      | Yes              | No                | No             | No                         | +                       |
| [GeoObj](#geoobj)   | [OBJ](http://fegemo.github.io/cefet-cg/attachments/obj-spec.pdf)  | Any                         | Yes              | Yes               | Yes            | Yes                        | ~                       |
| [GeoOFF](#geooff)   | [OFF](https://shape.cs.princeton.edu/benchmark/documentation/off_format.html)  | Any                         | No               | Yes               | Yes            | No                         | -                       |
| [GeoPly](#geoply)   | [Ply](http://graphics.stanford.edu/data/3Dscanrep/)  | Any                         | No               | Yes               | Yes            | Yes                        | ~                       |
| [GeoStl](#geostl)   | [Stl](https://www.fabbers.com/tech/STL_Format)  | Any                         | No               | No                | Yes            | No                         | --                      |
| [GML](https://www.ogc.org/standards/gml)      | [XML](https://www.w3.org/XML/)  | Any                         | Yes              | No                | No             | No                         | ++                      |
| [KML](https://developers.google.com/kml/documentation/kmlreference)      | [XML](https://www.w3.org/XML/)  | WGS 84                      | Yes              | No                | No             | No                         | ++                      |
### Size comparison

TODO

## Getting started

To set up and use the project have a look at the detailed description [here](./documentation/Tox.md)

### Importing files

The present project supports multiple reader implementations for importing (geo-referenced) geometry files (`.obj`, `.geoobj`,  `.ply`, `.geoply`, `.off`, `.geooff`, `.stl`, `.geostl`).
Using one of these readers is the entrypoint to the framework and allows to create an in-memory geometry model using the `GeoObjectFile` class. Note that only a subset of the features of the named files are currently supported. So reading files with non-supported features may result in a loss of information (e.g. smoothing groups in `.obj`, or exact property definitions of `.ply`)

```python
reader = GeoObjReader()
path = "mygreatfile.geoobj"
with open(path) as file:
    geoObjFile: GeoObjectFile = reader.read(file)
```

### Converting

The present framework supports different conversion methodologies as converting from one to another coordinate reference system.
Next to the CRS-conversion the framework also supports to transform between origin and non-origin based representations, as well as between geo-referenced and local representations. 
Finally, there is also basic support for transforming (scale, rotation, translation) a model's vertices.

```python
# 1. Change coordinate system
converter = CrsConverter()
converted = converter.convert(geoObjFile, "urn:ogc:def:crs:OGC:2:84")

# 2. Change to origin-based representation
originconverter = OriginConverter()
origin_based = originconverter.to_origin(converted)

# 3. Apply transformation
transformer = Transformer()
origin_based.scaling = [2, 2, 2]
origin_based.translation = [5, 10, -5]
origin_based.rotation = [45, 30, 90]
transformed = transformer.transform(origin_based)

```

### Exporting files

Finally, the in-memory model representations can be re-written to your hard drive using one of the writer implementations. 
Note:
1. That you can find more writers than readers in this project for evaluation purposes. The additional writers only use a minimal subset of the specific file format's features as base for comparison and are not complete. 
2. That some file formats presuppose specific CRS (e.g. `.kml` requires vertices in `Wgs84` representation)
3. Most file formats do not support transformation (scale, rotation, translation) meta-information. A model's vertices have to be transformed first before exported to such a file format.
4. The writers will automatically append the specific file type (unless you set `append_file_type` to `False`)
```python
writer = GeoPlyWriter()
writer.write("mygreatfile.geoply", transformed, append_file_type=False)
```