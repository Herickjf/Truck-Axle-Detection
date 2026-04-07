import os
import cv2
import matplotlib.pyplot as plt
import numpy as np


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
    bounding_boxes = []  # Lista de bounding_boxes
    current_axle = 0

    for i in range(len(clusters)):
        if clusters[i] != current_axle:  # Se o eixo quebrou
            current_axle += 1
            bounding_boxes.append([[wheels[i][0] - wheels[i][2] / 2,
                                    wheels[i][1] - wheels[i][3] / 2],
                                   [wheels[i][0] + wheels[i][2] / 2,
                                    wheels[i][1] + wheels[i][3] / 2]])  # Primeiro pneu
            continue

        lower_y = wheels[i][1] - wheels[i][3] / 2

        upper_x = wheels[i][0] + wheels[i][2] / 2
        upper_y = wheels[i][1] + wheels[i][3] / 2

        if lower_y < bounding_boxes[current_axle - 1][0][1]:
            bounding_boxes[current_axle - 1][0][1] = lower_y

        if upper_x > bounding_boxes[current_axle - 1][1][0]:
            bounding_boxes[current_axle - 1][1][0] = upper_x

        if upper_y > bounding_boxes[current_axle - 1][1][1]:
            bounding_boxes[current_axle - 1][1][1] = upper_y

    return bounding_boxes


def draw_bbox(image_path, bounding_boxes: list):
    if not os.path.exists(image_path):
        raise FileNotFoundError(f"Imagem não encontrada: {image_path}")

    img = cv2.imread(image_path)

    if img is None:
        raise ValueError(f"Erro ao carregar imagem: {image_path}")

    h, w = img.shape[:2]
    img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

    for bounding_box in bounding_boxes:
        cv2.rectangle(
            img,
            (
                int(float(bounding_box[0][0]) * w),
                int(float(bounding_box[0][1]) * h)
            ),  # (x_min, y_min)

            (
                int(float(bounding_box[1][0]) * w),
                int(float(bounding_box[1][1]) * h)
            ),  # (x_max, y_max)

            (255, 0, 0),
            2
        )

    plt.imshow(img)
    plt.axis("off")
    plt.show()

wheels = [(0.791883, 0.184829, 0.016526, 0.113664),
          (0.776655, 0.195531, 0.018028, 0.118698),
          (0.720963, 0.230532, 0.022876, 0.127778),
          (0.699505, 0.244331, 0.019726, 0.128202),
          (0.678472, 0.258703, 0.020700, 0.132657),
          (0.609416, 0.305464, 0.024630, 0.145506),
          (0.586237, 0.323710, 0.026395, 0.151888),
          (0.494099, 0.382791, 0.029505, 0.162379)]

image_path="/home/aria-unimed/axle-detection-herick/axle-clustering/images/noise_caminhao_682930408.png"

if __name__ == "__main__":
    clusters = axle_clustering(wheels)
    bounding_boxes = create_bounding_boxes(wheels, clusters)
    draw_bbox(image_path, bounding_boxes)