import asyncio
from pathlib import Path

from conf import BASE_DIR
from uploader.tencent_uploader.main import weixin_setup, TencentVideo
from utils.constant import TencentZoneTypes
from utils.files_times import generate_schedule_time_next_day, get_title_and_hashtags, generate_schedule_time, time_contorller

"""
if __name__ == '__main__':
    filepath = Path(BASE_DIR) / "videos"
    account_file = Path(BASE_DIR / "cookies" / "tencent_uploader" / "account.json")
    # 获取视频目录
    folder_path = Path(filepath)
    # 获取文件夹中的所有文件
    files = list(folder_path.glob("*.mp4"))
    file_num = len(files)
    publish_datetimes = generate_schedule_time(file_num, file_num, daily_times=[6, 10, 16])
    cookie_setup = asyncio.run(weixin_setup(account_file, handle=True))
    category = TencentZoneTypes.LIFESTYLE.value  # 标记原创需要否则不需要传
    #for index, file in enumerate(files):
    #    title, tags = get_title_and_hashtags(str(file))
    #    # 打印视频文件名、标题和 hashtag
    #    print(f"视频文件名：{file}")
    #    print(f"标题：{title}")
    #    print(f"Hashtag：{tags}")
    #    app = TencentVideo(title, file, tags, publish_datetimes[index], account_file, category)
    #    #app = TencentVideo(title, file, tags, 0, account_file, category)
    #    asyncio.run(app.main(), debug=False)
    for file in enumerate(files):
        title, tags = get_title_and_hashtags(str(file))
        # 打印视频文件名、标题和 hashtag
        print(f"视频文件名：{file}")
        print(f"标题：{title}")
        print(f"Hashtag：{tags}")
        app = TencentVideo(title, file, tags, publish_datetimes, account_file, category)
        #app = TencentVideo(title, file, tags, 0, account_file, category)
        asyncio.run(app.main(), debug=False)
"""

#if __name__ == "__main__" :
#    folderpath = Path(BASE_DIR) / "videos"
#    folder_path = Path(folderpath)
#    #folders = list(folder_path.glob("*"))
#    folders = [f for f in folder_path.glob("*") if f.is_dir()]
#    account_file = Path(BASE_DIR / "cookies" / "tencent_uploader" / "account.json")
#    publish_datetimes = time_contorller(len(folders), 6, 2, daily_times=[6, 10, 16])
#    for num, publish_time in zip(folders, publish_datetimes):
#        filepath_son = Path(BASE_DIR) / "videos" / f"{num}"
#        folder_path_son = Path(filepath_son)
#        files_son = list(folder_path_son.glob("*.mp4"))
#        file_num_son = len(files_son)
#        #publish_datetimes = generate_schedule_time(file_num_son, file_num_son, daily_times=[6, 10, 16])
#        cookie_setup = asyncio.run(weixin_setup(account_file, handle=True))
#        category = TencentZoneTypes.LIFESTYLE.value 
#        for file in files_son:
#            title, tags = get_title_and_hashtags(str(file))
#            # 打印视频文件名、标题和 hashtag
#            print(f"视频文件名：{file}")
#            print(f"标题：{title}")
#            print(f"Hashtag：{tags}")
#            app = TencentVideo(title, file, tags, publish_datetimes, account_file, category)
#            #app = TencentVideo(title, file, tags, 0, account_file, category)
#            asyncio.run(app.main(), debug=False)
            
if __name__ == "__main__":
    # --- 1. 收集文件夹并进行初始化设置 ---
    base_folder = Path(BASE_DIR) / "videos"
    
    # 获取所有子文件夹并按数字顺序排序，以确保 "0", "1", "2", "10" 的正确顺序
    folders = sorted(
        [f for f in base_folder.glob("*") if f.is_dir() and f.name.isdigit()],
        key=lambda f: int(f.name)
    )
    
    account_file = Path(BASE_DIR / "cookies" / "tencent_uploader" / "account.json")

    if not folders:
        print("没有找到视频文件夹，程序退出。")
    else:
        # --- 2. 生成总的时间表 & 执行一次性设置 ---
        print(f"找到了 {len(folders)} 个文件夹，正在为它们生成时间表...")
        # 注意: time_contorller 的第3个参数是 video_per_time (每个时间点发几个)
        # 因为您的设计是每个文件夹（即每个时间点）只上传一个视频，所以这里设为 1 最合适。
        publish_datetimes = time_contorller(len(folders), 6, 1, daily_times=[6, 10, 16, 18])
        print("时间表生成完毕。")
        print(publish_datetimes)
        print("\n正在执行一次性的 Cookie 设置...")
        asyncio.run(weixin_setup(account_file, handle=True))
        print("设置完成。")

        # --- 3. 循环处理配对好的文件夹和时间 ---
        print("\n开始上传流程...")
        # 正确使用 zip 将每个文件夹 folder 和一个唯一的发布时间 publish_time 配对
        for folder, publish_time in zip(folders, publish_datetimes):
            # 在当前文件夹中查找 .mp4 文件
            # 我们假设每个文件夹只有一个视频，所以取找到的第一个
            video_files = list(folder.glob("*.mp4"))
            if not video_files:
                print(f"!!! 警告: 在文件夹 '{folder.name}' 中未找到 .mp4 文件，已跳过。")
                continue
            
            video_file = video_files[0] # 获取第一个（也是唯一一个）mp4文件

            # --- 4. 准备并上传 ---
            title, tags = get_title_and_hashtags(str(video_file))
            category = TencentZoneTypes.LIFESTYLE.value

            print("-" * 30)
            print(f"正在处理: {video_file.name} (来自文件夹 {folder.name})")
            print(f"分配的发布时间: {publish_time.strftime('%Y-%m-%d %H:%M')}")

            # 使用这个视频对应的唯一时间来创建 app 实例
            app = TencentVideo(title, video_file, tags, publish_time, account_file, category)
            
            # 为这个特定的视频运行上传任务
            asyncio.run(app.main(), debug=False)
            print(f"已完成上传 {video_file.name}。")