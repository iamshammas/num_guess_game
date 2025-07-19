import random
from django.shortcuts import render

def gameViews(request):
    # Initialize game state in session
    if 'secret' not in request.session or 'retries' not in request.session or request.method == 'GET':
        request.session['secret'] = random.randint(1, 20)
        request.session['retries'] = 0
        request.session['history'] = []
        game_active = True
        message = ''
        message_type = ''
    else:
        game_active = True
        message = ''
        message_type = ''

    # Process POST request (guess submission)
    if request.method == 'POST':
        try:
            guess = int(request.POST.get('guess'))
            secret = request.session['secret']
            request.session['retries'] += 1
            retries = request.session['retries']
            
            # Add to history
            history = request.session.get('history', [])
            
            if guess == secret:
                history.append({'guess': guess, 'result': 'correct'})
                message = f'🎉 Correct! You guessed it in {retries} tries!'
                message_type = 'success'
                game_active = False
            elif retries >= 5:
                history.append({'guess': guess, 'result': 'high' if guess > secret else 'low'})
                message = f'😢 Out of tries! The number was {secret}'
                message_type = 'error'
                game_active = False
            else:
                if guess > secret:
                    result = 'high'
                    hint = 'Too High! Try a lower number'
                else:
                    result = 'low'
                    hint = 'Too Low! Try a higher number'
                
                history.append({'guess': guess, 'result': result})
                message = hint
                message_type = 'info'
            
            request.session['history'] = history
            request.session.modified = True
            
        except (ValueError, TypeError):
            message = 'Please enter a valid number between 1-20'
            message_type = 'error'

    context = {
        'attempts': request.session.get('retries', 0),
        'message': message,
        'message_type': message_type,
        'game_active': game_active,
        'history': request.session.get('history', [])
    }
    
    return render(request, 'game.html', context)