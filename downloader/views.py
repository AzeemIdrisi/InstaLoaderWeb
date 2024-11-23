from django.shortcuts import redirect, render
import instaloader, os, shutil
import threading

# os.path.exists("temp")


# Create your views here.


def index(request):
    return render(request, "downloader/index.html")


def posts(request):
    if request.method == "POST":
        url = str(request.POST["postURL"])
        if url != "":
            if url.startswith("https://www.instagram.com/") and url.endswith("/"):
                shortcode = url.split("/")[-2]
                print(f"{shortcode=}")
            elif url.startswith("https://www.instagram.com/"):
                shortcode = url.split("/")[-1]
                print(f"{shortcode=}")
            else:
                return render(
                    request, "downloader/posts.html", {"error": "Invalid URL."}
                )
        if shortcode != "":
            try:
                L = instaloader.Instaloader()
                L.save_metadata = False
                L.download_video_thumbnails = False
                L.post_metadata_txt_pattern = ""

                print("FINDING POST")
                post = instaloader.Post.from_shortcode(L.context, shortcode)
                print("FOUND")

                # Clearing temp folder before downloading
                if os.path.exists("temp"):
                    shutil.rmtree("temp")
                    print("DELETED OLD TEMP FILES")
                print("CLEANED")

                L.download_post(post, target="temp")
            except Exception as e:
                error_message = str(e)
                return render(
                    request,
                    "downloader/posts.html",
                    {"error": f"An error occurred: {error_message}"},
                )

    if os.path.exists("temp"):
        media_files = os.listdir("temp")
        images = [
            f
            for f in media_files
            if f.lower().endswith((".png", ".jpg", ".jpeg", ".gif"))
        ]
        videos = [
            f
            for f in media_files
            if f.lower().endswith((".mp4", ".avi", ".mov", ".wmv"))
        ]
        return render(
            request,
            "downloader/posts.html",
            {"data": True, "images": images, "videos": videos},
        )

    return render(request, "downloader/posts.html")


def reels(request):
    if request.method == "POST":
        url = str(request.POST["postURL"])
        if url != "":
            if url.startswith("https://www.instagram.com/") and url.endswith("/"):
                shortcode = url.split("/")[-2]
                print(f"{shortcode=}")
            elif url.startswith("https://www.instagram.com/"):
                shortcode = url.split("/")[-1]
                print(f"{shortcode=}")
            else:
                return render(
                    request, "downloader/reels.html", {"error": "Invalid URL."}
                )
        if shortcode != "":
            try:
                L = instaloader.Instaloader()
                L.save_metadata = False
                L.download_video_thumbnails = False
                L.post_metadata_txt_pattern = ""

                print("FINDING POST")
                post = instaloader.Post.from_shortcode(L.context, shortcode)
                print("FOUND")

                # Clearing temp folder before downloading
                if os.path.exists("temp"):
                    shutil.rmtree("temp")
                    print("DELETED OLD TEMP FILES")
                print("CLEANED")

                L.download_post(post, target="temp")
            except Exception as e:
                error_message = str(e)
                return render(
                    request,
                    "downloader/reels.html",
                    {"error": f"An error occurred: {error_message}"},
                )

    if os.path.exists("temp"):
        media_files = os.listdir("temp")
        images = [
            f
            for f in media_files
            if f.lower().endswith((".png", ".jpg", ".jpeg", ".gif"))
        ]
        videos = [
            f
            for f in media_files
            if f.lower().endswith((".mp4", ".avi", ".mov", ".wmv"))
        ]
        return render(
            request,
            "downloader/reels.html",
            {"data": True, "images": images, "videos": videos},
        )

    return render(request, "downloader/reels.html")


def download_posts_in_background(username):
    try:
        desktop_path = os.path.join(os.path.expanduser("~"), "Desktop")

        L = instaloader.Instaloader()
        L.save_metadata = False
        L.download_video_thumbnails = False
        L.post_metadata_txt_pattern = ""

        L.dirname_pattern = f"/InstaLoaderWeb/{username}"
        L.download_profile(username)
        print("Download Completed.")
    except Exception as e:
        print(f"An error occurred: {str(e)}")


def allposts(request):
    if request.method == "POST":
        username = str(request.POST["postURL"])

        if username != "":
            try:
                # Start the download in a new thread
                download_thread = threading.Thread(
                    target=download_posts_in_background, args=(username,)
                )
                download_thread.start()

                # Return a response immediately to the user
                return render(
                    request,
                    "downloader/allposts.html",
                    {
                        "message": "Download started! This may take a while, Please do not close this window."
                    },
                )
            except Exception as e:
                error_message = str(e)
                return render(
                    request,
                    "downloader/allposts.html",
                    {"error": f"An error occurred: {error_message}"},
                )
    desktop_path = os.path.join(os.path.expanduser("~"), "Desktop")
    print(f"{desktop_path=}")
    return render(request, "downloader/allposts.html")
