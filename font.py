import settings as stt
import pygame as pg
import game_math as gm
# load and uses custom font


class Font:
    def __init__(self, font_image_path: str,
                 divisor_color: pg.Color,
                 offset_color: pg.Color,
                 offset: int):
        """
        The image has to look like this:
        A B C D E F G H I J K L M N O P Q R S T U V W X Y Z a b c d e f g h i j k l m n o p q r s t u v w x y z 1 2 3 4 5 6 7 8 9 0 ( ) : ; " ' ? ! , . - + = _ $ # @ % ^ & * < > / \\ | ` ~ [ ] { }

        You can pass a file with missing letters, such that no letters after it are included (an error will be raised if you try to access non-existing letter in your file),
        then the program will just ignore it (but will raise an error, if you try to use a character that is not on the image)
        """
        self.all_letters = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz1234567890():;\"'?!,.-+=_$#@%^&*<>/\\|`~[]{}"
        self.image = pg.image.load(font_image_path).convert_alpha()
        self.letters_images = self.get_letters(divisor_color, offset_color, offset)
        self.offset = offset

    def get_letters(self, divisor_color: pg.Color, offset_color: pg.Color, offset: int) -> dict:
        letters = {}
        left_side_of_letter_pos = 0
        current_letter_idx = 0
        image_height = self.image.get_height()
        for x in range(self.image.get_width()):
            if self.image.get_at((x, 0)) == divisor_color:
                if self.image.get_at((x, image_height-1)) == offset_color:
                    letter_img_height = self.image.get_height()+offset
                    y = offset
                else:
                    letter_img_height = self.image.get_height()
                    y = 0

                letter_img = pg.Surface(((x-left_side_of_letter_pos), letter_img_height))
                letter_img.blit(self.image.subsurface((left_side_of_letter_pos, 0, (x-left_side_of_letter_pos), image_height)).copy(), (0, y))

                letters.update({self.all_letters[current_letter_idx]: letter_img})
                current_letter_idx += 1
                left_side_of_letter_pos = x+1  # +1 because the divisor color takes up 1 pixel of space

                if current_letter_idx == len(self.all_letters):
                    break

        letters.update({" ": pg.Surface((3, 1), pg.SRCALPHA)})

        return letters

    def render(self, text: str, scale_factor: int, draw_outline: bool) -> pg.Surface:
        letters = []
        total_width = 0

        for letter in text:
            letters.append(self.letters_images[letter])
            total_width += letters[-1].get_width()

        DA_IMAGE_YEAH = pg.Surface((total_width + len(text)+1, self.image.get_height()+self.offset))
        DA_IMAGE_YEAH.set_colorkey((0, 0, 0))
        left_border = 1

        for letter in letters:
            DA_IMAGE_YEAH.blit(letter, (left_border, 0))
            left_border += letter.get_width()+1

        if draw_outline:
            DA_IMAGE_YEAH = gm.draw_outline(DA_IMAGE_YEAH, 1)

        DA_IMAGE_YEAH = pg.transform.scale_by(DA_IMAGE_YEAH, scale_factor)

        return DA_IMAGE_YEAH
