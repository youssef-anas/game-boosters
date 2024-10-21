from django.shortcuts import render, HttpResponse, get_object_or_404
from .controller.forms import ProfileEditForm, ProfileEditForm, PasswordEditForm, PayPalEmailEditForm
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from booster.models import OrderRating, Photo, BoosterPortfolio, WorkWithUs, Booster, BoosterRank
from django.contrib.auth import get_user_model
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from booster.controller.serializers import RatingSerializer, CanChooseMeSerializer, TransactionSerializer
User = get_user_model()
from django.shortcuts import render, redirect , HttpResponse, get_object_or_404
from django.urls import reverse, reverse_lazy
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.db.models import Sum
from accounts.models import BaseOrder, Transaction, BoosterPercent, BaseUser, Wallet
from chat.models import Room, Message
from django.http import HttpResponseBadRequest
from rest_framework.pagination import PageNumberPagination
from customer.controllers.order_creator import create_order
from gameBoosterss.utils import refresh_order_page
from accounts.templatetags.custom_filters import wow_ranks, dota2_ranks, csgo2_ranks, custom_timesince, format_date
from django.db.models import Avg, Sum, Case, When, IntegerField, Max, F
from booster.forms import WorkWithUsLevel1Form, WorkWithUsLevel2Form, WorkWithUsLevel3Form, WorkWithUsLevel4Form, WorkWithUsForm
from gameBoosterss.utils import upload_image_to_firebase, get_booster_game_ids, send_change_data_msg, send_refresh_msg
import uuid
from gameBoosterss.permissions import IsBooster
from django.views.generic import View
import copy
from django.utils import timezone
from datetime import timedelta

# def register_booster_view(request):
#     form = Registeration_Booster()
#     if request.method == 'POST':
#         form = Registeration_Booster(request.POST,request.FILES)
#         if form.is_valid():
#             user = form.save(commit=False)
#             print(user.email_verified_at)
#             user.is_active = False  # Mark the user as inactive until they activate their account
#             user.is_booster = True
#             user.save()
#             # Send activation email
#             return HttpResponse(f'account created with username {user.username}')
#         return render(request, 'booster/registeration_booster.html', {'form': form}) # return error 
#     return render(request, 'booster/registeration_booster.html', {'form': form})

@login_required
def booster_setting(request):
    booster_instance = get_object_or_404(Booster, booster=request.user )
    paypal_email = booster_instance.paypal_account
    profile_form = ProfileEditForm(instance=request.user)
    paypal_form = PayPalEmailEditForm(user=request.user, initial={'paypal_account': paypal_email})
    password_form = PasswordEditForm(user=request.user)

    if request.method == 'POST':
        if 'profile_submit' in request.POST:
            profile_form = ProfileEditForm(request.POST, request.FILES, instance=request.user)
            if profile_form.is_valid():
                if request.FILES:
                    img= request.FILES.get('profile_image', None)
                    ext = img.name.split('.')[-1]
                    img.file.seek(0)

                    name = f"booster/images/{request.user.id}/{str(uuid.uuid4())}.{ext}"
                    url = upload_image_to_firebase(img, name)

                    booster = Booster.objects.get(booster = request.user)
                    booster.profile_image = url
                    booster.save()
                    booster.booster.save()
                profile_form.save()
                messages.success(request, 'Profile updated successfully.')
                return redirect('booster.setting')
            
        elif 'portfolio_submit' in request.POST:
            images = request.FILES.getlist('images')  # Get the list of uploaded images

            # Create a BoosterPortfolio instance for each uploaded image
            portfolios = []
            for image in images:
                ext = image.name.split('.')[-1]
                name = f"booster/images/{request.user.id}/portfolio/{str(uuid.uuid4())}.{ext}"
                url = upload_image_to_firebase(image, name)
                portfolio = BoosterPortfolio(booster=request.user.booster, image=url)
                portfolios.append(portfolio)

            # Bulk create the BoosterPortfolio instances
            BoosterPortfolio.objects.bulk_create(portfolios)

            return redirect('booster.setting')
        
        elif 'portfolio_id' in request.POST:
            portfolio_id = request.POST['portfolio_id']
            portfolio = get_object_or_404(BoosterPortfolio, id=portfolio_id)
            if request.method == 'POST':
                portfolio.delete()
                return redirect('booster.setting')
            
        elif 'paypal_submit' in request.POST:
            paypal_form = PayPalEmailEditForm(user=request.user, data=request.POST)
            if paypal_form.is_valid():
                paypal_form.save()
                messages.success(request, 'PayPal email updated successfully.')
                return redirect('booster.setting')
        
        elif 'password_submit' in request.POST:
            password_form = PasswordEditForm(request.user, request.POST)
            if password_form.is_valid():
                password_form.save()
                messages.success(request, 'Password changed successfully.')
                return redirect('booster.setting')

    return render(request, 'booster/setting.html', {'profile_form': profile_form, 'password_form': password_form, 'paypal_form': paypal_form})

# Orders Page
@login_required
def orders_jobs(request):
    # orders = BaseOrder.objects.filter(booster__isnull=True)
    ids = get_booster_game_ids(request.user)
    context = {
        "ids":ids,
    }
    return render(request,'booster/orders_jobs.html', context)

class ClaimOrderView(View):
    permission_classes = [IsBooster]
    def post(self, request, game_name, id):
        order = get_object_or_404(BaseOrder, id=id, booster__isnull=True)
        ids = get_booster_game_ids(request.user)
        captcha = request.POST.get('captcha_input', None)
        if order.game.id in ids and captcha == order.captcha.value:
            try:
                order.booster = request.user
                order.save()
            except Exception as e:
                return HttpResponseBadRequest(f"Error updating order{e}")
        else:
            messages.error(request, "You aren't playing this game!")
            return redirect(reverse_lazy('orders.jobs'))
        refresh_order_page()
        room = Room.get_specific_room(order.customer.username, order.name)
        if room:
            Message.create_booster_message(room, "Hi, I'm your booster. It's a pleasure to work together, and I will start your order in 15 minutes or less.", request.user)

        send_refresh_msg(request.user.username , order.customer.username, order.name)
        return redirect(reverse_lazy('booster.orders'))

# All Boosters
def boosters(request):
    def get_booster_info(game_id):
        game_fields_map = {
            1: ('is_wr_player', 'achived_rank_wr'),
            2: ('is_valo_player', 'achived_rank_valo'),
            3: ('is_pubg_player', 'achived_rank_pubg'),
            4: ('is_lol_player', 'achived_rank_lol'),
            5: ('is_tft_player', 'achived_rank_tft'),
            6: ('is_wow_player', 'achived_rank_wow'),
            7: ('is_hearthstone_player', 'achived_rank_hearthstone'),
            8: ('is_mobleg_player', 'achived_rank_mobleg'),
            9: ('is_rl_player', 'achived_rank_rl'),
            10: ('is_dota2_player', 'achived_rank_dota2'),
            11: ('is_hok_player', 'achived_rank_hok'),
            12: ('is_overwatch2_player', 'achived_rank_overwatch2'),
            13: ('is_csgo2_player', 'achived_rank_csgo2'),
        }

        return game_fields_map.get(game_id)

    if request.method == 'POST':
        game_id = request.POST.get('game_id')
    else:
        game_id = request.GET.get('game_id')

    try:
        game_id = int(game_id)
    except (TypeError, ValueError):
        game_id = 1  # Default game_id if none provided or invalid

    game_pk_condition = Case(
        When(booster_orders__game__pk=game_id, booster_orders__is_done=True, booster_orders__is_drop=False, then=1),
        default=0,
        output_field=IntegerField()
    )

    is_player_field, rank_field = get_booster_info(game_id)
    query_kwargs = {
        'is_booster': True,
        'booster__can_choose_me': True,
        f'booster__{is_player_field}': True,
    }
    boosters = User.objects.filter(**query_kwargs).annotate(
        achived_rank_name=F(f'booster__{rank_field}__rank_name'),
        achived_rank_image=F(f'booster__{rank_field}__rank_image'),
        order_count=Sum(game_pk_condition),
        last_boost=Max('booster_orders__created_at'),
    ).order_by('id')

    if request.headers.get('x-requested-with') == 'XMLHttpRequest':
        boosters_with_additional_data = []
        for booster in boosters:
            profile_image_url = booster.get_image_url()
            achived_rank_image_url = booster.achived_rank_image if booster.achived_rank_image else ''
            languages = [language.language for language in booster.booster.languages.all()]  # Convert to a list of strings
            data = {
                "id": booster.pk,
                "username": booster.username,
                "first_name": booster.first_name,
                "last_name": booster.last_name,
                "profile_image": profile_image_url,
                "achived_rank_name": booster.achived_rank_name,
                "achived_rank_image": achived_rank_image_url,
                "order_count": booster.order_count,
                "average_rating": booster.get_average_rating(),
                'languages': languages,  # Use the list of strings
                'last_boost': custom_timesince(booster.last_boost),
                'on_madboost': format_date(booster.created_at),
            }
            boosters_with_additional_data.append(data)
        return JsonResponse({'boosters': boosters_with_additional_data})

    else:
        context = {
            "boosters": boosters,
        }
        return render(request, 'booster/boosters.html', context)


def booster_details(request, booster_id):
    game_pk_condition = Case(
        When(booster_orders__is_done=True, booster_orders__is_drop=False, then=1),
        default=0,
        output_field=IntegerField()
    )
    
    # Get the queryset of User objects and annotate fields
    booster_queryset = User.objects.filter(
        pk=booster_id,
        is_booster=True
    ).annotate(
        orders_count=Sum(game_pk_condition),
        last_boost=Max('booster_orders__created_at'),
    ).order_by('id')

    # Get the specific User object from the queryset or return a 404 error if not found
    booster = get_object_or_404(booster_queryset)

    feedbacks = OrderRating.objects.filter(booster=booster_id).order_by('-created_at')

    feedbacks_count = feedbacks.count()
    if feedbacks_count == 0: feedbacks_count =1

    rate_with_5 = feedbacks.filter(rate=5).count()
    
    rate_5_percent = round((rate_with_5 / feedbacks_count) * 100, 2)

    completed_orders_query = BaseOrder.objects.filter(is_done=True, is_drop=False, booster_id=booster_id)

    completed_orders = []
    for order in completed_orders_query:
        content_type = order.content_type
        if content_type:
            completed_order = content_type.model_class().objects.get(order = order)

        completed_orders.append(completed_order)

    context = {
        "feedbacks": feedbacks,
        "booster": booster,
        "feedbacks_count": feedbacks_count,
        "rate_5_percent": rate_5_percent,
        "completed_orders": completed_orders
    }
    return render(request, 'booster/booster_details.html', context)

@login_required
def get_rate(request, order_id):
    order_obj = get_object_or_404(BaseOrder, id=order_id)
    customer = order_obj.customer
    booster = order_obj.booster
    if not (customer and booster):
        return HttpResponse(f"Can't set rate to order {order_id}, with customer {customer} and booster {booster}")
    if order_obj.is_done:
        if request.method == 'POST':
            serializer = RatingSerializer(data=request.POST)
            if serializer.is_valid():
                existing_rating = OrderRating.objects.filter(order=order_obj).first()
                if existing_rating:
                    return HttpResponse('Rate Already Added', status=status.HTTP_400_BAD_REQUEST)
                serializer.save(order=order_obj)
                return redirect('customer.orders')
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        return HttpResponse('Method Not Allowed', status=status.HTTP_400_BAD_REQUEST)
    return HttpResponse('Order Not Done', status=status.HTTP_400_BAD_REQUEST)
        
# this for only test and will remove it ----
def rate_page(request, order_id):
    order = BaseOrder.objects.get(id=order_id)
    return render(request,'booster/rating_page.html', context={'order':order})

@login_required
def booster_orders(request):
    refresh_orders = BaseOrder.objects.filter(booster=None, is_done=False, is_drop =False)
    for refresh_order in refresh_orders:
        refresh_order.update_actual_price()
        
    orders = BaseOrder.objects.filter(booster= request.user, is_done= False, is_drop = False).order_by('id')
    if not orders:
        return redirect(reverse_lazy('orders.jobs'))


    percentage = 0
    orders_with_percentage = []
    messages=[]
    for base_order in orders:
        content_type = base_order.content_type
        game = []
        if content_type:
            game = content_type.model_class().objects.get(order=base_order)
            
            update_rating_result = game.get_order_price()
            base_order.money_owed = update_rating_result['booster_price']
            base_order.save()
            percentage = update_rating_result['percent_for_view']
            # games.append(game)
        current_room = Room.get_specific_room(base_order.customer, base_order.name)
        
        if current_room is not None:
            messages=Message.objects.filter(room=current_room) 
            slug = current_room.slug
            order_data = {
                'order': game,
                'percentage': percentage,
                'now_price': update_rating_result['booster_price'],
                'half_price': round(base_order.actual_price / 2, 2),
                'user': request.user,
                'room': current_room,
                'messages': messages,
                'slug': slug,
            }
            orders_with_percentage.append(order_data)
        else:
            order_data = {
            'order': game,
            'percentage': percentage,
            'now_price': update_rating_result['booster_price'],
            'half_price': round(base_order.actual_price / 2, 2),
            'user': request.user,
            'room': None,
            'messages': None,
            'slug': None,
            }
            orders_with_percentage.append(order_data)
 
    context = {
        'orders': orders_with_percentage,
    }
    return render(request, 'booster/booster-orders.html', context=context)


class CanChooseMe(APIView):
    def post(self, request, *args, **kwargs):
        user = request.user 
        instance = user
        instance.booster.can_choose_me = not instance.booster.can_choose_me
        instance.booster.save()
        serializer = CanChooseMeSerializer(instance)
        return JsonResponse(serializer.data)
    
@login_required
def booster_history(request):
    history = Transaction.objects.filter(user=request.user).order_by('-id')
    return render(request, 'booster/booster_histoty.html', context={'history' : history})

# def confirm_details(request):
#     if request.method == 'POST':
#         order_id = request.POST.get('order_id')
#         if order_id:
#             order = get_object_or_404(BaseOrder, id=order_id)
#             order.message = None
#             order.data_correct = True
#             order.save()
#             return redirect(reverse_lazy('booster.orders'))
#     return JsonResponse({'success': False})
# @login_required
def alert_customer(request, order_id):
    if request.method == 'POST':
        order_id = order_id
        if order_id:
            order = get_object_or_404(BaseOrder, id=order_id)
            order.message = 'Pleace Specify Your Details'
            order.data_correct = False
            order.save()
            return JsonResponse({'success': True})
    return JsonResponse({'success': False})

@login_required
def upload_finish_image(request):
    if request.method == 'POST':
        order_id = request.POST.get('order_id')
        booster = request.user
        if not order_id.isdigit():
            return JsonResponse({'success': False, 'message': 'Invalid order ID'})
        order = get_object_or_404(BaseOrder, id=order_id, booster=booster)
        finish_image = request.FILES.get('finish_image')
        if not finish_image:
            return JsonResponse({'success': False, 'message': 'No finish image provided'})
        try:
            ext = finish_image.name.split('.')[-1]
            name = f"orders/images/{order.name}.{ext}"
            url = upload_image_to_firebase(finish_image, name)
        except Exception as e:
            return JsonResponse({'success': False, 'message': str(e)})
        order.finish_image = url
        order.is_done = True
        order.save()
        # update booster wallet
        return redirect(reverse_lazy('booster.orders'))
    return JsonResponse({'success': False, 'message': 'Invalid request method'})

# Drop
@login_required
def drop_order(request, order_id):
    if request.method == 'POST':
        # Get the current month and year
        current_month = timezone.now().month
        current_year = timezone.now().year

        # Filter BaseOrder by the same month and year
        booster_dropped_orders = BaseOrder.objects.filter(
            is_drop = True ,
            created_at__year=current_year,   # Filter by the current year
            created_at__month=current_month,  # Filter by the current month
            booster=request.user
        )
        if booster_dropped_orders.exists() :
            return HttpResponse('You Alredy Riched Max Limit of this Month')

        
        old_order = get_object_or_404(BaseOrder ,id =order_id, booster= request.user)
        if old_order.is_done:
            return redirect(reverse_lazy('booster.orders'))
        
        old_game = old_order.related_order


        customer_price = old_game.get_order_price()
        new_price= customer_price['main_price']
        percent = customer_price['percent']
        actual_price = round(new_price * (percent / 100),2)

        new_order = copy.deepcopy(old_order)
        new_order.pk = None
        new_order.save()

        new_game = copy.deepcopy(old_game)
        new_game.pk = None
        new_game.current_rank_id = old_game.reached_rank.id
        new_game.current_division = old_game.reached_division
        new_game.current_marks = old_game.reached_marks
        new_game.order = new_order
        new_game.save()

        new_order.object_id = new_game.pk
        new_order.details = new_game.__str__()
        new_order.booster = None
        new_order.price = new_price
        new_order.money_owed = 0
        new_order.status = 'Droped'
        new_order.actual_price = actual_price
        new_order.created_at = timezone.now()
        new_order.updated_at = timezone.now()
        new_order.save()

        old_order.is_drop = True
        old_order.is_done = True
        old_order.status = 'Droped'
        old_order.created_at = timezone.now()
        old_order.updated_at = timezone.now()
        old_order.save()

        room = Room.get_specific_room(customer=old_order.customer, order_name=old_order.name)
        drop_message = 'Your order has been dropped.\nPlease wait for another booster to accept your order.'
        Message.objects.create(content=drop_message, user_id= 1, room=room, msg_type=1)
        send_refresh_msg(request.user.username , old_order.customer.username, old_order.name)
        refresh_order_page()

        new_game.send_discord_notification()
        return redirect(reverse_lazy('booster.orders'))
    return JsonResponse({'success': False})

@login_required
def update_rating(request, order_id):
    if request.method == 'POST':
        base_order = get_object_or_404(BaseOrder,id=order_id, booster=request.user)
        game = base_order.related_order
        
        reached_division = request.POST.get('reached_division', 1)
        reached_marks = request.POST.get('reached_marks', 0)
        
        if base_order.game.pk == 6:
            reached_rank_id = wow_ranks(reached_division)[1]
        elif base_order.game.pk == 7:
            reached_rank_id = 1
        elif base_order.game.pk == 10:
            reached_rank_id = dota2_ranks(reached_division)[1]
        elif base_order.game.pk == 13 and base_order.game_type == 'A':
            reached_rank_id = csgo2_ranks(reached_division)[1]
        else:
            reached_rank_id = request.POST.get('reached_rank')

        game.reached_rank_id = reached_rank_id
        game.reached_division = reached_division
        game.reached_marks = reached_marks
        
        game.save()    

        send_refresh_msg(request.user.username , base_order.customer.username, base_order.name)

        return redirect(reverse_lazy('booster.orders'))
    return JsonResponse({'success': False})


class TransactionListView(APIView):
    permission_classes = [IsBooster]

    def get(self, request, *args, **kwargs):
        queryset = Transaction.objects.filter(user=request.user).order_by('-id')
        paginator = PageNumberPagination()
        paginator.page_size = 20

        result_page = paginator.paginate_queryset(queryset, request)
        serializer = TransactionSerializer(result_page, many=True)
        return paginator.get_paginated_response(serializer.data)


def work_with_us_level1_view(request):
    id = request.session.get('accepted_data_id')
    if id:
        return redirect(reverse('workwithus.accepted-data')) 
    if request.method == 'POST':
        form = WorkWithUsLevel1Form(request.POST)
        if form.is_valid():
            request.session['level'] = '2'
            request.session.pop('level', None)
            fields = ['nickname', 'email', 'discord_id', 'languages']
            for field in fields:
                if field == 'languages':
                    # Convert the QuerySet to a list before storing it in the session
                    request.session[field] = list(form.cleaned_data[field].values_list('pk', flat=True))
                else:
                    request.session[field] = form.cleaned_data[field]
            return redirect(reverse_lazy('workwithus.level2'))  
    else:
        form = WorkWithUsLevel1Form()
    return render(request, 'booster/work_with_us/workwithus_lvl1.html', {'form': form})

def work_with_us_level2_view(request):
    id = request.session.get('accepted_data_id')
    if id:
        return redirect(reverse('workwithus.accepted-data')) 
    if request.method == 'POST':
        form = WorkWithUsLevel2Form(request.POST)
        if form.is_valid():
            request.session['level'] = '3'
            request.session.pop('level', None)
            fields = ['rank', 'server']
            for field in fields:
                request.session[field] = form.cleaned_data[field]
            
            # Store primary keys of selected games in session
            games_pk = list(form.cleaned_data['game'].values_list('pk', flat=True))
            request.session['games_pk'] = games_pk
            
            return redirect(reverse_lazy('workwithus.level4'))  
    else:
        form = WorkWithUsLevel2Form()
    return render(request, 'booster/work_with_us/workwithus_lvl2.html', {'form': form})

# def work_with_us_level3_view(request):
#     id = request.session.get('accepted_data_id')
#     if id:
#         return redirect(reverse('workwithus.accepted-data')) 
#     level = request.session.get('level')
#     if request.method == 'POST':
#         form = WorkWithUsLevel3Form(request.POST, request.FILES)
#         if form.is_valid():
#             image = form.cleaned_data["image"]
#             image2 = form.cleaned_data["image2"]
#             image3 =  form.cleaned_data["image3"]
#             if image:
#                 Photo.objects.create(booster=data, image=image)
#             if image2:
#                 Photo.objects.create(booster=data, image=image2)
#             if image3:
#                 Photo.objects.create(booster=data, image=image3)
#             return redirect(reverse('workwithus.accepted-data'))  
        
#         # for field, errors in obj.errors.items():
#         #     for error in errors:
#         #         print(f"{field}: {error}")  
#         return HttpResponse("form not valied")    
#     else:
#         form = WorkWithUsLevel3Form()
#         return render(request, 'booster/work_with_us/workwithus_lvl3.html', {'form': form})

class WorkWithUsLevel4View(APIView):
    def get(self, request):
        id = request.session.get('accepted_data_id')
        if id:
            return redirect(reverse('workwithus.accepted-data')) 
        form = WorkWithUsLevel4Form()
        return render(request, 'booster/work_with_us/workwithus_lvl4.html', {'form': form})

    def post(self, request):
        form = WorkWithUsLevel4Form(request.POST)
        if form.is_valid():
            # Extract cleaned data from the form
            cleaned_data = form.cleaned_data

            # Extract session variables
            nickname = request.session.pop('nickname', None)
            email = request.session.pop('email', None)
            discord_id = request.session.pop('discord_id', None)
            languages_pk = request.session.pop('languages', None)
            rank = request.session.pop('rank', None)
            server = request.session.pop('server', None)
            games_pk = request.session.pop('games_pk', None)

            # Create WorkWithUs instance
            data = WorkWithUs.objects.create(
                nickname=nickname,
                email=email,
                discord_id=discord_id,
                rank=rank,
                server=server,
                about_you=cleaned_data['about_you'],
                country=cleaned_data['country'],
                agree_privacy= cleaned_data['agree_privacy'],
            )

            # Add languages and games if they exist
            if languages_pk:
                data.languages.add(*languages_pk)
            if games_pk:
                data.game.add(*games_pk)

            # Store accepted data ID in session
            request.session['accepted_data_id'] = str(data.id)

            # Redirect to accepted data page
            return redirect(reverse('workwithus.accepted-data'))  

        # If form is not valid, return the form with errors
        return render(request, 'booster/work_with_us/workwithus_lvl4.html', {'form': form})


def work_with_us_accepted_data(request):
    id = request.session.get('accepted_data_id')
    found = WorkWithUs.objects.filter(id=id).exists()

    # Clear session if accepted data does not exist
    if not found:
        request.session.pop('accepted_data_id', None)
        return redirect(reverse('workwithus'))

    # Redirect if accepted data ID is missing or invalid
    if not id:
        return redirect(reverse('homepage.index'))

    return render(request, 'booster/work_with_us/accepted_data.html', context={'id': id})


from django.views import View
from django.views.generic import CreateView


class WiningNumber(View):
    def update_wins(self ,order, wins_number, number_of_match):
        if wins_number <= number_of_match and wins_number >= 0 :
            order.wins_number = wins_number
            booster_prise = order.actual_price / number_of_match * wins_number
            order.money_owed = round(booster_prise, 2)
            order.save()
            return order.money_owed
    def post(self, request, order_id):
        order = get_object_or_404(BaseOrder, id=order_id, booster=request.user)
        wins_number = int(request.POST.get('wins_number', 0))
        number_of_match = 1
        if hasattr(order.related_order, 'number_of_match'):
            number_of_match = order.related_order.number_of_match

        if hasattr(order.related_order, 'number_of_wins'):
            number_of_match = order.related_order.number_of_wins    
            
        if order.game.pk in [2, 4, 5, 8, 9, 10, 12]:
            money = self.update_wins(order, wins_number, number_of_match)

            # room = Room.get_specific_room(order.customer, order.name)
            # message_change = Message.create_refresh_message(request.user, room)

            send_refresh_msg(request.user.username , order.customer.username, order.name)
        
        return redirect(reverse('booster.orders'))   


class BoosterRankCreateView(CreateView):
    model = BoosterRank
    template_name = 'booster/boosterrank_form.html'
    fields = ['rank_name', 'rank_image', 'game']
    success_url = reverse_lazy('boosterrank_create')

    def form_valid(self, form):
        booster_rank = form.save(commit=False)
        image_data = self.request.FILES.get('rank_image')
        ext = image_data.name.split('.')[-1]

        if image_data:
            image_name = 'rank/'+ str(uuid.uuid4()) + '.' + ext
            image_url = upload_image_to_firebase(image_data, image_name)
            booster_rank.rank_image = image_url  

        booster_rank.save()
        return super().form_valid(form)