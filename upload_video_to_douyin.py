import asyncio
from pathlib import Path

from conf import BASE_DIR
from uploader.douyin_uploader.main import douyin_setup, DouYinVideo
from utils.files_times import generate_schedule_time_next_day, get_title_and_hashtags, generate_schedule_time

"""
if __name__ == '__main__':
    filepath = Path(BASE_DIR) / "videos"
    account_file = Path(BASE_DIR / "cookies" / "douyin_uploader" / "account.json")
    # 获取视频目录
    folder_path = Path(filepath)
    # 获取文件夹中的所有文件
    files = list(folder_path.glob("*.mp4"))
    file_num = len(files)
    publish_datetimes = generate_schedule_time(file_num, daily_times=[6, 10, 16])
    cookie_setup = asyncio.run(douyin_setup(account_file, handle=False))
    #for index, file in enumerate(files):
    #    title, tags = get_title_and_hashtags(str(file))
    #    thumbnail_path = file.with_suffix('.png')
    #    # 打印视频文件名、标题和 hashtag
    #    print(f"视频文件名：{file}")
    #    print(f"标题：{title}")
    #    print(f"Hashtag：{tags}")
    #    # 暂时没有时间修复封面上传，故先隐藏掉该功能
    #    # if thumbnail_path.exists():
    #        # app = DouYinVideo(title, file, tags, publish_datetimes[index], account_file, thumbnail_path=thumbnail_path)
    #    # else:
    #    app = DouYinVideo(title, file, tags, publish_datetimes[index], account_file)
    #    asyncio.run(app.main(), debug=False)
    for file in enumerate(files):
        title, tags = get_title_and_hashtags(str(file))
        thumbnail_path = file.with_suffix('.png')
        # 打印视频文件名、标题和 hashtag
        print(f"视频文件名：{file}")
        print(f"标题：{title}")
        print(f"Hashtag：{tags}")
        # 暂时没有时间修复封面上传，故先隐藏掉该功能
        # if thumbnail_path.exists():
            # app = DouYinVideo(title, file, tags, publish_datetimes[index], account_file, thumbnail_path=thumbnail_path)
        # else:
        app = DouYinVideo(title, file, tags, publish_datetimes, account_file)
        asyncio.run(app.main(), debug=False)
"""
if __name__ == "__main__" :
    folderpath = Path(BASE_DIR) / "videos"
    folder_path = Path(folderpath)
    folders = [f for f in folder_path.glob("*") if f.is_dir()]
    account_file = Path(BASE_DIR / "cookies" / "douyin_uploader" / "account.json")
    for num in range(folders):
        filepath_son = Path(BASE_DIR) / "videos" / f"{num}"
        file_path_son = Path(filepath_son)
        files_son = list(filepath_son.glob("*.mp4"))
        file_num_son = len(files_son)
        publish_datetimes = generate_schedule_time(file_num_son, file_num_son, daily_times=[6, 10, 16])
        cookie_setup = asyncio.run(douyin_setup(account_file, handle=False))
        for file in files_son :
            title, tags = get_title_and_hashtags(str(file))
            thumbnail_path = file.with_suffix('.png')
            print(f"视频文件名：{file}")
            print(f"标题：{title}")
            print(f"Hashtag：{tags}")
            app = DouYinVideo(title, file, tags, publish_datetimes, account_file)
            asyncio.run(app.main(), debug=False)