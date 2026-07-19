## Coding Agent

Use the gli MCP server tools to implement this benchmark. If the gli MCP server is not available, stop immediately and report that it is required.

## Project Setup

Godot 4.7

The project must be created inside this folder (the agent does not know it is a benchmark, treat it as a project). Create a `project.godot` file and set the main scene in it. If it is a simple use case with at most a couple of scenes, do everything in the root; otherwise create a `scenes/` folder where everything is done. If testing is required, create a `test/` folder.

## Assets

assets/tilemap_packed.png

## Implementation

Create a Sprite2D with the knight texture at index - knight: (1,8) in the tileset provided as asset.
Set the scaling to nearest