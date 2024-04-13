from django.core.exceptions import ValidationError

def validate_current_rank_mobile_legends(rank, division, marks):
    if rank == 1:
        if division not in [3, 4, 5]:
            raise ValidationError(f"Error in rank: {division} is not valid for rank {rank}")
        if marks not in [1, 2, 3]:
            raise ValidationError(f"Error in mark: {marks} is not valid for rank {rank}")
    elif rank == 2:
        if division not in [2, 3, 4, 5]:
            raise ValidationError(f"Error in rank: {division} is not valid for rank {rank}")
        if marks not in [1, 2, 3]:
            raise ValidationError(f"Error in mark: {marks} is not valid for rank {rank}")
    elif rank == 3:
        if division not in [2, 3, 4, 5]:
            raise ValidationError(f"Error in rank: {division} is not valid for rank {rank}")
        if marks not in [1, 2, 3, 4]:
            raise ValidationError(f"Error in mark: {marks} is not valid for rank {rank}")
    elif rank in [4, 5, 6]:
        if division not in [1, 2, 3, 4, 5]:
            raise ValidationError(f"Error in rank: {division} is not valid for rank {rank}")
        if marks not in [1, 2, 3, 4, 5]:
            raise ValidationError(f"Error in mark: {marks} is not valid for rank {rank}")
    elif rank in [7, 8, 9]:
        if division not in [1, 2, 3, 4, 5]:
            raise ValidationError(f"Error in rank: {division} is not valid for rank {rank}")
        if marks not in [1, 2, 3, 4, 5]:
            raise ValidationError(f"Error in mark: {marks} is not valid for rank {rank}")
    else:
        raise ValidationError("Invalid rank.")

# def validate_desired_rank_mobile_legends(desired_rank):
#     if desired_rank > 10 or desired_rank < 0:
#         raise ValidationError("Invalid desired rank.")
