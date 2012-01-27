from django.http import HttpResponseRedirect
from django.shortcuts import render_to_response, get_object_or_404
from django.contrib.auth import decorators, models, logout
from django.template import RequestContext

@decorators.login_required
def profile(request):
    user = get_object_or_404(models.User, username=request.user.username)
    return render_to_response('login/profile.html',
                             {'user' : user},
                             context_instance=RequestContext(request))
