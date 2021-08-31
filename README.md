[TODO add badges]

![logo](./documentation/logo.png)
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

The different named file formats come with a variable amount of features according to e.g. the supported CRS, an origin for specifying a local coordinate system, multi-object support or also differ in the representation of vertices. To take up the last point, some formats use e.g. central vertex lists with referencing indices in the face definition and others re-define the vertices within every indiviudal face. Next to that there are many different other features (e.g. smoothing groups in `.obj`, `geographicalExtent` in `CityJSON` or exact property definitions in `.ply`), which vary between the file formats and lead to a diverse semantic expressiveness. 

| Format                                                                                      | Base format                                                                         | Encoding                                     | Coordinate Reference System                                                                                                                   | Multiple Objects | Vertex References | Origin Support | Transformation Information | Semantic Expressiveness |
|---------------------------------------------------------------------------------------------|-------------------------------------------------------------------------------------|----------------------------------------------|-----------------------------------------------------------------------------------------------------------------------------------------------|------------------|-------------------|----------------|----------------------------|-------------------------|
| [CityJSON](https://www.cityjson.org/)                                                       | [JSON](https://www.json.org/)                                                       | Text                                         | Any                                                                                                                                           | Yes              | Yes               | No             | No                         | ++                      |
| [GeoJSON](https://geojson.org/)                                                             | [JSON](https://www.json.org/)                                                       | Text                                         | WGS 84                                                                                                                                        | Yes              | No                | No             | No                         | +                       |
| [GeoObj](#geoobj)                                                                           | [OBJ](http://fegemo.github.io/cefet-cg/attachments/obj-spec.pdf)                    | Text *  | Any                                                                                                                                           | Yes              | Yes               | Yes            | Yes                        | ~                       |
| [GeoOFF](#geooff)                                                                           | [OFF](https://shape.cs.princeton.edu/benchmark/documentation/off_format.html)       | Text * | Any                                                                                                                                           | No               | Yes               | Yes            | No                         | -                       |
| [GeoPly](#geoply)                                                                           | [Ply](http://graphics.stanford.edu/data/3Dscanrep/)                                 | Text * | Any                                                                                                                                           | No               | Yes               | Yes            | Yes                        | ~                       |
| [GeoStl](#geostl)                                                                           | [Stl](https://www.fabbers.com/tech/STL_Format)                                      | Text * | Any                                                                                                                                           | No               | No                | Yes            | No                         | --                      |
| [GML](https://www.ogc.org/standards/gml)                                                    | [XML](https://www.w3.org/XML/)                                                      | Text                                         | Any                                                                                                                                           | Yes              | No                | No             | No                         | ++                      |
| [KML](https://developers.google.com/kml/documentation/kmlreference)                         | [XML](https://www.w3.org/XML/)                                                      | Text or compressed ([KMZ](https://www.google.com/earth/outreach/learn/packaging-content-in-a-kmz-file/))                     | WGS 84                                                                                                                                        | Yes              | No                | No             | No                         | ++                      |
| [GeoVRML](http://www.ai.sri.com/~reddy/geovrml/archive/geovrml1_0.pdf)                      | [VRML](http://www.martinreddy.net/gfx/3d/VRML.spec)                                 | Text or Binary                               | WGS84 / EPSG4326 / UTM                                                                                                                        | Yes              | Yes               | Yes            | Yes                        | +                       |
| [X3D](https://www.web3d.org/documents/specifications/19775-1/V3.3/Part01/Architecture.html) | [XML](https://www.w3.org/XML/), [VRML](http://www.martinreddy.net/gfx/3d/VRML.spec) | Text or Binary                               | [Multiple supported CRS](https://www.web3d.org/documents/specifications/19775-1/V3.3/Part01/components/geodata.html#t-Supportedspatialframes) | Yes              | Yes               | Yes            | Yes    | ++                      |
* Currently, only text support, but the base format would support binary, so a binary extension would be possible.


### Size comparison

**Note:** 
- The following file comparison uses the minimal required sub-set of the specific file formats to represent geo-referenced 3D models. Additional features (e.g. GeographicalExtent in `CityJSON`) are not considered as far as possible.
- X3D is currently not explicitly supported by the present framework since it can be encoded using XML or VRML. Next to that it is the successor of [VRML](http://www.martinreddy.net/gfx/3d/VRML.spec) and supports many features of [GeoVRML](http://www.ai.sri.com/~reddy/geovrml/archive/geovrml1_0.pdf) within the [geospatial extension](https://www.web3d.org/documents/specifications/19775-1/V3.3/Part01/components/geodata.html) with only minor differences. For this reason it would result in comparable size when using the VRML encoding.
- You can find the source of the used obj files [here](https://github.com/alecjacobson/common-3d-test-models)
- Sizes are in KiloByte (KB)
- When a file format supports an origin-based representation you will find two comma separated sized: At first, the non-origin based one and secondly the origin based one.


| File               | cityjson | geojson  | geoobj               | geooff              | geoply              | geostl               | geovrml              | gml      | kml       |
|--------------------|----------|----------|----------------------|---------------------|---------------------|----------------------|----------------------|----------|-----------|
| alligator.obj      | 308.53   | 1402.25  | 287.66 , 214.05     | 272.42 , 198.81    | 272.57 , 198.97    | 1396.25 , 984.62    | 1298.15 , 886.96    | 2202.64  | 2237.52   |
| armadillo.obj      | 5279.43  | 23622.39 | 4937.50 , 4819.14   | 4693.41 , 4575.04  | 4693.56 , 4575.20  | 23476.92 , 22766.42 | 22142.54 , 21432.48 | 36998.27 | 37583.91  |
| beast.obj          | 2850.39  | 9550.49  | 4192.73 , 3449.05   | 2566.04 , 1822.35  | 2566.19 , 1822.51  | 9686.46 , 6709.18   | 9516.06 , 6539.20   | 13723.15 | 13944.12  |
| beetle-alt.obj     | 2037.85  | 9120.80  | 1904.97 , 1443.79   | 1808.95 , 1347.77  | 1809.10 , 1347.93  | 9067.75 , 6380.97   | 8517.67 , 5831.33   | 14292.74 | 14519.08  |
| beetle.obj         | 105.10   | 485.01   | 160.34 , 130.52     | 92.38 , 62.56      | 92.53 , 62.72      | 599.52 , 439.33     | 444.46 , 284.70     | 759.87   | 771.74    |
| cheburashka.obj    | 667.26   | 3148.23  | 621.48 , 452.08     | 588.91 , 419.51    | 589.06 , 419.67    | 3129.51 , 2114.09   | 2914.98 , 1899.99   | 4932.36  | 5010.33   |
| cow.obj            | 286.76   | 1369.35  | 266.71 , 192.87     | 252.53 , 178.68    | 252.68 , 178.84    | 1361.40 , 918.19    | 1264.59 , 821.81    | 2146.05  | 2179.90   |
| fandisk.obj        | 646.64   | 3047.66  | 602.18 , 408.68     | 570.56 , 377.06    | 570.71 , 377.22    | 3031.65 , 1870.74   | 2823.32 , 1662.84   | 4779.88  | 4855.58   |
| happy.obj          | 5200.30  | 23271.05 | 4863.13 , 4828.63   | 4622.54 , 4588.04  | 4622.69 , 4588.20  | 23134.59 , 22926.30 | 21818.18 , 21610.32 | 36462.98 | 37040.56  |
| homer.obj          | 600.33   | 2832.50  | 559.11 , 396.36     | 529.80 , 367.05    | 529.95 , 367.21    | 2815.80 , 1839.43   | 2622.71 , 1646.77   | 4438.16  | 4508.31   |
| horse.obj          | 5161.59  | 23251.47 | 4829.96 , 4989.55   | 4593.21 , 4752.80  | 4593.36 , 4752.96  | 23025.46 , 23982.47 | 21729.74 , 22687.18 | 36224.65 | 36792.65  |
| igea.obj           | 14490.75 | 63413.22 | 13572.18 , 10155.50 | 12916.19 , 9499.51 | 12916.34 , 9499.67 | 63040.76 , 42540.49 | 59765.41 , 39265.58 | 99360.66 | 100934.83 |
| lucy.obj           | 5310.72  | 23867.91 | 4968.82 , 4847.85   | 4724.74 , 4603.76  | 4724.89 , 4603.92  | 23660.91 , 22935.55 | 22327.21 , 21602.28 | 37242.99 | 37828.60  |
| max-planck.obj     | 5296.99  | 23729.97 | 4954.95 , 4759.34   | 4710.58 , 4514.96  | 4710.73 , 4515.12  | 23558.65 , 22389.80 | 22223.06 , 21054.65 | 37107.86 | 37693.59  |
| nefertiti.obj      | 5288.27  | 23695.48 | 4946.47 , 3867.76   | 4702.47 , 3623.75  | 4702.62 , 3623.91  | 23529.73 , 17057.59 | 22196.35 , 15724.64 | 37066.29 | 37651.70  |
| ogre.obj           | 6569.39  | 29260.92 | 6145.14 , 3999.74   | 5841.82 , 3696.41  | 5841.97 , 3696.57  | 29090.92 , 16258.20 | 27450.40 , 14618.11 | 45852.03 | 46578.48  |
| rocker-arm.obj     | 1008.57  | 4742.64  | 939.70 , 709.05     | 890.65 , 660.00    | 890.80 , 660.15    | 4714.26 , 3330.66   | 4394.58 , 3011.40   | 7430.39  | 7547.93   |
| spot.obj           | 289.43   | 1380.09  | 420.83 , 346.42     | 254.89 , 180.48    | 255.04 , 180.63    | 1372.51 , 926.02    | 1275.06 , 829.00    | 2163.75  | 2197.91   |
| stanford-bunny.obj | 3719.00  | 16390.43 | 3480.22 , 2557.72   | 3307.08 , 2384.58  | 3307.23 , 2384.73  | 16294.39 , 10946.77 | 15350.55 , 10003.37 | 25682.41 | 26089.19  |
| suzanne.obj        | 41.65    | 149.19   | 64.68 , 50.85       | 37.04 , 23.20      | 37.19 , 23.36      | 175.03 , 121.17     | 144.37 , 90.94      | 213.99   | 217.22    |
| teapot.obj         | 341.20   | 1489.62  | 318.92 , 225.23     | 302.07 , 208.37    | 302.22 , 208.53    | 1481.45 , 993.01    | 1377.36 , 889.35    | 2335.36  | 2372.23   |
| woody.obj          | 63.44    | 297.24   | 58.83 , 43.03       | 55.56 , 39.76      | 55.71 , 39.91      | 295.92 , 209.22     | 272.52 , 186.26     | 466.95   | 474.21    |
| xyzrgb_dragon.obj  | 13455.47 | 59107.69 | 12600.72 , 9691.43  | 11990.17 , 9080.87 | 11990.32 , 9081.03 | 58735.04 , 41288.32 | 55643.17 , 38196.89 | 92555.01 | 94019.69  |

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
2. That some file formats presuppose a specific CRS (e.g. `.kml` requires vertices in `Wgs84` representation)
3. Most file formats do not support transformation (scale, rotation, translation) meta-information. A model's vertices have to be transformed first before exported to such a file format.
4. The writers will automatically append the specific file type (unless you set `append_file_type` to `False`)
```python
writer = GeoPlyWriter()
writer.write("mygreatfile.geoply", transformed, append_file_type=False)
```

## FAQ

- Why yet another 3D geometry file format like `.geoobj`?
  - During our research in the context of outdoor augmented reality applications, we were looking for a possibility for exchanging geo-referenced geometry models. In this context, the other named file formats come with a too high overhead (e.g. `XML` tags or not required meta information as object types like in `CityJson`) in our opinion and are for this reason not ideal.
- You describe multiple geo-referenced file formats. Which one should I use for geo-referenced 3D models?
  - This depends on the use case. If you have to exchange the models with as little overhead as possible we recommend using the proposed `.geoply`, `.geoobj` or `.geooff` format extensions. If you require semantic expressiveness, you should prefer other formats like `CityJson` or `GML`. 

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

[TODO zenodo doi]