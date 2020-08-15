from django.shortcuts import render, redirect
from .models import Vacation
from django.http import Http404
from django.urls import path
from django.contrib import messages, admin
from .forms import ImportForm


class MyModelAdmin(admin.ModelAdmin):
    def get_urls(self):
        urls = super().get_urls()
        my_urls = [
            path('import/', self.import_objects),
        ]
        return my_urls + urls
    
    def import_objects(self, request):
        errors = []
        if request.method == 'POST':
            form = ImportForm(request.POST)
            errors = self.save_data(request.FILES['file'])
            if not errors:
                messages.info(request, 'Объекты успешно импортированы')
            messages.error(request, f'Не удалось импортировать объекты: {", ".join(errors)}')
        form = ImportForm()
        context = dict(self.admin_site.each_context(request), form=form)
        return render(request, 'main/import.html', context)
    
    def save_data(self, file):
        return []
