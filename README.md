# Apply Modifiers With Shape Keys

> Read this in other languages: [English](README.md), [日本語](README.ja.md).

## About

Blender addon for applying modifiers with respecting shape keys.

Updated to support Blender 2.80 or higher from founder [mato.sus304](https://sites.google.com/site/matosus304blendernotes/home)'s original version.

## Usage

### Install

- Download zip archive from [Release page](../../releases) of github site.

- Press install button on addon panel of blender's preference window and choose just downloaded zip file.

- Enable 'Apply Modifiers With Shape Keys' addon.

Then, three menu items ('Apply All Modifiers With Shape Keys' 'Apply Selected Modifiers With Shape Keys' 'Apply Pose As Rest Pose With Shape Keys') are added into *Object > Apply* menu.

Select mesh object, and choose added menu item from *Object > Apply* (Ctrl + A) menu.

Blender's default apply function can't apply mirror modifier if mesh has shape keys, but this addon can apply in theese cases.

If mesh has no shape key, this addon works same as default function.

### Apply all modifiers with shape keys

You can apply all modifiers for all selected objects with one click.

### Apply selected modifier with shape keys

You can apply specified modifier with respecting shape keys for active object.

### Apply pose as rest pose with shape keys

You can apply armature modifiers for meshes referencing selected armature object in current view layer with respecting shape keys, and apply current pose as rest pose for selected armature object.

### Limitation

This addon behave to clone mesh object each shape keys, and apply modifiers each clone, and reconstruct shape keys.

Then, if modifier changes vertex count and coresponding vertex in shape key is unknown, this addon just skip reconstruction of applicable shape key.

In this case, result will have wrong shape key.

## Licence

[GNU GENERAL PUBLIC LICENSE (v2)](LICENSE)
