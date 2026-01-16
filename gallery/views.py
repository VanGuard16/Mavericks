from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse
from .models import Profile, Event, Photo
from .forms import ProfileForm
from django.core.paginator import Paginator
from django.contrib import messages
from django.contrib.auth.decorators import login_required, user_passes_test
# Create your views here.
def home(request):
    recent_photos = Photo.objects.order_by('-created_at')[:8]
    recent_events = Event.objects.order_by('-created_at')[:2]
    total_photos = 0
    for photo in recent_photos:
        total_photos +=1
    context = {
        'recent_photos': recent_photos,
        'recent_events': recent_events,
        'total_photos': total_photos
    }
    return render(request, 'home.html', context)
@login_required
def profile(request):
    photo_details = Photo.objects.filter(user=request.user)
    photo_count = Photo.objects.filter(user=request.user).count
    context = {
        'photo_details': photo_details,
        'photo_count': photo_count,
    }
    return render(request, 'profile.html', context)

@login_required
def edit_profile(request):
    profile = request.user.profile
    if request.method == 'POST':
        form = ProfileForm(
            request.POST,
            request.FILES,
            instance=profile
        )

        if form.is_valid():
            form.save()
            return redirect('profile')  # IMPORTANT
    else:
        form = ProfileForm(instance=profile)
    return render(request, 'edit_profile.html', {'form': form})


@login_required
def add_photo(request):
    events = Event.objects.all()

    if request.method == 'POST':
        images = request.FILES.getlist('images')  # 👈 multiple files
        caption = request.POST.get('caption', '').strip()
        event_id = request.POST.get('event')

        if not images:
            messages.error(request, 'Please select at least one image.')
            return redirect('add_photo')

        if not event_id:
            messages.error(request, 'Please select an event.')
            return redirect('add_photo')

        event = Event.objects.get(id=event_id)

        # Optional limit (recommended)
        if len(images) > 10:
            messages.error(request, 'You can upload a maximum of 10 images.')
            return redirect('add_photo')

        for image in images:
            Photo.objects.create(
                user=request.user,
                image=image,
                caption=caption,
                event=event
            )

        messages.success(request, 'Photos uploaded successfully!')
        return redirect('home')

    context = {
        'events': events
    }
    return render(request, 'add-photo.html', context)

def gallery(request):
    photos = Photo.objects.all()
    events = Event.objects.all()

    # Filter by event
    selected_event = request.GET.get('event')
    if selected_event:
        photos = photos.filter(event_id=selected_event)

    # Sort by date
    sort_order = request.GET.get('sort', 'desc')
    if sort_order == 'asc':
        photos = photos.order_by('created_at')
    else:
        photos = photos.order_by('-created_at')

    # Pagination
    paginator = Paginator(photos, 12)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {
        'page_obj': page_obj,
        'events': events,
        'sort_order': sort_order,
        'selected_event': int(selected_event) if selected_event else None  # ✅ Pass the ID as int or None
    }

    return render(request, 'gallery.html', context)

@user_passes_test(lambda u: u.is_superuser)
def add_event(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        description = request.POST.get('description')
        date = request.POST.get('date')

        if name and description and date:
            if not Event.objects.filter(name=name).exists():
                Event.objects.create(name=name, description=description, date=date)
                return redirect('home')
            else:
                messages.error(request, 'Event name already exist.')
                return redirect('add_event')
    return render(request, 'add-event.html')
def events(request):

    events = Event.objects.all().order_by('-date')  # latest events first
    paginator = Paginator(events, 9)  # 9 events per page
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    return render(request, 'events.html', {
        'page_obj': page_obj
    })


def event_detail(request, event_id):
    event = get_object_or_404(Event, id=event_id)
    photos = Photo.objects.filter(event=event).order_by('-created_at')
    paginator = Paginator(photos, 12)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    return render(request, 'event_detail.html', {
        'event': event,
        'page_obj': page_obj,
    })
