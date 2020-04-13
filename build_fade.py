# build_fade.py
from os.path import expanduser

from bs4 import BeautifulSoup


def generate_css():
    """Generate the CSS animations in this method.
    Rather than use `print` as we did before, use `yield`, to make the generated CSS easier for calling code to capture.
    """
    initial_delay = 0.5
    fadeout_time = 0.2
    wait_between_items = 0.5
    elements = ['nw-cell', 'n-cell', 'ne-cell']

    total_time = initial_delay + (fadeout_time + wait_between_items) * len(elements)

    def p(time):
        """Converts `time` to a percentage of total time for the animation"""
        return f'{time / total_time * 100}%'

    def anim_for_elem(elem_id, idx):
        start_fadeout = initial_delay + (fadeout_time + wait_between_items) * idx
        end_fadeout = start_fadeout + fadeout_time
        return f"""
            @keyframes anim-{elem_id} {{
                0%, {p(start_fadeout)} {{
                    opacity: 1;
                }}
                {p(end_fadeout)}, 100% {{
                    opacity: 0;
                }}
            }}

            #{elem_id} {{ animation: {total_time}s ease infinite anim-{elem_id}; }}
        """

    for idx, elem in enumerate(elements):
        yield anim_for_elem(elem, idx)

def main():
    input_filename = 'diagram-export.svg'
    # Have to save somewhere other than current directory; otherwise writing
    # this file will cause WatchGod to detect a change
    output_filename = expanduser('~/Desktop/diagram-export-animated.svg')
    all_css = "\n".join(generate_css())

    # Load / Parse the SVG file using BeautifulSoup
    with open(input_filename) as infile:
        soup = BeautifulSoup(infile, 'xml')

        # add the newly generated CSS to the XML
        style_tag = soup.new_tag('style', id='stylegen')
        style_tag.string = all_css
        svg = soup.find('svg')
        svg.insert(0, style_tag)

        # while we're here, let's set a width so that it renders with
        # a sensible default size when embedded in a webpage
        # (there's an extremely detailed guide here:
        # https://css-tricks.com/scale-svg)
        svg.attrs['width'] = '585'

        # Write amended SVG to OUTPUT_DIRECTORY.
        with open(output_filename, 'w') as outfile:
            outfile.write(str(soup))
    print(f'Wrote styled version to {output_filename}')

if __name__ == '__main__':
    main()
