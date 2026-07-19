## Coding Agent

Use the gli MCP server tools to implement this benchmark. If the gli MCP server is not available, stop immediately and report that it is required.

## Project Setup

Godot 4.7

The project must be created inside this folder (the agent does not know it is a benchmark, treat it as a project). Create a `project.godot` file and set the main scene in it. If it is a simple use case with at most a couple of scenes, do everything in the root; otherwise create a `scenes/` folder where everything is done. If testing is required, create a `test/` folder.

## Assets

assets/tilemap_packed.png

## Implementation

Let's create a simple node2D object with an AnimateSprite2D with two animations.
open
close
In the tilemap, the door frames are at
- door (animated):
  - open door: (9,0)
  - starting to close (9,1)
  - almost closed (9,2)
  - closed (9,2), of course if you registere in the animation in the opposite direction, it opens 