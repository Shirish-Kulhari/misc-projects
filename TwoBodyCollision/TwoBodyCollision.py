"""
See the simulate() function for the main docstring
"""

from fractions import Fraction

def updateVelocities(mass, velocity, position):
  """
  Looks at the current configuration of the blocks and updates velocities.
  
  By "collision", we mean that either the position of both the objects is the
  same (both collide against each other) or the position of the small block is
  0 (collision against wall)
  """
  if(position[0] == position[1] != 0):
    # Both blocks collide against each other
    temp = velocity[0]
  
    velocity[0] = Fraction(((2*mass[1]*velocity[1])+(mass[0]*velocity[0])-
                  (mass[1]*velocity[0])), (mass[0] + mass[1]))
    
    velocity[1] = Fraction(((2*mass[0]*temp)+(mass[1]*velocity[1])-
                  (mass[0]*velocity[1])), (mass[0] + mass[1]))
    
  elif(position[0] == 0 != position[1]):
    # The small block gets "reflected" off the wall
    velocity[0] = Fraction(-velocity[0], 1)
    
  elif(position[0] == position[1] == 0):
    # The rare instance in which both blocks move towards the wall and
    # collide with the wall and against each other simultaneously
    velocity[0], velocity[1] = Fraction(-velocity[0], 1), Fraction(
                              -velocity[1], 1)
  else:
    pass


def timeToNextCollision(velocity, position):
  """
  Given the current positions and velocities, find the time to next collision.
  """
  if(velocity[1] >= velocity[0] >= 0):
    # Both blocks move towards right, but the large block is faster and the
    # small block can't catch up
    return -1
  
  elif(velocity[0] >= 0 >= velocity[1]):
    # Both blocks are either moving towards each other, or one of the is at
    # rest and the other is moving towards it. The wall is obviously ignored
    # The condition velocity[0] == 0 == velocity[1] will also be ignored
    # since if that's true, only the first if statement would be executed.
    return Fraction(position[1] - position[0],
                    velocity[0] - velocity[1])
  
  elif((velocity[1] >= 0 > velocity[0]) or (velocity[0] <= velocity[1] < 0)):
    # Both blocks move towards left, but the large block can't catch up with
    # the small block before the latter runs into the wall
    return Fraction(-position[0], velocity[0])
  
  elif(position[0] == 0):
    # Special case for when the small block is currently at the wall
    if(velocity[1] >= abs(velocity[0])):
      # Small block can no longer catch up with large block
      return -1
    else:
      # Large block is either moving towards left or too slow moving towards
      # the right. In either case, they will collide
      return Fraction(position[1], (abs(velocity[0]) - velocity[1]))
  else:
    # Both blocks move towards left, but large block is faster. If the
    # distance between blocks is small enough compared to that between the wall
    # and the small block, they will collide. Otherwise the small block will
    # reach the wall before the large block has a chance to catch up
    return min(Fraction(-position[0], velocity[0]),
               Fraction((position[1] - position[0]), 
                       (velocity[0] - velocity[1])))
    
def getInputs():
  """ Receives inputs specifying initial conditions. """
  print("\nPlease enter INTEGER VALUES ONLY (negative values of mass will")
  print("be automatically converted to positive). Default values:\n")
  print("Small mass: 1. Large mass: 10000.\nSmall block velocity = ", end = "")
  print("0. Large block velocity = -1.\nSmall block position = 1.", end = "")
  print(" Large block position = 2.")
  str = " [<Enter> to use default value]: "
  try:
    mass = [abs(int(input("Mass of smaller block"+str) or "1")), 
            abs(int(input("Mass of larger block"+str) or "10000"))]
    velocity = [int(input("Velocity of smaller block"+str)
            or "0"), int(input("Velocity of larger block"+str) or "-1")]
    position = [int(input("Position of smaller block"+str)
            or "1"), int(input("Position of larger block"+str) or "2")]
    return mass, velocity, position
  except:
    return [], [], []

def simulate():
  """
  Based on the following video by 3Blue1Brown:
  https://www.youtube.com/watch?v=HEfHFsfGXjs
  
  Simulates a two-body collision to approximate the value of Pi. Consider the
  positive x-axis as a frictionless floor and the positive y-axis as a wall.
  
  Given two blocks at y=0 with user-specified masses, initial x-axis positions 
  and initial horizontal velocities, this function finds the total number of
  perfectly elastic collisions that can happen.
  
  If:
    0 < small block's position < large block's position,
    the small block has UNIT mass, 
    the large block's mass equals the n-th power of 100,
    the large block has a sufficiently large velocity towards the left with
    respect to the small block,
    
  then the total number of collisions should equal floor(Pi*(10^n)).
  
  Thanks to Quuxplusone from Code Review stackexchange for suggesting a
  substantial performance improvement as well as helpful tweaks.

  [ https://codereview.stackexchange.com/users/16369/quuxplusone ]
  [ https://codereview.stackexchange.com/questions/211882/
   simulating-a-two-body-collision-problem-to-find-digits-of-pi ]
  """
  mass, velocity, position = getInputs()
  if(not(mass and velocity and position)):
    print("Invalid input(s). Exiting...")
    return
  collisionCount = 0
  
  print("\nPlease wait...")
  while True:
    t = timeToNextCollision(velocity, position)
    if(t == -1):
      # No more collisions
      break
    # Update the distances to what they'll be during the next collision
    position[0] += velocity[0]*t
    position[1] += velocity[1]*t
            
    # Update collision count and velocities to post-collision values
    if(position == [0, 0]):
      # Extra collision counted when both blocks simultaneously reach the wall
      # and bounce off it and each other
      collisionCount += 1
    collisionCount += 1
    updateVelocities(mass, velocity, position)
    
    # Limit the value that the numerator and denominator can take to prevent
    # them from blowing up and slowing down the program. Thanks to Quuxplusone
    # (https://codereview.stackexchange.com/users/16369/quuxplusone) for
    # suggesting this
    position[0] = position[0].limit_denominator(2**32)
    position[1] = position[1].limit_denominator(2**32)
    velocity[0] = velocity[0].limit_denominator(2**32)
    velocity[1] = velocity[1].limit_denominator(2**32)
  print("--------------------------\nTotal number of collisions:", 
        collisionCount)
  return collisionCount

if __name__ == "__main__":
  simulate()
