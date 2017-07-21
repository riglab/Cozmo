from PIL import Image, ImageDraw, ImageFont
from random import randint
import cozmo
import time
import cozmo.lights as lights
from cozmo.util import degrees

class vocabquiz:
	abc = ["","A.", "B.", "C."]
	font = ImageFont.truetype("arial.ttf", 20)
	def __init__(self, coz):
		self.cozmo = coz
		self.question = ["pleasant", "delightful", "sad", "robotic", 1]
		self.players = ["Houston", "Hamish"]
		cube1 = self.cozmo.world.get_light_cube(1)
		cube2 = self.cozmo.world.get_light_cube(2)
		cube3 = self.cozmo.world.get_light_cube(3)
		self.cubes = [None, cube1, cube2, cube3]
	
	def main(self):
		self.cozmo.set_head_angle(degrees(180)).wait_for_completed()
		

		answ = self.generate(self.question)

		
		def object_tapped(evt, *, obj, tap_count, tap_duration, tap_intensity, **kwargs):
			print ("Tapped!", obj)
			if (obj == self.cubes[answ]):
				obj.set_lights(lights.green_light)
				self.cozmo.say_text("correct!").wait_for_completed()
			else:
				obj.set_lights(lights.red_light)
				self.cozmo.say_text("try again").wait_for_completed()

		self.cozmo.add_event_handler(cozmo.objects.EvtObjectTapped, object_tapped)

		time.sleep(30)

	

	def generate(self, question):
		
		self.cozmo.say_text("Quiz starts").wait_for_completed()
		for i in range(4):
			img = make_text_image(self.abc[i]+self.question[i], 10, 6, self.font)
			face_data = cozmo.oled_face.convert_image_to_screen_data(img)
			display = self.cozmo.display_oled_face_image(face_data,5000.0,in_parallel = True)
			say = self.cozmo.say_text(self.abc[i]+"     "+self.question[i],in_parallel = True)
			
			display.wait_for_completed()
			say.wait_for_completed()

		#self.cozmo.say_text("Please choose your answer").wait_for_completed()
		return question[-1]


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

def run(coz_conn):
	'''The run method runs once Cozmo is connected.'''
	coz = coz_conn.wait_for_robot()

	# Turn on image receiving by the camera
	coz.camera.image_stream_enabled = True

	session = vocabquiz(coz)
	session.main()

if __name__ == '__main__':
	cozmo.setup_basic_logging()
	
	cozmo.connect(run)
	