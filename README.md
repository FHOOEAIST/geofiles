[![GitHub release](https://img.shields.io/github/v/release/fhooeaist/geofiles.svg)](https://github.com/FHOOEAIST/geofiles/releases)
[![License: MPL 2.0](https://img.shields.io/badge/License-MPL%202.0-brightgreen.svg)](https://opensource.org/licenses/MPL-2.0)
[![PyPI version](https://badge.fury.io/py/geofiles.svg)](https://badge.fury.io/py/geofiles)
[![DOI](https://zenodo.org/badge/401244311.svg)](https://zenodo.org/badge/latestdoi/401244311)

![logo](https://github.com/FHOOEAIST/geofiles/raw/main/documentation/logo.png)
# Geo-referenced Geometry File Formats

Classic geometry file formats as `.obj`, `.off`, `.ply`, `.stl` or `.dae` do not support the utilization of coordinate systems besides from a local system, that can not be defined more precisely.
This feature is a major requirement for global applications, exchanging geo-referenced models e.g. in the context of outdoor augmented reality applications.

For this reason, the present project evaluates different possibilities of geo-referenced geometry files.

Next to wide-spread standards as `GeoVRML`, `X3D`, `CityJSON`, `GeoJSON`, `GML` or `KML`, we introduce four geo-referenced extensions called `.geoobj`, `.geooff`, `.geoply` and `.geostl`.
While, the named standard formats allow defining objects with multiple additional features, they also come with an overhead according to the file size and an increased structural complexity with disadvantages to the read performance.
This overhead has to be minimized in many use cases and for this reason, some file formats are more suitable than others. For completeness: the overhead can be further reduced using binary representations (like binary `obj` or `stl`) instead of textual ones, but since not all named formats support a binary mode, this is ignored in favor of human-readability within this project and comparison.

## Geo-referenced Extensions

In this chapter you can find multiple extensions of classic geometry file formats.
All of these extensions support two major features:

1. Defining the coordinate reference system (CRS) of the used vertices' coordinates
2. Defining an optional origin, which represents an absolute geo-referenced location and an implicit local Cartesian coordinate frame for the models with a metric unit.

### Additional features

Some proposed file formats support additional features such as:
- Geographical extent
- Transformation information (local per object or global for all vertices)
  - Scaling factor
  - Translation
  - Rotation
- Arbitrary meta information:
  - Global per file such as:
    - Translation unit: any unit can be used. The present project only supports transformations with metres (m)
    - Rotation unit: any unit can be used. The present project only supports transformations with degrees (deg)
  - Local per object (such as type information)


### GeoOBJ

The `.geoobj` file format extends the classic `.obj` file format with two line-types:

1. The `crs` line type is used to define the coordinate system which is used within the file
2. The `or` line type is used to define the optional origin of the vertices

Example:
```
crs urn:ogc:def:crs:EPSG::4326
or 48.3028533074941 14.2842865755919 279.307006835938
```

#### Addons

Next to the geo-referencing features, the `.geoobj` extension also supports exchanging `scale`, `rotation`, as well as `translation` information using the following line prefixes:

1. `sc` for adding scale information (`s` is already defined in `.obj` for smoothing groups)
2. `t` for translation information
3. `r` for rotation angular information
4. `tu` for defining the file's translation unit (default is metres `m`)
5. `ru` for defining the file's rotation unit (default is degrees `deg`)
6. `m` for arbitrary meta information. Every meta entry contains a key as first element followed by one or more values

Example:

```
sc 1.5 2 5
t 10 -5 4
r 90 45 10
tu inch
ru rad
m axis_ordering x y z
```

Note that: if either a scaling, a translation or a rotation information is stated after an object definition with the prefix `o`, the transformation is not interpreted globally, but locally for the specific object.

Next to that it also supports the optional geographical extent meta information, containing the minimal (first three values) and maximal (remaining three values) coordinate value expressions using the line prefix `e`.
This information can be useful for filtering geo-referenced files without any need to iterate all vertices.
```
e -0.5 -0.5 -0.5 0.5 0.5 0.5
```

### GeoOFF

The `.geooff` file format extends the classic `.off` file. 
For this we introduce a new file header using `GeoOFF` instead of `OFF`.
The next non-empty line after this header is used to define the crs.

Example:
```
GeoOFF
urn:ogc:def:crs:EPSG::4326
```

GeoOFF supports alternative headers, using different postfix values. The pattern of the header is based on the `OFF` header definition and is defined like `[ST][C][N][4][n]GeoOFF[o][e][s][t][r]`.
Like this GeoOFF is able to support:
- An absolute origin using the `o` header postfix symbol
- Extent information using the `e` header postfix symbol
- Global scaling information using the `s` header postfix symbol
- Global translation information using the `t` header postfix symbol
- Global rotation information using the `r` header postfix symbol
- Arbitrary meta information using the `m` header postfix symbol
  - Defined as blank-separated list of key/value pairs
  - Values may be again list of values that are separated with a pipe symbol `|`
  - Reserved keys:
    - `tu` for defining the translation unit (default is metres `m`)
    - `ru` for defining the rotation unit (default is degrees `deg`)

Example: 
```
GeoOFFostrm
urn:ogc:def:crs:OGC:2:84
14.2842798233032 48.30284881591775 279.807006835938
2 2 2
10 50 100
90 0 0
tu inch type genericobject axis_ordering x|y|z
```

**Note:** The `.off` prefixes are currently not supported in the implementations.

### GeoPLY

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

Next to the geo-referencing features, the `.geply` extension also supports exchanging global `scale`, `rotation`, as well as `translation` information using the following line prefixes:

1. `scale` for adding scale information
2. `translate` for translation information
3. `rotate` for rotation angular information
4. `meta` for arbitrary meta information. Every meta entry contains a key as first element followed by one or more values
5. `tu` for defining the translation unit (default is metres `m`)
6. `ru` for defining the rotation unit (default is degrees `deg`)


Example:

```
geoply
...
scale 1.5 2 5
translate 10 -5 4
rotate 90 45 10
tu m
ru deg
meta type genericobject
meta axis_ordering x y z
...
end_header
```

Next to that it also supports the optional geographical extent meta information, containing the minimal (first three values) and maximal (remaining three values) coordinate value expressions using the `extent` header.
This information can be useful for filtering geo-referenced files without any need to iterate all vertices.
```
geoply
...
extent -0.5 -0.5 -0.5 0.5 0.5 0.5
...
end_header
```

### GeoSTL

The `.geostl` file format extends the classic `.stl` file using the `geosolid` root element.
Followed by the `geosolid` prefix of the file format a meta-data tuple is introduced.
This tuple consists of the crs at the first position, followed by the optional origin coordinates and finally the optional stl name.

``` 
geosolid urn:ogc:def:crs:OGC:2:84 48.3028533074941 14.2842865755919 279.307006835938 fileName
```

## File format comparison

The different named file formats come with a variable amount of features according to e.g. the supported CRS, an origin for specifying a local coordinate system, the meta information of the minimal and maximal coordinates (geographical extent), multi-object support or also differ in the representation of vertices. To take up the last point, some formats use e.g. central vertex lists with referencing indices in the face definition and others re-define the vertices within every indiviudal face. Next to that there are many different other features (e.g. smoothing groups in `.obj`, `geographicalExtent` in `CityJSON` or exact property definitions in `.ply`), which vary between the file formats and lead to a diverse semantic expressiveness. 

| Format                                                                                      | Base format                                                                         | Encoding                                                                                                 | Coordinate Reference System                                                                                                                   | Multiple Objects | Vertex References  | Origin Support | Transformation Information                                                             | Geographical Extent | Semantic Expressiveness |
|---------------------------------------------------------------------------------------------|-------------------------------------------------------------------------------------|----------------------------------------------------------------------------------------------------------|-----------------------------------------------------------------------------------------------------------------------------------------------|------------------|--------------------|----------------|----------------------------------------------------------------------------------------|---------------------|-------------------------|
| [CityJSON](https://www.cityjson.org/)                                                       | [JSON](https://www.json.org/)                                                       | Text                                                                                                     | Any                                                                                                                                           | Yes              | Yes                | No             | [Global Translation + Scaling](https://www.cityjson.org/specs/1.0.3/#transform-object) | Yes                 | ++                      |
| [CityGML](https://www.ogc.org/standards/citygml)                                            | [XML](https://www.w3.org/XML/)                                                      | Text                                                                                                     | Any                                                                                                                                           | Yes              | No                 | No             | No                                                                                     | No                  | ++                      |
| [Collada](https://www.khronos.org/collada/)                                                 | [XML](https://www.w3.org/XML/)                                                      | Text                                                                                                     | None (due to XML structure easily addable)                                                                                                    | Yes              | Yes                | No             | No                                                                                     | No                  | ++                      |
| [GeoJSON](https://geojson.org/)                                                             | [JSON](https://www.json.org/)                                                       | Text                                                                                                     | WGS 84                                                                                                                                        | Yes              | No                 | No             | No                                                                                     | No                  | +                       |
| [GeoObj](#geoobj)                                                                           | [OBJ](http://fegemo.github.io/cefet-cg/attachments/obj-spec.pdf)                    | Text *                                                                                                   | Any                                                                                                                                           | Yes              | Yes                | Yes            | Yes                                                                                    | Yes                 | ~                       |
| [GeoOFF](#geooff)                                                                           | [OFF](https://shape.cs.princeton.edu/benchmark/documentation/off_format.html)       | Text *                                                                                                   | Any                                                                                                                                           | No               | Yes                | Yes            | Yes                                                                                    | Yes                 | -                       |
| [GeoPLY](#geoply)                                                                           | [PLY](http://graphics.stanford.edu/data/3Dscanrep/)                                 | Text *                                                                                                   | Any                                                                                                                                           | No               | Yes                | Yes            | Yes                                                                                    | Yes                 | ~                       |
| [GeoSTL](#geostl)                                                                           | [STL](https://www.fabbers.com/tech/STL_Format)                                      | Text *                                                                                                   | Any                                                                                                                                           | No               | No                 | Yes            | No                                                                                     | No                  | --                      |
| [GML](https://www.ogc.org/standards/gml)                                                    | [XML](https://www.w3.org/XML/)                                                      | Text                                                                                                     | Any                                                                                                                                           | Yes              | No                 | No             | No                                                                                     | No                  | ++                      |
| [KML](https://developers.google.com/kml/documentation/kmlreference)                         | [XML](https://www.w3.org/XML/)                                                      | Text or compressed ([KMZ](https://www.google.com/earth/outreach/learn/packaging-content-in-a-kmz-file/)) | WGS 84                                                                                                                                        | Yes              | No                 | No             | No                                                                                     | No                  | ++                      |
| [GeoVRML](http://www.ai.sri.com/~reddy/geovrml/archive/geovrml1_0.pdf)                      | [VRML](http://www.martinreddy.net/gfx/3d/VRML.spec)                                 | Text or Binary                                                                                           | WGS84 / EPSG4326 / UTM                                                                                                                        | Yes              | Locally per object | Yes            | Yes                                                                                    | Yes                 | +                       |
| [X3D](https://www.web3d.org/documents/specifications/19775-1/V3.3/Part01/Architecture.html) | [XML](https://www.w3.org/XML/), [VRML](http://www.martinreddy.net/gfx/3d/VRML.spec) | Text or Binary                                                                                           | [Multiple supported CRS](https://www.web3d.org/documents/specifications/19775-1/V3.3/Part01/components/geodata.html#t-Supportedspatialframes) | Yes              | Locally per object | No            | Yes                                                                                    | Yes                 | ++                      |

\* Currently, only text support, but the base format would support binary, so a binary extension would be possible.


### Size comparison

The following file comparison uses the minimal required sub-set of the specific file formats to represent geo-referenced 3D models. Additional features (e.g. GeographicalExtent in `CityJSON`) are not considered as far as possible, to avoid a negative bias of the comparison. Next to that also the used reader does not support all features of the input files (e.g. `.mtb` material information) and may use different line-ending symbols (Windows vs Linux). This would lead to the situation that in some cases the input file size is greater than the geo-referenced version. For this reason we have decided to do a normalization first by reading the input files with our custom reader and exporting the normalized representation using our custom obj writer. The exported and normalized files are used as basis of comparison.

You can find the used obj files [here](https://github.com/alecjacobson/common-3d-test-models). Also note that, X3D is currently not explicitly supported by the present framework since it can be encoded using XML or VRML. Next to that it is the successor of [VRML](http://www.martinreddy.net/gfx/3d/VRML.spec) and supports many features of [GeoVRML](http://www.ai.sri.com/~reddy/geovrml/archive/geovrml1_0.pdf) within the [geospatial extension](https://www.web3d.org/documents/specifications/19775-1/V3.3/Part01/components/geodata.html) with only minor  differences. For this reason it would result in a comparable size when using the VRML encoding and is left out in the following comparison.


| file           | vertices | original | cityjson | geojson  | geoobj   | geoobj-origin | geooff   | geooff-origin | geoply   | geoply-origin | geostl   | geostl-origin | geovrml  | geovrml-origin | gml      | kml       |
|----------------|----------|----------|----------|----------|----------|---------------|----------|---------------|----------|---------------|----------|---------------|----------|----------------|----------|-----------|
| alligator      | 3208     | 184.07   | 308.53   | 1402.25  | 278.69   | 184.16        | 272.42   | 177.89        | 272.57   | 178.04        | 1396.25  | 877.53        | 1298.16  | 779.88         | 2202.64  | 2237.52   |
| armadillo      | 49990    | 3608.54  | 5279.43  | 23622.39 | 4791.05  | 3608.63       | 4693.41  | 3510.98       | 4693.56  | 3511.14       | 23476.92 | 16381.74      | 22142.56 | 15047.81       | 36998.27 | 37583.91  |
| beast          | 32311    | 1873.35  | 2850.39  | 9550.49  | 2629.15  | 1873.44       | 2566.04  | 1810.33       | 2566.19  | 1810.48       | 9686.46  | 6660.98       | 9516.07  | 6491.01        | 13723.15 | 13944.12  |
| beetle-alt     | 19887    | 1364.18  | 2037.85  | 9120.80  | 1847.80  | 1364.26       | 1808.95  | 1325.41       | 1809.10  | 1325.57       | 9067.75  | 6249.00       | 8517.69  | 5699.37        | 14292.74 | 14519.08  |
| beetle         | 1148     | 64.34    | 105.07   | 485.01   | 94.64    | 64.42         | 92.38    | 62.16         | 92.53    | 62.32         | 482.03   | 319.74        | 444.47   | 282.62         | 759.87   | 771.75    |
| cheburashka    | 6669     | 420.93   | 667.26   | 3148.23  | 601.94   | 421.01        | 588.91   | 407.98        | 589.06   | 408.14        | 3129.51  | 2044.29       | 2914.99  | 1830.21        | 4932.36  | 5010.33   |
| cow            | 2903     | 182.93   | 286.76   | 1369.35  | 258.21   | 183.01        | 252.53   | 177.33        | 252.68   | 177.49        | 1361.40  | 909.95        | 1264.61  | 813.58         | 2146.05  | 2179.90   |
| fandisk        | 6475     | 391.15   | 646.64   | 3047.66  | 583.21   | 391.23        | 570.56   | 378.58        | 570.71   | 378.73        | 3031.65  | 1879.89       | 2823.33  | 1672.00        | 4779.88  | 4855.58   |
| happy          | 49251    | 3443.42  | 5200.30  | 23271.05 | 4718.75  | 3443.51       | 4622.54  | 3347.30       | 4622.69  | 3347.45       | 23134.59 | 15475.17      | 21818.19 | 14159.20       | 36462.98 | 37040.56  |
| homer          | 6002     | 378.70   | 600.33   | 2832.50  | 541.53   | 378.78        | 529.80   | 367.06        | 529.95   | 367.21        | 2815.80  | 1839.43       | 2622.72  | 1646.78        | 4438.16  | 4508.31   |
| horse          | 48485    | 4847.43  | 5161.59  | 23251.47 | 4687.92  | 4847.51       | 4593.21  | 4752.80       | 4593.36  | 4752.96       | 23025.46 | 23982.47      | 21729.76 | 22687.20       | 36224.65 | 36792.65  |
| igea           | 134345   | 9716.50  | 14490.75 | 63413.22 | 13178.60 | 9716.58       | 12916.19 | 9454.18       | 12916.34 | 9454.33       | 63040.76 | 42268.45      | 59765.43 | 38993.54       | 99360.66 | 100934.83 |
| lucy           | 49987    | 3728.41  | 5310.72  | 23867.91 | 4822.38  | 3728.49       | 4724.74  | 3630.85       | 4724.89  | 3631.01       | 23660.91 | 17097.44      | 22327.22 | 15764.19       | 37242.99 | 37828.60  |
| max-planck     | 50077    | 3628.48  | 5296.99  | 23729.97 | 4808.40  | 3628.57       | 4710.58  | 3530.75       | 4710.73  | 3530.91       | 23558.65 | 16499.04      | 22223.07 | 15163.89       | 37107.86 | 37693.59  |
| nefertiti      | 49971    | 3621.60  | 5288.27  | 23695.48 | 4800.08  | 3621.68       | 4702.47  | 3524.08       | 4702.62  | 3524.23       | 23529.73 | 16459.26      | 22196.36 | 15126.32       | 37066.29 | 37651.70  |
| ogre           | 62194    | 3820.09  | 6569.39  | 29260.92 | 5963.30  | 3820.17       | 5841.82  | 3698.69       | 5841.97  | 3698.85       | 29090.92 | 16271.91      | 27450.41 | 14631.83       | 45852.03 | 46578.48  |
| rocker-arm     | 10044    | 666.93   | 1008.57  | 4742.64  | 910.28   | 667.02        | 890.65   | 647.39        | 890.80   | 647.55        | 4714.26  | 3254.51       | 4394.59  | 2935.27        | 7430.39  | 7547.93   |
| spot           | 2930     | 186.35   | 289.43   | 1380.09  | 260.62   | 186.44        | 254.89   | 180.71        | 255.04   | 180.86        | 1372.51  | 927.39        | 1275.07  | 830.39         | 2163.75  | 2197.91   |
| stanford-bunny | 35947    | 2442.78  | 3719.00  | 16390.43 | 3377.29  | 2442.86       | 3307.08  | 2372.64       | 3307.23  | 2372.80       | 16294.39 | 10877.71      | 15350.57 | 9934.32        | 25682.41 | 26089.19  |
| suzanne        | 507      | 23.76    | 41.65    | 149.19   | 38.03    | 23.84         | 37.04    | 22.85         | 37.19    | 23.01         | 150.40   | 95.17         | 144.38   | 89.59          | 213.99   | 217.22    |
| teapot         | 3644     | 202.44   | 341.20   | 1489.62  | 309.19   | 202.52        | 302.07   | 195.40        | 302.22   | 195.55        | 1481.45  | 937.85        | 1377.37  | 834.21         | 2335.36  | 2372.23   |
| woody          | 694      | 36.33    | 63.44    | 297.24   | 56.92    | 36.42         | 55.56    | 35.06         | 55.71    | 35.22         | 295.92   | 186.12        | 272.54   | 163.17         | 466.95   | 474.21    |
| xyzrgb_dragon  | 125066   | 9283.49  | 13455.47 | 59107.69 | 12234.45 | 9283.57       | 11990.17 | 9039.29       | 11990.32 | 9039.44       | 58735.04 | 41041.19      | 55643.19 | 37949.77       | 92555.01 | 94019.69  |

**Note:** Sizes are in KiloByte (KB)

**Note 2:** Some results are below the baseline. GeoOFF and GeoPLY are for example smaller compared to the input OBJ file's, because of the missing line prefix. While vertices and faces are marked with `v` and `f` in OBJ, this prefix is implicitly given by the ordering and the number of elements in the two mentioned file formats (and their base formats `OFF` and `PLY`). The line prefix results in a comparable high overhead, when it comes to files with thousands of lines.

An interactive visualization of the size comparison can be found [here](https://fhooeaist.github.io/geofiles/).

## Getting started

To set up and use the project have a look at the detailed description [here](./documentation/Tox.md)

You can install the framework via pip:

```
pip install geofiles
```

### Importing files

The present project supports multiple reader implementations for importing (geo-referenced) geometry files (`.obj`, `.geoobj`,  `.ply`, `.geoply`, `.off`, `.geooff`, `.stl`, `.geostl`, `CityJSON`, `GeoJSON`, `KML`, `GML`, `CityGML`, `Collada (DAE)`).
Using one of these readers is the entrypoint to the framework and allows to create an in-memory geometry model using the `GeoObjectFile` class. Note that only a subset of the features of the named files are currently supported. So reading files with non-supported features may result in a loss of information (e.g. smoothing groups in `.obj`, exact property definitions of `.ply` or classes of CityObjects in `CityJSON`, etc.)

```python
reader = GeoObjReader()
path = "mygreatfile.geoobj"
with open(path) as file:
    geoObjFile: GeoObjectFile = reader.read(file)
```

Next to file imports, the framework also supports to read geometric objects from strings:

```python
geoobj = """
         crs urn:ogc:def:crs:OGC:2:84
         v 14.2842865755919 48.3028533074941 279.307006835938
         v 14.2842865755919 48.3028533074941 280.307006835938
         v 14.2842865755907 48.3028443243414 280.307006835938
         o triangle
         f 1 2 3
         """
geoObjFile: GeoObjectFile = reader.read_string(file)
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

### Determining Geographical Extent

The geographical extent of a file can be determined in two ways:
1. Only searching for the min and max coordinates of the values (not considering transformation or origin information)
2. Determining the geographical extent considering all available meta information

Depending on the use case one variant is more suitable than the other. If you are going to ignore transformation information in your application, the additional overhead of the second method is not required, otherwise if you want to know the extents considering this meta information you have to use the `ExtentCalculator` class.

```python
# 1. Classic geographical extent 
geoObjFile: GeoObjectFile = ...
geoObjFile.update_extent()

# 2. Using the ExtentCalculator
objFileWithExtents = ExtentCalculator.update_extent(geoObjFile, True, True)
```

### Exporting files

Finally, the in-memory model representations can be re-written to your hard drive using one of the writer implementations. 
Note:
1. That some file formats presuppose a specific CRS (e.g. `.kml` requires vertices in `Wgs84` representation)
2. Most file formats do not support transformation (scale, rotation, translation) meta-information. A model's vertices have to be transformed first before exported to such a file format.
3. The writers will automatically append the specific file type (unless you set `append_file_type` to `False`)
```python
writer = GeoPlyWriter()
writer.write("mygreatfile.geoply", transformed, append_file_type=False)
```

Alternatively, the writers can also be used to create file format specific output like JSON (for GeoJSON, CityJSON, ...), XML (for GML, KML, ...) or just string:

```python
writer = GeoPlyWriter()
string_output = writer.write_to_string(transformed)
```

```python
writer = GeoJsonWriter()
json_output = writer.create_json(transformed)
```

```python
writer = GmlWriter()
xml_output = writer.create_xml(transformed)
```

## FAQ

- Why yet another 3D geometry file format like `.geoobj`?
  - During our research in the context of outdoor augmented reality applications, we were looking for a possibility for exchanging geo-referenced geometry models. In this context, the other named file formats come with a too high overhead (e.g. `XML` tags or not required meta information as object types like in `CityJson`) in our opinion and are for this reason not ideal.
- You describe multiple geo-referenced file formats. Which one should I use for geo-referenced 3D models?
  - This depends on the use case. If you have to exchange the models with as little overhead as possible we recommend using the proposed `.geoply`, `.geoobj` or `.geooff` format extensions. If you require semantic expressiveness, you should prefer other formats like `CityJson` or `GML`. 
- How are vertices defined, if I use the origin-based approach of `.geoobj`, `.geoply`, `.geooff` or `.geostl`?
  - In the origin-based version, vertices are represented within a local Cartesian coordinate system with the defined origin as coordinate system origin (0, 0, 0). 
  - The local coordinate system is intended as a left handed system.
  - The local coordinate system uses the x-axis as abscissa axis (width information), y-axis as ordinate axis (length information) and z-axis as applicate axis (height information).
  - The units used in this type of coordinate system are assumed to be in **meters**. 
- How is the transformation information defined?
  - The proposed transformation information is separated into tuples (one value per axis) for translation, rotation and scale. 
  - Per default: For the translation, meter based offsets are intended to be used, the rotation is based on degrees and the scale tuple is represented using numeric factors.
  - `GeoOBJ`, `GeoOFF` and `GeoPLY` support to change the used unit for translation/rotation information

## Contributing

**First make sure to read our [general contribution guidelines](https://fhooeaist.github.io/CONTRIBUTING.html).**
   
## Licence

Copyright (c) 2021 the original author or authors.
DO NOT ALTER OR REMOVE COPYRIGHT NOTICES.

This Source Code Form is subject to the terms of the Mozilla Public
License, v. 2.0. If a copy of the MPL was not distributed with this
file, You can obtain one at https://mozilla.org/MPL/2.0/.

## Research

If you are going to use this project as part of a research paper, we would ask you to reference this project by citing
it. 

[![DOI](https://zenodo.org/badge/401244311.svg)](https://zenodo.org/badge/latestdoi/401244311)
