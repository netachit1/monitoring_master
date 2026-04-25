from email import message_from_binary_file

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


def total_disk():
    df = sh.df("-h")
    df_list = df.split('\n')
    for i in df_list:
        if i.endswith("/"):
            ilist = i.split()
            disk_usage = ilist[1]
            return disk_usage.rstrip("Gi")


def total_ram():
    free = sh.free("-h")
    freelist = free.split('\n')
    lis = freelist[1].split()
    return lis[1].rstrip("Gi")


def free_ram():
    free = sh.free("-h")
    freelist = free.split('\n')
    lis = freelist[1].split()
    return lis[3].rstrip("Gi")

get_ram_usage = get_ram_usage()
get_disk_usage = get_disk_usage()
get_total_disk = total_disk()
get_total_ram = total_ram()




def show_function():
    print (f"ram usage: {get_ram_usage}/{get_total_ram}")
    print (f"disk usage: {get_disk_usage}/{get_total_disk}")


if __name__ == '__main__':
    show_function()

