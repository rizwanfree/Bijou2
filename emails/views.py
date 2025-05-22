
from django.views.generic import ListView, CreateView, DetailView
from django.urls import reverse_lazy
from .models import Message, EmailAttachment
from .forms import ComposeEmailForm
from django.shortcuts import redirect
from django_mailbox.models import Mailbox
from django.views.decorators.http import require_POST
from django.http import JsonResponse
from django.views.generic import FormView

class EmailListView(ListView):
    model = Message
    template_name = 'emails/list.html'
    paginate_by = 20

    def get_queryset(self):
        return Message.objects.all().order_by('-processed')



class EmailDetailView(DetailView):
    model = Message
    template_name = 'emails/detail.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['attachments'] = EmailAttachment.objects.filter(email=self.object)
        return context



class ComposeEmailView(FormView):
    form_class = ComposeEmailForm
    template_name = 'emails/compose.html'
    success_url = reverse_lazy('email-list')

    def form_valid(self, form):
        form.request = self.request  # Pass request to form
        form.send_email()
        return super().form_valid(form)   
    template_name = 'emails/compose.html'
    success_url = reverse_lazy('email-list')

    def form_valid(self, form):
        form.request = self.request  # Pass request to access FILES
        form.send_email()
        return super().form_valid(form)

def fetch_emails(request):
    mailboxes = Mailbox.objects.all()
    for mailbox in mailboxes:
        mailbox.get_new_mail()
    return redirect('email-list')


@require_POST
def mark_email_read(request, pk):
    try:
        email = Message.objects.get(pk=pk)
        email.read = True
        email.save()
        return JsonResponse({'status': 'success'})
    except Message.DoesNotExist:
        return JsonResponse({'status': 'error'}, status=404)