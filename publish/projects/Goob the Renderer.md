---
name: Goob the Renderer
language: C++23
status: in progress
layout: project
github: goob2
slug: proj_1
description: Learning project to grasp core ideas of graphical engines.
tags:
  - watch
---
**file last reviewed:** 26.9.2025

This is a OpenGL-like rendering engine project. It started off in my second year in my bachelor's program. I didn't get very far although it produced some cool outputs.

## Current Tasks
- [ ] Implement opening and test of RGB TGA Image

## Successful Outcome
A working graphic renderer based on [tiny_renderer](github.com/ssloy/tinyrenderer) project. Additionally another software that is able to render TGA images at 24 FPS. This way I could potentially create renders inside games/videos inside a picture format.

## Core

- [ ]  **Phase 1: TGA Output** - Generate and work with TGA images correctly - IN PROGRESS
- [ ]  **Phase 2: Basic Renderer** - Working and tested implementation
- [ ]  **Phase 3: Real-time Renderer** - 24 FPS TGA sequence generator

## Reference Material
- tiny_renderer project - https://github.com/ssloy/tinyrenderer
- [[TGA]] format details - http://www.paulbourke.net/dataformats/tga/

## Technical goals
### TGA Image System
- [-]  Research TGA format specifications 
- [ ]  Implement TGA writer from scratch - IN PROGRESS
- [ ]  Optimize TGA writing performance 
- [ ]  Add RLE support

## Prepared tasks
- [-] Set-up build system (CMake)
- [-] Decide on the project structure
- [-] Set-up tests (Catch2)
- [-] Add color module
- [-] Research [[TGA]]
- [-] Decide on the structure
- [-] Implement TGAImage interface
- [ ] Implement and test opening of RGB TGA Image
- [ ] Implement and test opening of Grayscale TGA Image
- [ ] Implement and test opening of Color-mapped TGA Image
- [ ] Implement and test opening of RLE compression

## Development Environment
- **language:** c++23
- **compiler:** clang
- **build system:** cmake
- **ide:** vscode, neovim
- **debug:** gdb
- **Profiler:** -