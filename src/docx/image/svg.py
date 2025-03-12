from io import BytesIO
import xml.etree.ElementTree as ET

from .constants import MIME_TYPE
from .image import BaseImageHeader


class Svg(BaseImageHeader):
    """
    Image header parser for SVG images.
    """

    @classmethod
    def from_stream(cls, stream: BytesIO):
        """
        Return |Svg| instance having header properties parsed from SVG image
        in *stream*.
        """
        px_width, px_height = cls._dimensions_from_stream(stream)
        return cls(px_width, px_height, 72, 72)

    @property
    def content_type(self):
        """
        MIME content type for this image, unconditionally `image/svg+xml` for
        SVG images.
        """
        return MIME_TYPE.SVG

    @property
    def default_ext(self):
        """
        Default filename extension, always 'svg' for SVG images.
        """
        return "svg"

    @classmethod
    def _length_to_px(cls, length: str):
        """
        Convert SVG length unit to pixels.

        See the table of absolute length units in W3 CSS Values 3
        https://www.w3.org/TR/css-values-3/#absolute-lengths
        """
        s = str(length)
        unit = s.lstrip("0123456789.").casefold()
        value_string = s[: -len(unit)] if len(unit) > 0 else s
        value = float(value_string)
        inch = 96
        cm = inch / 2.54
        units = {
            "cm": cm,
            "mm": cm / 10,
            "q": cm / 40,
            "in": inch,
            "pc": inch / 6,
            "pt": inch / 72,
            "px": 1,
        }
        px = value * units.get(unit, 1)
        return int(px)

    @classmethod
    def _dimensions_from_stream(cls, stream: BytesIO):
        stream.seek(0)
        data = stream.read()
        root = ET.fromstring(data)
        width = cls._length_to_px(root.attrib["width"])
        height = cls._length_to_px(root.attrib["height"])
        return width, height
