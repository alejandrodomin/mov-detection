def mov_filter(frame, last_frame, filter):
    """
    :param last_frame:
    :param frame:
    :type filter: High pass filter that removes the most intense pixels. These pixels are usually noise.
    """
    transformed_frame = frame - last_frame
    transformed_frame[transformed_frame > filter] = 0

    return transformed_frame