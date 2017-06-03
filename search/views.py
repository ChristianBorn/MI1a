import logging
from django.shortcuts import render

def search_town(request):
    logging.basicConfig(filename='textfielinput.log', level=logging.INFO)   #in dieses Dokument wird der Input aus dem Textfeld probeweise geschrieben.
    logging.info(request.POST.get('suchanfrage'))

    checkboxen = request.POST.getlist('checks[]')
    print(checkboxen)
    logging.info(request.POST.getlist('checks[]'))
    # return render(request,  'search/easy_living.html')
    return render(request, 'search/index.html')



