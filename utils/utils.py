from django.utils import timezone


def auto_update_old_offers(offers):
    now = timezone.now()
    if not offers:
        pass
    if len(offers) == 0:
        pass
    else:
        for o in offers:
            if o.status == 'PENDING' and o.date < now:
                o.status = 'REJECTED'
                o.save()

