# Highlight to Obsidian

A small personal browser extension that sends text you select on a web page to a note in your Obsidian vault, sorted by highlight color. Built for taking notes while learning online.

- Select text on any page and pick a color.
- A local Python server writes the highlight to a Markdown note.
- Each color has its own heading in the note, with a link back to the source page.

## How it works

```
Browser extension  →  Flask server (localhost)  →  Obsidian note (.md)
```

Example of the resulting note:

```markdown
## Key ideas

- Python is dynamically typed ([Python docs](https://python.org))

## Definitions

- A list is an ordered collection ([Tutorial](https://example.com))
```

## Requirements

- Python 3.9 or newer
- Chrome or Edge (Manifest V3)
- An Obsidian vault (any folder of Markdown files works)

## Installation

### 1. Server

```powershell
git clone https://github.com/YOUR-USERNAME/highlight-to-obsidian.git
cd highlight-to-obsidian
pip install -r requirements.txt
cd server
copy config.example.py config.py
```

Open `server/config.py` and set `NOTES_DIR` to a folder in your vault. You can also change the note name and the headings for each color.

Start the server:

```powershell
python server.py
```

### 2. Extension

1. Open `chrome://extensions` (or `edge://extensions`).
2. Turn on **Developer mode**.
3. Click **Load unpacked** and select the `extension` folder.

## Usage

1. Make sure the server is running.
2. Select text on a web page (refresh pages that were open before installing the extension).
3. Click a color dot. A ✓ means it was saved, a ✗ means the server is not reachable.

## Run the server at Windows startup (optional)

1. Press `Win + R`, type `shell:startup`, press Enter.
2. Create a shortcut to `start-server.bat` in that folder.
3. In the shortcut's properties (Shortcut tab), set **Run** to **Minimized**.

## Customizing colors

Colors are defined in two places, and the names must match exactly:

- `server/config.py`: the color name and its heading in the note.
- `extension/content.js`: the color name and its dot color.

Restart the server and reload the extension after changing them.

## Project structure

```
extension/
  manifest.json   Extension settings
  content.js      Detects selected text and shows the color bar
  background.js   Sends highlights to the server
server/
  server.py       Flask server (POST /highlight)
  notes.py        Writes highlights to the Markdown note
  config.example.py  Example settings (copy to config.py)
```

## Limitations

- Personal project, meant for local use only.
- The server listens on `127.0.0.1` only and is not exposed to the network.
- Highlights are saved to the note but not displayed on the web page.
- Does not work on browser internal pages or Chrome's built-in PDF viewer.