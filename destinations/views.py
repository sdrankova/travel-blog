from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect

from destinations.forms import CommentForm, EditCreateForm
from destinations.models import Destination, Like, Comment


def all_destinations(request):
    context = {
        'destinations': Destination.objects.all(),
    }
    return render(request, 'destinations/all-destinations.html', context)

@login_required
def description_and_comment_destination(request, pk):
    destination = Destination.objects.get(pk=pk)
    if request.method == 'GET':
        context = {
            'destination': destination,
            'form': CommentForm(),
            'can_delete': request.user == destination.current_user.user,

            'can_edit': request.user == destination.current_user.user,
            'already_liked': destination.like_set.filter(current_user_id=request.user.userprofile.id).exists(),
        }
        return render(request, 'destinations/description-destination.html', context)

    else:
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = Comment(text=form.cleaned_data['comment'])
            comment.destination = destination
            comment.current_user = request.user.userprofile
            comment.save()
            return redirect('description and comment', pk)
        context = {
            'destination': destination,
            'form': form,
        }
        return render(request, 'destinations/description-destination.html', context)

@login_required
def like_destination(request, pk):
    like = Like.objects.filter(current_user_id=request.user.userprofile.id, destination_id=pk).first()
    if like:
        like.delete()
    else:
        destination = Destination.objects.get(pk=pk)
        like = Like(test=str(pk), current_user=request.user.userprofile)
        like.destination = destination
        like.save()
    return redirect('description and comment', pk)

@login_required
def edit_destination(request, pk):
    destination = Destination.objects.get(pk=pk, current_user=request.user.userprofile)
    if destination.current_user.user != request.user:
        pass
    if request.method == 'GET':
        form = EditCreateForm(instance=destination)

        context = {
            'form': form,
            'destination': destination,
        }

        return render(request, 'destinations/edit.html', context)
    else:
        form = EditCreateForm(
            request.POST,
            request.FILES,
            instance=destination,
        )
        if form.is_valid():
            form.save()

            return redirect('description and comment', destination.pk)

        context = {
            'form': form,
            'destination': destination,
        }

        return render(request, 'destinations/edit.html', context)

@login_required
def delete(request, pk):
    destination = Destination.objects.get(pk=pk)
    if destination.current_user.user != request.user:
        pass
    if request.method == 'GET':
        context = {
            'destination': destination,
        }
        return render(request, 'destinations/delete.html', context)
    else:
        destination.delete()
        return redirect('destinations')
