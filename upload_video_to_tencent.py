import asyncio
from pathlib import Path

from conf import BASE_DIR
from uploader.tencent_uploader.main import weixin_setup, TencentVideo
from utils.constant import TencentZoneTypes
from utils.files_times import generate_schedule_time_next_day, get_title_and_hashtags, generate_schedule_time

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

if __name__ == "__main__" :
    folderpath = Path(BASE_DIR) / "videos"
    folder_path = Path(folderpath)
    #folders = list(folder_path.glob("*"))
    folders = [f for f in folder_path.glob("*") if f.is_dir()]
    account_file = Path(BASE_DIR / "cookies" / "tencent_uploader" / "account.json")
    for num in range(len(folders)) :
        filepath_son = Path(BASE_DIR) / "videos" / f"{num}"
        folder_path_son = Path(filepath_son)
        files_son = list(folder_path_son.glob("*.mp4"))
        file_num_son = len(files_son)
        publish_datetimes = generate_schedule_time(file_num_son, file_num_son, daily_times=[6, 10, 16])
        cookie_setup = asyncio.run(weixin_setup(account_file, handle=True))
        category = TencentZoneTypes.LIFESTYLE.value 
        for file in files_son:
            title, tags = get_title_and_hashtags(str(file))
            # 打印视频文件名、标题和 hashtag
            print(f"视频文件名：{file}")
            print(f"标题：{title}")
            print(f"Hashtag：{tags}")
            app = TencentVideo(title, file, tags, publish_datetimes, account_file, category)
            #app = TencentVideo(title, file, tags, 0, account_file, category)
            asyncio.run(app.main(), debug=False)