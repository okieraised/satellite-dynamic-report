import os


def list_file_with_same_ext(dir_name: str, ext: str) -> [str]:

    res: [str] = []
    for file in os.listdir(dir_name):
        if file.endswith(ext):
            res.append(os.path.join(dir_name, file))

    return res
