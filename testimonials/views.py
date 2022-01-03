from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Testimonial
from .forms import TestimonialForm


def all_testimonials(request):
    """ A view that renders the (all) testimonials page """
    testimonials = Testimonial.objects.all()
    context = {
        'testimonials': testimonials
    }
    return render(request, 'testimonials/all_testimonials.html', context)


@login_required
def add_testimonial(request):
    if request.method == 'POST':
        form = TestimonialForm(request.POST)
        if form.is_valid():
            form.save()
            # Return to all_testimonials(request): above
            return redirect('all_testimonials')
    form = TestimonialForm()
    context = {
        'form': form,
        'author': request.user,
    }
    return render(request, 'testimonials/add_testimonial.html', context)


@login_required
def edit_testimonial(request, testimonial_id):
    testimonial = get_object_or_404(Testimonial, id=testimonial_id)
    if request.method == 'POST':
        form = TestimonialForm(request.POST, instance=testimonial)
        if form.is_valid():
            form.save()
            return redirect('all_testimonials')
    form = TestimonialForm(instance=testimonial)
    context = {
        'form': form,
        'author': request.user,
    }
    return render(request, 'testimonials/edit_testimonial.html', context)


@login_required
def delete_testimonial(request, testimonial_id):
    testimonial = get_object_or_404(Testimonial, id=testimonial_id)
    testimonial.delete()
    # Return to all_testimonials(request): above
    return redirect('all_testimonials')
