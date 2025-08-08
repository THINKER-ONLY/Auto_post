from datetime import timedelta

from datetime import datetime
from datetime import time
from pathlib import Path

from conf import BASE_DIR


def get_absolute_path(relative_path: str, base_dir: str = None) -> str:
    # Convert the relative path to an absolute path
    absolute_path = Path(BASE_DIR) / base_dir / relative_path
    return str(absolute_path)


def get_title_and_hashtags(filename):
    """
  获取视频标题和 hashtag

  Args:
    filename: 视频文件名

  Returns:
    视频标题和 hashtag 列表
  """

    # 获取视频标题和 hashtag txt 文件名
    txt_filename = filename.replace(".mp4", ".txt")

    # 读取 txt 文件
    with open(txt_filename, "r", encoding="utf-8") as f:
        content = f.read()

    # 获取标题和 hashtag
    splite_str = content.strip().split("\n")
    title = splite_str[0]
    hashtags = splite_str[1].replace("#", "").split(" ")

    return title, hashtags


def generate_schedule_time_next_day(total_videos, videos_per_day = 1, daily_times=None, timestamps=False, start_days=0):
    """
    Generate a schedule for video uploads, starting from the next day.

    Args:
    - total_videos: Total number of videos to be uploaded.
    - videos_per_day: Number of videos to be uploaded each day.
    - daily_times: Optional list of specific times of the day to publish the videos.
    - timestamps: Boolean to decide whether to return timestamps or datetime objects.
    - start_days: Start from after start_days.

    Returns:
    - A list of scheduling times for the videos, either as timestamps or datetime objects.
    """
    if videos_per_day <= 0:
        raise ValueError("videos_per_day should be a positive integer")

    if daily_times is None:
        # Default times to publish videos if not provided
        daily_times = [6, 11, 14, 16, 22]

    if videos_per_day > len(daily_times):
        raise ValueError("videos_per_day should not exceed the length of daily_times")

    # Generate timestamps
    schedule = []
    current_time = datetime.now()

    for video in range(total_videos):
        day = video // videos_per_day + start_days + 1  # +1 to start from the next day
        daily_video_index = video % videos_per_day

        # Calculate the time for the current video
        hour = daily_times[daily_video_index]
        time_offset = timedelta(days=day, hours=hour - current_time.hour, minutes=-current_time.minute,
                                seconds=-current_time.second, microseconds=-current_time.microsecond)
        timestamp = current_time + time_offset

        schedule.append(timestamp)

    if timestamps:
        schedule = [int(time.timestamp()) for time in schedule]
    return schedule

def generate_schedule_time(total_videos, videos_per_day, daily_times=None, timestamps=False, start_days=0):
    schedule = []
    current_time = datetime.now()
    current_hour = current_time.hour
    
    for hour in daily_times:
        if current_hour < hour :
            return current_time.replace(hour=hour, minute=0, second=0, microsecond=0)

    next_day = (current_time + timedelta(days=1)).date()
    return datetime.combine(next_day, datetime.min.time()).replace(hour=daily_times[0])

def time_contorller_fixed(total_videos, videos_per_day, video_per_time, daily_times):
    """
    根据当前时间，生成一个未来的视频发布时间表（修正版）。
    - 修复了当某天名额用尽后，会低效地遍历完当天剩余时间点的问题。
    - 结构更清晰，避免了潜在的无限循环风险。
    """
    # --- 初始化部分（与原版相同） ---
    time_schedule = []
    daily_times.sort()
    current_time = datetime.now()
    next_schedule_time = None

    for hour in daily_times:
        if current_time.hour < hour:
            next_schedule_time = current_time.replace(hour=hour, minute=0, second=0, microsecond=0)
            break
    
    if next_schedule_time is None:
        tomorrow = current_time.date() + timedelta(days=1)
        next_schedule_time = datetime.combine(tomorrow, time(hour=daily_times[0]))

    # --- 循环生成部分（核心逻辑修正） ---
    while len(time_schedule) < total_videos:
        videos_on_this_day = len([t for t in time_schedule if t.date() == next_schedule_time.date()])

        # 如果当天的名额已经用完
        if videos_on_this_day >= videos_per_day:
            # 直接跳转到第二天的第一个时间点
            next_day_date = next_schedule_time.date() + timedelta(days=1)
            next_schedule_time = datetime.combine(next_day_date, time(hour=daily_times[0]))
            continue # 使用 continue 立刻开始下一次循环，用新的时间点重新判断

        # 如果名额没用完，就添加视频
        for _ in range(video_per_time):
            # 再次检查确保不会在本次添加中超过单日上限
            if len(time_schedule) < total_videos and videos_on_this_day < videos_per_day:
                time_schedule.append(next_schedule_time)
                videos_on_this_day += 1
            else:
                break 
        
        # 添加完毕后，正常推进到下一个时间点
        current_hour_index = daily_times.index(next_schedule_time.hour)
        if current_hour_index + 1 < len(daily_times):
            # 推进到今天的下一个时间点
            next_hour = daily_times[current_hour_index + 1]
            next_schedule_time = next_schedule_time.replace(hour=next_hour)
        else:
            # 推进到明天的第一个时间点
            next_day_date = next_schedule_time.date() + timedelta(days=1)
            next_schedule_time = datetime.combine(next_day_date, time(hour=daily_times[0]))

    return time_schedule
