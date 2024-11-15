from django.shortcuts import render, get_object_or_404, get_list_or_404
from django.views.generic import CreateView
from django.views import View
from news.models import Blog, SubHeader
from django.urls import reverse_lazy
import uuid
from gameBoosterss.utils import upload_image_to_firebase


class CreateBlogView(CreateView):
    model = Blog
    template_name = 'blog/create_blog.html'
    fields = '__all__'
    success_url = reverse_lazy('blog_create')

    def form_valid(self, form):
        blog = form.save(commit=False)

        def handle_image_upload(image_field, folder='blog'):
            if image_field:
                ext = image_field.name.split('.')[-1]
                image_name = f'{folder}/{uuid.uuid4()}.{ext}'
                return upload_image_to_firebase(image_field, image_name)
            return None

        image_main = self.request.FILES.get('main_image')
        image_main_headline = self.request.FILES.get('main_image2')
        image_order = self.request.FILES.get('order_image')
        order_image2 = self.request.FILES.get('order_image2')

        blog.main_image = handle_image_upload(image_main) or blog.main_image
        blog.main_image2 = handle_image_upload(image_main_headline) or blog.main_image2
        blog.order_image = handle_image_upload(image_order) or blog.order_image
        blog.order_image2 = handle_image_upload(order_image2) or blog.order_image2

        blog.save()
        return super().form_valid(form)
    
class BlogHomeView(View):
    model = Blog
    template_name = 'blog/home.html'  

    def get(self, request, *args, **kwargs):
        headlines = self.model.objects.all().order_by('id')
        blog = headlines.first()
        return render(request, self.template_name, {'blog': blog, 'headlines': headlines})  



class BlogDetailsView(View):
    template_name = 'blog/blog.html'  
    def get(self, request, id):
       blog = get_object_or_404(Blog, id=id)
       headlines = Blog.objects.all().order_by('id')
       sub_headers = SubHeader.objects.filter(blog=blog).order_by('id')
       return render(request, self.template_name, {'blog': blog, "sub_headers": sub_headers, 'headlines':headlines})