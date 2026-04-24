import sh


def get_ram_usage():
    free = sh.free("-h")
    freelist = free.split('\n')
    lis = freelist[1].split()
    return lis[2].rstrip("Gi")


def get_disk_usage():
    df = sh.df("-h")
    df_list = df.split('\n')
    for i in df_list:
        if i.endswith("/"):
            ilist = i.split()
            disk_usage = ilist[2]
            return disk_usage.rstrip("Gi")

