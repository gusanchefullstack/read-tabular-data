# read-tabular-data

A small Python CLI that reads a table of `(x, y, character)` coordinates from a published Google Doc and plots those characters on a grid to reveal a hidden message drawn in Unicode blocks.

![Python](https://img.shields.io/badge/python-3.14+-3776AB?logo=python&logoColor=white)
![pandas](https://img.shields.io/badge/pandas-3.1-150458?logo=pandas&logoColor=white)
![NumPy](https://img.shields.io/badge/numpy-array-013243?logo=numpy&logoColor=white)
![uv](https://img.shields.io/badge/managed%20with-uv-DE5FE9)

## Why This Exists

This is a coding exercise on reading **tabular data** with Python. The input is a Google Doc that holds a table, not a CSV or a spreadsheet. Each row says which character goes at which coordinate. When the characters are placed on a Cartesian grid, the output spells a word in block letters. The challenge is to fetch the data, clean the headers, and turn the coordinates into grid positions.

## How It Works

The core logic lives in [`decoding_secret(url)`](src/read_tabular_data/decoding_secret.py). It runs in six steps:

1. **Fetch the table.** `pd.read_html(url)` downloads the published Google Doc and parses every HTML `<table>` into a DataFrame. The function keeps only the first one.

2. **Fix the header row.** Google Docs tables have no `<th>` cells, so pandas treats the real header (`x-coordinate`, `Character`, `y-coordinate`) as data. The first row is promoted to column names and then dropped:
   ```python
   df.columns = pd.Index(df.iloc[0].astype(str))
   df = df[1:].reset_index(drop=True)
   ```

3. **Find the grid size.** The values come in as strings, so they are cast to `int`. The maximum `x` and `y` set the grid's width (`max_x + 1`) and height (`max_y + 1`).

4. **Create an empty grid.** `np.full((rows, cols), " ", dtype="<U1")` builds a 2D NumPy array of single-character strings, all filled with spaces.

5. **Place each character.** Each row becomes `[x, y, symbol]`, and the symbol is written to `matrix[y, x]`. The row index is `y` and the column index is `x`.

6. **Print with the y-axis flipped.** On a Cartesian plane `y = 0` is at the bottom, but array row 0 prints at the top. The function prints rows from `rows - 1` down to `0`, so the picture comes out the right way up.

```
Google Doc table ──► DataFrame ──► fix headers ──► int coords ──► NumPy grid ──► print bottom-up
```

## Installation

**Prerequisites**

- Python **3.14+** (pinned in [`.python-version`](.python-version))
- [uv](https://docs.astral.sh/uv/) (recommended) or pip
- Internet access, because the data is downloaded from Google Docs

```bash
git clone https://github.com/gusanchefullstack/read-tabular-data.git
cd read-tabular-data
uv sync
```

## Usage

Run the installed console script:

```bash
uv run read-tabular-data
```

Output for the default document:

```
██░     ██░    ███████░     ██░     ██░     ██████░ ████████░    ████████░     ████████░
██░     ██░  ███░    ██░   ████░   ████░      ██░   ██░     ██░  ██░     ██░ ███░     ███░
██░     ██░ ███░           ██░██░ ██░██░      ██░   ██░      ██░ ██░     ██░ ██░       ██░
██████████░ ██░           ███░ ██░██░ ██░     ██░   ██░      ██░ ████████░   ██░       ██░
██░     ██░ ███░          ██░  █████░ ███░    ██░   ██░      ██░ ██░     ██░ ██░       ██░
██░     ██░  ███░    ██░ ███░   ███░   ██░    ██░   ██░     ██░  ██░     ██░ ███░     ███░
██░     ██░    ███████░  ██░           ███░ ██████░ ████████░    ████████░     ████████░
```

To decode a different document, call the function from Python:

```python
from read_tabular_data import decoding_secret

decoding_secret("https://docs.google.com/document/d/e/<DOC_ID>/pub")
```

The document must be **published to the web** (*File → Share → Publish to web*). Its first table must have the columns `x-coordinate`, `Character`, `y-coordinate`, in that order.

| x-coordinate | Character | y-coordinate |
|--------------|-----------|--------------|
| 0            | █         | 0            |
| 0            | █         | 1            |
| 1            | ▀         | 1            |

## Project Structure

```
src/read_tabular_data/
├── __init__.py          # main() entry point; holds the Google Doc URL
├── decoding_secret.py   # decoding_secret(url): fetch, parse and plot
└── challenge.py         # Earlier commented-out draft (uses tabulate for debugging)
pyproject.toml           # Dependencies and the `read-tabular-data` script
```

## What I Learned

- **`pandas.read_html`** can parse any HTML table straight from a URL, including a published Google Doc. It needs `lxml` installed as the parser. See the [docs](https://pandas.pydata.org/docs/reference/api/pandas.read_html.html).
- **Header promotion.** Tables without `<th>` cells come in with numeric column names. Using `df.iloc[0]` as the header and slicing it off is a common clean-up step.
- **Type casting.** Values parsed from HTML are strings. Taking `max()` of strings compares them in text order (`"9" > "10"`), so the coordinates must go through `.astype(int)` first.
- **NumPy string arrays.** `np.full(..., dtype="<U1")` creates a fixed-width Unicode grid that can be indexed as `matrix[row, col]`.
- **Cartesian vs. matrix coordinates.** `(x, y)` maps to `matrix[y, x]`, and the rows must be printed in reverse so that `y` increases upward.
- **Packaging with uv.** `[project.scripts]` in `pyproject.toml` turns `main()` into the `read-tabular-data` command.

## Tests

There are no automated tests yet (see the Roadmap).

## Roadmap

- [x] Parse coordinate table from a published Google Doc
- [x] Render the hidden message in the terminal
- [ ] Accept the URL as a CLI argument instead of hard-coding it
- [ ] Look up columns by name instead of by position
- [ ] Add pytest tests with a local HTML fixture
- [ ] Add a LICENSE file

## License

No license file has been added yet, so all rights are reserved by default.

## Credits

- [pandas](https://pandas.pydata.org/): HTML table parsing and DataFrames
- [NumPy](https://numpy.org/): the character grid
- [lxml](https://lxml.de/): HTML parser backend for `read_html`
- [tabulate](https://github.com/astanin/python-tabulate): pretty-printing tables while debugging

## Author

**Gustavo Sanchez Galarza**

<a href="https://github.com/gusanchefullstack"><img src="https://img.shields.io/badge/GitHub-gusanchefullstack-181717?logo=github" alt="GitHub"></a>
<a href="https://www.linkedin.com/in/gustavosanchezgalarza/"><img src="https://img.shields.io/badge/LinkedIn-gustavosanchezgalarza-0A66C2?logo=linkedin" alt="LinkedIn"></a>
<a href="https://x.com/gusanchedev"><img src="https://img.shields.io/badge/X-@gusanchedev-000000?logo=x" alt="X"></a>
<a href="https://bsky.app/profile/gusanchedev.bsky.social"><img src="https://img.shields.io/badge/Bluesky-gusanchedev-0285FF?logo=bluesky&logoColor=white" alt="Bluesky"></a>
<a href="https://dev.to/gusanchedev"><img src="https://img.shields.io/badge/DEV-gusanchedev-0A0A0A?logo=devdotto" alt="DEV"></a>
<a href="https://www.frontendmentor.io/profile/gusanchefullstack"><img src="https://img.shields.io/badge/Frontend%20Mentor-gusanchefullstack-3F54A3?logo=frontendmentor" alt="Frontend Mentor"></a>
<a href="https://master.dev/u/gustavosanchezdev/"><img src="https://img.shields.io/badge/Master.dev-gustavosanchezdev-555555" alt="Master.dev"></a>
<a href="mailto:hello@gustavosanchez.dev"><img src="https://img.shields.io/badge/Email-hello%40gustavosanchez.dev-D14836?logo=gmail&logoColor=white" alt="Email"></a>

Website: [gustavosanchez.dev](https://www.gustavosanchez.dev)
