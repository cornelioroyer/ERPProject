from django.conf.urls.defaults import patterns
from django.contrib import admin
from django.http import HttpResponse
def admin_my_view(request, model_admin):
    opts = model_admin.model._meta
    admin_site = model_admin.admin_site
    has_perm = request.user.has_perm(opts.app_label +'.' \
                                        + opts.get_change_permission())
    context = {
        'admin_site': admin_site.name,
        'title': "My Custom View",
        'opts': opts,
        'root_path':'/%s' % admin_site.root_path,
        'app_label': opts.app_label,
        'has_change_permission': has_perm
    }
    template = 'admin/accountreceivable/my_view.html'
    return render_to_response(template, context,
            context_instance=RequestContext (request))