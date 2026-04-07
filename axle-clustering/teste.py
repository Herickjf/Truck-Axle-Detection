import cv2
import matplotlib.pyplot as plt
import numpy as np

# class Point:
#     def __init__(self, x, y):
#         self.x_center = x
#         self.y_center = y

# class Wheel:
#     def __init__(self, x, y, width):
#         self.center = Point(x, y)
#         self.width = width

# class Axle:
#     def __init__(self, point: Point, first_wheel: Wheel):
#         self.first_point = point
#         self.wheels = [first_wheel]
    

def axle_clustering(wheels):
    wheels.sort(key=lambda x: x[0])  # Ordenar por coordenada x
    
    clusters = [0] * len(wheels) # Lista de indicadores de axles
    current_cluster = 1

    for i in range(len(wheels) - 1):
        permissiveness = wheels[i][2] / wheels[i][3]

        dist = np.linalg.norm(np.array([wheels[i][0], wheels[i][1]]) - 
                              np.array([wheels[i + 1][0], wheels[i + 1][1]])) # Distância entre pontos centrais
        
        base_max = wheels[i][2] + (permissiveness * wheels[i][2]) # Base do triângulo de permissivade

        threshold = base_max * dist / np.abs(wheels[i][0] - wheels[i + 1][0]) # Maior distância permitida
    
        # Pneus estão em eixos diferentes
        if dist > threshold:
            clusters[i] = current_cluster
            current_cluster += 1 # Quebra o axle
            clusters[i + 1] = current_cluster
            
        # Pneus estão no mesmo eixo
        else:
            clusters[i] = current_cluster
            clusters[i + 1] = current_cluster

    return clusters

def create_bounding_boxes(wheels, clusters):
    bounding_boxes = [] # Lista de bounding_boxes
    current_axle = 0

    for i in range(len(clusters)):
        if clusters[i] != current_axle: # Se o eixo quebrou
            current_axle += 1
            bounding_boxes.append([(wheels[i][0] - wheels[i][2] / 2,
                                    wheels[i][1] + wheels[i][3] / 2),
                                    (wheels[i][0] + wheels[i][2] / 2,
                                     wheels[i][1] - wheels[i][3] / 2)]) # Primeiro pneu
            
            continue

        upper_y = wheels[i][1] + wheels[i][3] / 2

        lower_x = wheels[i][0] + wheels[i][2] / 2
        lower_y = wheels[i][1] - wheels[i][3] / 2
        
        if upper_y > bounding_boxes[current_axle - 1][0][1]:
            bounding_boxes[current_axle - 1][0][1] = upper_y
        
        if lower_x > bounding_boxes[current_axle - 1][0][0]:
            bounding_boxes[current_axle - 1][0][1] = upper_y
        
        if upper_y > bounding_boxes[current_axle - 1][0][1]:
            bounding_boxes[current_axle - 1][0][1] = upper_y

        

def draw_bbox_notebook(image_path, p1, p2):
    img = cv2.imread(image_path)
    img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

    x_min, y_min = map(int, p1)
    x_max, y_max = map(int, p2)

    cv2.rectangle(img, (x_min, y_min), (x_max, y_max), (255, 0, 0), 2)

    plt.imshow(img)
    plt.axis("off")
    plt.show()







# 0  0.791883  0.184829  0.016526  0.113664
# 0  0.776655  0.195531  0.018028  0.118698
# 0  0.720963  0.230532  0.022876  0.127778
# 0  0.699505  0.244331  0.019726  0.128202
# 0  0.678472  0.258703  0.020700  0.132657
# 0  0.609416  0.305464  0.024630  0.145506
# 0  0.586237  0.323710  0.026395  0.151888
# 0  0.494099  0.382791  0.029505  0.162379

# wheels = [(0.791883, 0.184829, 0.016526, 0.113664),
#           (0.776655, 0.195531, 0.018028, 0.118698),
#           (0.720963, 0.230532, 0.022876, 0.127778),
#           (0.699505, 0.244331, 0.019726, 0.128202),
#           (0.678472, 0.258703, 0.020700, 0.132657),
#           (0.609416, 0.305464, 0.024630, 0.145506),
#           (0.586237, 0.323710, 0.026395, 0.151888),
#           (0.494099, 0.382791, 0.029505, 0.162379)]

# 0 0.310897 0.557336 0.032452 0.230057
# 0 0.238501 0.419729 0.022035 0.220798
# 0 0.216146 0.380910 0.022443 0.204416
# 0 0.155692 0.269892 0.016110 0.178908
# 0 0.141369 0.243217 0.015542 0.170148

wheels = [(0.310897, 0.557336, 0.032452, 0.230057), 
          (0.238501, 0.419729, 0.022035, 0.220798), 
          (0.216146, 0.380910, 0.022443, 0.204416), 
          (0.155692, 0.269892, 0.016110, 0.178908), 
          (0.141369, 0.243217, 0.015542, 0.170148)]


if __name__ == "__main__":
    clusters = axle_clustering(wheels)
    print(clusters)