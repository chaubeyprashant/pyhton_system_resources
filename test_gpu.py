import GPUtil

def test_gpu():
    try:
        gpus = GPUtil.getGPUs()
        if not gpus:
            print("No GPUs found")
        else:
            for gpu in gpus:
                print("GPU ID: {}, Name: {}, Load: {:.2f}%, Memory Utilization: {:.2f}%".format(gpu.id, gpu.name, gpu.load * 100, gpu.memoryUtil * 100))
    except Exception as e:
        print("Error: {}".format(e))

if __name__ == '__main__':
    test_gpu()
