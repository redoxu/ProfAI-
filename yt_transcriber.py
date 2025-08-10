from youtube_transcript_api import YouTubeTranscriptApi
from pytube import Playlist
import json
import time

################################## EXECUTE THIS FILE TO GENERATE THE JSON FILE WITH RAW TRANSCRIPTS (CHUNKING DONE LATER)

def get_video_transcription(video_id: str):
    ytt_api = YouTubeTranscriptApi()
    transcript_list = ytt_api.list(video_id)
    try:
        transcript = transcript_list.find_transcript(['en'])
    except Exception:
        transcript = transcript_list.find_transcript(['en-US'])
    transcript = transcript.fetch()
    full_text = " ".join(segment.text for segment in transcript)
    return full_text


def get_playlist_transcriptions(video_IDs: list[str], delay_seconds: float = 5):
    all_transcripts = {}
    for video_id in video_IDs:
        try:
            text = get_video_transcription(video_id)
            all_transcripts[video_id] = text

            print(f"video {video_id} transcribed succesfully")
            print("\nTranscript:\n{transcript[:300]}...\n") 

        except Exception as e:
            all_transcripts[video_id] = f"Error: {str(e)}"

        time.sleep(delay_seconds)  # wait between requests to avoid IP ban over multiple fast requests

    return all_transcripts

# Example usage:
# playlists = ["https://www.youtube.com/playlist?list=PLOspHqNVtKAC-FUNMq8qjYVw6_semZHw0"]

video_IDs = ['jcgaNrC4ElU', '5sLYAQS9sWQ', 'QPQy7jUpmyA', 'QzY57FaENXg', 'TpMIssRdhco',
              'ZXiruGOCn9s', 'b61DPVFX03I', 'fLvJ8VdHLA0', '1I6bQ12VxV0', 'gkXX4h3qYm4',
                'qiUEgSCyY5o', 'y7sXDpffzQQ', '7TqhmX92P6U', '0RT2Q0qwXSA', 'i62czvwDlsw',
                  'L3ynnRgpZwg', 'T7Wr7wVK5Wo', 'jevuDDjFEsM', '6dyrBRcC5KA', 'W01tIRP_Rqs',
                    'GE3JOFwTWVM', 'OejCJL2EC3k', 'T-w_5T-j-dA', 'S5AGN9XfPK4', 'zqv1eELa7fs',
                      'fJ40w_2h8kk', '85RfazjDPwA', 'OThahaOga20', 'XctooiH0moI', 'Cgiqx0pJuLo', 'F8NKVhkZZWI']

transcriptions = get_playlist_transcriptions(video_IDs)

with open("output2.json", "w", encoding="utf-8") as f:
    json.dump(transcriptions, f, ensure_ascii=False, indent=4)


