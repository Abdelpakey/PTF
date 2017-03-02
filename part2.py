import random
import numpy as np
import matplotlib.pyplot as plt

def sample_normal_distribution(b):
    sum = 0.0
    for i in xrange(12):
        sum += random.uniform(-b, b)
    return sum / 2.0

def sample_motion_model(u, pose):
    delta_rot_1, delta_rot_2, delta_trans = u
    x, y, theta = pose

    delta_rot_1_hat = delta_rot_1 + sample_normal_distribution(alpha_1 * abs(delta_rot_1) + alpha_2 * delta_trans)
    delta_rot_2_hat = delta_rot_2 + sample_normal_distribution(alpha_1 * abs(delta_rot_2) + alpha_2 * delta_trans)
    delta_trans_hat = delta_trans + sample_normal_distribution(
        alpha_3 * delta_trans + alpha_4 * (abs(delta_rot_1) + abs(delta_rot_2)))

    x_new = x + delta_trans_hat * np.cos(theta + delta_rot_1_hat)
    y_new = y + delta_trans_hat * np.sin(theta + delta_rot_1_hat)
    theta_new = theta + delta_rot_1_hat + delta_rot_2_hat

    return [x_new, y_new, theta_new]

def update_pose(u, pose):
    delta_rot_1, delta_rot_2, delta_trans = u
    x, y, theta = pose
    x_new = x + delta_trans * np.cos(theta + delta_rot_1)
    y_new = y + delta_trans * np.sin(theta + delta_rot_1)
    theta_new = theta + delta_rot_1 + delta_rot_2
    return [x_new, y_new, theta_new]


alpha = 0.2
alpha_1 = alpha
alpha_2 = alpha
alpha_3 = alpha
alpha_4 = alpha

n_particles = 200
init_pose = [6., 5., 0.]
odom_commands = [
    [0, 0, 2],
    [0, 0, 2],
    [0, 0, 2],
    [np.pi / 2.0, 0, 2],
    [0, 0, 2],
    [0, 0, 2],
    [np.pi / 2.0, 0, 2],
    [0, 0, 2],
    [0, 0, 2],
    [0, 0, 2],
    [0, 0, 2]
]
shown_odom_ids = range(1, 12)
random.seed()

particle_poses = []
for particle_id in xrange(n_particles):
    particle_poses.append(init_pose)

true_poses = [init_pose]
odom_id = 0
# plt.hold(True)
for u in odom_commands:
    for particle_id in xrange(n_particles):
        particle_poses[particle_id] = sample_motion_model(u, particle_poses[particle_id])

    odom_id += 1
    true_poses.append(update_pose(u, true_poses[odom_id - 1]))

    prev_x, prev_y = true_poses[odom_id - 1][0:2]
    curr_x, curr_y = true_poses[odom_id][0:2]

    plt.plot([prev_x, curr_x], [prev_y, curr_y], color=[0, 0, 0])
    if odom_id in shown_odom_ids:
        plt.scatter(np.array(particle_poses)[:, 0], np.array(particle_poses)[:, 1], s=0.2, color=[1, 0, 0])
plt.xlim([0, 15])
plt.ylim([0, 15])
plt.xlabel('x')
plt.ylabel('y')
plt.title('Pose estimation with alpha = {:f}'.format(alpha))
plt.show()







