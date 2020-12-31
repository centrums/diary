import sqlite3
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import get_object_or_404, render, redirect
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.models import User
from django.db import transaction
from django.utils import timezone
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login, authenticate

from .models import Entry
from .models import EntryForm

# Create your views here.
@login_required
def index(request):
    owner = request.user
    entries = owner.entry_set.all().order_by('-pub_date')
    form = EntryForm()
    context = {'entries': entries, 'owner': owner, 'form': form}
    return render(request, 'diary/index.html', context)

@login_required
def read(request, entry_id):
    owner = request.user
    entry = get_object_or_404(Entry, pk=entry_id)
    """
    #making things secure
    if owner == entry.owner:
        context = {'entry': entry}
        return render(request, 'diary/read.html', context)
    """
    context = {'entry': entry}
    return render(request, 'diary/read.html', context)
        
    return redirect('diary:index')

@login_required
@transaction.atomic
def add(request):
    if request.method == 'POST':
        form = EntryForm(request.POST)
        if form.is_valid():
            owner = request.user
            now = timezone.now()
            title = form.cleaned_data['title']
            content = form.cleaned_data['content']
            conn = sqlite3.connect('db.sqlite3')
            cursor = conn.cursor()
            cursor.executescript("INSERT INTO diary_entry (pub_date, edit_date, owner_id, title, content) VALUES ('%s', '%s', '%s','%s', '%s')" %(now, now, owner.id, title, content))
            """
            #making things secure
            entry = owner.entry_set.create(title=title, content=content, pub_date=now, edit_date=now)
            """
            return HttpResponseRedirect(reverse('diary:index'))
        else:
            owner = request.user
            entries = owner.entry_set.all().order_by('-pub_date')
            context = {'entries': entries, 'owner': owner, 'form': form}
            return render(request, "diary/index.html", context)  
    return redirect('diary:index')
    
    
@login_required
def edit(request, entry_id):
    if request.method == 'POST':
        entry = get_object_or_404(Entry, pk=entry_id)
        if request.user == entry.owner:
            form = EntryForm(instance=entry)
            #context = {'entry': entry}
            context = {'form': form, 'e_id': entry_id}
            return render(request, 'diary/edit.html', context)
    return redirect('diary:index')
    
@login_required
@transaction.atomic
def update(request, entry_id):
    if request.method == 'POST':
        entry = get_object_or_404(Entry, pk=entry_id)
        if request.user == entry.owner:
            form = EntryForm(request.POST)
            if form.is_valid():
                entry.title = form.cleaned_data['title']
                entry.content = form.cleaned_data['content']
                entry.edit_date = timezone.now()
                entry.save()
                return HttpResponseRedirect(reverse('diary:index'))
            else:
                return render(request, "diary/edit.html", {'form':form, 'e_id': entry_id})  
    return redirect('diary:index')
    
    
def delete(request, entry_id):
    entry = get_object_or_404(Entry, pk=entry_id)
    request.session['entry_id'] = entry_id
    return render(request, 'diary/delete.html')
    
"""
@login_required
def delete(request, entry_id):
    if request.method == 'POST':
        entry = get_object_or_404(Entry, pk=entry_id)
        if request.user == entry.owner:
            request.session['entry_id'] = entry_id
            return render(request, 'diary/delete.html')
    return redirect('diary:index')
"""
    
    
@transaction.atomic
def confirm(request):
    if request.method == "GET":
        entry_id = request.session['entry_id']
        entry = get_object_or_404(Entry, pk=entry_id)
        entry.delete()
        return HttpResponseRedirect(reverse('diary:index'))
    return redirect('diary:index')
    
"""    
@login_required
@transaction.atomic
def confirm(request):
    if request.method == "POST":
        entry_id = request.session['entry_id']
        entry = get_object_or_404(Entry, pk=entry_id)
        if request.user == entry.owner:
            entry.delete()
            del request.session['entry_id']
            return HttpResponseRedirect(reverse('diary:index'))
    return redirect('diary:index')
"""

@transaction.atomic
def signup(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            """
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)
            login(request, user)
            """
            return HttpResponseRedirect(reverse('diary:index'))
    else:
        form = UserCreationForm()
    return render(request, 'diary/signup.html', {'form': form})
    

