"""
该脚本是基于待删除的批次列表txt，进行相关路径下的大量文件的删除，主要包含以下处理：
1）删除前，统计批次路径下各个part对应的文件数
2）通过"rsync"命令删除整个文件夹，比"rm -rf"命令要快很多
"""

import os
import subprocess as sp
from concurrent.futures import ThreadPoolExecutor
from multiprocessing import Pool



def get_cnt_of_part(path):
    res = sp.Popen(f"find {path} -type f | wc -l", shell=True, stout=sp.PIPE, stderr=sp.PIPE)
    print(f"\n ##{path}##file_number: {res.communicate()[0].decode('utf-8')}\n")


def stats_worker(path):
    part_list = os.listdir(path)
    part_list = list(filter(lambda x: x.startswith("part-"), part_list))
    with ThreadPoolExecutor(max_workers=100) as tp:
        tasks = [tp.submit(get_cnt_of_part, os.path.join(path, part)) for part in part_list]


def del_worker(pici_name):
    print(f"1111 {pici_name} start...")
    root_video_json_save_path = f"/sora3/Result/{pici_name}/CroppedVideos/"

    recode = 999
    if os.path.exists(root_video_json_save_path):
        print(f"11@ {root_video_json_save_path}")
        stats_worker(root_video_json_save_path)
        cmd = f"rsync --delete-before -d /sora3/Users/l30053295/tmp/replaceDIR/ {root_video_json_save_path}"
        ret = sp.run(cmd, shell=True, stdout=sp.PIPE, stderr=sp.PIPE)
        recode = ret.returncode

    print(f"\n2222 {pici_name} recode={recode} end...\n")


if __name__ == '__main__':
    with open("./to_be_del_list.txt", 'r', encoding="utf-8") as p_file:
        to_be_deal_batch_list = list(map(str.strip, p_file.readlines()))
        to_be_deal_batch_list = [b for b in to_be_deal_batch_list if (b is not None and b != "")]

    with Pool(30) as pool:
        pool.map(del_worker, to_be_deal_batch_list)