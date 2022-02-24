"""
Create artwork.

os.path.join(BASE, '..', 'static', 'fonts', 'Raleway-SemiBold.ttf'),
"""
from flask import Blueprint, jsonify, request, send_file
from flask_api import status
from .utils import request_wrapper
import os
import random
from PIL import Image, ImageDraw, ImageFont
from io import BytesIO


ART_STYLES = [
    'CHECKERED',
    'GRADIENT',
    'SOLID'
]

FONTS = {
    'amatic_bold': 'Amatic-Bold.ttf',
    'opensans_bold': 'OpenSans-Bold.ttf',
    'opensans_bold_italic': 'OpenSans-BoldItalic.ttf',
    'opensans_extra_bold': 'OpenSans-ExtraBold.ttf',
    'opensans_extra_bold_italic': 'OpenSans-ExtraBoldItalic.ttf',
    'opensans_semibold': 'OpenSans-Semibold.ttf',
    'opensans_semibold_italic': 'OpenSans-SemiboldItalic.ttf',
    'raleway_bold': 'Raleway-Bold.ttf',
    'raleway_extra_bold': 'Raleway-ExtraBold.ttf',
    'raleway_extra_bold_italic': 'Raleway-ExtraBoldItalic.ttf',
    'raleway_semibold': 'Raleway-SemiBold.ttf',
}

COLORS = [  # https://www.color-hex.com/color-names.html
    {
        'name': 'Blue',
        'hex': '#137CBD'
    },
    {
        'name': 'Ocean Blue',
        'hex': '#4f42b5'
    },
    {
        'name': 'Orange',
        'hex': '#D9822B'
    },
    {
        'name': 'Yellow',
        'hex': '#f8d02b'
    },
    {
        'name': 'Green',
        'hex': '#0F9960'
    },
    {
        'name': 'Red',
        'hex': '#DB3737'
    },
    {
        'name': 'Purple',
        'hex': '#a020f0'
    },
    {
        'name': 'Pink',
        'hex': '#fc8eac'
    },
]


create_artwork_bp = Blueprint(
    'artwork_generator_bp',
    __name__,
    template_folder='routes'
)


BASE_PATH = os.path.abspath(os.path.dirname(__file__))


def conv_hex_to_rgb(hexcode):
    return tuple(int(hexcode.lstrip('#')[i:i + 2], 16) for i in (0, 2, 4))


@create_artwork_bp.route('/api/1/create-artwork', methods=['POST'])
@request_wrapper
def create_artwork():
    """ Create artwork!

    Example:
        r = requests.post(
            'http://127.0.0.1:5000/api/1/create-artwork',
            json={
                'art_style': 'GRADIENT',
                'color1': '#9966cc',
                'color2': '#2f847c',
                'font': 'raleway_bold'
            }
        )
        print(r.status_code)
        with open('this.png', 'wb') as w:
            w.write(r.content)

    :return:
    """
    if request.method == 'POST':
        # Check the payload
        data = request.get_json()

        # Check art style
        if 'art_style' in data:
            if data['art_style'] not in ART_STYLES:
                return jsonify({'error': f'{data["art_style"]} is not a valid art style'
                                         f' ({", ".join(ART_STYLES)}).'}), status.HTTP_400_BAD_REQUEST
        else:
            data['art_style'] = 'SOLID'

        # Check colors
        if 'color1' not in data:
            data['color1'] = random.choice(COLORS)['hex']

        if data['art_style'] != 'SOLID':
            if 'color2' not in data:
                while True:
                    data['color2'] = random.choice(COLORS)['hex']
                    if data['color2'] != data['color1']:
                        break

        # Check text/font
        if 'text' in data:
            if not isinstance(data['text'], str):
                return jsonify({'error': 'text entry must be a string.'}), status.HTTP_400_BAD_REQUEST
            if len(data['text']) > 50:
                return jsonify({'error': 'text entry must be less than 50 characters.'}), status.HTTP_400_BAD_REQUEST

            if 'font' in data:
                if data['font'] not in FONTS:
                    return jsonify({'error': f'{data["font"]} is not a valid font '
                                             f'({", ".join(FONTS.keys())}).'}),\
                           status.HTTP_400_BAD_REQUEST
            else:
                data['font'] = random.choice(list(FONTS.keys()))

        # Build artwork
        width = 500
        height = 500
        w_count = 2
        h_count = 2
        font_size = 96
        tag_offset_w = 35
        tag_offset_h = 35
        stroke_width = 2

        boxw = width / w_count
        boxh = height / h_count

        # SOLID
        if data['art_style'] == 'SOLID':
            color1_rgb = conv_hex_to_rgb(data['color1'])
            img = Image.new("RGB", (width, height), color1_rgb)

        # CHECKERED
        elif data['art_style'] == 'CHECKERED':
            color1_rgb = conv_hex_to_rgb(data['color1'])
            color2_rgb = conv_hex_to_rgb(data['color2'])

            img = Image.new("RGB", (width, height))
            pixels = img.load()

            for w in range(width):
                wi = int(w / boxw)

                for h in range(height):
                    hi = int(h / boxh)

                    if (wi + hi) % 2 == 0:
                        pixels[w, h] = color1_rgb
                    else:
                        pixels[w, h] = color2_rgb

        # GRADIENT
        else:
            color1_rgb = conv_hex_to_rgb(data['color1'])
            color2_rgb = conv_hex_to_rgb(data['color2'])

            img = Image.new('RGB', (width, height), color1_rgb)
            top = Image.new('RGB', (width, height), color2_rgb)
            mask = Image.new('L', (width, height))
            mask_data = []
            for y in range(height):
                for x in range(width):
                    mask_data.append(int(255 * (y / height)))
            mask.putdata(mask_data)
            img.paste(top, (0, 0), mask)

        # Add tag image
        tag_img = Image.open(os.path.join(BASE_PATH, '..', 'static', 'img', 'art.png'))
        img.paste(tag_img, (tag_offset_w, tag_offset_h))

        if 'text' in data and data['text']:
            font_style = os.path.join(BASE_PATH, '..', 'static', 'fonts', FONTS[data['font']])
            font = ImageFont.truetype(font_style, size=font_size)
            draw = ImageDraw.Draw(img)
            w, h = draw.textsize(data['text'], font=font)

            while w > (width - tag_offset_w):
                font_size -= 12
                font = ImageFont.truetype(font_style, size=font_size)
                draw = ImageDraw.Draw(img)
                w, h = draw.textsize(data['text'], font=font)

            draw.text(
                ((width - w) / 2, (height - h) / 2 - 25),
                data['text'],
                fill='white',
                font=font,
                align='center',
                stroke_width=stroke_width,
                stroke_fill='black'
            )

        img_io = BytesIO()
        img.save(img_io, 'PNG', quality=50)
        img_io.seek(0)

        return send_file(
            img_io,
            mimetype='image/png',
            attachment_filename='art.png',
            as_attachment=True
        )
