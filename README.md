Folder where I put example benchmarks for my agent tools for developing godot scripts and scenes.


## Benchmarks

| Name | Passed | Notes |
|------|--------|-------|
| sprite | ✅ | I had to accept that godot, LLMs and other people index images in a cartesian way (x,y), not in a matrix like way (row,column) |
| animated_door | ✅ | I had to create specific tools for creating animations. I also had to implement topological ordering of the subresources otherwise godot would crash |

## Acknowledgments

This examples could not have been possible with the incredible assets made by Kenney. Check them out at http://patreon.com/kenney/
