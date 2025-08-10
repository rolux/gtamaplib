![gtamaplib](readme/gtamaplib.png)

# gtamaplib

**gtamaplib** is a mapping and 3D triangulation library for GTA-like worlds – specifically for [Grand Theft Auto VI](https://www.rockstargames.com/VI/), scheduled for release in 2026.

"Mapping GTA" is a popular activity[^1] that begins years before the release of the game. One goal is to create a maximally accurate map of the game world, based on the geography shown in promotional screenshots and trailers. **gtamaplib** was developed to facilitate this process, and functions as a companion project to the [GTA Landmarks Map](https://github.com/rolux/gtadb.org).

The core of **gtamaplib** are its `Camera` and `Map` classes. A `Camera` turns a screenshot into a configurable camera object that can be programatically calibrated to match its true position and orientation in 3D space. A `Map` aggregates cameras, the rays originating from them, and the landmarks at their intersections, into a shared 2D representation. Cameras can be projected onto maps, maps can be projected into cameras, and it's even possible to project one camera into another one.

"Mapping GTA" often involves triangulation. Two or more known cameras can be used to find the coordinates of a shared landmark, and with a sufficiently large number of known landmarks, it is possible to determine the position and orientation of unknown cameras. **gtamaplib** provides the trigonometric primitives for accurate 3D triangulation, and a `find_camera` method that performs a parallelized, multi-dimensional parameter sweep within a given search area, which returns – based on visible landmarks that are either known or can be seen from other known cameras – an optimally positioned and calibrated camera object. Rays and landmarks can be rendered directly into the camera image, and the log loss landscape of the search can be displayed on a map.

**gtamaplib** comes with two companions: `gtamapdata` is a database of well-established cameras, frame-by-frame annotations, and triangulated landmark coordinates, and `gtamaputils` contains a collection of utilities and user scripts.

Please note that v0.1.0 is a the first, pre-release version of the library. More information, further updates (and maybe even proper documentation!) will follow shortly.

[^1]: see the [Mapping Los Santos](https://gtaforums.com/topic/491242-mapping-los-santos-buildinglandmark-analysis/) and [Mapping Vice City](https://gtaforums.com/topic/985670-mapping-vice-city-map-discussion-thread-no-leak-footage-allowed/) threads on GTAForums

<br><br><br>

![leonida keys](<readme/leonida keys.png>)

![watson bay](<readme/watson bay.png>)

![hamlet prison](<readme/hamlet prison.png>)

<br><br><br>
