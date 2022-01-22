import qrcode
from qrcode.image.styledpil import StyledPilImage
from qrcode.image.styles.moduledrawers import RoundedModuleDrawer, HorizontalBarsDrawer, VerticalBarsDrawer


# todo: more attributes: https://github.com/lincolnloop/python-qrcode


def create_code_c(data, file_name, fcolor=(0, 0, 0), bgcolor=(255, 255, 255), box_size=6):
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=box_size,
        border=2,
    )

    qr.add_data(data)
    qr.make(fit=True)

    img = qr.make_image(fill_color=fcolor, back_color=bgcolor)
    img.save(file_name)


def create_code_b(data, file_name, mode):
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_H,
        box_size=6,
        border=2
    )

    qr.add_data(data)
    img = qr.make_image(image_factory=StyledPilImage, module_drawer=mode)

    img.save(file_name)


if __name__ == '__main__':
    create_code_c('testing some data for exchange', 'test.png', (0, 0, 0), (255, 255, 255), 6)
