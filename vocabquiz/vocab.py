from PIL import Image, ImageDraw, ImageFont
from random import randint
import cozmo
import time
import cozmo.lights as lights
from cozmo.util import degrees
def make_text_image(text_to_draw, x, y, font=None):
    '''Make a PIL.Image with the given text printed on it

    Args:
        text_to_draw (string): the text to draw to the image
        x (int): x pixel location
        y (int): y pixel location
        font (PIL.ImageFont): the font to use

    Returns:
        :class:(`PIL.Image.Image`): a PIL image with the text drawn on it
    '''

    # make a blank image for the text, initialized to opaque black
    text_image = Image.new('RGBA', cozmo.oled_face.dimensions(), (0, 0, 0, 255))

    # get a drawing context
    dc = ImageDraw.Draw(text_image)

    # draw the text
    dc.text((x, y), text_to_draw, fill=(255, 255, 255, 255), font=font)

    return text_image

question = ["pleasant", "delightful", "sad", "robotic", 1]
abc = ["","A.", "B.", "C."]
font = ImageFont.truetype("arial.ttf", 20)


def vocab(robot: cozmo.robot.Robot):
	cube1 = robot.world.get_light_cube(1)
	cube2 = robot.world.get_light_cube(2)
	cube3 = robot.world.get_light_cube(3)
	cubes = [None, cube1, cube2, cube3]

	robot.set_head_angle(degrees(180)).wait_for_completed()

	def generate(question):
		
		robot.say_text("Quiz starts").wait_for_completed()
		for i in range(4):
			img = make_text_image(abc[i]+question[i], 10, 6, font)
			face_data = cozmo.oled_face.convert_image_to_screen_data(img)
			display = robot.display_oled_face_image(face_data,5000.0,in_parallel = True)
			say = robot.say_text(abc[i]+"     "+question[i],in_parallel = True)
			
			display.wait_for_completed()
			say.wait_for_completed()
		robot.say_text("Please choose your answer").wait_for_completed()
		return question[-1]
	

	answ = generate(question)
	
	def object_tapped(evt, *, obj, tap_count, tap_duration, tap_intensity, **kwargs):
		print ("Tapped!", obj)
		if (obj == cubes[answ]):
			obj.set_lights(lights.green_light)
			robot.say_text("correct!").wait_for_completed()
		else:
			obj.set_lights(lights.red_light)
			robot.say_text("try again").wait_for_completed()
	
	robot.add_event_handler(cozmo.objects.EvtObjectTapped, object_tapped)

	time.sleep(30)

cozmo.run_program(vocab)
