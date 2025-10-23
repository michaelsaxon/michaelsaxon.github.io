Title: Colophon
remove_footnote_section: true

*Built by Michael Saxon from scratch between 2017 and today in Arizona, California, and Washington. Heavy Cursor use to build plugins and CSS.*

<img src="https://saxon.me/theme/img/logomark_trans.png" alt="drawing" width="100" style="opacity: 0.6;
    filter: var(--logo-filter); margin-left: auto; margin-right: auto;"/>

### Stack

*This webpage is built using [Pelican](https://getpelican.com/), a Python-based static blog generator. It uses a custom, framework-free Jinja theme with [custom Markdown extensions and Pelican plugins](#plugins)*.

#### Design

The following fonts are used under personal licenses:

- **Calluna** from [exljbris](https://www.exljbris.com/calluna.html) for main body text.
- **Berkeley Mono** from [US Graphics Co.](https://usgraphics.com/products/berkeley-mono) for headers, code blocks, and  decorative monospace.
- **Univers Next Pro** from [Cufon fonts](https://www.cufonfonts.com/font/univers-next-pro-extended) for sans serif.
- **Triptych Italick** from the [Pyte Foundry](https://thepytefoundry.net/typefaces/triptych/) for decorative headers.

The color scheme is based on the [Kanagawa](https://terminalcolors.com/themes/kanagawa/) Nvim/iTerm theme with slight modifications.

#### Plugins

`infobox`: custom infobox styles for quotes (supports GitHub-flavored markdown, [examples](#infobox-examples)).

`footnote_popups`: renders mouseover pop-ups for footnotes[^1].

`image_processor`: processes post header images: grabs the image linked in the `md`, and maps it into the site theme colors and compresses it using OpenCV.

`dash_shortcuts`: converts strings into nice unicode characters, in particular mapping the en-dash `--` to -- and em-dash `---` to ---.

`smart_quotes`: beautify `"` and `'` by converting them to left and right versions in a contextually-appropriate manner. Examples: "double quotes" and 'single quotes' get correctly mapped, but contractions aren't changed.

`html_comment_sanitizer`: completely removes inline HTML comments `<!-- -->` from rendered HTML[^2] so that comments I put in the files while writing posts aren't leaked.

`pelican_bibtex`: uses the Python `pybtex` package to scan a Bibtex file containing all my papers to generate my [Publications](../Publications) page.


[^1]: Like this! It uses some JS to keep the popup centered over the footnote tag, unless it will fall outside of the bounding box of the main text.
[^2]: It's stupid that I even need to implement this...but there are no Markdown-specific ways to write comments, the official way is to just put HTML comments which interacts with `dash_shortcuts` badly and 

All plugins are CC-BY-SA and accessible from my source github repo.

##### `infobox` examples

I have implemented default, `warning`, `info`, and `tip` boxes.

> This is an ordinary quote.

> [!WARNING]
> This is a WARNING.

> [!NOTE]
> This is a NOTE.

> [!TIP]
> This is a TIP.
