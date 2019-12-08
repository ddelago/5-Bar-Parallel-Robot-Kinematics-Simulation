import sys
import math
import matplotlib.pyplot as plt

l0 = 4.05  # Length between origin and the two motors
l1 = 8.05 # Length from motor to passive joints
l2 = 12.05 # Length from passive joints to end effector

def calc_angles(x, y):
    # Angle from left shoulder to end effector
    beta1 = math.atan2( y, (l0 + x) )

    # Angle from right shoulder to end effector
    beta2 = math.atan2( y, (l0 - x) )

    # Alpha angle pre-calculations
    alpha1_calc = (l1**2 + ( (l0 + x)**2 + y**2 ) - l2**2) / (2*l1*math.sqrt( (l0 + x)**2 + y**2 ))  
    alpha2_calc = (l1**2 + ( (l0 - x)**2 + y**2 ) - l2**2) / (2*l1*math.sqrt( (l0 - x)**2 + y**2 ))  

    # If calculations > 1, will fail acos function
    if alpha1_calc > 1 or alpha2_calc > 1:
        print("Unreachable coordinates")
        quit()

    # Angle of left shoulder - beta1 and right shoulder - beta2
    alpha1 = math.acos(alpha1_calc)
    alpha2 = math.acos(alpha2_calc)

    # Angles of left and right shoulders
    shoulder1 = beta1 + alpha1
    shoulder2 = math.pi - beta2 - alpha2
    
    return(shoulder1, shoulder2)

def plot_arms(shoulder1, shoulder2, efx, efy):
    # Passive joints (x, y) location
    p1 = ( -l0 + l1*math.cos(shoulder1), l1*math.sin(shoulder1)  )
    p2 = ( l0 + l1*math.cos(shoulder2), l1*math.sin(shoulder2)  )

    # Left arm
    plt.plot([-l0, p1[0], efx], [0, p1[1], efy], 'bo-')
    plt.text(-l0+0.3, 0+0.3, "{:.2f} degrees".format(math.degrees(shoulder1)))
    plt.text(p1[0]+0.3, p1[1]+0.3, "({:.2f}, {:.2f})".format(p1[0], p1[1]))

    # Right arm
    plt.plot([l0, p2[0], efx], [0, p2[1], efy], 'bo-')
    plt.text(l0+0.3, 0+0.3, "{:.2f} degrees".format(math.degrees(shoulder2)))
    plt.text(p2[0]+0.3, p2[1]+0.3, "({:.2f}, {:.2f})".format(p2[0], p2[1]))

    # EF
    plt.plot(efx, efy, 'ro')
    plt.text(efx+0.3, efy+0.3, "({:.2f}, {:.2f})".format(efx, efy))

def plot_plot(efx, efy):
    plt.title('5-Bar Parallel Robot Kinematics')
    plt.plot(-15, -4, 'bo')
    plt.plot(15, 15, 'bo')

    s1, s2 = calc_angles(efx, efy)
    plot_arms(s1, s2, efx, efy)
    plt.draw()
    plt.pause(.01)
    plt.clf()

if __name__ == "__main__":
    # End effector coordinates
    # x, y = float(sys.argv[1]), float(sys.argv[2])
    # s1, s2 = calc_angles(x, y)

    while True:
        for i in range(-5, 6):
            plot_plot(i, 10)
        for j in range(10, 16):
            plot_plot(i, j)
        for k in range(5, -6, -1):
            plot_plot(k, j)
        for l in range(15, 10, -1):
            plot_plot(k, l)