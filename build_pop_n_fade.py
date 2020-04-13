# build_pop_n_fade.py
from os.path import expanduser

from bs4 import BeautifulSoup


def generate_css():
    initial_delay = 2
    popout_time = 0.2
    wait_after_pop = 0.5
    fadeout_time = 0.2
    wait_between_items = 0.5
    elements = ['nw-cell', 'n-cell', 'ne-cell']

    time_per_element = popout_time + wait_after_pop + fadeout_time + wait_between_items

    total_time = initial_delay + time_per_element * len(elements)

    def p(time):
        """Converts `time` to a percentage of total time for the animation"""
        return f'{time / total_time * 100}%'

    def anim_for_elem(elem_id, idx):
        start_popout = initial_delay + time_per_element * idx
        end_popout = start_popout + popout_time
        start_fadeout = end_popout + wait_after_pop
        end_fadeout = start_fadeout + fadeout_time
        return f"""
                    @keyframes anim-{elem_id} {{
                        0%, {p(start_popout)} {{
                            opacity: 1;
                            transform: none;
                        }}
                        {p(end_popout)}, {p(start_fadeout)} {{
                            opacity: 1;
                            transform: translate(-2px,-2px);
                        }}
                        {p(end_fadeout)}, 100% {{
                            opacity: 0;
                            transform: translate(-2px,-2px);
                        }}
                    }}

                    #{elem_id} {{ animation: {total_time}s ease infinite anim-{elem_id}; }}
                """

    for idx, elem in enumerate(elements):
        yield anim_for_elem(elem, idx)

def main():
    input_filename = 'diagram-export.svg'
    # Have to save somewhere other than current directory; otherwise writing
    # this file will cause WatchGod to restart
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
