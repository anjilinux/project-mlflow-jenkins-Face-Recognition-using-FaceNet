import os

def count_images(data_dir):
    stats = {}
    for person in os.listdir(data_dir):
        stats[person] = len(os.listdir(os.path.join(data_dir, person)))
    return stats

if __name__ == "__main__":
    print(count_images("data/raw"))
