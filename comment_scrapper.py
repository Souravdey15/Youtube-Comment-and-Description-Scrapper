import requests, sys, os, argparse
from datetime import datetime

# List of simple to collect features
snippet_features = ["authorDisplayName"]

# Any characters to exclude, generally these are things that become problematic in CSV files
unsafe_characters = ['\n', '"']

# Used to identify columns, currently hardcoded order
header = ["video_id"] + snippet_features + ["textDisplay", "textOriginal", "publishedAt", "updatedAt", "replyCount", "likeCount"]


def setup(api_path, code_path):
    with open(api_path, 'r') as file:
        api_key = file.readline()
    with open(code_path) as file:
        country_codes = [x.rstrip()[1:] for x in file]
    return api_key, country_codes


def prepare_feature(feature):
    # Removes any character from the unsafe characters list and surrounds the whole item in quotes
    for ch in unsafe_characters:
        feature = str(feature).replace(ch, "")
    return f'"{feature}"'


def api_request(country_code):
    # Builds the URL and requests the JSON from it
    request_url = f"https://www.googleapis.com/youtube/v3/commentThreads?part=snippet,replies&videoId={country_code}&maxResults=100&key={api_key}"
    request = requests.get(request_url)
    if request.status_code == 429:
        print("Temp-Banned due to excess requests, please wait and continue later")
        sys.exit()
    return request.json()


def get_tags(tags_list):
    # Takes a list of tags, prepares each tag and joins them into a string by the pipe character
    return prepare_feature("|".join(tags_list))


def get_videos(items):
    lines = []
    for video in items:
        parent_ref = video['snippet']['topLevelComment']['snippet']
        reply_count = video['snippet']['totalReplyCount']
        like_count = video['snippet']['topLevelComment']['snippet']['likeCount']
        new_id = parent_ref.get("videoId", "")
        authorName = parent_ref.get("authorDisplayName", "")
        textDisplay = parent_ref.get("textDisplay", "")
        textOriginal = parent_ref.get("textOriginal", "")
        publishedAt = parent_ref.get("publishedAt", "")
        updatedAt = parent_ref.get("updatedAt", "")
        line = [new_id] + [prepare_feature(x) for x in [authorName, textDisplay, textOriginal, publishedAt, updatedAt, reply_count, like_count]]
        if datetime.strptime(line[4][1:8], '%Y-%m') > datetime(2019, 12, 31) and len(line)>0:
            lines.append(",".join(line))
    return lines


def get_pages(country_code):
    country_data = []
    video_data_page = api_request(country_code)
    items = video_data_page.get('items', [])
    country_data += get_videos(items)
    return country_data


def write_to_file(country_code, country_data, dir):
    print(f"Writing {dir} data to file...")

    with open(f"{output_dir}/{dir}comments.csv", "w+", encoding='utf-8') as file:
        for row in country_data:
            file.write(f"{row}\n")


def get_data(dir):
    country_data = [",".join(header)]
    for country_code in country_codes:
        x = get_pages(country_code)
        if len(x)>0:
            country_data.append(x)
    write_to_file(country_code, country_data,dir)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('--key_path',
                        help='Path to the file containing the api key, by default will use api_key.txt in the same directory',
                        default='api_key.txt')
    parser.add_argument('--country_code_path',
                        help='Path to the file containing the list of country codes to scrape, by default will use country_codes.txt in the same directory',
                        default='country_codes.txt')
    parser.add_argument('--output_dir', help='Path to save the outputted files in', default='Comments')

    args = parser.parse_args()

    output_dir = args.output_dir
    start_time = datetime.now()
    for i in os.listdir("India"):
        print("Working on " + i + " folder\n")
        api_key, country_codes = setup(args.key_path, "India/" + i)
        get_data("India/" + i)

    for i in os.listdir("USA"):
        print("Working on " + i + " folder\n")
        api_key, country_codes = setup(args.key_path, "USA/" + i)
        get_data("USA/" + i)

    print(datetime.now() - start_time)
