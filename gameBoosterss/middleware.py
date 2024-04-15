from django.http import HttpResponseBadRequest

class ImageSizeLimitMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # Check if the request is a file upload
        if request.method == 'POST':
            for field_name, file_obj in request.FILES.items():
                # Check if the file is an image
                if not file_obj.content_type.startswith('image'):
                    return HttpResponseBadRequest("Only image files are allowed.")
                # Check if the file size exceeds the limit (10 MB)
                if file_obj.size > 10 * 1024 * 1024:  # 10 MB in bytes
                    return HttpResponseBadRequest("Image size cannot exceed 10 MB.")
        return self.get_response(request)
