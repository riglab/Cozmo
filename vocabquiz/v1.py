from PIL import Image, ImageDraw, ImageFont
from random import randint
import cozmo
import time
import cozmo.lights as lights
from cozmo.util import degrees

class vocabquiz:
	cho = ["Choose the synonym for   ","","",""]
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
		self.choice = [None, None]
		
	def main(self):
		
		self.cozmo.play_anim_trigger(cozmo.anim.Triggers.MeetCozmoFirstEnrollmentCelebration).wait_for_completed()
		self.cozmo.set_head_angle(degrees(180)).wait_for_completed()
		'''
		self.cozmo.play_anim_trigger(cozmo.anim.Triggers.MemoryMatchPlayerWinGame).wait_for_completed()
		self.cozmo.play_anim_trigger(cozmo.anim.Triggers.MajorWin).wait_for_completed()
		
		self.cozmo.play_anim_trigger(cozmo.anim.Triggers.ConnectWakeUp).wait_for_completed()
		self.cozmo.play_anim_trigger(cozmo.anim.Triggers.CodeLabVictory).wait_for_completed()
		'''
		
		self.cozmo.say_text("Hello %s and %s. My name is Cozmo. Welcome to the word quiz!" 
			%(self.players[0],self.players[1]), duration_scalar = 1.5, voice_pitch = 0.5).wait_for_completed()
				
		time.sleep(2) 
		self.generate(self.question)
		self.ask()
		

	def determine(self):
		if self.choice[0] == self.choice[1]:
			self.cozmo.say_text("Wow! You guys have the same answer! Let's check if it's correct", duration_scalar = 1.5,).wait_for_completed()
			if self.cubes.index(self.choice[0]) == self.question[-1]:
				self.cozmo.say_text("Correct! Congradulations", duration_scalar = 1.5, play_excited_animation=True).wait_for_completed()
				self.cozmo.play_anim_trigger(cozmo.anim.Triggers.CodeLabVictory).wait_for_completed()
				for i in range(4):
					self.cubes[self.question[-1]].set_lights(green_light)
					time.sleep(2)
					self.cubes[self.question[-1]].set_lights_off()
					
			else:
				self.cozmo.say_text("Oh no. How about you guys try again?", duration_scalar = 1.5,).wait_for_completed()
				self.ask()
		else:
			self.cozmo.say_text("You guys have different answers. Discuss and try again", duration_scalar = 1.5,).wait_for_completed()
			self.cozmo.play_anim_trigger(cozmo.anim.Triggers.CodeLabVictory).wait_for_completed()
			time.sleep(10) 
			self.ask()
		return
	def ask(self):
		for i in range(1,4):
			self.cubes[i].set_lights_off()
		self.turn_to_ask(0)
		self.handler_1()
		self.turn_to_ask(1)
		self.handler_2()
		self.determine()
	def handler_1(self):
		def object_tapped_1(evt, *, obj, tap_count, tap_duration, tap_intensity, **kwargs):
			print ("Tapped!", obj)
			self.choice[0] = obj
			
			obj.set_lights(lights.red_light)
			i = self.cubes.index(obj)
			self.cozmo.say_text("%s chose %s" %(self.players[0],self.abc[i]+self.question[i]), in_parallel = True).wait_for_completed()
				#self.cozmo.say_text("try again").wait_for_completed()
			print ("=========================================================")
			self.cozmo.turn_in_place(degrees(-45), in_parallel = True).wait_for_completed()
		self.cozmo.add_event_handler(cozmo.objects.EvtObjectTapped, object_tapped_1)
		
		time.sleep(10)
		self.cozmo.remove_event_handler(cozmo.objects.EvtObjectTapped, object_tapped_1)
		return

	def handler_2(self):
		def object_tapped_2(evt, *, obj, tap_count, tap_duration, tap_intensity, **kwargs):
			print ("Tapped!", obj)
			self.choice[1] = obj
			
			obj.set_lights(lights.blue_light)
			i = self.cubes.index(obj)
				#self.cozmo.say_text("correct!").wait_for_completed()
			
				#self.cozmo.say_text("try again").wait_for_completed()
			self.cozmo.say_text("%s chose %s" %(self.players[1],self.abc[i]+self.question[i]), in_parallel = True).wait_for_completed()
				#self.cozmo.say_text("try again").wait_for_completed()
			print ("--------------------------------------------------------")
			self.cozmo.turn_in_place(degrees(45), in_parallel = True).wait_for_completed()

		self.cozmo.add_event_handler(cozmo.objects.EvtObjectTapped, object_tapped_2)
		
		time.sleep(10)
		self.cozmo.remove_event_handler(cozmo.objects.EvtObjectTapped, object_tapped_2)
		return
	def turn_to_ask(self, player):
		if player == 0:
			self.cozmo.turn_in_place(degrees(45)).wait_for_completed()
			self.cozmo.play_anim_trigger(cozmo.anim.Triggers.CodeLabHappy).wait_for_completed()
			self.cozmo.set_head_angle(degrees(180)).wait_for_completed()
			self.cozmo.say_text("Now  %s, please choose your answer" %(self.players[0]), duration_scalar = 1.5,).wait_for_completed()
		else:
			self.cozmo.turn_in_place(degrees(-45)).wait_for_completed()
			self.cozmo.play_anim_trigger(cozmo.anim.Triggers.CodeLabHappy).wait_for_completed()
			self.cozmo.set_head_angle(degrees(180)).wait_for_completed()
			self.cozmo.say_text("Now  %s, please choose your answer" %(self.players[1]), duration_scalar = 1.5,).wait_for_completed()

	def generate(self, question):
		
		self.cozmo.say_text("Quiz starts", duration_scalar = 1.5,).wait_for_completed()
		for i in range(4):
			img = make_text_image(self.abc[i]+self.question[i], 10, 6, self.font)
			face_data = cozmo.oled_face.convert_image_to_screen_data(img)
			display = self.cozmo.display_oled_face_image(face_data,5000.0,in_parallel = True)
			say = self.cozmo.say_text(self.cho[i] + self.abc[i]+"     "+self.question[i],in_parallel = True)
			
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
	