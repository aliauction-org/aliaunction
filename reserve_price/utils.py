def reserve_status(auction):
    if not hasattr(auction, "reserve"):
        return None

    return "MET" if auction.reserve.is_met() else "NOT_MET"
