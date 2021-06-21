from django.shortcuts import get_object_or_404, render, redirect
from .models import Notification
from unsc.models import ComplianceOfficer, Company
# Create your views here.

def notification(request):
    #print('Entered notificcation function')
    goto = request.GET.get('goto', '')
    #print('goto is:', goto)
    notification_id = request.GET.get('notification', 0)

    if goto != '':
        notification = get_object_or_404(Notification, pk=notification_id)
        notification.is_read = True    
        notification.save()
    return render(request, 'notifications/notifications.html')


def notification_details(request, pk):
    note = get_object_or_404(Notification, id=pk)
    note.is_read = True
    note.save()
    officer = get_object_or_404(ComplianceOfficer, user=request.user)
    comp = get_object_or_404(Company, company_name=officer.company)
    context = {'note': note, 'comp': comp}
    return render(request, 'notifications/notification_details.html', context)


def create_notification(request,to_user, notification_type, extra_id, message, created_by):
    notification = Notification.objects.create(to_user=to_user, notification_type=notification_type, extra_id=extra_id, message=message, created_by=created_by)
