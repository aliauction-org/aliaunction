def submit_for_approval(auction):
    workflow = auction.workflow
    if workflow.status == "DRAFT":
        workflow.status = "PENDING"
        workflow.save()
