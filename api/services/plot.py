from azure.storage.blob import BlobServiceClient, BlobClient, ContainerClient
from constants.const import IMG_DIR, CONTAINER_NAME, BLOB_NAME
from matplotlib import pyplot as plt
import os


def store_graph(
        approximation_id: int,
        prefix: str, suffix: str,
        ind_var: str, IND_values: list[float],
        dep_var: str, DEP_values: list[float],
        func: str
) -> str | None:
    # Define la ruta donde se guardarán las imágenes
    if not os.path.exists(IMG_DIR):
        os.makedirs(IMG_DIR)

    # Define el nombre de la imagen
    image_name: str = f'{prefix}_{suffix}_{approximation_id}.png'
    path_url = f'{IMG_DIR}/{image_name}'
    # path_url = os.path.join(IMG_DIR, image_name)

    # Genera y guarda la gráfica
    plt.figure()
    plt.plot(IND_values, DEP_values, '#12CFE1')
    plt.grid()
    plt.xlabel(ind_var)  # New args
    plt.ylabel(f'{dep_var}({ind_var})')  # New args
    # plt.title(f'Solución de {func}, {dep_var}({eval_val})={x_0}')

    plt.savefig(path_url)
    plt.close()

    # Retorna la ruta relativa de la imagen
    return path_url


def store_graphs(
        approximation_id: int,
        prefix: str, suffix: str,
        ind_var: str, dep_var: str,
        data_euler: list[dict[str, float]],
        data_rk2: list[dict[str, float]],
        data_rk4: list[dict[str, float]],
        func: str
) -> str | None:
    # Define la ruta donde se guardarán las imágenes
    if not os.path.exists(IMG_DIR):
        os.makedirs(IMG_DIR)

    # Define el nombre de la imagen
    image_name: str = f'{prefix}_{suffix}_{approximation_id}.png'
    path_url = f'{IMG_DIR}/{image_name}'
    # path_url = os.path.join(IMG_DIR, image_name)

    # Genera y guarda la gráfica
    plt.figure()
    plt.plot(IND_values_euler, DEP_values, '#12CFE1')
    plt.grid()
    plt.xlabel(ind_var)  # New args
    plt.ylabel(f'{dep_var}({ind_var})')  # New args
    # ! plt.title('Solución de $\dot{x}=ax$, $x(0)=x_0$') # New args

    plt.savefig(path_url)
    plt.close()

    # Retorna la ruta relativa de la imagen
    return path_url


def upload_to_azure(blob_service_client, data):
    blob_client = blob_service_client.get_blob_client(
        container=CONTAINER_NAME, blob=BLOB_NAME
    )
    blob_client.upload_blob(data)
