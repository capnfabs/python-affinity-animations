# cssgenerator.py

# all times in seconds
initial_delay = 1
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
    print(f"""
        @keyframes anim-{elem_id} {{
            0%, {p(start_fadeout)} {{
                opacity: 1;
            }}
            {p(end_fadeout)}, 100% {{
                opacity: 0;
            }}
        }}

        #{elem_id} {{ animation: {total_time}s ease infinite anim-{elem_id}; }}
    """)

for idx, elem in enumerate(elements):
    anim_for_elem(elem, idx)
