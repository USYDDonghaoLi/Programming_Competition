from django.shortcuts import render

def runoob(request):

    views_list = ["a", "b", "c"]
    return render(request, 'runoob.html', {"views_list": views_list})