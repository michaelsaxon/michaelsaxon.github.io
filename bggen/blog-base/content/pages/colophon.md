Title: Colophon
remove_footnote_section: true

> [!note]
> <img src="https://upload.wikimedia.org/wikipedia/commons/e/e1/Inkunabel.ValMax.finis.detail.jpg" alt="Sample colophon from Wikipedia."> 
> A *colophon*[^4] is a page that describes how the site is made, with what tools, supporting what technologies.  Having the key principles that govern your site in one place means that any user who visits does not need to read through the archives of your site or speak with you to understand what mattered most to you when you constructed your site. 
> ---[IndieWebCamp](https://indieweb.org/colophon)

[^4]: The term [colophon](https://en.wikipedia.org/wiki/Colophon_(publishing)) comes from publishing, to describe the pages in the forward of a volume which name where and by whom it was printed, what font it is set in, and other details.

Built from scratch on the west coast by Michael Saxon, from 2017 to today. Heavy Cursor use to build plugins and CSS. Feel free to steal my source on [GitHub](https://github.com/michaelsaxon/michaelsaxon.github.io)!

<img src="https://saxon.me/theme/img/logomark_trans.png" alt="Logomark" class="colophon-img"/>

#### Design

The following fonts are used under personal licenses:

- **Calluna** from [exljbris](https://www.exljbris.com/calluna.html) for main body text.
- **Berkeley Mono** from [US Graphics Co.](https://usgraphics.com/products/berkeley-mono) for headers, code blocks, and  decorative monospace.
- **Univers Next Pro** from [Cufon fonts](https://www.cufonfonts.com/font/univers-next-pro-extended) for sans serif.
- **Triptych Italick** from the [Pyte Foundry](https://thepytefoundry.net/typefaces/triptych/) for decorative headers.

The color scheme is based on the [Kanagawa](https://terminalcolors.com/themes/kanagawa/) Nvim/iTerm theme with slight modifications.

Design inspirations for this site include [Justine Zhang's site](http://tisjune.github.io), [Gwern](https://gwern.net/)[^3], and [US Graphics Co.](https://usgraphics.com/) (if you would believe it).

[^3]: I know, cringe... but the pop up footnotes are awesome man!

### Stack

*This webpage is built using [Pelican](https://getpelican.com/), a Python-based static blog generator. It uses a custom, framework-free Jinja theme with [custom Markdown extensions and Pelican plugins](#plugins)*.

#### Plugins

`infobox`: custom infobox styles for quotes (supports GitHub-flavored markdown, [examples](#infobox-examples)).

`footnote_popups`: renders mouseover pop-ups for footnotes[^1].

`image_processor`: processes post header images: grabs the image linked in the `md`, and maps it into the site theme colors and compresses it using OpenCV.

`dash_shortcuts`: converts strings into nice unicode characters, in particular mapping the en-dash `--` to -- and em-dash `---` to ---.

`smart_quotes`: beautify `"` and `'` by converting them to left and right versions in a contextually-appropriate manner. Examples: "double quotes" and 'single quotes' get correctly mapped, but contractions aren't changed.

<!-- `underscore_underline`: Parses underscores `_` in markdown as _underlines_ and not as *emphasis*. -->

`html_comment_sanitizer`: completely removes inline HTML comments `<!-- -->` from rendered HTML[^2] so that comments I put in the files while writing posts aren't leaked.

`pelican_bibtex`: uses the Python `pybtex` package to scan a Bibtex file containing all my papers to generate my [Publications](../Publications) page. This plugin was inspired by, but is effectively completely different from [Vlad Niculae's own `pelican-bibtex` plugin.](https://github.com/vene/pelican-bibtex).


[^1]: Like this! It uses some JS to keep the popup centered over the footnote tag, unless it will fall outside of the bounding box of the main text.
[^2]: It's stupid that I even need to implement this...but there are no Markdown-specific ways to write comments, the official way is to just put HTML comments which interacts with `dash_shortcuts` badly and creates `<!&ndash &ndash>`, which renders normally instead of being removed.

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

### Hosting & Domain

The site is hosted for free using [GitHub pages](https://docs.github.com/en/pages). The domain is provided by Namecheap. I am thinking about moving to better providers and aspire to eventually self host, but GH pages is pretty good for static sites.

### Privacy

For a long time I used [Clustrmaps](https://clustrmaps.com/site/1bs8p) for visitor tracking.
While obviously, any free service for this sort of thing will be using it for data gathering, I didn't realize quite how nasty Clustrmaps is.
Beyond just a run-of-the-mill databroker, it actually uses its data to power a by-name people search service which correlates IPs to addresses.

I got rid of it in October 2025 and replaced it with Google Analytics (that way the data being collected only goes to me, and Google who is in my opinion much less pernicious---they are already tracking you anyway).
I rolled a custom visitor map generator I'm calling [`analytics2map`](https://github.com/michaelsaxon/analytics2map) which pulls the latest Google analytics data and renders it to svgs hosted at [`saxon.me/analytics2map`](https://saxon.me/analytics2map). Eventually, I'm going to make it run as a periodic Github action, and I will have fully recovered the useful, automatic behavior Clustrmaps gave without as hairy of privacy issues.

![The visitor map for my site.](https://saxon.me/analytics2map/output/visitors-large.svg)
