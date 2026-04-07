import os
import cv2
import matplotlib.pyplot as plt
import numpy as np


def _cluster_wheels(wheels):
    """
    Agrupa rodas em eixos (axles) com base na distância entre elas.
    """
    if not wheels or len(wheels) < 2:
        return [1] * len(wheels)

    wheels.sort(key=lambda x: x[0])  # Ordenar por coordenada x

    clusters = [0] * len(wheels)
    current_cluster = 1

    for i in range(len(wheels) - 1):
        permissiveness = wheels[i][2] / wheels[i][3]

        dist = np.linalg.norm(
            np.array([wheels[i][0], wheels[i][1]]) -
            np.array([wheels[i + 1][0], wheels[i + 1][1]])
        )

        base_max = wheels[i][2] + (permissiveness * wheels[i][2])

        # evitar divisão por zero
        dx = np.abs(wheels[i][0] - wheels[i + 1][0])
        if dx == 0:
            dx = 1e-6

        threshold = base_max * dist / dx

        if dist > threshold:
            clusters[i] = current_cluster
            current_cluster += 1
            clusters[i + 1] = current_cluster
        else:
            clusters[i] = current_cluster
            clusters[i + 1] = current_cluster

    return clusters


def _build_bounding_boxes(wheels, clusters):
    """
    Cria bounding boxes para cada eixo a partir das rodas.
    """
    if not wheels or not clusters:
        return []

    bounding_boxes = []
    current_axle = 0

    for i in range(len(clusters)):
        if clusters[i] != current_axle:
            current_axle += 1
            bounding_boxes.append([
                [wheels[i][0] - wheels[i][2] / 2,
                 wheels[i][1] - wheels[i][3] / 2],
                [wheels[i][0] + wheels[i][2] / 2,
                 wheels[i][1] + wheels[i][3] / 2]
            ])
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


def cluster_axles(wheels):
    """
    Função principal que:
    - agrupa rodas em eixos
    - gera bounding boxes por eixo

    Retorna:
    {
        "clusters": [...],
        "bounding_boxes": [...]
    }
    """
    if wheels is None or len(wheels) == 0:
        raise ValueError("Lista de rodas vazia")

    clusters = _cluster_wheels(wheels)
    bounding_boxes = _build_bounding_boxes(wheels, clusters)

    return {
        "clusters": clusters,
        "bounding_boxes": bounding_boxes
    }


def show_axles(image_path, axles_data):
    """
    Exibe a imagem com bounding boxes dos eixos.

    axles_data deve ser o retorno de cluster_axles()
    """
    if not os.path.exists(image_path):
        raise FileNotFoundError(f"Imagem não encontrada: {image_path}")

    if "bounding_boxes" not in axles_data:
        raise ValueError("Formato inválido de dados de eixos")

    img = cv2.imread(image_path)

    if img is None:
        raise ValueError(f"Erro ao carregar imagem: {image_path}")

    h, w = img.shape[:2]
    img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

    for bounding_box in axles_data["bounding_boxes"]:
        cv2.rectangle(
            img,
            (
                int(float(bounding_box[0][0]) * w),
                int(float(bounding_box[0][1]) * h)
            ),
            (
                int(float(bounding_box[1][0]) * w),
                int(float(bounding_box[1][1]) * h)
            ),
            (255, 0, 0),
            2
        )

    plt.imshow(img)
    plt.axis("off")
    plt.show()


# Exemplo de uso
if __name__ == "__main__":
    wheels = [(0.791883, 0.184829, 0.016526, 0.113664),
              (0.776655, 0.195531, 0.018028, 0.118698),
              (0.720963, 0.230532, 0.022876, 0.127778),
              (0.699505, 0.244331, 0.019726, 0.128202),
              (0.678472, 0.258703, 0.020700, 0.132657),
              (0.609416, 0.305464, 0.024630, 0.145506),
              (0.586237, 0.323710, 0.026395, 0.151888),
              (0.494099, 0.382791, 0.029505, 0.162379)]

    image_path="/home/aria-unimed/axle-detection-herick/axle-clustering/images/noise_caminhao_682930408.png"


    axles_data = cluster_axles(wheels)
    show_axles(image_path, axles_data)