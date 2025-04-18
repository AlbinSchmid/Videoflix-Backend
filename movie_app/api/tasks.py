import subprocess
import os

def convert_hls(slug, source, quality_name, quality_height):
    target_dir = os.path.join('media', 'movies', slug, quality_name)
    target = os.path.join(target_dir, f"{slug}_{quality_name}.m3u8")
    os.makedirs(target_dir, exist_ok=True)
    cmd = 'ffmpeg -i {} -vf scale=-2:{} -c:v libx264 -profile:v baseline -level 3.0 -c:a aac -b:a 128k -ac 2 -hls_time 4 -hls_list_size 0 -f hls {}'.format(source, quality_height, target)
    
    subprocess.run(cmd)
    if quality_height == 1080:
        create_master_playlist(slug)

    if os.path.exists(source) and quality_height == 1080:
        os.remove(source)

def create_master_playlist(slug):
    target_dir = os.path.join('media', 'movies', slug)
    master_path = os.path.join(target_dir, f"{slug}.m3u8")
    resolutions = [
        ("360p", "640x360", 800000),
        ("480p", "854x480", 1400000),
        ("720p", "1280x720", 2800000),
        ("1080p", "1920x1080", 5000000),
    ]

    lines = ["#EXTM3U"]

    for folder, resolution, bandwidth in resolutions:
        variant_path = f"{folder}/{slug}_{folder}.m3u8"
        lines.append(f"#EXT-X-STREAM-INF:BANDWIDTH={bandwidth},RESOLUTION={resolution}")
        lines.append(variant_path)

    with open(master_path, "w") as f:
        f.write("\n".join(lines))

