import cozmo
from cozmo.util import degrees, Pose, distance_mm
import speech_recognition as sr



def cozmo_program(robot: cozmo.robot.Robot):
    def speech():
        recognizer = sr.Recognizer()
        microphone = sr.Microphone()
    
        with microphone as source:
            recognizer.adjust_for_ambient_noise(source)
    
        parsedText = ""
        print ("speak")
        robot.say_text("what is your answer").wait_for_completed()
        
        with microphone as source:
            voice = recognizer.listen(source, 5)
    
        parsedText = recognizer.recognize_google(voice)
    
        return parsedText
    
    a = robot.world.connect_to_cubes()
    
    cube1 = robot.world.get_light_cube(2)
    cube2 = robot.world.get_light_cube(1)
    cube3 = robot.world.get_light_cube(3)
    cubes = [cube1, cube2, cube3]
    
    #print (cube1)
    look_around = robot.start_behavior(cozmo.behavior.BehaviorTypes.LookAroundInPlace)
    c=robot.world.wait_until_observe_num_objects(num=3, object_type=cozmo.objects.LightCube, timeout=60)
    look_around.stop()
    numbs = ["five", "times", "eleven", "55"]
    for i in range(3):
        print ("==============="+str(i)+"------------------")
        #robot.go_to_pose(cubes[i].pose, relative_to_robot=False).wait_for_completed()]
        print (cubes[i])
        cubes[i].set_lights(cozmo.lights.red_light)
        #robot.go_to_object(cubes[i], distance_mm(70.0)).wait_for_completed()
        #robot.pickup_object(cubes[i]).wait_for_completed()
        current_action = robot.pickup_object(cubes[i], num_retries=3)
        current_action.wait_for_completed()
        if current_action.has_failed:
            code, reason = current_action.failure_reason
            result = current_action.result
            print("Pickup Cube failed: code=%s reason='%s' result=%s" % (code, reason, result))
            return
        robot.go_to_pose(Pose(200, 0-75*i, 0, angle_z=degrees(0)), relative_to_robot=False).wait_for_completed()
    
        robot.place_object_on_ground_here(cubes[i]).wait_for_completed()
        robot.say_text(numbs[i]).wait_for_completed()
    
    robot.turn_in_place(degrees(180))
    answ = speech()
    print (answ)
    if answ == numbs[3]:
        robot.say_text("Correct! very good", play_excited_animation=True).wait_for_completed()
        robot.play_anim_trigger(cozmo.anim.Triggers.MajorWin).wait_for_completed()
    else:
        robot.say_text("you are wrong").wait_for_completed()
        robot.play_anim_trigger(cozmo.anim.Triggers.CodeLabUnhappy).wait_for_completed()
cozmo.run_program(cozmo_program, use_viewer = True)