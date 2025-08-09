import configparser
from pathlib import Path
from time import sleep

from xhs import XhsClient

from conf import BASE_DIR
from utils.files_times import generate_schedule_time_next_day, get_title_and_hashtags, time_contorller
from uploader.xhs_uploader.main import sign_local, beauty_print

config = configparser.RawConfigParser()
config.read(Path(BASE_DIR / "uploader" / "xhs_uploader" / "accounts.ini"))

"""
if __name__ == '__main__':
    filepath = Path(BASE_DIR) / "videos"
    # 获取视频目录
    folder_path = Path(filepath)
    # 获取文件夹中的所有文件
    files = list(folder_path.glob("*.mp4"))
    file_num = len(files)

    cookies = config['account1']['cookies']
    xhs_client = XhsClient(cookies, sign=sign_local, timeout=60)
    # auth cookie
    # 注意：该校验cookie方式可能并没那么准确
    try:
        xhs_client.get_video_first_frame_image_id("3214")
    except:
        print("cookie 失效")
        exit()

    publish_datetimes = generate_schedule_time_next_day(file_num, 1, daily_times=[16])

    for index, file in enumerate(files):
        title, tags = get_title_and_hashtags(str(file))
        # 加入到标题 补充标题（xhs 可以填1000字不写白不写）
        tags_str = ' '.join(['#' + tag for tag in tags])
        hash_tags_str = ''
        hash_tags = []

        # 打印视频文件名、标题和 hashtag
        print(f"视频文件名：{file}")
        print(f"标题：{title}")
        print(f"Hashtag：{tags}")

        topics = []
        # 获取hashtag
        for i in tags[:3]:
            topic_official = xhs_client.get_suggest_topic(i)
            if topic_official:
                topic_official[0]['type'] = 'topic'
                topic_one = topic_official[0]
                hash_tag_name = topic_one['name']
                hash_tags.append(hash_tag_name)
                topics.append(topic_one)

        hash_tags_str = ' ' + ' '.join(['#' + tag + '[话题]#' for tag in hash_tags])

        note = xhs_client.create_video_note(title=title[:20], video_path=str(file),
                                            desc=title + tags_str + hash_tags_str,
                                            topics=topics,
                                            is_private=False,
                                            post_time=publish_datetimes[index].strftime("%Y-%m-%d %H:%M:%S"))

        beauty_print(note)
        # 强制休眠30s，避免风控（必要）
        sleep(30)
"""
if __name__ == '__main__':
    base_folder = Path(BASE_DIR) / "videos"
    folders = sorted(
        [f for f in base_folder.glob("*") if f.is_dir() and f.name.isdigit()],
        key=lambda f: int(f.name)
    )
    if not folders:
        print("没有找到视频文件夹，程序退出。")
    else:
        print(f"找到了 {len(folders)} 个文件夹，正在为它们生成时间表...")
        publish_datetimes = time_contorller(len(folders), 6, 1, daily_times=[6, 10, 16])
        print("时间表生成完毕。")
        print(publish_datetimes)
        print("\n正在执行一次性的 Cookie 设置...")
        cookies = config['account1']['cookies']
        xhs_client = XhsClient(cookies, sign=sign_local, timeout=60)
        try:
            xhs_client.get_video_first_frame_image_id("3214")
        except:
            print("cookie 失效")
            exit()
        print("设置完成。")
        print("\n开始上传流程...")
        for folder, publish_time in zip(folders, publish_datetimes):
            video_files = list(folder.glob("*.mp4"))
            if not video_files:
                print(f"!!! 警告: 在文件夹 '{folder.name}' 中未找到 .mp4 文件，已跳过。")
                continue

            video_file = video_files[0]
            title, tags = get_title_and_hashtags(str(video_file))
            # 加入到标题 补充标题（xhs 可以填1000字不写白不写）
            tags_str = ' '.join(['#' + tag for tag in tags])
            hash_tags_str = ''
            hash_tags = []

            # 打印视频文件名、标题和 hashtag
            print(f"视频文件名：{video_file}")
            print(f"标题：{title}")
            print(f"Hashtag：{tags}")

            topics = []
            # 获取hashtag
            for i in tags[:3]:
                topic_official = xhs_client.get_suggest_topic(i)
                if topic_official:
                    topic_official[0]['type'] = 'topic'
                    topic_one = topic_official[0]
                    hash_tag_name = topic_one['name']
                    hash_tags.append(hash_tag_name)
                    topics.append(topic_one)

            hash_tags_str = ' ' + ' '.join(['#' + tag + '[话题]#' for tag in hash_tags])

            note = xhs_client.create_video_note(title=title[:20], video_path=str(video_file),
                                                desc=title + tags_str + hash_tags_str,
                                                topics=topics,
                                                is_private=False,
                                                post_time=publish_time.strftime("%Y-%m-%d %H:%M:%S"))

            beauty_print(note)
            # 强制休眠30s，避免风控（必要）
            sleep(30)