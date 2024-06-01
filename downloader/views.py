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
            except:

                return render(
                    request,
                    "downloader/index.html",
                    {"error": "Something's Wrong."},
                )
    return render(request, "downloader/index.html")
