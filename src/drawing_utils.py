# Drawing utility functions

import cv2 as cv
import colors


def text(image, text, text_position, text_color=colors.BLACK):
    """
    Draws text on an input image.

    Args:
        image (numpy.ndarray): The input image as a NumPy array.
        text (str): The text to be drawn on the image.
        text_position (tuple): The position of the text on the image, specified as a tuple of (x, y) coordinates,
                              where x is the horizontal coordinate and y is the vertical coordinate.
        text_color (tuple, optional): The color of the drawn text, specified as a tuple of (B, G, R) values.
                                     Defaults to colors.COLOR_BLACK.

    Returns:
        numpy.ndarray: The input image with the text drawn on it.

    Raises:
        None.

    Example usage:
        # Load an image
        image = cv.imread('image.jpg')

        # Draw text on the image
        text = "Hello, World!"
        text_position = (10, 30)
        text_color = (0, 0, 255)  # Red color
        image_with_text = draw_text(image, text, text_position, text_color)

    Note:
        - The function uses OpenCV's cv.putText() function to draw the text on the input image.
        - The text_position parameter specifies the position of the text on the image, with (0,0) at the top-left corner
          of the image and (x_max, y_max) at the bottom-right corner of the image.
        - The text_color parameter specifies the color of the drawn text, specified as a tuple of (B, G, R) values,
          where B is the blue channel, G is the green channel, and R is the red channel.
        - The drawn text is positioned just below the text_position coordinates, with a small margin for readability.
        - The function returns the input image with the text drawn on it.
    """
    (text_width, text_height), _ = cv.getTextSize(text, cv.FONT_HERSHEY_SIMPLEX, 0.5, 1)
    x, y = text_position
    overlay = image.copy()
    cv.putText(
        image, text, (x, y + text_height), cv.FONT_HERSHEY_SIMPLEX, 0.5, text_color, 1
    )
    return image


def text_with_background(
    image,
    text,
    position,
    text_color=colors.WHITE,
    background_color=colors.GRAY,
    background_opacity=1.0,
    padding_x=5,
    padding_y=5,
):
    """
    Draws text on an input image with a background box.

    Args:
        image (numpy.ndarray): The input image as a NumPy array.
        text (str): The text to be drawn on the image.
        position (tuple): The position of the text on the image, specified as a tuple of (x, y) coordinates,
                          where x is the horizontal coordinate and y is the vertical coordinate.
        text_color (tuple, optional): The color of the text, specified as a tuple of (B, G, R) values.
                                     Defaults to colors.COLOR_WHITE.
        background_color (tuple, optional): The color of the background box, specified as a tuple of (B, G, R) values.
                                            Defaults to colors.COLOR_GRAY.
        background_opacity (float, optional): The opacity of the background box, ranging from 0.0 to 1.0.
                                             Defaults to 1.0, fully opaque.
        padding_x (int, optional): The horizontal padding between the text and the background box. Defaults to 5 pixels.
        padding_y (int, optional): The vertical padding between the text and the background box. Defaults to 5 pixels.

    Returns:
        numpy.ndarray: The input image with the text drawn on it with a background box.

    Raises:
        None.

    Example usage:
        # Load an image
        image = cv.imread('image.jpg')

        # Draw text with a background box on the image
        text = "Hello, World!"
        position = (10, 30)
        text_color = (255, 255, 255)  # White color
        background_color = (128, 128, 128)  # Gray color
        background_opacity = 0.5  # 50% opacity
        padding_x = 10
        padding_y = 5
        image_with_text = draw_text_with_background(image, text, position, text_color, background_color, background_opacity, padding_x, padding_y)

    Note:
        - The function uses OpenCV's cv.putText() and cv.rectangle() functions to draw the text and background box
          on the input image, respectively.
        - The position parameter specifies the position of the text on the image, with (0,0) at the top-left corner
          of the image and (x_max, y_max) at the bottom-right corner of the image.
        - The text_color parameter specifies the color of the text, specified as a tuple of (B, G, R) values,
          where B is the blue channel, G is the green channel, and R is the red channel.
        - The background_color parameter specifies the color of the background box, specified as a tuple of (B, G, R) values.
        - The background_opacity parameter specifies the opacity of the background box, ranging from 0.0 (fully transparent)
          to 1.0 (fully opaque).
        - The padding_x and padding_y parameters specify the horizontal and vertical padding between the text and the
          background box, respectively.
        - The function returns the input image with the text drawn on it with a background box.
    """
    (text_width, text_height), _ = cv.getTextSize(text, cv.FONT_HERSHEY_SIMPLEX, 0.5, 1)
    x, y = position
    overlay = image.copy()
    cv.rectangle(
        overlay,
        (x, y),
        (x + text_width + 2 * padding_x, y + text_height + 2 * padding_y),
        background_color,
        -1,
    )
    new_image = cv.addWeighted(
        overlay, background_opacity, image, 1 - background_opacity, 0
    )
    cv.putText(
        new_image,
        text,
        (x + padding_x, y + padding_y + text_height),
        cv.FONT_HERSHEY_SIMPLEX,
        0.5,
        text_color,
        1,
    )
    image = new_image
    return image
