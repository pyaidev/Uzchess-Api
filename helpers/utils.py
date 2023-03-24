from PIL import Image, ImageDraw, ImageFont
import time, random, string


def get_timer(length: float, type: str = 'long'):
    h = length // 3600
    m = length % 3600 // 60
    s = length % 3600 % 60
    if type == 'short':
        return f"{h}h {f'0{m}' if m < 10 else m}m"

    if type == 'min':
        return f"{f'0{m}' if m < 10 else m}min"

    else:
        if h >= 1:
            return f"{h}:{f'0{m}' if m < 10 else m}:{f'0{round(s)}' if s < 10 else round(s)}"
        else:
            return f"{f'0{int(m)}' if m < 10 else m}:{f'0{round(s)}' if s < 10 else round(s)}"


def certificaty(name, course):
    cert_template = Image.open("././././static/shablon/1.jpg")
    font = ImageFont.load_default()
    font_style = ImageFont.truetype("././././static/fonts/Roboto/Roboto-BoldItalic.ttf", 40)

    draw = ImageDraw.Draw(cert_template)

    date = f'Data: {time.strftime("%d/%m/%Y")}'

    congart = "Congratulations!"

    name_pos = (300, 350)
    course_pos = (300, 450)
    date_pos = (300, 550)
    congart_pos = (300, 250)

    draw.text(name_pos, name, font=font_style, fill='black')
    draw.text(course_pos, course, font=font_style, fill='black')
    draw.text(date_pos, date, font=font_style, fill='black')
    draw.text(congart_pos, congart, font=font_style, fill='black')

    cert_template.save(f"././././static/certicats/{name}-{course}.jpg")

    return f"././././static/certicats/{name}-{course}.jpg"




# def randomize_certificate_number():
#     from apps.course.models import Certificate
#
#     cids = Certificate.objects.values_list("cid", flat=True)
#     while True:
#         random_cid = "".join(random.choice(string.digits + string.ascii_uppercase) for _ in range(7))
#         if random_cid not in cids:
#             return random_cid
