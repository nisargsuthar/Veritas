<h1 align="center">
  <br>
  <a href="https://github.com/nisargsuthar/Veritas"><img src="https://github.com/nisargsuthar/Veritas/blob/main/images/Veritas.png" width="50%"></a>
  <br>
  Veritas
  <br>
</h1>

<h3 align="center">Veraciously Effective Renderer In Typical Artifact Structures</h3>

<p align="center">
   <a href="LICENSE" alt="License">
   <img src="https://img.shields.io/github/license/nisargsuthar/Veritas?style=flat" /></a>
   <a href="https://github.com/nisargsuthar/Veritas/issues" alt="Issues">
   <img src="https://img.shields.io/github/issues/nisargsuthar/Veritas?style=flat" /></a>
   <a href="https://github.com/nisargsuthar/Veritas/graphs/contributors" alt="Contributors">
   <img src="https://img.shields.io/github/contributors/nisargsuthar/Veritas?style=flat" /></a>
   <a href="https://github.com/nisargsuthar/Veritas/pulls?q=is%3Apr+is%3Aclosed" alt="Closed PRs">
   <img src="https://img.shields.io/github/issues-pr-closed/nisargsuthar/Veritas?style=flat" /></a>
   <a href="https://github.com/nisargsuthar/Veritas/network/members/" alt="Forks">
   <img src="https://img.shields.io/github/forks/nisargsuthar/Veritas?style=flat" /></a>
   <a href="https://github.com/nisargsuthar/Veritas/stargazers/" alt="Stars">
   <img src="https://img.shields.io/github/stars/nisargsuthar/Veritas?style=flat" /></a>
   <a href="https://github.com/nisargsuthar/Veritas/watchers/" alt="Watchers">
   <img src="https://img.shields.io/github/watchers/nisargsuthar/Veritas?style=flat" /></a>
</p>

## About
Tired of always having to look up different versions of file structures & manually mapping the bytes while working with hex?

Veritas is an elementary **WIP** hex viewer made for forensicators, which automatically identifies different artifacts and applies the correct template. These templates are generated dynamically to accurately highlight data with appropriate color markers.

## Last Still(s)
![StillOne.png](https://raw.githubusercontent.com/nisargsuthar/Veritas/main/images/StillOne.png?)
![StillTwo.png](https://raw.githubusercontent.com/nisargsuthar/Veritas/main/images/StillTwo.png?)
![StillThree.png](https://raw.githubusercontent.com/nisargsuthar/Veritas/main/images/StillThree.png?)

## Disclaimer
Veritas is not meant to be an advanced hex viewer with functionalities that a real hex editor might have. It **solely** aims for one thing, convenience for data validation. It is suggested that this hex viewer be used in accordance with other good hex editors that offer searching and goto functions. Over time, Veritas will support more file structures; but as of now I'm the only one working on this project when I'm able to.

For issues/discussions regarding the project, kindly join the [Digital Forensics Discord Server](https://discord.gg/pNMZunG) and head over to this [thread](https://discord.com/channels/427876741990711298/1129637465636999208)!

## Features
* Dynamic artifact templates.
* Color coded artifact file structure with sub-sections.
* Load multiple files simultaneously in tabs with standard keybinds.
* Drag-n-drop artifacts into Veritas with deduplication.

## Supported Artifacts
| NTOS                        | Images          | Documents       | Databases                |
|-----------------------------|-----------------|-----------------|--------------------------|
| :white_check_mark: Prefetch | :clipboard: PNG | :clipboard: PDF | :construction: SQLite    |
| :white_check_mark: LNK      | :clipboard: JPG |                 |                          |
| :pause_button: Registry     | :clipboard: BMP |                 |                          |
| :clipboard: MFT             | :clipboard: GIF |                 |                          |

|:white_check_mark: - Completed | :construction: - Work In Progress | :pause_button: - Halted | :clipboard: - Planned |
|---|---|---|---|

## Requirements
* Python >= 3.10.4
* Kivy >= 2.1.0
* Plyer >= 2.1.0

## Installation
**Step 1**: Create a virtual environment using:
```python
python.exe -m venv veritas
```

**Step 2**: Depending on your OS, activate the virtual environment using:
* Windows: `.\veritas\Scripts\activate`
* Linux: `source veritas/Scripts/activate`

**Step 3**: Install Kivy using:
```python
python.exe -m pip install "kivy[base]"
```

**Step 4**: Install Plyer using:
```python
python.exe -m pip install plyer
```

## Usage
```python
python.exe main.py
```

|  Shortcut |   Description   |
|-----------|-----------------|
|Ctrl + O   | Open a file     |
|Ctrl + W   | Close a file    |
|Ctrl + PgUp| Cycle tabs left |
|Ctrl + PgDn| Cycle tabs right|

## Special Thanks (Check [RESOURCES.md](https://github.com/nisargsuthar/Veritas/blob/main/RESOURCES.md) for more)
[Andrew Rathbun](https://twitter.com/bunsofwrath12), [el3phanten](https://github.com/el3), [Gary Kessler](https://www.linkedin.com/in/garykessler), [Joachim Metz](https://github.com/joachimmetz), [Forensics Wiki](https://forensics.wiki/)
