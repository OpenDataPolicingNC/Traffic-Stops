import math

def get_chunks(xs, chunk_count=3):
    """
    Helper function to split a list into roughly equally sized chunks.
    """
    chunk_width = math.ceil(len(xs) / chunk_count)
    ranges = range(0, len(xs), chunk_width)
    return [xs[x:x + chunk_width] for x in ranges]
