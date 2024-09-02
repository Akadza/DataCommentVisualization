import numpy as np
# сохранение расчета эмбеддинга для комментариев
def saveVecToBin(file_path: str, vectors):
    np.save(file_path, vectors)

# загрузка расчета эмбеддинга для комментариев
def loadVecFromBin(file_path: str):
    return np.load(file_path)

