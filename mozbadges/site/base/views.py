from mozbadges.utils.decorators import render_to


@render_to('home.html')
def home (request):
    pass


@render_to('create/design.html')
def create (request):
    pass


@render_to('claim.html')
def claim (request, code=None):
    pass


@render_to('studio/studio.html')
def studio (request):
    pass
