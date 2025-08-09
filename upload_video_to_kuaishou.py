import asyncio
from pathlib import Path

from conf import BASE_DIR
from uploader.ks_uploader.main import ks_setup, KSVideo
from utils.files_times import generate_schedule_time_next_day, get_title_and_hashtags, generate_schedule_time, time_contorller

"""
if __name__ == '__main__':
    filepath = Path(BASE_DIR) / "videos"
    account_file = Path(BASE_DIR / "cookies" / "ks_uploader" / "account.json")
    # 获取视频目录
    folder_path = Path(filepath)
    # 获取文件夹中的所有文件
    files = list(folder_path.glob("*.mp4"))
    file_num = len(files)
    publish_datetimes = generate_schedule_time(file_num, daily_times=[6, 10, 16])
    cookie_setup = asyncio.run(ks_setup(account_file, handle=False))
    #for index, file in enumerate(files):
    #    title, tags = get_title_and_hashtags(str(file))
    #    # 打印视频文件名、标题和 hashtag
    #    print(f"视频文件名：{file}")
    #    print(f"标题：{title}")
    #    print(f"Hashtag：{tags}")
    #    app = KSVideo(title, file, tags, publish_datetimes[index], account_file)
    #    asyncio.run(app.main(), debug=False)
    for file in enumerate(files):
        title, tags = get_title_and_hashtags(str(file))
        # 打印视频文件名、标题和 hashtag
        print(f"视频文件名：{file}")
        print(f"标题：{title}")
        print(f"Hashtag：{tags}")
        app = KSVideo(title, file, tags, publish_datetimes, account_file)
        asyncio.run(app.main(), debug=False)
"""
#if __name__ == '__main__':
#    folderpath = Path(BASE_DIR) / "videos"
#    folder_path = Path(folderpath)
#    folders = [f for f in folder_path.glob("*") if f.is_dir()]
#    account_file = Path(BASE_DIR / "cookies" / "ks_uploader" / "account.json")
#    for num in range(len(folders)) :
#        filepath_son = Path(BASE_DIR) / "videos" / f"{num}"
#        folder_path_son = Path(filepath_son)
#        files_son = list(folder_path_son.glob("*.mp4"))
#        file_num_son = len(files_son)
#        publish_datetimes = generate_schedule_time(file_num_son, file_num_son, daily_times=[6, 10, 16])
#        cookie_setup = asyncio.run(ks_setup(account_file, handle=False))
#        for file in files_son:
#            title, tags = get_title_and_hashtags(str(file))
#            # 打印视频文件名、标题和 hashtag
#            print(f"视频文件名：{file}")
#            print(f"标题：{title}")
#            print(f"Hashtag：{tags}")
#            app = KSVideo(title, file, tags, publish_datetimes, account_file)
#            asyncio.run(app.main(), debug=False)

if __name__ == "__main__":
    base_folder = Path(BASE_DIR) / "videos"
    folders = sorted(
        [f for f in base_folder.glob("*") if f.is_dir() and f.name.isdigit()],
        key=lambda f: int(f.name)
    )
    account_file = Path(BASE_DIR / "cookies" / "ks_uploader" / "account.json")
    if not folders:
        print("没有找到视频文件夹，程序退出。")
    else:
        print(f"找到了 {len(folders)} 个文件夹，正在为它们生成时间表...")
        publish_datetimes = time_contorller(len(folders), 6, 1, daily_times=[6, 10, 16])
        print("时间表生成完毕。")
        print(publish_datetimes)
        print("\n正在执行一次性的 Cookie 设置...")
        cookie_setup = asyncio.run(ks_setup(account_file, handle=False))
        print("设置完成。")
        print("\n开始上传流程...")
        for folder, publish_time in zip(folders, publish_datetimes):
            video_files = list(folder.glob("*.mp4"))
            if not video_files:
                print(f"!!! 警告: 在文件夹 '{folder.name}' 中未找到 .mp4 文件，已跳过。")
                continue
            video_file = video_files[0]
            title, tags = get_title_and_hashtags(str(video_file))
            print(f"正在处理: {video_file.name} (来自文件夹 {folder.name})")
            print(f"分配的发布时间: {publish_time.strftime('%Y-%m-%d %H:%M')}")
            app = KSVideo(title, video_file, tags, publish_datetimes, account_file)
            asyncio.run(app.main(), debug=False)
        print(f"已完成上传 {video_file.name}。")