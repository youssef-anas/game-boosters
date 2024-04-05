def boosters(request):
    if request.method == 'POST':
        game_id = request.POST.get('game_id', 1)  # Set default value to 1 if not present in POST data
    else:
        game_id = 1  # Default value if it's a GET request or not an AJAX POST

    game_pk_condition = Case(
        When(booster_division__game__pk=game_id, then=1),
        default=0,
        output_field=IntegerField()
    )

    boosters = User.objects.filter(
        is_booster=True,
        booster__can_choose_me=True
    )
    
    # Filter boosters based on game_id
    # TODO Will make Language come From Database
    if game_id == 1:
            boosters = boosters.filter(
            booster__is_wr_player=True,
        ).annotate(
            achived_rank_name=F('booster__achived_rank_wr__rank_name'),
            achived_rank_image=F('booster__achived_rank_wr__rank_image')
        )

    elif game_id == 2:
        boosters = boosters.filter(
            booster__is_valo_player=True,
        ).annotate(
            achived_rank_name=F('booster__achived_rank_valo__rank_name'),
            achived_rank_image=F('booster__achived_rank_valo__rank_image')
        )

    elif game_id == 3:
        boosters = boosters.filter(
            booster__is_pubg_player=True,
        ).annotate(
            achived_rank_name=F('booster__achived_rank_pubg__rank_name'),
            achived_rank_image=F('booster__achived_rank_pubg__rank_image')
        )
    elif game_id == 4:
        boosters = boosters.filter(
            booster__is_lol_player=True,
        ).annotate(
            achived_rank_name=F('booster__achived_rank_lol__rank_name'),
            achived_rank_image=F('booster__achived_rank_lol__rank_image')
        )
    elif game_id == 5:
        boosters = boosters.filter(
            booster__is_tft_player=True,
        ).annotate(
            achived_rank_name=F('booster__achived_rank_tft__rank_name'),
            achived_rank_image=F('booster__achived_rank_tft__rank_image')
        )
    elif game_id == 6:
        boosters = boosters.filter(
            booster__is_wow_player=True,
        ).annotate(
            achived_rank_name=F('booster__achived_rank_wow__rank_name'),
            achived_rank_image=F('booster__achived_rank_wow__rank_image')
        )
    elif game_id == 7:
        boosters = boosters.filter(
            booster__is_hearthstone_player=True,
        ).annotate(
            achived_rank_name=F('booster__achived_rank_hearthstone__rank_name'),
            achived_rank_image=F('booster__achived_rank_hearthstone__rank_image')
        )
    elif game_id == 8:
        boosters = boosters.filter(
            booster__is_mobleg_player=True,
        ).annotate(
            achived_rank_name=F('booster__achived_rank_mobleg__rank_name'),
            achived_rank_image=F('booster__achived_rank_mobleg__rank_image')
        )
    elif game_id == 9:
        boosters = boosters.filter(
            booster__is_rl_player=True,
        ).annotate(
            achived_rank_name=F('booster__achived_rank_rl__rank_name'),
            achived_rank_image=F('booster__achived_rank_rl__rank_image')
        )
    elif game_id == 10:
        boosters = boosters.filter(
            booster__is_dota2_player=True,
        ).annotate(
            achived_rank_name=F('booster__achived_rank_dota2__rank_name'),
            achived_rank_image=F('booster__achived_rank_dota2__rank_image')
        )
    elif game_id == 11:
        boosters = boosters.filter(
            booster__is_hok_player=True,
        ).annotate(
            achived_rank_name=F('booster__achived_rank_hok__rank_name'),
            achived_rank_image=F('booster__achived_rank_hok__rank_image')
        )
    elif game_id == 12:
        boosters = boosters.filter(
            booster__is_overwatch2_player=True,
        ).annotate(
            achived_rank_name=F('booster__achived_rank_overwatch2__rank_name'),
            achived_rank_image=F('booster__achived_rank_overwatch2__rank_image')
        )
    elif game_id == 13:
        boosters = boosters.filter(
            booster__is_csgo2_player=True,
        ).annotate(
            achived_rank_name=F('booster__achived_rank_csgo2__rank_name'),
            achived_rank_image=F('booster__achived_rank_csgo2__rank_image')
        )

    boosters = boosters.annotate(
        average_rating=Coalesce(Avg('ratings_received__rate'), Value(0.0)),
        order_count=Sum(game_pk_condition),
        last_boost=Max('booster_division__created_at'),
    ).order_by('id')

    if request.headers.get('x-requested-with') == 'XMLHttpRequest':
        # boosters_with_additional_data = []
        # for booster in boosters:
        #     additional_data = {
        #         'languages': ['En', 'Ar'],
        #         'ach': booster.field2,
        #     }
        #     booster_data = {
        #         'booster': model_to_dict(booster),
        #         'additional_data': additional_data
        #     }
        #     boosters_with_additional_data.append(booster_data)

        # return JsonResponse({'boosters': boosters_with_additional_data})

        data = {
            'boosters': list(boosters.values()),  # Convert queryset to list of dictionaries
        }
        return JsonResponse(data)

    else:
        # Handle non-AJAX requests
        context = {
            # Initial context data if any
            "boosters": boosters,  # Pass boosters to the template
        }
        return render(request, 'booster/boosters.html', context)
