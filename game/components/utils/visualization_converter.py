def convert_to_progress_string(percentage, block_length):
    filled_blocks = int(percentage * block_length)
    # TODO: empty space " " is not equal width with "█", make it weird
    empty_blocks = int((block_length - filled_blocks) * 3 / 2)

    # Create the bar
    bar = "█" * filled_blocks + " " * empty_blocks
    return f"[{bar}]"
