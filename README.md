# csci580_public
create_world.py for robot localization with visualization


run from command line using python3

reads input from command line in the form of 

python3 createworld.py [World Width] [World Height] [No.Observations]

example command:

python3 create_world.py 20 10 10

would create a world size 20 wide by 10 tall

and gathers 10 observations of the robot from within this world

creates 3 files

test.in

input of the world for robot localization for a robot that can look in 8 directions

test.obs

observations of the robot that was placed into this world and wandered around for a bit

test.debug

the true route taking by the robot and other additional useful bits of info

optionally takes 1 additonal input [debug] to output info to console during run time

ie: python3 create_world.py 20 10 10 1
