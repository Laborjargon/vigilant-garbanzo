import numpy as np
import matplotlib.pyplot as plt

# Define the L-system rules
def apply_rules(axiom, rules):
    return ''.join(rules.get(char, char) for char in axiom)

# Generate the L-system sequence
def generate_l_system(axiom, rules, iterations):
    l_system = axiom
    for _ in range(iterations):
        l_system = apply_rules(l_system, rules)
    return l_system

# Interpret the L-system sequence to draw lines
def interpret_l_system(l_system, angle):
    current_angle = 0
    stack = []
    points = [(0, 0)]
    for char in l_system:
        if char == 'F':
            x, y = points[-1]
            new_x = x + np.cos(np.radians(current_angle))
            new_y = y + np.sin(np.radians(current_angle))
            points.append((new_x, new_y))
        elif char == '+':
            current_angle += angle
        elif char == '-':
            current_angle -= angle
        elif char == '[':
            stack.append((points[-1], current_angle))
        elif char == ']':
            points.append(stack[-1][0])
            current_angle = stack[-1][1]
            stack.pop()
    return points

# Define the axiom and rules for the L-systems
axiom = 'F'
rules = {'F': 'FF[+FF][-F]'}

# Generate the L-system sequences
iterations = 5
angles = np.arange(0, 45, 1)  # Angles for interpretation such an array [33, 35, 37, 39, 41, 43]

# Choose a colormap
cmap = plt.get_cmap('viridis')

# Plot the L-systems one at a time in a loop
plt.figure(figsize=(6, 4))
for i, angle in enumerate(angles):
    plt.clf()  # Clear the previous plot
    l_system = generate_l_system(axiom, rules, iterations)
    points = interpret_l_system(l_system, angle)
    x, y = zip(*points)
    color = cmap(i / len(angles))  # Interpolating color across the colormap
    plt.plot(x, y, color=color, label=f'Angle {angle}°')
    plt.title('L-systems with Different Angles')
    plt.axis('off')
    plt.draw()
    plt.pause(0.01)

plt.show()
