from django.core.exceptions import ValidationError

def validate_marks_for_rank(rank_id, marks):
    if rank_id == 1:  # Iron
        if not (0 <= marks <= 2):
            raise ValidationError("Wrong Marks Number for Iron rank")
    elif rank_id in [2, 3]:  # Bronze and Silver
        if not (0 <= marks <= 3):
            raise ValidationError("Wrong Marks Number for Bronze or Silver rank")
    elif rank_id in [4, 5]:  # Gold and Platinum
        if not (0 <= marks <= 4):
            raise ValidationError("Wrong Marks Number for Gold or Platinum rank")
    elif rank_id == 6:  # Emerald
        if not (0 <= marks <= 5):
            raise ValidationError("Wrong Marks Number for Emerald rank")
    elif rank_id == 7:  # DIAMOND
        if not (marks == 0):
            print(marks)
            raise ValidationError("Wrong Marks Number for DIAMOND rank")
    elif rank_id == 8:  # MASTER
        if not (marks == 0):
            raise ValidationError("Wrong Marks Number for MASTER rank")
    else:
        raise ValidationError("Invalid rank ID")

def validate_master_division(division):
    if not division == 1:
        raise ValidationError("Wrong Division Number for MASTER rank")
