from Grooving.models import Artist, Customer,Offer


def auto_update_old_offers(offers):
    if not offers:
        return None
    if len(offers) == 0:
        return None
    else:
        pending_offers = []
        for o in offers:
            if o.status == 'PENDING' and o.date is None:
                pass
