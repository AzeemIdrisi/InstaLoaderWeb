from django.shortcuts import redirect, render
import instaloader, os, shutil

os.path.exists("temp")


# Create your views here.
def homepage(request):
    if request.method == "POST":
        url = str(request.POST["postURL"])
        if url != "":
            if url.startswith("https://www.instagram.com/"):
                shortcode = url.split("/")[4]
                print(f"{shortcode=}")
            else:
                return render(
                    request, "downloader/index.html", {"error": "Invalid URL."}
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
                    "downloader/index.html",
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
            "downloader/index.html",
            {"data": True, "images": images, "videos": videos},
        )

    return render(request, "downloader/index.html")
