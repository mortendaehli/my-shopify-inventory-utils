from PIL import Image


def expand_to_square(image: Image, fill_color: tuple = (255, 255, 255)) -> Image:
    width, height = image.size
    if width == height:
        return image
    elif width > height:
        result = Image.new(image.mode, (width, width), fill_color)
        result.paste(image, (0, (width - height) // 2))
        return result
    else:
        result = Image.new(image.mode, (height, height), fill_color)
        result.paste(image, ((height - width) // 2, 0))
        return result
