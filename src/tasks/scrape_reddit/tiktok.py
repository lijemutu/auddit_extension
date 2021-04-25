from TikTokApi import TikTokApi
import os
def dwn_tiktok(context,count=15):
    # Starts TikTokApi
    api = TikTokApi()

    try:
        mode = api.trending(count,language='es')
    except:
        raise Exception("not scraping tiktoks")

    i=1    
    post_data = []
    for tiktok in mode:
        post_info ={}
        # Prints the text of the tiktok
        """with open("tiktokList.txt", 'r') as tikTokList:
            elements_on_list = tikTokList.read().split()
            if str(tiktok['id']) in elements_on_list:
        continue """
        tiktokData = api.get_Video_By_DownloadURL(tiktok['video']['downloadAddr'])
        video_path = f"data/video/tmp_video/video{i}.mp4"
        post_info['video_path'] = video_path
        with open(video_path, 'wb') as out:
            out.write(tiktokData)

        i += 1
        post_data.append(post_info)
    context['post'] = post_data
    del api
    return