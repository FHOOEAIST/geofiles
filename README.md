[![GitHub release](https://img.shields.io/github/v/release/fhooeaist/geofiles.svg)](https://github.com/FHOOEAIST/geofiles/releases)
[![License: MPL 2.0](https://img.shields.io/badge/License-MPL%202.0-brightgreen.svg)](https://opensource.org/licenses/MPL-2.0)
[![PyPI version](https://badge.fury.io/py/geofiles.svg)](https://badge.fury.io/py/geofiles)
[![DOI](https://zenodo.org/badge/401244311.svg)](https://zenodo.org/badge/latestdoi/401244311)

![logo](https://github.com/FHOOEAIST/geofiles/raw/main/documentation/logo.png)

# Geo-referenced Geometry File Formats

Classic geometry file formats as `.obj`, `.off`, `.ply`, `.stl` or `.dae` do not support the utilization of coordinate
systems besides from a local system, that can not be defined more precisely.
This feature is a major requirement for global applications, exchanging geo-referenced models e.g. in the context of
outdoor augmented reality applications.

For this reason, the present project evaluates different possibilities of geo-referenced geometry files.

Next to wide-spread standards as `GeoVRML`, `X3D`, `CityJSON`, `GeoJSON`, `GML` or `KML`, we introduce four
geo-referenced extensions called `.geoobj`, `.geooff`, `.geoply` and `.geostl`.
While, the named standard formats allow defining objects with multiple additional features, they also come with an
overhead according to the file size and an increased structural complexity with disadvantages to the read performance.
This overhead has to be minimized in many use cases and for this reason, some file formats are more suitable than
others. For completeness: the overhead can be further reduced using binary representations (like binary `obj` or `stl`)
instead of textual ones, but since not all named formats support a binary mode, this is ignored in favor of
human-readability within this project and comparison.

## Geo-referenced Extensions

In this chapter you can find multiple extensions of classic geometry file formats.
All of these extensions support two major features:

1. Defining the coordinate reference system (CRS) of the used vertices' coordinates
2. Defining an optional origin, which represents an absolute geo-referenced location and an implicit local Cartesian
   coordinate frame for the models with a metric unit.

### Additional features

Some proposed file formats support additional features such as:

- Geographical extent
- Transformation information (local per object or global for all vertices)
    - Scaling factor
    - Translation
    - Rotation
- Arbitrary meta information, with three fixed keys:
    - Global per file such as:
        - Translation unit (`tu`): any unit can be used. The present project only supports transformations with metres (
          m)
        - Rotation unit (`ru`: any unit can be used. The present project only supports transformations with degrees (
          deg)
    - Local per object
        - Type (`type`): Type of the geo-object such as Building, Car, etc.

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

Next to the geo-referencing features, the `.geoobj` extension also supports exchanging `scale`, `rotation`, as well
as `translation` information using the following line prefixes:

1. `sc` for adding scale information (`s` is already defined in `.obj` for smoothing groups)
2. `t` for translation information
3. `r` for rotation angular information

Example:

```
sc 1.5 2 5
t 10 -5 4
r 90 45 10
```

Note that: if either a scaling, a translation or a rotation information is stated after an object definition with the
prefix `o`, the transformation is not interpreted globally, but locally for the specific object.

Next to that it also supports the optional geographical extent meta information, containing the minimal (first three
values) and maximal (remaining three values) coordinate value expressions using the line prefix `e`.
This information can be useful for filtering geo-referenced files without any need to iterate all vertices.

```
e -0.5 -0.5 -0.5 0.5 0.5 0.5
```

GeoObj also supports meta information on file or on object level:

4. `m` for arbitrary object based meta information. Every meta entry contains a key as first element followed by one or
   more values. Reserved keys:
    - `type` for object type information
5. `mf` for arbitrary file based meta information. Every meta entry contains a key as first element followed by one or
   more values. Reserved keys:
    - `tu` for defining the translation unit (default is metres `m`)
    - `ru` for defining the rotation unit (default is degrees `deg`)

```
mf tu inch
mf ru rad
m axis_ordering x y z
```

And finally GeoObj contains an extension to map object hierarchy:

6. `h` can be used before an object definition to change the hierarchy level. Like this an object tree can be created
    - Uses the absolute index of the used hierarchy level (e.g. 2 represents a grandchildren-object root->children->
      grandchildren)
    - Use 0 for root level
    - Parents are set to the last object of the specified level

```
crs urn:ogc:def:crs:OGC:2:84
or 14.2842798233032 48.30284881591775 279.807006835938
v -0.5009357136907019 -0.4994462475020125 0.5
v -0.5009357136907019 -0.4994462475020125 -0.5
v -0.5009356247086404 0.4994462914230726 -0.5
g cubes
h 1
o child1
f 1 2 3
o child2
f 1 2 3
h 2
o child3
f 1 2 3
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

GeoOFF supports alternative headers, using different postfix values. The pattern of the header is based on the `OFF`
header definition and is defined like `[ST][C][N][4][n]GeoOFF[o][e][s][t][r][f*][m*]`.
Like this GeoOFF is able to support:

- An absolute origin using the `o` header postfix symbol
- Extent information using the `e` header postfix symbol
- Global scaling information using the `s` header postfix symbol
- Global translation information using the `t` header postfix symbol
- Global rotation information using the `r` header postfix symbol
- Arbitrary meta information using the `m` header postfix symbol for object information or `f` for file information (
  which can occur multiple times)
    - Defined as blank-separated list of key/value pairs like `key value`
    - Values may be again a list of values that are separated with a whitespace like `key value1 value2 value3`
    - Reserved keys for file meta information (`f`):
        - `tu` for defining the translation unit (default is metres `m`)
        - `ru` for defining the rotation unit (default is degrees `deg`)
    - Reserved keys for object meta information (`m`):
        - `type` for object type information

Example:

```
GeoOFFostrffm
urn:ogc:def:crs:OGC:2:84
14.2842798233032 48.30284881591775 279.807006835938
2 2 2
10 50 100
90 0 0
tu inch 
axis_ordering x y z
type genericobject 
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

Next to the geo-referencing features, the `.geply` extension also supports exchanging global `scale`, `rotation`, as
well as `translation` information using the following line prefixes:

1. `scale` for adding scale information
2. `translate` for translation information
3. `rotate` for rotation angular information
4. `meta` for arbitrary object based meta information. Every meta entry contains a key as first element followed by one
   or more values. Reserved keys:
    - `type` for object type information
5. `metaf` for arbitrary file based meta information. Every meta entry contains a key as first element followed by one
   or more values. Reserved keys:
    - `tu` for defining the translation unit (default is metres `m`)
    - `ru` for defining the rotation unit (default is degrees `deg`)

Example:

```
geoply
...
scale 1.5 2 5
translate 10 -5 4
rotate 90 45 10
metaf tu m
metaf ru deg
meta type genericobject
metaf axis_ordering x y z
...
end_header
```

Next to that it also supports the optional geographical extent meta information, containing the minimal (first three
values) and maximal (remaining three values) coordinate value expressions using the `extent` header.
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
This tuple consists of the crs at the first position, followed by the optional origin coordinates and finally the
optional stl name.

``` 
geosolid urn:ogc:def:crs:OGC:2:84 48.3028533074941 14.2842865755919 279.307006835938 fileName
```

## File format comparison

The different named file formats come with a variable amount of features according to e.g. the supported CRS, an origin
for specifying a local coordinate system, the meta information of the minimal and maximal coordinates (geographical
extent), multi-object support or also differ in the representation of vertices. To take up the last point, some formats
use e.g. central vertex lists with referencing indices in the face definition and others re-define the vertices within
every indiviudal face. Next to that there are many different other features (e.g. smoothing groups in `.obj`
, `geographicalExtent` in `CityJSON` or exact property definitions in `.ply`), which vary between the file formats and
lead to a diverse semantic expressiveness.

|          | File        |                      | Geo-Reference                                   |                 |                     | Geometry   |                   |                  |                   | Appearance                 |            |               | Scene         |                  |                            | Animation  |
|----------|-------------|----------------------|-------------------------------------------------|-----------------|---------------------|------------|-------------------|------------------|-------------------|----------------------------|------------|---------------|---------------|------------------|----------------------------|------------|
|          | Base Format | Encoding             | CRS                                             | Origin  Support | Geographical Extent | Faceted    | Multiple  Objects | Object Hierarchy | Vertex References | Color                      | Material   | Image texture | Light sources | Viewport/Cameras | Transformation Information |            |
| [CityJSON](https://www.cityjson.org/) | [JSON](https://www.json.org/)        | Text                 | Any                                             | †                | ✓          | ✓ | ✓        |                  | Global            | ✓                 | ✓ | ✓    |               |                  | [Global Translation + Scaling](https://www.cityjson.org/specs/1.0.3/#transform-object)      |            |
| [GeoJSON](https://geojson.org/)  | [JSON](https://www.json.org/)         | Text                 | WGS84                                           |                 | Via bounding box per object                    | ✓ | ✓        |                  |                   | [Via GeoJSON  CSS extension](https://wiki.openstreetmap.org/wiki/Geojson_CSS)  |            |               |               |                  |                            |            |
| [GeoOBJ](https://github.com/FHOOEAIST/geofiles#geoobj)   | [OBJ](http://fegemo.github.io/cefet-cg/attachments/obj-spec.pdf)          | Text*                | Any                                             | ✓      | ✓          | ✓ | ✓        | ✓       | Global            | ✓                 | ✓ | ✓    |               |                  | ✓                 |            |
| [GeOFF](https://github.com/FHOOEAIST/geofiles#geooff)    | [OFF](https://shape.cs.princeton.edu/benchmark/documentation/off_format.html)          | Text*                | Any                                             | ✓      | ✓          | ✓ |                   |                  | Global            | ✓                 |            |               |               |                  | ✓                 |            |
| [GeoPLY](https://github.com/FHOOEAIST/geofiles#geoply)   | [PLY](http://graphics.stanford.edu/data/3Dscanrep/)          | Text*                | Any                                             | ✓      | ✓          | ✓ |                   |                  | Global            | ✓                 | ✓ | ✓    |               |                  | ✓                 |            |
| [GeoSTL](https://github.com/FHOOEAIST/geofiles#geostl)   | [STL](https://www.fabbers.com/tech/STL_Format)          | Text*                | Any                                             | ✓      |                     | ✓ |                   |                  |                   |                            |            |               |               |                  |                            |            |
| [GML](https://www.ogc.org/standards/gml)      | [XML](https://www.w3.org/XML/)          | Text                 | Any                                             |                 |                     | ✓ | ✓        | ✓       |                   | ✓                 |            |               |               |                  |                            |            |
| [CityGML](https://www.ogc.org/standards/citygml)  | [GML](https://www.ogc.org/standards/gml)          | Text                 | Any                                             |                 |                     | ✓ | ✓        | ✓       |                   | ✓                 | ✓ | ✓    |               |                  |                            |            |
| [KML](https://developers.google.com/kml/documentation/kmlreference)      | [XML](https://www.w3.org/XML/)          | Text or zipped ([KMZ]() ) | WGS84                                           |                 |                     | ✓ | ✓        |                  |                   | ✓                 |            |               |               |                  |                            |            |
| [GeoVRML](http://www.ai.sri.com/~reddy/geovrml/archive/geovrml1_0.pdf)  | [VRML](http://www.martinreddy.net/gfx/3d/VRML.spec)         | Text or  Binary      | WGS84 / EPSG4326 / UTM                              | ✓      | ✓          | ✓ | ✓        | ✓       | Local             | ✓                 | ✓ | ✓    | ✓    | ✓       | ✓                 | ✓ |
| [X3D](https://www.web3d.org/documents/specifications/19775-1/V3.3/Part01/Architecture.html)      | [XML](https://www.w3.org/XML/), [VRML](http://www.martinreddy.net/gfx/3d/VRML.spec) or [JSON](https://www.json.org/)  | Text or Binary       | [Multiple supported](https://www.web3d.org/documents/specifications/19775-1/V3.3/Part01/components/geodata.html#t-Supportedspatialframes)                              | †                | ✓          | ✓ | ✓        | ✓       | Local             | ✓                 | ✓ | ✓    | ✓    | ✓       | ✓                 | ✓ |
| [Collada](https://www.khronos.org/collada/)  | [XML](https://www.w3.org/XML/)          | Text                 | None (but, due to XML structure easily addable) |                 |                     | ✓ | ✓        | ✓       | Local             | ✓                 | ✓ | ✓    | ✓    | ✓       | ✓                 | ✓ |

† Some file formats do not explicitly support an origin representation, but this feature can be approximated using translations.


\* Currently, only text support, but the base format would support binary, so a binary extension would be possible.

### Size comparison

The following file comparison uses the minimal required sub-set of the specific file formats to represent geo-referenced
3D models. Additional features (e.g. GeographicalExtent in `CityJSON`) are not considered as far as possible, to avoid a
negative bias of the comparison. Next to that also the used reader does not support all features of the input files (
e.g. `.mtb` material information) and may use different line-ending symbols (Windows vs Linux). This would lead to the
situation that in some cases the input file size is greater than the geo-referenced version. For this reason we have
decided to do a normalization first by reading the input files with our custom reader and exporting the normalized
representation using our custom obj writer. The exported and normalized files are used as basis of comparison.

You can find most of the used obj files [here](https://github.com/alecjacobson/common-3d-test-models). The only
exceptions are the Amsterdam (find it [here](https://3dbag.nl/)) and Berlin (find
it [here](https://www.businesslocationcenter.de/en/economic-atlas/download-portal/)) city model files. Also note that,
X3D is currently not explicitly supported by the present framework since it can be encoded using XML or VRML. Next to
that it is the successor of [VRML](http://www.martinreddy.net/gfx/3d/VRML.spec) and supports many features
of [GeoVRML](http://www.ai.sri.com/~reddy/geovrml/archive/geovrml1_0.pdf) within
the [geospatial extension](https://www.web3d.org/documents/specifications/19775-1/V3.3/Part01/components/geodata.html)
with only minor differences. For this reason it would result in a comparable size when using the VRML encoding and is
left out in the following comparison.

| File                 | Vertices | Original | CityJSON | CityJSON (Origin) | GeoJSON   | GeoOBJ   | GeoOBJ (Origin) | GeoOFF   | GeoOFF (Origin) | GeoPLY   | GeoPLY (Origin) | GeoSTL    | GeoSTL (Origin) | GeoVRML  | GeoVRML (Origin) | GML       | CityGML   | KML       | Collada  |
|----------------------|----------|----------|----------|-------------------|-----------|----------|-----------------|----------|-----------------|----------|-----------------|-----------|-----------------|----------|------------------|-----------|-----------|-----------|----------|
| alligator            | 3208     | 184.07   | 308.59   | 214.05            | 1402.25   | 278.69   | 184.16          | 272.42   | 177.89          | 272.57   | 178.04          | 1396.25   | 877.53          | 319.46   | 225.36           | 2202.64   | 2204.78   | 2237.52   | 252.84   |
| amsterdam (lod12)    | 81666    | 5532.22  | 8470.13  | 6299.01           | 36669.92  | 7703.42  | 5532.30         | 7543.88  | 5372.76         | 7544.03  | 5372.91         | 36455.35  | 24063.04        | 8732.87  | 6562.18          | 57459.33  | 57461.47  | 58369.68  | 7010.23  |
| amsterdam (lod13)    | 87528    | 5941.45  | 9095.58  | 6765.49           | 39431.34  | 8271.61  | 5941.53         | 8100.62  | 5770.54         | 8100.78  | 5770.70         | 39202.33  | 25855.52        | 9375.49  | 7045.83          | 61789.56  | 61791.70  | 62768.62  | 7526.90  |
| amsterdam (lod22)    | 111874   | 7713.57  | 11764.69 | 8775.59           | 50944.43  | 10702.75 | 7713.66         | 10484.21 | 7495.11         | 10484.36 | 7495.27         | 50646.45  | 33341.37        | 12115.75 | 9127.09          | 79824.73  | 79826.87  | 81089.43  | 9743.88  |
| armadillo            | 49990    | 3608.54  | 5279.48  | 4097.05           | 23622.39  | 4791.05  | 3608.63         | 4693.41  | 3510.98         | 4693.56  | 3511.14         | 23476.92  | 16381.74        | 5426.15  | 4244.15          | 36998.27  | 37000.41  | 37583.91  | 4352.77  |
| beast                | 32311    | 1873.35  | 2850.45  | 2094.72           | 9550.49   | 2629.15  | 1873.44         | 2566.04  | 1810.33         | 2566.19  | 1810.48         | 9686.46   | 6660.98         | 3008.32  | 2253.03          | 13723.15  | 13725.28  | 13944.12  | 2440.75  |
| beetle-alt           | 19887    | 1364.18  | 2037.91  | 1554.36           | 9120.80   | 1847.80  | 1364.26         | 1808.95  | 1325.41         | 1809.10  | 1325.57         | 9067.75   | 6249.00         | 2099.64  | 1616.53          | 14292.74  | 14294.88  | 14519.08  | 1677.35  |
| beetle               | 1148     | 64.34    | 105.13   | 74.90             | 485.01    | 94.64    | 64.42           | 92.38    | 62.16           | 92.53    | 62.32           | 482.03    | 319.74          | 109.43   | 79.64            | 759.87    | 762.01    | 771.75    | 86.36    |
| berlin (112-100-1-1) | 487859   | 48961.10 | 55113.58 | 53715.41          | 236389.97 | 50359.34 | 48961.18        | 49406.48 | 48008.32        | 49406.63 | 48008.47        | 233359.29 | 224993.29       | 56550.75 | 55153.02         | 366578.82 | 366580.96 | 372280.36 | 46080.28 |
| berlin (112-103-1-1) | 306495   | 30495.91 | 34371.91 | 33481.48          | 148411.10 | 31386.41 | 30495.99        | 30787.77 | 29897.35        | 30787.92 | 29897.50        | 146510.83 | 141185.76       | 35275.95 | 34385.95         | 230153.20 | 230155.34 | 233732.98 | 28699.57 |
| bimba                | 112455   | 8132.82  | 12024.37 | 9231.32           | 53081.70  | 10925.94 | 8132.90         | 10706.28 | 7913.25         | 10706.43 | 7913.40         | 52769.77  | 36012.02        | 12354.04 | 9561.43          | 83171.85  | 83173.99  | 84489.50  | 9938.64  |
| cheburashka          | 6669     | 420.93   | 667.32   | 486.38            | 3148.23   | 601.94   | 421.01          | 588.91   | 407.98          | 589.06   | 408.14          | 3129.51   | 2044.29         | 687.07   | 506.57           | 4932.36   | 4934.50   | 5010.33   | 544.41   |
| cow                  | 2903     | 182.93   | 286.82   | 211.61            | 1369.35   | 258.21   | 183.01          | 252.53   | 177.33          | 252.68   | 177.49          | 1361.40   | 909.95          | 295.53   | 220.75           | 2146.05   | 2148.19   | 2179.90   | 233.77   |
| fandisk              | 6475     | 391.15   | 646.70   | 454.71            | 3047.66   | 583.21   | 391.23          | 570.56   | 378.58          | 570.71   | 378.73          | 3031.65   | 1879.89         | 665.88   | 474.32           | 4779.88   | 4782.02   | 4855.58   | 527.38   |
| happy                | 49251    | 3443.42  | 5200.36  | 3925.11           | 23271.05  | 4718.75  | 3443.51         | 4622.54  | 3347.30         | 4622.69  | 3347.45         | 23134.59  | 15475.17        | 5344.56  | 4069.74          | 36462.98  | 36465.11  | 37040.56  | 4286.65  |
| homer                | 6002     | 378.70   | 600.39   | 437.64            | 2832.50   | 541.53   | 378.78          | 529.80   | 367.06          | 529.95   | 367.21          | 2815.80   | 1839.43         | 618.19   | 455.87           | 4438.16   | 4440.30   | 4508.31   | 489.86   |
| horse                | 48485    | 4382.41  | 5150.79  | 4856.22           | 23164.35  | 4677.06  | 4382.50         | 4582.36  | 4287.79         | 4582.51  | 4287.94         | 22960.07  | 21192.62        | 5293.05  | 4998.91          | 36137.53  | 36139.67  | 36705.53  | 4252.00  |
| igea                 | 134345   | 9716.50  | 14490.80 | 11028.78          | 63413.22  | 13178.60 | 9716.58         | 12916.19 | 9454.18         | 12916.34 | 9454.33         | 63040.76  | 42268.45        | 14884.60 | 11423.02         | 99360.66  | 99362.80  | 100934.83 | 11998.91 |
| lucy                 | 49987    | 3728.41  | 5310.78  | 4216.88           | 23867.91  | 4822.38  | 3728.49         | 4724.74  | 3630.85         | 4724.89  | 3631.01         | 23660.91  | 17097.44        | 5457.44  | 4363.98          | 37242.99  | 37245.13  | 37828.60  | 4384.12  |
| max-planck           | 50077    | 3628.48  | 5297.05  | 4117.21           | 23729.97  | 4808.40  | 3628.57         | 4710.58  | 3530.75         | 4710.73  | 3530.91         | 23558.65  | 16499.04        | 5444.44  | 4265.04          | 37107.86  | 37110.00  | 37693.59  | 4369.81  |
| nefertiti            | 49971    | 3621.60  | 5288.33  | 4109.92           | 23695.48  | 4800.08  | 3621.68         | 4702.47  | 3524.08         | 4702.62  | 3524.23         | 23529.73  | 16459.26        | 5434.94  | 4256.97          | 37066.29  | 37068.42  | 37651.70  | 4361.96  |
| ogre                 | 62194    | 3820.09  | 6569.44  | 4426.30           | 29260.92  | 5963.30  | 3820.17         | 5841.82  | 3698.69         | 5841.97  | 3698.85         | 29090.92  | 16271.91        | 6752.97  | 4610.26          | 45852.03  | 45854.17  | 46578.48  | 5418.86  |
| rocker-arm           | 10044    | 666.93   | 1008.63  | 765.36            | 4742.64   | 910.28   | 667.02          | 890.65   | 647.39          | 890.80   | 647.55          | 4714.26   | 3254.51         | 1038.25  | 795.42           | 7430.39   | 7432.53   | 7547.93   | 823.07   |
| spot                 | 2930     | 186.33   | 289.49   | 215.27            | 1380.09   | 260.62   | 186.41          | 254.89   | 180.68          | 255.04   | 180.84          | 1372.51   | 927.27          | 298.28   | 224.50           | 2163.75   | 2165.89   | 2197.91   | 235.95   |
| stanford-bunny       | 35947    | 2442.78  | 3719.06  | 2784.62           | 16390.43  | 3377.29  | 2442.86         | 3307.08  | 2372.64         | 3307.23  | 2372.80         | 16294.39  | 10877.71        | 3757.36  | 2852.21          | 25682.41  | 25684.54  | 26089.19  | 3069.58  |
| suzanne              | 507      | 23.76    | 41.71    | 27.51             | 149.19    | 38.03    | 23.84           | 37.04    | 22.85           | 37.19    | 23.01           | 150.40    | 95.17           | 44.44    | 30.68            | 213.99    | 216.13    | 217.22    | 36.16    |
| teapot               | 3644     | 202.44   | 341.26   | 234.58            | 1489.62   | 309.19   | 202.52          | 302.07   | 195.40          | 302.22   | 195.55          | 1481.45   | 937.85          | 354.97   | 248.73           | 2335.36   | 2337.50   | 2372.23   | 281.07   |
| woody                | 694      | 36.33    | 63.50    | 42.99             | 297.24    | 56.92    | 36.42           | 55.56    | 35.06           | 55.71    | 35.22           | 295.92    | 186.12          | 66.09    | 46.01            | 466.95    | 469.08    | 474.21    | 52.25    |
| xyzrgb_dragon        | 125066   | 9280.75  | 13452.33 | 10501.45          | 59080.21  | 12231.71 | 9280.83         | 11987.42 | 9036.55         | 11987.57 | 9036.70         | 58707.68  | 41024.43        | 13811.48 | 10864.75         | 92511.88  | 92514.01  | 93975.87  | 11134.29 |
| Average              | 66883    | 5531.91  | 7236.09  | 6177.45           | 31497.91  | 6590.63  | 5532.00         | 6459.99  | 5401.35         | 6460.14  | 5401.51         | 31220.14  | 25006.22        | 7435.08  | 6378.00          | 49078.82  | 49080.95  | 49849.96  | 6010.68  |

**Note:** Sizes are in KiloByte (KB)

**Note 2:** Some results are below the baseline. GeoOFF and GeoPLY are for example smaller compared to the input OBJ
file's, because of the missing line prefix. While vertices and faces are marked with `v` and `f` in OBJ, this prefix is
implicitly given by the ordering and the number of elements in the two mentioned file formats (and their base
formats `OFF` and `PLY`). The line prefix results in a comparable high overhead, when it comes to files with thousands
of lines.

An interactive visualization of the size comparison can be found [here](https://fhooeaist.github.io/geofiles/).

## Getting started

To set up and use the project have a look at the detailed description [here](./documentation/Tox.md)

You can install the framework via pip:

```
pip install geofiles
```

### Importing files

The present project supports multiple reader implementations for importing (geo-referenced) geometry files (`.obj`
, `.geoobj`,  `.ply`, `.geoply`, `.off`, `.geooff`, `.stl`, `.geostl`, `CityJSON`, `GeoJSON`, `KML`, `GML`, `CityGML`
, `Collada (.dae)`).
Using one of these readers is the entrypoint to the framework and allows to create an in-memory geometry model using
the `GeoObjectFile` class. Note that only a subset of the features of the named files are currently supported. So
reading files with non-supported features may result in a loss of information (e.g. smoothing groups in `.obj`, exact
property definitions of `.ply` or classes of CityObjects in `CityJSON`, etc.)

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

The present framework supports different conversion methodologies as converting from one to another coordinate reference
system.
Next to the CRS-conversion the framework also supports to transform between origin and non-origin based representations,
as well as between geo-referenced and local representations.
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

Depending on the use case one variant is more suitable than the other. If you are going to ignore transformation
information in your application, the additional overhead of the second method is not required, otherwise if you want to
know the extents considering this meta information you have to use the `ExtentCalculator` class.

```python
# 1. Classic geographical extent 
geoObjFile: GeoObjectFile = ...
geoObjFile.update_extent()

# 2. Using the ExtentCalculator
objFileWithExtents = ExtentCalculator.update_extent(geoObjFile, True, True)
```

### Exporting files

Finally, the in-memory model representations can be re-written to your hard drive using one of the writer
implementations.
Note:

1. That some file formats presuppose a specific CRS (e.g. `.kml` requires vertices in `Wgs84` representation)
2. Most file formats do not support transformation (scale, rotation, translation) meta-information. A model's vertices
   have to be transformed first before exported to such a file format.
3. The writers will automatically append the specific file type (unless you set `append_file_type` to `False`)

```python
writer = GeoPlyWriter()
writer.write("mygreatfile.geoply", transformed, append_file_type=False)
```

Alternatively, the writers can also be used to create file format specific output like JSON (for GeoJSON, CityJSON, ...)
, XML (for GML, KML, ...) or just string:

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
    - During our research in the context of outdoor augmented reality applications, we were looking for a possibility
      for exchanging geo-referenced geometry models. In this context, the other named file formats come with a too high
      overhead (e.g. `XML` tags or not required meta information as object types like in `CityJson`) in our opinion and
      are for this reason not ideal.
- You describe multiple geo-referenced file formats. Which one should I use for geo-referenced 3D models?
    - This depends on the use case. If you have to exchange the models with as little overhead as possible we recommend
      using the proposed `.geoply`, `.geoobj` or `.geooff` format extensions. If you require semantic expressiveness,
      you should prefer other formats like `CityJson` or `GML`.
- How are vertices defined, if I use the origin-based approach of `.geoobj`, `.geoply`, `.geooff` or `.geostl`?
    - In the origin-based version, vertices are represented within a local Cartesian coordinate system with the defined
      origin as coordinate system origin (0, 0, 0).
    - The local coordinate system is intended as a left handed system.
    - The local coordinate system uses the x-axis as abscissa axis (width information), y-axis as ordinate axis (length
      information) and z-axis as applicate axis (height information).
    - The units used in this type of coordinate system are assumed to be in **meters**.
- How is the transformation information defined?
    - The proposed transformation information is separated into tuples (one value per axis) for translation, rotation
      and scale.
    - Per default: For the translation, meter based offsets are intended to be used, the rotation is based on degrees
      and the scale tuple is represented using numeric factors.
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

```bibtex
@article{Praschl2023,
  title = {Extending 3D geometric file formats for geospatial applications},
  volume = {16},
  ISSN = {1866-928X},
  url = {http://dx.doi.org/10.1007/s12518-023-00543-6},
  DOI = {10.1007/s12518-023-00543-6},
  number = {1},
  journal = {Applied Geomatics},
  publisher = {Springer Science and Business Media LLC},
  author = {Praschl,  Christoph and Krauss,  Oliver},
  year = {2023},
  month = dec,
  pages = {161–180}
}
```
